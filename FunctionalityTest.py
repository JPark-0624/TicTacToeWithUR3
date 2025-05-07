import urx
import time
import numpy as np
# --- CONFIGURATION ---
ROBOT_IP = "192.168.1.209"  #UR3 IP address
joint1 = [3.85,-45.6,7.34,-52.25,-91.62,1.0] # First joint angles in degrees
joint2 = [3.33,-53.48,-4.82,-52.25,-91.62,1.0] # Second joint angles in degrees

velocity = 0.2  # rad/s
acceleration = 0.4  # rad/s^2
monitor_rate = 0.1  # seconds between position printouts
# --- CONVERSION ---
target_joint_rad1 = np.deg2rad(joint1)  # Convert to radians

target_joint_rad2 = np.deg2rad(joint2)  # Convert to radians
# --- CONNECT ---
robot = urx.Robot(ROBOT_IP)
print("Connected to robot.")

initial_joint_angles = robot.getj()
print("initial joint angles (deg):", np.rad2deg(initial_joint_angles))
initial_tool_pose = robot.getl()
print("initial tool pose :", initial_tool_pose)


try:
    # --- Start moving ---
    print("Moving to target joint configuration...")
    robot.movej(target_joint_rad1, acc=acceleration, vel=velocity, wait=False)

    time.sleep(10)
    
    first_target_joint_angles = robot.getj()
    print("first_target_joint_angles (deg):", np.rad2deg(first_target_joint_angles))
    first_tool_pose = robot.getl()
    print("first_tool_pose :", first_tool_pose)

    robot.movej(target_joint_rad2, acc=acceleration, vel=velocity, wait=False)
    print("Movement complete.")

    time.sleep(10)
    
    second_target_joint_angles = robot.getj()
    print("second_target_joint_angles (deg):", np.rad2deg(second_target_joint_angles))
    second_tool_pose = robot.getl()
    print("second_tool_pose :", second_tool_pose)


except KeyboardInterrupt:
    print("Movement interrupted by user.")
finally:
    robot.close()
    print("Connection closed.")