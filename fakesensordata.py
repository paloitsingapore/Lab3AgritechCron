import datetime
import dbHandler
import json
import time
import logging
import logHandler 

logHandler.run("fake_data")

sensorList = ['000000001', '000000002', '000000003']
sensorTemp = 29
sensorHumid = 70

def insertdb(data):
    try:
        value = json.loads(data)
        dbHandler.InsertDB('TH_DATA',**value)
    except Exception as e:
        logging.info("Database Insertion is Fail:" + str(e))

ListOfContainer = dbHandler.GetListContainer()

for i in range(5):
    CURRENTDT = str(datetime.datetime.now())
    data ={"mac_add": "outdoor", "time": CURRENTDT, "temperature": "28", "humidity": "60"}
    json_data = json.dumps(data)
    insertdb(json_data)
    for each_container in ListOfContainer:
        start_humid, stop_humid, start_temp, stop_temp, fan_id, mist_id, fanning, auto_fanning, misting, auto_misting = dbHandler.GetContainerInfo(each_container)
        if (not fanning and not misting):
            sensorTemp += 0.5
            sensorHumid -= 0.2
            for sensor in sensorList:
                data = {"mac_add": sensor, "time": CURRENTDT, "temperature": str(sensorTemp), "humidity": str(sensorHumid)}
                json_data = json.dumps(data)
                insertdb(json_data)
            logging.info("No system on -> Insert MacAdd 0001 temp increasing and humiditu decreasing")
        elif (fanning and not misting):
            sensorTemp -= 0.2
            sensorHumid -= 0.2
            for sensor in sensorList:
                data = {"mac_add": sensor, "time": CURRENTDT, "temperature": str(sensorTemp), "humidity": str(sensorHumid)}
                json_data = json.dumps(data)
                insertdb(json_data)
            logging.info("Fanning is on -> Insert MacAdd 0001 temp decreasing and humidity increasing")
        elif (not fanning and misting):
            sensorTemp += 0.2
            sensorHumid += 0.2
            for sensor in sensorList:
                data = {"mac_add": sensor, "time": CURRENTDT, "temperature": str(sensorTemp), "humidity": str(sensorHumid)}
                json_data = json.dumps(data)
                insertdb(json_data)
            logging.info("Misting is on -> Insert MacAdd 0001 temp increasing and humidity increasing")
        elif (fanning and misting):
            sensorTemp -= 0.2
            sensorHumid += 0.2
            for sensor in sensorList:
                data = {"mac_add": sensor, "time": CURRENTDT, "temperature": str(sensorTemp), "humidity": str(sensorHumid)}
                json_data = json.dumps(data)
                insertdb(json_data)
            logging.info("Misting and Fanning are on -> Insert MacAdd 0001 temp decreasing and humidity indreasing")

        logging.info(str(sensorTemp))
        logging.info(str(sensorHumid))
    time.sleep(60)
