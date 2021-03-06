import serial
import json
import sys
import datetime
import time
import logging
import logging.handlers
import os
import persistqueue
#SID=sys.argv[1]

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/logs/SWITCH_SENSOR__" + datetime.datetime.today().strftime('%Y-%m-%d') + "_error.log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
#formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

def Switch_On_Device(SID):
    try:
        #port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
        #port.close()
        #port.open()
        #port.write(str.encode("ID=" + SID + ",switch on\r\n"))
        q = persistqueue.SQLiteQueue('run-switch', auto_commit=True)
        q.put("ID=" +  SID  +",switch on\r\n")
        logging.info("Adding Switch on command for SID "+ SID +" in Queue" )


    except Exception as e:
        logging.error("Not able to switch on the power" + str(e))
        raise


