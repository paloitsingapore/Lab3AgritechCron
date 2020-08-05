import serial
import json
import sys
import datetime
import time
import logging
import logging.handlers
import os
import persistqueue
import logHandler 

logHandler.run("switch_sensors")

def trigger(SID,SYSTEM,STAT,ACT):
    q = persistqueue.SQLiteQueue('lora-switch', auto_commit=True)
    time.sleep(2)
    if STAT == "1":
        y = dict(qreq= "ID=" +  SID  +",RELAY=?\r\n", qstat =STAT, qsys = SYSTEM, qsid = SID)
        q.put(y)
    elif STAT == "2":
        x = dict(qreq= "ID=" +  SID  +",SWITCH "+ACT+"\r\n", qstat =STAT, qsys = SYSTEM, qsid = SID)
        q.put(x)
    exec(open('/home/pi/Lab3AgritechCron/qm.py').read())

def action(SYSTEM,STAT="1",ACT="NIL"):
    try:
        if SYSTEM == "FAN":
            a = ["1240","1241","1243"]
            for x in range(len(a)): 
                logging.info(a[x])
                trigger(a[x],SYSTEM,STAT,ACT)
        elif SYSTEM == "MIST":
            b = ["1239"]
            for x in range(len(b)): 
                logging.info(b[x])
                trigger(b[x],SYSTEM,STAT,ACT)

    except Exception as e:
        logging.info("Not able to switch on the power" + str(e))


if __name__ == "__main__":
    action("MIST","1","ON")

