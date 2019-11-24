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

ser = None

#ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)
try:
    ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
except:
    print("port not working")
data_path = '/home/pi/data'

def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print(host_ip)
        return host_ip
    except:
        print("Unable to get Hostname and IP")

def dataformat(data):
    try:
        ID = re.findall(r",ID:(.+?),STAT",data)
        TEMP = re.findall(r",T:(.+?)\\xa1\\xe6,", data)
        HUMIDITY = re.findall(r",H:(.+?)%,", data)
        CURRENTDT = str(datetime.datetime.now())

        print(ID[0])
        print(TEMP[0])
        print(HUMIDITY[0])

        return {"mac_add": ID[0], "time": CURRENTDT, "temperature": TEMP[0], "humidity": HUMIDITY[0]}

    except ValueError as ve:
        print (ve)



def insertdb(data):
    try: 
        value = json.loads(data)
        dbHandler.InsertDB(**value)
    except:
        print ("Insert Fail")

def writefile(data):
    try:
        file = open(data_path + '/' + datetime.datetime.today().strftime('%Y-%m-%d') + '-THDATA.txt',"a+")
        file.write(json.dumps(data) + '\n')
        file.close
    except:
        print("Not able to write to the file")

while True:
    try:
        rcv = ser.read(300)
        if (str(rcv)[1:] != '\'\''):
            data = str(rcv)[1:]
            print(data)
            #data = 'GW_ID:2,TYPE:T&H,ID:286851425,STAT:00000000,T:25.9\xa1\xe6,H:62.3%,ST:5M,V:3.55v,SN:72,RSSI:-48dBm,S:22.5769,E:113.9712,Time:0-0-0 0:0:0,T_RSSI:-80dBm\r\n'
            try:
                json_data = json.dumps(dataformat(data))
                writefile(json_data)
                masterip = str(subprocess.run(["python3", "IsMaster.py"], stdout=subprocess.PIPE).stdout)
                masterip = masterip[2:-3]
                currentip = get_Host_name_IP()
                if str(masterip).strip() == str(currentip).strip(): 
                    insertdb(json_data)
                else:
                    print("i am not master")
            except Exception as e:
                print("record error:" + str(e))
    except:
        try:
            time.sleep(10)
            ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
        except:
            print ("waiting for gateway")
	
	

