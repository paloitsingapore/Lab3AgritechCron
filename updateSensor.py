import datetime
import dbHandler
import time
import timeConvert
import logging
import logHandler 
import fmtLocal

logHandler.run("sensor_status")

def check():
    timestamp_n = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(timestamp_n)
    mac_list = dbHandler.GetMacAll()
    logging.info(mac_list)
    delta = 0
    for mac in mac_list:
        mac = fmtLocal.remSqBQ(str(mac))
        logging.info("MAC Address: " + str(mac))
        latest_ts = dbHandler.GetSensorTsLatest(mac)
        delta = timeConvert.getDelta(ts_1=latest_ts,ts_2=timestamp_n, dt="min")
        delta = round(delta,1)
        logging.info(str(delta)+ " Min")
        if delta > 30:  
            dbHandler.UpdateSensor(mac,"deactivate")
        elif delta < 30:
            dbHandler.UpdateSensor(mac,"activate")   
        logging.info("Last updated sensor ts: " + str(latest_ts))
    if delta > 0 :
        return 1
    else:
        return 0

if __name__ == '__main__':
    result = check()
    logging.info(str(result))
