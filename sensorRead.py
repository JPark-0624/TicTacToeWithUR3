import RPi.GPIO as GPIO
import time
import numpy as np  # We will use numpy for the 3x3 matrix
 
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
 
# GPIO Setup
GPIO.setmode(GPIO.BCM)
for pin in sensor_pins.values():
    GPIO.setup(pin, GPIO.IN)
 
print("Reading 9 sensors into 3x3 matrix... Press Ctrl+C to exit.")
 
try:
    while True:
        # Create empty 3x3 numpy array
        sensor_matrix = np.zeros((3, 3), dtype=int)
 
        # Fill the matrix based on sensor readings
        for sensor_num, gpio_pin in sensor_pins.items():
            reading = GPIO.input(gpio_pin)
            value = 1 if reading == GPIO.HIGH else 0
 
            # Map sensor number to matrix position
            if sensor_num in [7, 8, 9]:  # Top row
                row = 0
                col = sensor_num - 7
            elif sensor_num in [4, 5, 6]:  # Middle row
                row = 1
                col = sensor_num - 4
            elif sensor_num in [1, 2, 3]:  # Bottom row
                row = 2
                col = sensor_num - 1
 
            sensor_matrix[row, col] = value
 
        # Clear the screen (optional)
        # print("\033c", end="")  # Uncomment this line if you want to clear screen every time
 
        # Print the matrix nicely
        for row in sensor_matrix:
            print(' | '.join(str(x) for x in row))
            print("---+---+---")
        print("\n")  # Extra newline between updates
 
        time.sleep(0.2)
 
except KeyboardInterrupt:
    print("Exiting program.")
 
finally:
    GPIO.cleanup()