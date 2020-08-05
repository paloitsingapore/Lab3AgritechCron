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
import logHandler 
import switchSensors
logHandler.run("brain")

switch_server1_ip = "192.168.1.103"
switch_server2_ip = "192.168.1.104"
wechat_url = "54.255.187.114"
user_id = ["ok99-wWEUEanEXFDBjxsd1vH7Rvo","ok99-wev6t-aZRaAHffRZS1tAP0g"]

def sendhttp_request(sensor_id,status,system):
    try:
        switchSensors.action(system,"2",status)
        time.sleep(10)
        switchSensors.action(system,"2",status)
        logging.info("{} system has been switched {}".format(system, status))
    except Exception as e:
        logging.error("Switch is not Working. ERROR: " + str(e))  
 
      
def sendhttp_request2(sensor_id,status, system):
    request_str_1 = ''
    request_str_2 = ''
    if status == "ON":
        request_str_1 = "http://{}:8090/switch/ON/{}".format(switch_server1_ip, sensor_id)
        request_str_2 = "http://{}:8090/switch/ON/{}".format(switch_server2_ip, sensor_id)
    elif status == "OFF":
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
            avetemp, avehumid, ts = dbHandler.GetAveTempHumid(container_id)
            endtime = str(datetime.datetime.now())
            sendhttp_request(sensor_id, "OFF", systemtype)
            dbHandler.UpdateActivity(activity_id, sensor_id, endtime, avetemp, avehumid)
            logging.info("TC: not currentmisting " + str(currentmisting) + " endtime " + str(endtime) + " avetemp "+ str(avetemp) + " avehumid " + str(avehumid) + " ts: "+ str(ts))
            try:
                for each_user in user_id:
                    url = "http://{}/alert/{}/{} is STOPPED MANUALLY. Current temp is {} and humidity is {}".format(wechat_url, each_user, typing, round(avetemp, 1), round(avehumid, 1))
                    requests.get(url, timeout=2)
            except:
                logging.info("error with wechat sending")
            time.sleep(30)
            break
     
        if current_time > target_time:
            dbHandler.UpdateUserActions('2', systemtype, 'true', container_id, '1')
            avetemp, avehumid, ts = dbHandler.GetAveTempHumid(container_id)
            endtime = str(datetime.datetime.now())
            sendhttp_request(sensor_id,"OFF", systemtype) 
            dbHandler.UpdateContainerStatus(container_id, typing, "false")
            dbHandler.UpdateActivity(activity_id, sensor_id, endtime, avetemp, avehumid)
            logging.info("TC: current_time > target_time " + " endtime " + str(endtime) + " avetemp "+ str(avetemp) + " avehumid " + str(avehumid) + " ts: "+ str(ts))
            try:
                for each_user in user_id:
                    url = "http://{}/alert/{}/{} is STOPPED due to time up. Current temp is {} and humidity is {}".format(wechat_url, each_user, typing, round(avetemp, 1), round(avehumid, 1))
                    requests.get(url, timeout=2)
            except:
                logging.info("error with wechat sending")
            time.sleep(30)            
            break
        time.sleep(30)

def startmisting(container_id, before_avehumid, upper_target_humid, lower_target_humid, sensor_id, manual=False, time_duration=0):
    index = 0
    indexofstart = True
    dbHandler.UpdateContainerStatus(container_id, "misting", "true")
    time.sleep(2)
    start_time = str(datetime.datetime.now())
    activity_id = int('{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now()))
    logging.info("5. Start misting ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    logging.info( "indexofstart: " + str(indexofstart) + " before_avehumid: " + str(before_avehumid) +" lower_target_humid: " + str(lower_target_humid) +" upper_target_humid: " + str(upper_target_humid))        
    if manual:
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/Misting is STARTED MANUALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(before_avehumid, 1))
                requests.get(url, timeout=2)
        except:
            logging.info("error with wechat sending")
    else:
        sendhttp_request(sensor_id,"ON", "MIST")
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/Misting is STARTED AUTOMATICALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(before_avehumid, 1))
                requests.get(url, timeout=2)
        except:
            logging.info("error with wechat sending")
    
    while True:
        avetemp, avehumid, ts = dbHandler.GetAveTempHumid(container_id)
        upper_target_humid, lower_target_humid = dbHandler.GetContainerHumidInfo(container_id)
        currentmisting = dbHandler.GetContainerStatus(container_id, "misting")
        auto_misting = dbHandler.GetContainerStatus(container_id, "auto_misting")
        index = index + 1
        logging.info("6."+ str(index) + ".SM Inside While loop ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logging.info("currentmisting: " + str(currentmisting)+ " indexofstart: " + str(indexofstart) +" avehumid: " + str(avehumid)  +" ts: "+ str(ts) + " before_avehumid: " + str(before_avehumid)
                  +" lower_target_humid: " + str(lower_target_humid) +" upper_target_humid: " + str(upper_target_humid) +" auto_misting: " + str(auto_misting))     
        if indexofstart:
            dbHandler.InsertActivity(activity_id, sensor_id, start_time, "MIST", avetemp, avehumid)
            indexofstart = False
            logging.info("6."+ str(index) + ".SM: indexofstart")   
        if(not currentmisting) or (not auto_misting and not manual):
            endtime = str(datetime.datetime.now())
            sendhttp_request(sensor_id, "OFF", "MIST")
            dbHandler.UpdateContainerStatus(container_id, "misting", "false")
            dbHandler.UpdateActivity(activity_id, sensor_id, endtime, avetemp, avehumid)
            try:
                for each_user in user_id:
                    url = "http://{}/alert/{}/Misting is STOPPED MANUALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(avehumid, 1))
                    requests.get(url, timeout=2)
            except:
                logging.info("error with wechat sending")        
            time.sleep(60)
            break

        if manual:
            sendhttp_request(sensor_id,"ON", "MIST")
            p = Process(target=Timechecking, args=(time_duration, container_id, sensor_id, start_time, "misting", "MIST"))
            p.start()
            break
            
        else:
            if(avehumid < lower_target_humid):
	        #startmisting-switch keep on starting              
                time.sleep(10)
                logging.info("6."+ str(index) + ".SM: avehumid < lower_target_humid") 
            elif(avehumid > lower_target_humid and avehumid < upper_target_humid):
                time.sleep(10)
                logging.info("6."+ str(index) + ".SM: avehumid > lower_target_humid and avehumid < upper_target_humid")  
            elif(avehumid > upper_target_humid):
                endtime = str(datetime.datetime.now())
                sendhttp_request(sensor_id, "OFF", "MIST") 
                #update database 
                dbHandler.UpdateContainerStatus(container_id, "misting", "false")
                dbHandler.UpdateActivity(activity_id, sensor_id, endtime, avetemp, avehumid)
                logging.info("6."+ str(index) + ".SM: avehumid > upper_target_humid .. Success: Humidity has reached Upper Target limit") 
                try:
                    for each_user in user_id:
                        url = "http://{}/alert/{}/Misting is STOPPED AUTOMATICALLY. Current humidity at farm is {}".format(wechat_url, each_user, round(avehumid, 1))
                        requests.get(url, timeout=2)
                except:
                    logging.info("error with wechat sending")
                time.sleep(10)            
                break
            else:
                logging.info("6."+ str(index) + ".SM: finally else")       
            

        if avehumid > before_avehumid:
            logging.info("6."+ str(index) + ".SM: avehumid > before_avehumid.. this is good. humidity is increasing")
        elif avehumid < before_avehumid:
            logging.info("6."+ str(index) + ".SM: avehumid < before_avehumid .. this is NOT good. humidity is decreasing")
    
        time.sleep(20)
        
            
def startfanning(container_id, before_avetemp, upper_target_temp, lower_target_temp, sensor_id, manual=False, time_duration=0):
    index = 0
    indexofstart = True
    start_time = str(datetime.datetime.now())
    activity_id = int('{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now()))
    dbHandler.UpdateContainerStatus(container_id, "fanning", "true")
    time.sleep(2)
    if manual:
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/FANNING is STARTED MANUALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(before_avetemp, 1))
                requests.get(url, timeout=2)
        except:
            logging.info("error with wechat sending")        
    else:
        for each in sensor_id:
            sendhttp_request(each, "ON", "FAN")            
            time.sleep(30)
        logging.info("5. Start Fanning ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logging.info( "indexofstart: " + str(indexofstart) 
                  + " before_avetemp: " + str(before_avetemp)
                  +" lower_target_temp: " + str(lower_target_temp) 
                  +" upper_target_temp: " + str(upper_target_temp) )     
        try:
            for each_user in user_id:
                url = "http://{}/alert/{}/FANNING is STARTED AUTOMATICALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(before_avetemp, 1))
                requests.get(url, timeout=2)
        except:
            logging.info("error with wechat sending")
    while True:
        avetemp, avehumid, ts = dbHandler.GetAveTempHumid(container_id)
        upper_target_temp, lower_target_temp = dbHandler.GetContainerTempInfo(container_id)
        currentfanning = dbHandler.GetContainerStatus(container_id, "fanning")
        auto_fanning = dbHandler.GetContainerStatus(container_id, "auto_fanning")
        index = index + 1
        logging.info("6."+ str(index) + ".SF Inside While loop ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logging.info("currentfanning: " + str(currentfanning) + " indexofstart: " + str(indexofstart) + " avetemp: " + str(avetemp) + " ts: "+ str(ts) + " before_avetemp: " + str(before_avetemp) 
                                        + " lower_target_temp: " + str(lower_target_temp) + " upper_target_temp: " + str(upper_target_temp)  + " auto_fanning: " + str(auto_fanning))   
        if indexofstart:
            for each in sensor_id:
                dbHandler.InsertActivity(str(activity_id) + str(each), each, start_time, "FAN", avetemp, avehumid)
            indexofstart = False
            logging.info("6."+ str(index) + ".SF: indexofstart")  

        if(not currentfanning) or (not auto_fanning and not manual):
            endtime = str(datetime.datetime.now())
            for each in sensor_id:
                dbHandler.UpdateActivity(str(activity_id) + str(each), each, endtime, avetemp, avehumid)
                dbHandler.UpdateContainerStatus(container_id, "fanning", "false")
                sendhttp_request(each, "OFF", "FAN")            
                time.sleep(30)
                
            try:    
                for each_user in user_id:    
                    url = "http://{}/alert/{}/FANNING is STOPPED MANUALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(avetemp, 1))
                    requests.get(url, timeout=2)
            except:
                logging.info("error with wechat sending")
            time.sleep(60)
            break
        
        if manual:
            for each in sensor_id:
                sendhttp_request(each, "ON", "FAN")
                p = Process(target=Timechecking, args=(time_duration, container_id, each, str(activity_id) + str(each), "fanning", "FAN", ))
                p.start()
                time.sleep(30)
            break
        
        else:                 
            if(avetemp > upper_target_temp):
	            #startmisting-switch keep on starting                
                time.sleep(10)
                logging.info("6."+ str(index) + ".SF: avetemp > upper_target_temp")    
            elif(avetemp < upper_target_temp  and avetemp > lower_target_temp):
                time.sleep(10)
                logging.info("6."+ str(index) + ".SF: avetemp < upper_target_temp  and avetemp > lower_target_temp")  
            elif(avetemp < lower_target_temp):
                time.sleep(10)
                endtime = str(datetime.datetime.now())
                for each in sensor_id:
                    sendhttp_request(each, "OFF", "FAN") 
                    time.sleep(30)
                    #update database 
                    dbHandler.UpdateActivity(str(activity_id) + str(each), each, endtime,avetemp, avehumid)
                dbHandler.UpdateContainerStatus(container_id, "fanning", "false")
                logging.info("6."+ str(index) + ".SF: avetemp < lower_target_temp .. Success: Temperature has reached Lower Target limit") 
                try:
                    for each_user in user_id:
                        url = "http://{}/alert/{}/FANNING is STOPPED AUTOMATICALLY. Current temperature at farm is {}".format(wechat_url, each_user, round(avetemp, 1))
                        requests.get(url, timeout=2)
                except:
                    logging.info("error with wechat sending")        
                time.sleep(10)            
                break
            else:
                logging.info("6."+ str(index) + ".SF: finally else")        
            
        if avetemp < before_avetemp:
            logging.info("6."+ str(index) + ".SF: avetemp < before_avetemp.. this is good. Temperature is decreasing")
        elif avetemp > before_avetemp:
            logging.info("6."+ str(index) + ".SF: avetemp > before_avetemp.. this is NOT good. Temperature is increasing")
            
        time.sleep(20)

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
        logging.info("1.Containers info   +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logging.info("start_humid:" + str(start_humid) + " stop_humid: " + str(stop_humid) + " start_temp: " + str(start_temp) + " stop_temp: "  + str(stop_temp) + " fan_id: "     + str(fan_id) 
                  + " mist_id: "    + str(mist_id) + " fanning: "+ str(fanning) + " auto_fanning: "+ str(auto_fanning) + " misting: "+ str(misting) + " auto_misting: "+ str(auto_misting))
        logging.info("2. Average Temperature  +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")          
        avetemp, avehumid, ts = dbHandler.GetAveTempHumid(each_container)
        logging.info("avetemp: "+ str(avetemp)
                  + " avehumid: "     + str(avehumid)
                  + " ts: "+ str(ts))
        logging.info("3. Fan Mist +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #   should_fanning - Make decision based on the Temp inside the GreenHouse
        #   should_misting - Make decision based on the Humidity inside the GreenHouse
        should_misting, should_fanning = ShoudStartFanMist(start_humid, start_temp, avetemp, avehumid)
        logging.info("should_misting:" + str(should_misting) 
                  + " should_fanning: " + str(should_fanning)) 
        fan_id_list = fan_id.split(',')
  

        manual_start_misting = dbHandler.GetSystemStatus('MIST', each_container, '(0,1)','true')
        manual_start_fanning = dbHandler.GetSystemStatus('FAN', each_container, '(0,1)', 'true')
        
        manual_stop_misting = dbHandler.GetSystemStatus('MIST', each_container, '(0)', 'false')
        manual_stop_fanning = dbHandler.GetSystemStatus('FAN', each_container, '(0)', 'false')
        
        manual_starting_misting = dbHandler.GetSystemStatus('MIST', each_container, '(0)','true')
        manual_starting_fanning = dbHandler.GetSystemStatus('FAN', each_container, '(0)', 'true')
        

        running_misting = dbHandler.GetRunningData('1','MIST', each_container)
        running_fanning = dbHandler.GetRunningData('1','FAN', each_container)
        logging.info("4. Running Status FAN vs MIST ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        logging.info("running_misting:" + str(running_misting) 
                  + " running_fanning: " + str(running_fanning)) 

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
                       
        #   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #   For Example: 14.1 - 19.1  - 24.1
        #   LT - OT - HT
        #   If Temp above [HT], activate the FAN
        #   Fan attempt to reach the optimum temp [OT]  -- (fanning)
        #   Stop the FAN if [OT] is reached 

        #   For Example: 63.6 - 66.1  - 68.6
        #   LH - OH - HH
        #   If Humidity below [LH], activate the SPRINKLER 
        #   Sprinkler attempt to reach the optimum humidity [OH] -- (misting)
        #   Stop the MIST if [OH] is reached 
        #   ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        #   Manual override has Very High preference over Automation
        #   Misting has High preference over Fanning 
        #   Turn off the Fan and Turn on the Sprinkler

        if should_misting and auto_misting and not misting and fanning and not manual_start_misting and not manual_start_fanning:
            dbHandler.UpdateContainerStatus(each_container, "fanning", "false")
            time.sleep(10)
            dbHandler.UpdateContainerStatus(each_container, "misting", "true")
            time.sleep(30)       
            p = Process(target=startmisting, args=(each_container, avehumid, stop_humid, start_humid,mist_id))
            p.start()
            logging.info("MAIN: De-activate Fans request has been submitted" + " & "
                              " Activate Sprinkler request has been submitted")

        #   Turn on the Sprinkler if not Misting
        elif should_misting and auto_misting and not misting and not manual_start_misting and not manual_start_fanning:
            dbHandler.UpdateContainerStatus(each_container, "misting", "true")
            time.sleep(10)
            p = Process(target=startmisting, args=(each_container, avehumid, stop_humid, start_humid, mist_id))
            p.start()
            logging.info("MAIN: Activate Sprinkler request has been submitted")

        #   Fanning has least preference over Misting 
        #   Turn off the sprinkler and Turn on the Fan           
        elif should_fanning and auto_fanning and not fanning and not misting and not manual_start_misting and not manual_start_fanning:
            dbHandler.UpdateContainerStatus(each_container, "fanning", "true")
            time.sleep(10)
            p = Process(target=startfanning, args=(each_container, avetemp, stop_temp, start_temp, fan_id_list, ))
            p.start()
            logging.info("MAIN: Activate Fans request has been submitted")
            
        else:
            logging.info("MAIN: No Action is required")