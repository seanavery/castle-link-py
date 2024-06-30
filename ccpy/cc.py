"""
CC class used to read/write from tty interface
"""
import serial

if __name__ == "__main__":
    # connect to /dev/ttyUSB0
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    
    # check if the connection is open
    if ser.isOpen():
        print("Connected to: " + ser.portstr)
    else:
        print("Failed to connect to: " + ser.portstr)
        exit(1)
        