from pymodbus.client.sync import ModbusTcpClient
import time
# Connect to OnRobot Eye box (adjust IP if needed)
client = ModbusTcpClient('192.168.1.1', port=502)
client.connect()
# Register addresses (examples based on OnRobot Modbus protocol)
REGISTER_FORCE = 0x00      # Desired force in tenths of N (e.g., 400 = 40 N)
REGISTER_WIDTH = 0x01      # Desired width in tenths of mm (e.g., 600 = 60 mm)
REGISTER_CONTROL = 0x02    # Command register
def close_gripper(width_mm=20.0, force_n=40.0):
   print("Closing gripper...")
   client.write_register(REGISTER_FORCE, int(force_n * 10), unit=65)
   client.write_register(REGISTER_WIDTH, int(width_mm * 10), unit=65)
   client.write_register(REGISTER_CONTROL, 1, unit=65)  # Command = 1 → grip
   time.sleep(2)
def open_gripper(width_mm=70.0, force_n=40.0):
   print("Opening gripper...")
   client.write_register(REGISTER_FORCE, int(force_n * 10), unit=65)
   client.write_register(REGISTER_WIDTH, int(width_mm * 10), unit=65)
   client.write_register(REGISTER_CONTROL, 1, unit=65)  # Command = 1 → grip to width
   time.sleep(2)
try:
   open_gripper()
   time.sleep(1)
   close_gripper()
finally:
   client.close()