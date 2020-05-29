import persistqueue
from tendo import singleton
import json

import runpy


if __name__ == '__main__':

    q = persistqueue.SQLiteQueue('lora-switch', auto_commit=True)
    STAT = input("Type 1 to get the status of Switch \r\nType 2 to Turn ON/OFF Lora Switch \r\nEnter your input: ")
    SID = input("###1239,1240,1241,1243### \r\nEnter device ID: ") 
    

    if STAT == "1":
        y = dict(qreq= "ID=" +  SID  +",RELAY=?\r\n", qstat ="start", qsys = "FAN", qsid = SID)
        q.put(y)
    if STAT == "2":
        ACT = input("Your Action ON/OFF: ")
        x = dict(qreq= "ID=" +  SID  +",SWITCH "+ACT+"\r\n", qstat ="start", qsys = "FAN", qsid = SID)
        q.put(x)


    exec(open('/home/pi/codebase/Lab3AgritechCron/switch.py').read())
  
