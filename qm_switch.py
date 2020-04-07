import logging.handlers
import serial
import json
import sys
import datetime
import time
import logging
import logging.handlers
import os
import persistqueue
import time
import sys
import time
from tendo import singleton


handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE",
                   "/home/pi/logs/SWITCH_SENSOR_REPORT" + datetime.datetime.today().strftime('%Y-%m-%d') + "_error.log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}', style='{')
handler.setFormatter(formatter)
root = logging.getLogger()
 
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)


def run_cmd(cmd):
    try_cmd = True
    try_cnt = 0
    logging.info('trying switch on ')
    while try_cmd and try_cnt < 2:
        logging.info( str(os.getpid()) +'inside while loop')
        port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
        try:
            logging.info( str(os.getpid()) +'insid try')
            ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
            rcv = ser.read(300)
            print(str(rcv))
            logging.info( str(os.getpid()) +str(rcv))
        except Exception as e:
            logging.error("Unable to open serial port to read command status")
        port.close()
        port.open()
        port.write(str.encode(cmd))
        print(cmd)
        logging.info( str(os.getpid()) +cmd + " sent...")
 
        count = 0
        while True:
            rcv = ser.read(300)
            logging.info( str(os.getpid()) +" Receive... " + str(rcv))
            if 'CMD Send OK!' in str(rcv):
                try_cmd = False
                try_cnt = 4
                print("Ack Received for .." + str(cmd))
                print(str(rcv))
                logging.info( str(os.getpid()) +"Ack Received for " + str(rcv))
                break;
            if count > 7:
                print('No Response from Switch after 10 Sec also')
 
                logging.error('No Response from Switch after 10 Sec also')
                break;
            print(count)
            logging.info( str(os.getpid()) + str(count))
            count = count + 1
            time.sleep(1)
        if not try_cmd:
 
            break;
        try_cmd = True
        try_cnt = try_cnt + 1
        if try_cnt < 3:
            print('Retry ' + str(try_cnt))
        else:
            print('Switch not responding after 3 retry also')

if __name__ == '__main__':
    # port.write(str.encode("ID=" + SID + ",switch on\r\n"))
    logging.info( str(os.getpid()) +'Executing qm_switch python...'+ str(os.getpid()))
    try:
        me = singleton.SingleInstance()
        q = persistqueue.SQLiteQueue('run-switch', auto_commit=True)       
    except Exception as e:
        logging.error('process is already running')
        sys.exit(1)
    while True:
        time.sleep(1)        
        #print('looking for command to run..')
       
        if q.size > 0:
            print(q.size)
            logging.info( str(os.getpid()) +str(q.size) + " items to be processed ")
            cmd = q.get()
            logging.info( str(os.getpid()) +"Processing ..." + str(cmd))
            print(cmd)
            run_cmd(cmd)
        else:
            q = persistqueue.SQLiteQueue('run-switch', auto_commit=True)


