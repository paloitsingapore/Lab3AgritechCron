import serial
import json
import sys
import datetime
import time 

import logging
import logging.handlers
import os
import persistqueue
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/logs/SWITCH_SENSOR__" + datetime.datetime.today().strftime('%Y-%m-%d') + "_error.log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
#formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

#SID=sys.argv[1]

def Switch_Off_Device(SID):
    try:
        #port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
        #port.close()
        #port.open()
        #port.write(str.encode("ID=" + SID + ",switch off\r\n"))
        q = persistqueue.SQLiteQueue('run-switch', auto_commit=True)
        q.put("ID=" +  SID  +",switch off\r\n")
        logging.info("Switch off command for SID "+ SID +" id added to queue") 

    except Exception as e:
        logging.error("Not able to switch off the power" + str(e))
        raise

