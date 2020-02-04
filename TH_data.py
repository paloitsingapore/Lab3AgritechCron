import sys
import time
import datetime
import subprocess
import socket
sys.path.append("./")
import re
import serial
import json
import dbHandler

import logging
import logging.handlers
import os

ser = None

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/logs/TH_SENSOR__" + datetime.datetime.today().strftime('%Y-%m-%d') + "_error.log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
#formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

#ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
try:
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
except Exception as e:
    logging.error("Port is not Working:" + str(e))
data_path = '/home/pi/data'

def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        return host_ip
    except Exception as e:
        logging.error("Unable to get Hostname and IP:" + str(e))

def dataformat(data):
    try:
        ID = re.findall(r",ID:(.+?),STAT",data)
        TEMP = re.findall(r",T:(.+?)\\xa1\\xe6,", data)
        HUMIDITY = re.findall(r",H:(.+?)%,", data)
        CURRENTDT = str(datetime.datetime.now())

        return {"mac_add": ID[0], "time": CURRENTDT, "temperature": TEMP[0], "humidity": HUMIDITY[0]}

    except ValueError as e:
        logging.error("Data Formate is wrong:" + str(e))



def insertdb(data, sensor_type):
    try: 
        value = json.loads(data)
        if (sensor_type == 'AIR'):
            dbHandler.InsertDB('TH_DATA',**value)
        if (sensor_type == 'SOIL'):
            dbHandler.InsertDB('SOIL_DATA',**value)

    except Exception as e:
        logging.error("Database Insertion is Fail:" + str(e))

def writefile(data, sensor_type):
    try:
        if(sensor_type == 'AIR'):
            file = open(data_path + '/' + datetime.datetime.today().strftime('%Y-%m-%d') + '-AIR-THDATA.txt',"a+")
            file.write(json.dumps(data) + '\n')
            file.close
        if(sensor_type == 'SOIL'):
            file = open(data_path + '/' + datetime.datetime.today().strftime('%Y-%m-%d') + '-SOIL-THDATA.txt',"a+")
            file.write(json.dumps(data) + '\n')
            file.close

    except Exception as e:
        logging.error("Not able to write to the file:" + str(e))

while True:
    try:
        rcv = ser.read(300)
        if (str(rcv)[1:] != '\'\''):
            data = str(rcv)[1:]
            #data = 'GW_ID:2,TYPE:T&H,ID:286851425,STAT:00000000,T:25.9\xa1\xe6,H:62.3%,ST:5M,V:3.55v,SN:72,RSSI:-48dBm,S:22.5769,E:113.9712,Time:0-0-0 0:0:0,T_RSSI:-80dBm\r\n'
            try:
                value = dataformat(data)
                json_data = json.dumps(value)
                sensor_type = dbHandler.GetSensorType(value['mac_add'])
                writefile(json_data, sensor_type)
                masterip = str(subprocess.run(["python3", "IsMaster.py"], stdout=subprocess.PIPE).stdout)
                masterip = masterip[2:-3]
                currentip = get_Host_name_IP()
                if str(masterip).strip() == str(currentip).strip(): 
                    insertdb(json_data, sensor_type)
                else:
                    print("i am not master")
            except Exception as e:
                logging.error("record value:" + str(data))
                logging.error("record error:" + str(e))
    except:
        try:
            time.sleep(10)
            ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
        except:
            logging.error("Waiting for gateway.")
	
	

