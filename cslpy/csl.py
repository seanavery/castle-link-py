"""
CC class used to read/write from tty interface
"""
import serial
import threading
import time
from itertools import chain
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
    crc = -(command_start + reg) & 0xFF  # Checksum
    buf = bytearray([command_start, reg, 0, 0, crc])
    ser.write(buf)

    # Read the response
    response = ser.read(3)
    if len(response) == 3:
        # Calculate and check the CRC
        if sum(response) & 0xFF == 0:
            value = (response[0] << 8) | response[1]
            return value
    return None

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
    ser.write(packet)
    
def castle_parse(value_reg, scale):
    return (value_reg / 2042) * scale

class CastleSerialLink:
    cc_state = {
        "voltage": 0.0,
        "ripple": 0.0,
        "current": 0.0,
        "throttle": 0,
        "power": 0.0,
        "speed": 0.0,
        "temperature": 0.0,
        "bec_voltage": 0.0,
        "bec_current": 0.0,
        "raw_ntc": 0.0,
        "raw_linear": 0.0,
        "link_live": 0,
        "failsafe": 0,
        "e_stop": 0,
        "packet_in": 0,
        "packet_out": 0,
        "check_baud": 0,
        "packet_bad": 0,
    }
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
    
    # listen background thread that reads all values for a given Hz
    def listen(self, hz):
        self.listening = True
        thread = threading.Thread(target=self.listen_thread, args=(hz,))
        thread.daemon = True
        thread.start()
        
    def listen_thread(self, hz):
        while self.listening:
            for reg, name in read_reg_to_name.items():
                value = castle_read(self.ser, reg)
                if value:
                    self.cc_state[name] = castle_parse(value, convert_name_to_parse[name][0])
            time.sleep(1/hz)
    
    def stop(self):
        self.listening = False

       
if __name__ == "__main__":
    csl = CastleSerialLink(port="/dev/ttyUSB0", baudrate=115200)
    
    csl.listen(1)
    for i in range(10):
        csl.write(THROTTLE_WRITE, 4000)
        print(csl.cc_state)
        time.sleep(0.5)
    
    