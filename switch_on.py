import serial
import json

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)

port.close()

port.open()
port.write(str.encode("ID=1234,switch on\r\n"))


