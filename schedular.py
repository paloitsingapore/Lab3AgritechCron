import os
import sys
import dbHandler
import time
import json
import requests
import datetime
from datetime import timedelta

from multiprocessing import Process

import logging
import logging.handlers
import os

import switch_on
import switch_off

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/logs/BRAIN_" + datetime.datetime.today().strftime('%Y-%m-%d') + "_error.log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
#formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

switch_server1_ip = "192.168.1.103"
switch_server2_ip = "192.168.1.104"
wechat_url = "54.255.187.114"
user_id = ["ok99-wWEUEanEXFDBjxsd1vH7Rvo","ok99-wev6t-aZRaAHffRZS1tAP0g"]

def sendhttp_request(sensor_id,status,system):
    try:
        if status == "start":
            switch_on.Switch_On_Device(sensor_id)
            time.sleep(10)
            switch_on.Switch_On_Device(sensor_id)
        if status == "stop":
            switch_off.Switch_Off_Device(sensor_id)
            time.sleep(10)
            switch_off.Switch_Off_Device(sensor_id)

        logging.info("{} SWITCH ID: {} HAS BEEN {}ed".format(system, sensor_id, status))
    except Exception as e:
        logging.error("SWITCH NOT WORKING. ERROR: " + str(e))  
         
    
    
def sendhttp_request2(sensor_id,status, system):
    request_str_1 = ''
    request_str_2 = ''
    if status == "start":
        request_str_1 = "http://{}:8090/switch/ON/{}".format(switch_server1_ip, sensor_id)
        request_str_2 = "http://{}:8090/switch/ON/{}".format(switch_server2_ip, sensor_id)
    elif status == "stop":
        request_str_1 = "http://{}:8090/switch/OFF/{}".format(switch_server1_ip, sensor_id)
        request_str_2 = "http://{}:8090/switch/OFF/{}".format(switch_server2_ip, sensor_id)
    
    try:
        try:
            response = requests.get(request_str_1, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if result["STATUS"] == 'success':
                    logging.info("{} SWITCH ID: {} HAS BEEN {}ed".format(system, sensor_id, status))
                    return True
                elif result["STATUS"] == 'fail':
                    logging.info("Server1 {} is not working. Let's change to another Server {}".format(switch_server1_ip, switch_serve2_ip))
                    response2 = requests.get(request_str_2, timeout=10)
                    if response2.return_code == 200:
                        result2 = response2.json()
                        if result2["STATUS"] == 'success':
                            logging.info("{} SWITCH ID: {} HAS BEEN {}".format(system, sensor_id, status))
                            return True
                        elif result["STATUS"] == 'fail':
                            logging.error("Server2 {} is not working too. Please check".format(switch_server2_ip))
                            return False
                    else:
                        logging.error("Both servers switch is not working. Please Control the Switch manually")  

        except:
            logging.info("Server1 {} is not working. Let's change to another Server {}".format(switch_server1_ip, switch_server2_ip))
            response2 = requests.get(request_str_2, timeout=10)
            if response2.status_code == 200:
                result2 = response2.json()
                if result2["STATUS"] == 'success':
                    logging.info("{} SWITCH ID: {} HAS BEEN {}ed".format(system, sensor_id, status))
                    return True
                elif result["STATUS"] == 'fail':
                    logging.error("Server2 {} is not working too. Please check".format(switch_server2_ip))
                    return False
            else:
                logging.error("Both servers switch is not working. Please Control the Switch manually")  
                
    except Exception as e:
        logging.error("Both servers switch is not working. Please Control the Switch manually" + str(e))  
                
        
    
def Timechecking(time_min, container_id, sensor_id, activity_id, typing, systemtype):
    target_time = datetime.datetime.now() + datetime.timedelta(minutes = time_min)
    while True:
        currentmisting = dbHandler.GetContainerStatus(container_id, typing)
        current_time = datetime.datetime.now()
        if(not currentmisting):
            dbHandler.UpdateUserActions('2', systemtype, 'true', container_id, '1')
            avetemp, avehumid = dbHandler.GetAveTempHumid(container_id)
            endtime = str(datetime.datetime.now())
            sendhttp_request(sensor_id, "stop", systemtype)
            dbHandler.UpdateActivity(activity_id, sensor_id, endtime, avetemp, avehumid)
            try:
                for each_user in user_id:
                    url = "http://{}/alert/{}/{} is STOPPED MANUALLY. Current temp is {} and humidity is {}".format(wechat_url, each_user, typing, round(avetemp, 1), round(avehumid, 1))
                    requests.get(url, timeout=2)
            except:
                print("error with wechat sending")
            time.sleep(30)
            break;
     
        if current_time > target_time:
            dbHandler.UpdateUserActions('2', systemtype, 'true', container_id, '1')
            avetemp, avehumid = dbHandler.GetAveTempHumid(container_id)
            endtime = str(datetime.datetime.now())
            sendhttp_request(sensor_id,"stop", systemtype) 
            dbHandler.UpdateContainerStatus(container_id, typing, "false")
            dbHandler.UpdateActivity(activity_id, sensor_id, endtime, avetemp, avehumid)
            try:
                for each_user in user_id:
                    url = "http://{}/alert/{}/{} is STOPPED due to time up. Current temp is {} and humidity is {}".format(wechat_url, each_user, typing, round(avetemp, 1), round(avehumid, 1))
                    requests.get(url, timeout=2)
            except:
                print("error with wechat sending")
            time.sleep(30)            
            break;
        time.sleep(30)
	    
def startmisting(container_id, humid_now, upper_target_humid, lower_target_humid,sensor_id, manual=False, time_duration=0):
    index = 0
    indexofstart = True
    beforehumid=0
    time_flag = False
    timenow = str(datetime.datetime.now())
    dbHandler.UpdateContainerStatus(container_id, "misting", "true")
    time.sleep(2)
    
    if manual:
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/Misting is STARTED MANUALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(humid_now, 1))
                requests.get(url, timeout=2)
        except:
            print("error with wechat sending")
    else:
        sendhttp_request(sensor_id,"start", "MIST")
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/Misting is STARTED AUTOMATICALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(humid_now, 1))
                requests.get(url, timeout=2)
        except:
            print("error with wechat sending")
    
    while True:
        avetemp, avehumid = dbHandler.GetAveTempHumid(container_id)
        currentmisting = dbHandler.GetContainerStatus(container_id, "misting")
        if indexofstart:
            dbHandler.InsertActivity(timenow, sensor_id, timenow, "MIST", avetemp, avehumid)
            indexofstart = False

        if(not currentmisting):
            endtime = str(datetime.datetime.now())
            sendhttp_request(sensor_id, "stop", "MIST")
            #dbHandler.UpdateContainerStatus(container_id, "misting", "false")
            dbHandler.UpdateActivity(timenow, sensor_id, endtime, avetemp, avehumid)
            try:
                for each_user in user_id:
                    url = "http://{}/alert/{}/Misting is STOPPED MANUALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(avehumid, 1))
                    requests.get(url, timeout=2)
            except:
                print("error with wechat sending")        
            time.sleep(60)
            break;

        if manual:
            sendhttp_request(sensor_id,"start", "MIST")
            p = Process(target=Timechecking, args=(time_duration, container_id, sensor_id, timenow, "misting", "MIST", ))
            p.start()
            break;
            
        else:
            if(avehumid < lower_target_humid):
	        #startmisting-switch keep on starting              
                time.sleep(10)
            elif(avehumid > lower_target_humid and avehumid < upper_target_humid):
                time.sleep(10)
            elif(avehumid > upper_target_humid):
                endtime = str(datetime.datetime.now())
                sendhttp_request(sensor_id, "stop", "MIST") 
                #update database 
                dbHandler.UpdateContainerStatus(container_id, "misting", "false")
                dbHandler.UpdateActivity(timenow, sensor_id, endtime, avetemp, avehumid)
                try:
                    for each_user in user_id:
                        url = "http://{}/alert/{}/Misting is STOPPED AUTOMATICALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(avehumid, 1))
                        requests.get(url, timeout=2)
                except:
                    print("error with wechat sending")
                time.sleep(10)            
                break;
            else:
                print("testing")        
            
        if avehumid < beforehumid:
            print("this is good. humidity is increasing")
            beforehumid = avehumid
            time.sleep(10)
            
        if beforehumid < avehumid:
            print("this is the alert. we have problem of switching misting now")
            ++index
            if index < 5:
                print("this is still ok")
            else:
                alert("Please check the misting")
            
        time.sleep(20)
        
            
def startfanning(container_id, temp_now, upper_target_temp, lower_target_temp,sensor_id, manual=False, time_duration=0):
    index = 0
    indexofstart = True
    beforetemp=100
    timenow = datetime.datetime.now()
    dbHandler.UpdateContainerStatus(container_id, "fanning", "true")
    time.sleep(2)
    if manual:
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/FANNING is STARTED MANUALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(temp_now, 1))
                requests.get(url, timeout=2)
        except:
            print("error with wechat sending")        
    else:
        for each in sensor_id:
            sendhttp_request(each, "start", "FAN")            
            time.sleep(30)
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/FANNING is STARTED AUTOMATICALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(temp_now, 1))
                requests.get(url, timeout=2)
        except:
            print("error with wechat sending")
    while True:
        avetemp, avehumid = dbHandler.GetAveTempHumid(container_id)
        currentfanning = dbHandler.GetContainerStatus(container_id, "fanning")
        if indexofstart:
            for each in sensor_id:
                dbHandler.InsertActivity(int(round(timenow.timestamp())) + int(each), each, str(timenow), "FAN", avetemp, avehumid)
            indexofstart = False
            
        if(not currentfanning):
            endtime = str(datetime.datetime.now())
            for each in sensor_id:
                dbHandler.UpdateActivity(int(round(timenow.timestamp())) + int(each), each, endtime, avetemp, avehumid)
                sendhttp_request(each, "stop", "FAN")            
                time.sleep(30)
            try:    
                for each_user in user_id:    
                    url = "http://{}/alert/{}/FANNING is STOPPED MANUALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(avetemp, 1))
                    requests.get(url, timeout=2)
            except:
                print("error with wechat sending")
            #dbHandler.UpdateContainerStatus(container_id, "fanning", "false")
            time.sleep(60)
            break;
        
        if manual:
            for each in sensor_id:
                sendhttp_request(each, "start", "FAN")
                p = Process(target=Timechecking, args=(time_duration, container_id, each, int(round(timenow.timestamp())) + int(each), "fanning", "FAN", ))
                p.start()
                time.sleep(30)
            break;
        
        else:                 
            if(avetemp > upper_target_temp):
	            #startmisting-switch keep on starting  
                
                time.sleep(10)
            elif(avetemp < upper_target_temp  and avetemp > lower_target_temp):
                time.sleep(10)
            elif(avetemp < lower_target_temp):
                endtime = str(datetime.datetime.now())
                for each in sensor_id:
                    sendhttp_request(each, "stop", "FAN") 
                    time.sleep(30)
                #update database 
                    dbHandler.UpdateActivity(int(round(timenow.timestamp())) + int(each), each, endtime,avetemp, avehumid)
                dbHandler.UpdateContainerStatus(container_id, "fanning", "false")
                try:
                    for each_user in user_id:
                        url = "http://{}/alert/{}/FANNING is STOPPED AUTOMATICALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(avetemp, 1))
                        requests.get(url, timeout=2)
                except:
                    print("error with wechat sending")        
                time.sleep(10)            
                break;
            else:
                print("testing")        
            
        if avetemp > beforetemp:
            print("this is good. Temperature is decreasing")
            beforetemp = avetemp
            time.sleep(10)
        if beforetemp > avetemp:
            print("this is the alert. we have problem of switching fanninf now")
            ++index
            if index < 5:
                print("this is still ok")
            else:
                alert("Please check the fanning")
            
        time.sleep(20)
        

def stopfanning(container_id, fan_id):
    dbHandler.UpdateContainerStatus(container_id, "fanning", "false") 
    #for each in fan_id:
    #    sendhttp_request(each, "stop", "FAN")
    #    time.sleep(100)
        
    time.sleep(180)    

def ShoudStartFanMist(start_humid, start_temp, avetemp, avehumid):
    fanning = False
    misting = False

    if(avehumid < start_humid):
        misting = True
    if(avetemp > start_temp):
        fanning = True

    return misting, fanning    

if __name__ == '__main__':
    ListOfContainer = dbHandler.GetListContainer()
    for each_container in ListOfContainer:
        start_humid, stop_humid, start_temp, stop_temp, fan_id, mist_id, fanning, auto_fanning, misting, auto_misting = dbHandler.GetContainerInfo(each_container)
        avetemp, avehumid = dbHandler.GetAveTempHumid(each_container)
        should_misting, should_fanning = ShoudStartFanMist(start_humid, start_temp, avetemp, avehumid)
        fan_id_list = fan_id.split(',')
        
        manual_start_misting = dbHandler.GetSystemStatus('MIST', each_container, '(0,1)','true')
        manual_start_fanning = dbHandler.GetSystemStatus('FAN', each_container, '(0,1)', 'true')
        
        manual_stop_misting = dbHandler.GetSystemStatus('MIST', each_container, '(0)', 'false')
        manual_stop_fanning = dbHandler.GetSystemStatus('FAN', each_container, '(0)', 'false')
        
        manual_starting_misting = dbHandler.GetSystemStatus('MIST', each_container, '(0)','true')
        manual_starting_fanning = dbHandler.GetSystemStatus('FAN', each_container, '(0)', 'true')
        
        running_misting = dbHandler.GetRunningData('1','MIST', each_container)
        running_fanning = dbHandler.GetRunningData('1','FAN', each_container)

        if running_misting:
            timenow_number = int('{0:%Y%m%d%H%M}'.format(datetime.datetime.now()))
            time_should = int(running_misting[2]) + int(running_misting[1]) + 10
            if timenow_number > time_should:
                dbHandler.ClearUserActions(running_misting[0], '3', 'Unhealthy data')
                logging.info("Clear Unhealthy Misting Data ID {}".format(running_misting[0]))
        if running_fanning:
            timenow_number = int('{0:%Y%m%d%H%M}'.format(datetime.datetime.now()))
            time_should = int(running_fanning[2]) + int(running_fanning[1]) + 10
            if timenow_number > time_should:
                dbHandler.ClearUserActions(running_fanning[0], '3', 'Unhealthy data')
                logging.info("Clear Unhealthy fanning Data ID {}".format(running_fanning[0]))

        if manual_stop_misting:
            dbHandler.UpdateUserActions('2', 'MIST', 'false', each_container, '0')
            dbHandler.UpdateContainerStatus(each_container, "misting", "false")
            logging.info("Misting System Has Been Deactivated Manually")
        if manual_stop_fanning:
            dbHandler.UpdateUserActions('2', 'FAN', 'false', each_container, '0')
            dbHandler.UpdateContainerStatus(each_container, "fanning", "false")
            logging.info("Fanning System Has Been Deactivated Manually")
        if manual_starting_misting:
            time_delay = dbHandler.GetDelayTime('0', 'MIST', each_container, 'true')
            dbHandler.UpdateUserActions('1', 'MIST', 'true', each_container, '0')
            p = Process(target=startmisting, args=(each_container, avehumid, stop_humid, start_humid, mist_id, True, time_delay))
            p.start()
            logging.info("Manual is Taking Over And Misting System Has Been Activated Manually For {} Mins.".format(time_delay))
        
        if manual_starting_fanning:
            time_delay = dbHandler.GetDelayTime('0', 'FAN', each_container, 'true')
            dbHandler.UpdateUserActions('1', 'FAN', 'true', each_container, '0')
            p = Process(target=startfanning, args=(each_container, avetemp, stop_temp, start_temp, fan_id_list, True, time_delay))
            p.start()
            logging.info("Manual is Taking Over And Fanning System Has Been Activated Manually for {} Mins.".format(time_delay))
        
        
        if should_misting and auto_misting and not misting and fanning and not manual_start_misting and not manual_start_fanning:
            dbHandler.UpdateContainerStatus(each_container, "fanning", "false")
            time.sleep(10)
            dbHandler.UpdateContainerStatus(each_container, "misting", "true")
            time.sleep(30)       
            p = Process(target=startmisting, args=(each_container, avehumid, stop_humid, start_humid,mist_id, ))
            p.start()
            logging.info("Fanning System Has Been Deactivated Automatically AND Misting System Has Been Activated Automatically.")
        elif should_misting and auto_misting and not misting and not manual_start_misting and not manual_start_fanning:
            dbHandler.UpdateContainerStatus(each_container, "misting", "true")
            time.sleep(10)
            p = Process(target=startmisting, args=(each_container, avehumid, stop_humid, start_humid, mist_id, ))
            p.start()
            logging.info("Misting System Has Been Activated Automatically")
            
        elif should_fanning and auto_fanning and not fanning and not misting and not manual_start_misting and not manual_start_fanning:
            dbHandler.UpdateContainerStatus(each_container, "fanning", "true")
            time.sleep(10)
            p = Process(target=startfanning, args=(each_container, avetemp, stop_temp, start_temp, fan_id_list, ))
            p.start()
            logging.info("Fanning System Has Been Activated Automatically")
        else:
            print("No Action is required")
            
