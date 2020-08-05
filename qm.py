import logging.handlers
import serial
import json
import sys
import datetime
import time
import logging
import os
import persistqueue
from tendo import singleton
import logHandler 

logHandler.run("switch_sensors_qm")


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
            logging.error("Unable to open serial port to read command status: " + str(e))
        logging.info("Request: "+  str(cmd["qreq"]))
        count = 0
        while True:
            rcv = ser.read(300)
            logging.info("Response: " + str(rcv))
            if 'ON' in str(rcv):
                try_cmd = False
                try_cnt = 2
                if 'RELAY=?' in str(cmd):
                    logging.info("Looking for Switch ID: " +str(cmd["qsid"]))
                if 'SWITCH ON' in str(cmd):
                    logging.info("Switching ON Device ID: "+str(cmd["qsid"]))    
                logging.info("Status=============> ON")
                break
            if 'OFF' in str(rcv):
                try_cmd = False
                try_cnt = 2
                #logging.info(str(rcv))
                if 'RELAY=?' in str(cmd):
                    logging.info("Looking for Switch ID: " +str(cmd["qsid"]))
                if 'SWITCH OFF' in str(cmd):
                    logging.info("Switching OFF Device ID: "+str(cmd["qsid"]))    
                logging.info("Status=============> OFF")
                break
            if count > 4:
                logging.info('No feeback from Switch')
                break
            count = count + 1
            try_cnt = try_cnt + 1
            time.sleep(2)

if __name__ == '__main__':
    logging.info('Executing code with pid...'+ str(os.getpid()))
    while True:
        try:
            q = persistqueue.SQLiteQueue('lora-switch', auto_commit=True)       
        except Exception as e:
            logging.error('process is already running'+ str(e))
            sys.exit(1)
        time.sleep(1)        
        if q.size > 0:
            logging.info(str(q.size) + " items to be processed")
            cmd = q.get()
            logging.info("Processing ..." + str(cmd["qreq"]))
            run_cmd(cmd)        
        else:
            sys.exit(1)
 


