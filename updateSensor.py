import datetime
import dbHandler
import time
import timeConvert
import logging
import logHandler 
import fmtLocal

logHandler.run("sensor_status")

def check(container):
    timestamp_n = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(timestamp_n)
    container = dbHandler.GetListContainer()
    container = fmtLocal.remSqBQ(str(container)) 
    logging.info(container)
    mac_list = dbHandler.GetMac(container)
    logging.info(mac_list)
    delta = 0
    for mac in mac_list:
        mac = fmtLocal.remSqBQ(str(mac))
        logging.info("MAC Address: " + str(mac))
        latest_ts = dbHandler.GetSensorTsLatest(mac)
        delta = timeConvert.getDelta(ts_1=latest_ts,ts_2=timestamp_n, dt="min")
        delta = round(delta,1)
        logging.info(str(delta)+ " Min")
        if delta > 15:  
            dbHandler.UpdateSensor(mac,container,"deactivate")
        elif delta < 15:
            dbHandler.UpdateSensor(mac,container,"activate")   
        logging.info("Last updated sensor ts: " + str(latest_ts))
    if delta > 0 :
        return 1
    else:
        return 0

if __name__ == '__main__':
    container = dbHandler.GetListContainer()
    result = check(container)
    logging.info(str(result))
