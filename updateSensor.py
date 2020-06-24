import os
import sys
import datetime
import subprocess
from crate import client
from myip import GetIP 
import dbHandler
import time
import math
import pytz
import timeConvert
import logging
import logging.handlers
import os

import switch_on
import switch_off

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/logs/sensor_status_" + datetime.datetime.today().strftime('%Y-%m-%d') + ".log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

def check(container):
    timestamp_n = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(timestamp_n)
    container = dbHandler.GetListContainer()
    container = str(container).replace('[','').replace(']','').replace('\'', '')
    mac_list = dbHandler.GetMac(container)
    delta = 0
    for mac in mac_list:
        mac = str(mac).replace('[','').replace(']','').replace('\'', '')
        logging.info("MAC Address: " + str(mac))
        latest_ts = dbHandler.GetSensorTsLatest(mac)
        delta = timeConvert.getDelta(ts_1=latest_ts,ts_2=timestamp_n, dt="min")
        delta = round(delta,1)
        logging.info(str(delta)+ " Min")
        if delta > 15:  
            dbHandler.UpdateSensor(mac,container,"deactivate")
        elif delta < 15:
            dbHandler.UpdateSensor(mac,container,"activate")
        
        logging.info("Last updated timestamp: " + str(latest_ts))
    if delta > 0 :
        return 1
    else:
        return 0

if __name__ == '__main__':
    container = dbHandler.GetListContainer()
    result = check(container)
    logging.info(str(result))
