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
    0x1E: "check_baud",
    0x1F: "packet_bad",
}
# Write Registers
THROTTLE_WRITE = 0x80
FAIL_SAFE_WRITE = 0x81
E_STOP_WRITE = 0x82
PACKET_IN_WRITE = 0x83
PACKET_OUT_WRITE = 0x84
CHECK_BAUD_WRITE = 0x85
PACKET_BAD_WRITE = 0x86

# Parse
# Scale, Max, Units
VOLTAGE_PARSE = (20.0, 100, "Volts")
RIIPLE_PARSE = (4.0, 20, "Volts")
CURRENT_PARSE = (50.0, 250, "Amps")
POWER_PARSE = (0.2502, 1, "Percent")
RPM_PARSE = (20416.66, 100000, "Electrical RPM")
BEC_VOLTAGE_PARSE = (4.0, 20, "Volts")
BEC_CURRENT_PARSE = (4.0, 20, "Amps")
TEMPERATURE_PARSE = (30.0, 150, "Degrees C")
RAW_NTC_PARSE = (63.8125, 255, "Units")
RAW_LINEAR_PARSE = (30.0, 150, "Degrees C")

convert_name_to_parse = {
    "voltage": (20.0, 100, "Volts"),
    "ripple": (4.0, 20, "Volts"),
    "current": (50.0, 250, "Amps"),
    "throttle": (0.2502, 1, "Percent"),
    "power": (0.2502, 1, "Percent"),
    "speed": (20416.66, 100000, "Electrical RPM"),
    "temperature": (30.0, 150, "Degrees C"),
    "bec_voltage": (4.0, 20, "Volts"),
    "bec_current": (4.0, 20, "Amps"),
    "raw_ntc": (63.8125, 255, "Units"),
    "raw_linear": (30.0, 150, "Degrees C"),
    "link_live": (1.0, 1, "Boolean"),
    "failsafe": (1.0, 1, "Boolean"),
    "e_stop": (1.0, 1, "Boolean"),
    "packet_in": (1.0, 1, "Boolean"),
    "packet_out": (1.0, 1, "Boolean"),
    "check_baud": (1.0, 1, "Bits per second"),
    "packet_bad": (1.0, 1, "Boolean"),
}
