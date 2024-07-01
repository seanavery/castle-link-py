"""
CC class used to read/write from tty interface
"""
import serial

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

if __name__ == "__main__":
    # connect to /dev/ttyUSB0
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    
    # check if the connection is open
    if ser.isOpen():
        print("Connected to: " + ser.portstr)
    else:
        print("Failed to connect to: " + ser.portstr)
        exit(1)
        
    # write to tty
    # 0 Voltage The controller’s input voltage
    """
    The three digital forms of communication (TTL Serial, SPI, and I2C) are implemented by reading / writing 
    to a set of 16-bit registers. The available registers are described in the tables below. 
    Note: that the registers are divided into Read and Write registers.
    """
    command_start = 1  # Command start is always 1
    device_id = 0x00
    first_byte = (command_start << 7) | (device_id & 0x3F) 
    # print bits of first_byte
    print(bin(first_byte)[2:].zfill(8))
    
    device_id = 0x00
    voltage_register = 0x00
    current_register = 0x03 # 3
    
    castle_read(ser, current_register)
    
    # test writing throttle
    """
    Register Name Description Write
    128 Throttle The controller’s commanded throttle value 0 to 65535
    """
    
    throttle_register = 128
    throttle_value = 21845 # 0x8000
    castle_write(ser, throttle_register, throttle_value)
    