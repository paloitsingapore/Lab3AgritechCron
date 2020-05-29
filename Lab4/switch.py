import persistqueue
from tendo import singleton
import os
import datetime
import time
import sys
import logging
import logging.handlers
import os
import persistqueue
#from serial import Serial
import serial
import time
import sys
import time

def run_cmd(cmd):
    try_cmd = True
    try_cnt = 0
    while try_cmd and try_cnt < 2:
        port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
        try:
            ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
            rcv = ser.read(300)
            port.close()
            port.open()
            port.write(str.encode(cmd["qreq"]))
            
        except Exception as e:
            logging.error("Unable to open serial port to read command status")
        print("Request: "+  str(cmd["qreq"]))
        count = 0
        while True:
            rcv = ser.read(300)
            print("Response: " + str(rcv))
            if 'RELAY=ON' in str(rcv):
                try_cmd = False
                try_cnt = 2
                if 'RELAY=?' in str(cmd):
                    print("Looking for Switch ID: " +str(cmd["qsid"]))
                if 'SWITCH ON' in str(cmd):
                    print("Switching ON Device ID: "+str(cmd["qsid"]))    
                print("Status=============> ON")
                break;
            if 'RELAY=OFF' in str(rcv):
                try_cmd = False
                try_cnt = 2
                #print(str(rcv))
                if 'RELAY=?' in str(cmd):
                    print("Looking for Switch ID: " +str(cmd["qsid"]))
                if 'SWITCH OFF' in str(cmd):
                    print("Switching OFF Device ID: "+str(cmd["qsid"]))    
                print("Status=============> OFF")
                #print("Ack Received for " + str(cmd["qsys"]))
                break;
            if count > 4:
                print('No Response from Switch after 10 Sec also')
                #break;
                sys.exit(1)
            count = count + 1
            time.sleep(2)

if __name__ == '__main__':
    # port.write(str.encode("ID=" + SID + ",switch on\r\n"))
    print('Executing code with pid...'+ str(os.getpid()))
    try:
        q = persistqueue.SQLiteQueue('lora-switch', auto_commit=True)     
          
    except Exception as e:
        logging.error('process is already running')
        sys.exit(1)
    while True:
        time.sleep(1)        
        if q.size > 0:
            print(str(q.size) + " items to be processed ")
            cmd = q.get()
            print("Processing ..." + str(cmd["qreq"]))
            run_cmd(cmd)
        else:
            q = persistqueue.SQLiteQueue('lora-switch', auto_commit=True)
            sys.exit(1)
 
    
    

