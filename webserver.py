from flask import Flask, request
from flask_restful import Resource, Api

#import switch_on
#import switch_off

import logging
import logging.handlers
import os
import datetime
import subprocess
import time
from myip import GetIP
import dbHandler
import json
import boto3

handler = logging.handlers.WatchedFileHandler(os.environ.get("LOGFILE","/home/pi/logs/wechat" + datetime.datetime.today().strftime('%Y-%m-%d') + ".log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
#formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

graph_path = "/home/pi/graph"

S3 = boto3.client('s3')
BUCKET_NAME = 'lab3agritechpaloit'


app = Flask(__name__)
api = Api(app)

Rstatus='None'

class Switch(Resource):
    def get(self, status, SID):
        if status == 'ON':
            try:
                #switch_on.Switch_On_Device(SID)
                Rstatus='success'
            except:
                Rstatus = 'fail'
                return{'STATUS':Rstatus}
        elif status == 'OFF':
            try:
                #switch_off.Switch_Off_Device(SID)
                Rstatus='success'
            except:
                Rstatus = 'fail'
                return{'STATUS':Rstatus}
                
        else:
            Rstatus='fail'
        time.sleep(5)
        return{'STATUS':Rstatus}

class Update(Resource):
    def get(self):
        result = subprocess.run('./RunUpdate.sh')
        logging.info(result.returncode)
        if result.returncode == 0:
            Rstatus = 'success'
        else:
            Rstatus = "fail"
        return{'STATUS': Rstatus}
        
class Wechat(Resource):
    def get(self,action):
        if action == 'now':
            avetemp, avehumid = dbHandler.GetAveTempHumid('01579684047480')
            temp = round(avetemp, 1)
            humid = round(avehumid, 1)
            logging.info('fetch data from db')
            
            return {'temp': temp, 'humid':humid}

        if action == 'config':
            start_humid, stop_humid, start_temp, stop_temp, fan_id, mist_id, fanning, auto_fanning, misting, auto_misting = dbHandler.GetContainerInfo('01579684047480')
            return {'hightemp': round(start_temp,1), 'lowtemp':round(stop_temp,1), 'highhumid':round(stop_humid,1), 'lowhumid':round(start_humid,1)}

class Setting(Resource):
    def get(self, action, sign, value):
        if action == 'temp':
            logging.info(sign)
            logging.info(value)
            return {'status': 'success'}
        if action == 'humid':
            return {'status': 'success'}
            
class Graph(Resource):
    def get (self, date):
        time_value, tmp_value, hum_value = [], [], []
        for i in range(0, 24):
            flag = True
            current_time = str(i).zfill(2)
            time_value.append(current_time + ':00')
            logging.info(current_time)
            for each in result:
               current_date = datetime.fromtimestamp(int(each[0])/1000).strftime('%H')
               logging.info(current_date)
               if (str(current_time) == str(current_date)):
                    flag = False
                    tmp_value.append(int(each[1]))
                    hum_value.append(int(each[2]))
            if flag:
                tmp_value.append(None)
                hum_value.append(None)        
                    
            
        fig = plt.figure(dpi=128, figsize=(10, 6))
        plt.plot(time_value, tmp_value, c='red', alpha=0.5)
        plt.plot(time_value, hum_value, c='blue', alpha=0.5)
            
        plt.title("Temp And Humidity Graph for", fontsize=24)
        plt.xlabel('', fontsize=16)
        fig.autofmt_xdate()
        plt.ylabel("Temp(C) And Humidity(%)", fontsize=16)
        plt.tick_params(axis='both', which='major', labelsize=16)
        plt.savefig(graph_path + "/temperature.png", bbox_inches='tight')
        S3.upload_file(graph_path + "/temperature.png", BUCKET_NAME, 'graph/temperature.png')
        return {"url": url}
            

try:
    logging.info("Inside webpsever")
    api.add_resource(Switch, '/switch/<status>/<SID>')
    api.add_resource(Update, '/update')
    api.add_resource(Wechat, '/wechat/<action>')
    api.add_resource(Setting, '/setting/<action>/<sign>/<value>')
    api.add_resource(Graph, '/graph/<date>')
except Exception as e:
    logging.error("Not able to handle the API: " + str(e))


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=8090)
