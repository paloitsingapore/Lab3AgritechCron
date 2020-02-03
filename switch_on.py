import serial
import json
import sys
import datetime
import time
import logging
import logging.handlers
import os

#SID=sys.argv[1]

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/logs/SWITCH_SENSOR__" + datetime.datetime.today().strftime('%Y-%m-%d') + "_error.log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
#formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

def write_file(STATUS):
    print('inside write file')
    f = open('webserver_status.txt','w')
    f.write(str(STATUS))
    f.close()

def read_file():
    try:
        f = open('webserver_status.txt', 'r')
        status = f.read()
        f.close
        print(status)
        return status
    except Exception as e:
        print(e)
        return 0 

def Switch_On_Device(SID):
    try:
        if read_file() == '0':
            
            write_file(1)
            time.sleep(3)
            port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)

            port.close()

            port.open()
            port.write(str.encode("ID=" + SID + ",switch on\r\n"))

         
        else:	
            logging.error("Too Many Request")

        write_file(0)

    except Exception as e:
        write_file(0)
        logging.error("Not able to switch on the power" + str(e))
        raise


