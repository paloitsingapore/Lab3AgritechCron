import serial
import json
import sys

SID=sys.argv[1]

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)

port.close()

port.open()
port.write(str.encode("ID=" + SID + ",switch on\r\n"))


