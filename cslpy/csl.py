import serial
import threading
import time
from itertools import chain
from params import *

def checksum(data):
    """
The checksum is a modular sum. Correctly compute it as follows:
Checksum = 0 - (Byte 0 + Byte 1 + Byte 2 + Byte 3)
    """
    return -sum(data) & 0xFF

def castle_read(ser, reg):
    # Clear the input buffer
    while ser.in_waiting > 0:
        ser.read()

    # Create the command packet
    command_start = 0b10000000  # Start bit with Device ID of 0
    packet = [command_start, reg, 0, 0]
    crc = checksum(packet)
    buf = bytearray(packet + [crc])
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
    crc = checksum(packet)
    buf = bytearray(packet + [crc])
    ser.write(buf)
    
    while ser.in_waiting > 0:
        ser.read()
    
def castle_parse(value_reg, scale):
    return (value_reg / 2042) * scale

class CastleSerialLink:
    state = {
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

    def write(self, name="throttle", value=65535//2):
        if name in write_name_to_reg:
            reg = write_name_to_reg[name]
            return castle_write(self.ser, reg, value)
        else:
            print("Invalid name", name)
            return
    
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
                if not value:
                    continue
                if value and name in scale_name_to_parse:
                    self.state[name] = castle_parse(value, scale_name_to_parse[name][0])
                elif value and name in num_name_to_parse:
                    self.state[name] = value
            time.sleep(1/hz)

    def stop(self):
        self.listening = False

       
if __name__ == "__main__":
    csl = CastleSerialLink(port="/dev/ttyUSB0", baudrate=115200)
    
    csl.listen(40)
    for i in range(100):
        time.sleep(0.5)
        print(csl.state)
    csl.stop()
    