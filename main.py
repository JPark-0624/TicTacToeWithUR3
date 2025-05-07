import time
import numpy as np
import RPi.GPIO as GPIO
# from FunctionalityTest import move_to_position  # We'll define this helper soon
import urx
from TicTacToeAI import CompAI, win_check, full_board_check, place_marker

# ------------------ SETUP ------------------

# Define GPIO pins for each sensor (same as before)
sensor_pins = {
    1: 10,  # Bottom Left
    2: 9,   # Bottom Middle
    3: 11,  # Bottom Right
    4: 17,  # Middle Left
    5: 27,  # Center
    6: 22,  # Middle Right
    7: 2,   # Top Left
    8: 3,   # Top Middle
    9: 4    # Top Right
}

GPIO.setmode(GPIO.BCM)
for pin in sensor_pins.values():
    GPIO.setup(pin, GPIO.IN)

# Define robot positions for each of the 9 grid positions
# Assume pre-recorded joint angles or poses
# 0~9 are the positions on the board
# 11~19 are the positions above the board 
# 'box, boxReady' are the positions for the box
joint_position_map = {
    1: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    2: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    3: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    4: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    5: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    6: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    7: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    8: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    9: [3.85,-45.6,7.34,-52.25,-91.62,1.0],

    11: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    12: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    13: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    14: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    15: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    16: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    17: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    18: [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    19: [3.85,-45.6,7.34,-52.25,-91.62,1.0],

    'box' : [3.85,-45.6,7.34,-52.25,-91.62,1.0],
    'boxReady' : [3.85,-45.6,7.34,-52.25,-91.62,1.0],
}



# ------------------ MAIN LOOP ------------------
theBoard = [' '] * 10  # board[1~9] valid
available = [' '] + [str(i) for i in range(1, 10)]  # display purposes

player_symbol = 'X'
cpu_symbol = 'O'

def read_sensor_input(prev_state = np.zeros((3,3), dtype=int),turn = 'Human'):
    print("Waiting for human move...")
    while True:
        sensor_matrix = np.zeros((3, 3), dtype=int)
        for s_num, gpio_pin in sensor_pins.items():
            val = 1 if GPIO.input(gpio_pin) == GPIO.HIGH else 0
            if s_num in [7, 8, 9]: row, col = 0, s_num - 7
            elif s_num in [4, 5, 6]: row, col = 1, s_num - 4
            elif s_num in [1, 2, 3]: row, col = 2, s_num - 1
            sensor_matrix[row][col] = val
        # check if there is a difference from previous state
        if not np.array_equal(sensor_matrix, prev_state):
            diff = sensor_matrix - prev_state
            idx = np.where(diff == 1)
            if len(idx[0]) == 1:
                r, c = idx[0][0], idx[1][0]
                pos = 3 * (2 - r) + (c + 1) # convert to 1~9
                if theBoard[pos] == ' ':
                    print(f"{turn} played at position {pos}")
                    return pos, sensor_matrix
        time.sleep(0.1)

def move_to_goal(pos: int, robot):
    goal = int(pos)
    goalAbove = int(goal + 10)
    # first, move to the ready position which is above the box
    robot.movej(joint_position_map['boxReady'], acc=0.4, vel=0.2)
    time.sleep(10)

    # second, move to the box position
    robot.movej(joint_position_map['box'], acc=0.4, vel=0.2)
    time.sleep(5)

    # robot.grapp() # grab the box

    # return to the ready position
    robot.movej(joint_position_map['boxReady'], acc=0.4, vel=0.2)

    # move to the position above the target position
    robot.movej(joint_position_map[goalAbove], acc=0.4, vel=0.2)
    time.sleep(15)

    # last, move down to the target position
    robot.movej(joint_position_map[goal], acc=0.4, vel=0.2)
    time.sleep(10)

    # robot.release() # release the box

    robot.movej(joint_position_map[goalAbove], acc=0.4, vel=0.2)
    time.sleep(5)

    # return to the ready position
    robot.movej(joint_position_map['boxReady'], acc=0.4, vel=0.2)




def main():
    turn = 'Human'
    game_on = True
    print("Game Start!")
    board_state = np.zeros((3,3), dtype=int)

    ROBOT_IP = "192.168.1.209"  #UR3 IP address
    robot = urx.Robot(ROBOT_IP)
    print("Connected to robot.")

    while game_on:
        if turn == 'Human':
            pos,board_state = read_sensor_input(board_state,turn)
            place_marker(theBoard, available, player_symbol, pos)

            if win_check(theBoard, player_symbol):
                print("Human wins!")
                game_on = False
            elif full_board_check(theBoard):
                print("It's a draw!")
                game_on = False
            else:
                turn = 'CPU'

        elif turn == 'CPU':
            print("CPU is thinking...")
            pos = CompAI(theBoard, 'CPU', cpu_symbol) # decision making
            move_to_goal(pos,robot)  # action
            _,board_state = read_sensor_input(board_state,turn) # physical board update
            place_marker(theBoard, available, cpu_symbol, pos) #logical board update

            if win_check(theBoard, cpu_symbol):
                print("CPU wins!")
                game_on = False
            elif full_board_check(theBoard):
                print("It's a draw!")
                game_on = False
            else:
                turn = 'Human'

    print("Game Over")


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
