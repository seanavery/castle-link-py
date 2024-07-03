# Read Registers
read_reg_to_name = {
    0x00: "voltage",
    0x01: "ripple",
    0x02: "current",
    0x03: "throttle",
    0x04: "power",
    0x05: "speed",
    0x06: "temperature",
    0x07: "bec_voltage",
    0x08: "bec_current",
    0x09: "raw_ntc",
    0x0A: "raw_linear",
    0x19: "link_live",
    0x1A: "failsafe",
    0x1B: "e_stop",
    0x1C: "packet_in",
    0x1D: "packet_out",
    0x1E: "baudrate",
    0x1F: "packet_bad",
}

# Write Registers
write_name_to_reg = {
    "throttle": 0x80,
    "fail_safe": 0x81,
    "e_stop": 0x82,
    "packet_in": 0x83,
    "packet_out": 0x84,
    "baudrate": 0x85,
    "packet_bad": 0x86,
}

# Parse
# Scale, Max, Units
scale_name_to_parse = {
    "voltage": (20.0, 100, "Volts"),
    "ripple": (4.0, 20, "Volts"),
    "current": (50.0, 250, "Amps"),
    "throttle": (0.2502, 1, "Percent"),
    "power": (0.2502, 1, "Percent"),
    "speed": (20416.66, 100000, "Electricl RPM"),
    "temperature": (30.0, 150, "Degraees C"),
    "bec_voltage": (4.0, 20, "Volts"),
    "bec_current": (4.0, 20, "Amps"),
    "raw_ntc": (63.8125, 255, "Units"),
    "raw_linear": (30.0, 150, "Degrees C"),
}

num_name_to_parse = {
    "link_live": (1.0, 1, "Boolean"),
    "failsafe": (1.0, 1, "Boolean"),
    "e_stop": (1.0, 1, "Boolean"),
    "packet_in": (1.0, 1, "Packets"),
    "packet_out": (1.0, 1, "Packets"),
    "baudrate": (1.0, 1, "Bits per second"),
    "packet_bad": (1.0, 1, "Packets"),
}
