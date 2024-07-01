"""
CC class used to read/write from tty interface
"""
import serial
from params import *
def checksum(data):
    """
    The checksum is a modular sum. Correctly compute it as follows:
 Checksum = 0 - (Byte 0 + Byte 1 + Byte 2 + Byte 3)
If the checksum is correct, the result of adding the bytes in the command or response packet together
will be 0x00 (ignoring overflows). The response checksum can be verified by adding the Response Data
bytes and the response checksum, if valid they will total to 0x00 (ignoring overflows).
    """
    return sum(data) & 0xFF

def castle_read(ser, reg):
    # Clear the input buffer
    while ser.in_waiting > 0:
        ser.read()

    # Create the command packet
    command_start = 0b10000000  # Start bit with Device ID of 0
    crc = -(command_start + reg) & 0xFF  # Calculate the checksum
    buf = bytearray([command_start, reg, 0, 0, crc])
    print([command_start, reg, 0, 0, crc])
    ser.write(buf)

    # Read the response
    response = ser.read(3)
    print(response)
    if len(response) == 3:
        # Calculate and check the CRC
        if sum(response) & 0xFF == 0:
            value = (response[0] << 8) | response[1]
            return True, value
    return False, None

def castle_write(ser, reg, value):
    # Clear the input buffer
    while ser.in_waiting > 0:
        ser.read()

    # Create the command packet
    command_start = 0b10000000
    high_byte = (value >> 8) & 0xFF
    low_byte = value & 0xFF
    packet = [command_start, reg, high_byte, low_byte]
    crc = -sum(packet) & 0xFF
    packet+= [crc]
    print(packet)
    ser.write(packet)

class CastleSerialLink:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        if self.ser.isOpen():
            print("Connected to: " + self.ser.portstr)
        else:
            print("Failed to connect to: " + self.ser.portstr)
            exit(1)

    def read(self, reg):
        return castle_read(self.ser, reg)

    def write(self, reg, value):
        return castle_write(self.ser, reg, value)

if __name__ == "__main__":
    csl = CastleSerialLink(port="/dev/ttyUSB0", baudrate=115200)
    
    print(csl.read(VOLTAGE_READ))
    csl.write(THROTTLE_WRITE, 4000)
    