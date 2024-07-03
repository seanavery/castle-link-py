# castle-link-py
> read/write to castle creations esc with python

![Castle Serial Link](./etc/castle_serial_link.png)

## Why?

Want to get the vEgo (velocity) of your rc-car without installing wheel encoders? How about realtime battery metrics? You can even control the throttle without a pwm driver! 

## How?

### Hardware
You are going to need some Castle Creations hardware.
- Castle Creations ESC
- Castle Creations Serial Link
- FTDI Serial TTY Adapter

### Software

```
csl = CastleSerialLink(port="/dev/ttyUSB0", baudrate=115200)
```

### Read

```
csl.listen(40)
for i in range(100):
    time.sleep(0.5)
    print(csl.state)
csl.stop()
```

## Remove sudo requirement
```
sudo usermod -a -G dialout
```

## Refs
- [old castle link docs](https://www.astramodel.cz/manualy/castle_creations/castle_serial_link_v1_5.pdf)
