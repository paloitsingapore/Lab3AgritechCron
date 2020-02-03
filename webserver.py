from flask import Flask, request
from flask_restful import Resource, Api

import switch_on
import switch_off

import logging
import logging.handlers
import os
import datetime
import subprocess
import time
from myip import GetIP

handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "/home/pi/logs/WEB_ERROR__" + datetime.datetime.today().strftime('%Y-%m-%d') + "_error.log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}',style='{')
#formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

app = Flask(__name__)
api = Api(app)

Rstatus='None'

class Switch(Resource):
    def get(self, status, SID):
        if status == 'ON':
            try:
                switch_on.Switch_On_Device(SID)
                Rstatus='success'
            except:
                Rstatus = 'fail'
                return{'STATUS':Rstatus}
        elif status == 'OFF':
            try:
                switch_off.Switch_Off_Device(SID)
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
        print (result.returncode)
        if result.returncode == 0:
            Rstatus = 'success'
        else:
            Rstatus = "fail"
        return{'STATUS': Rstatus}

try:
    api.add_resource(Switch, '/switch/<status>/<SID>')
    api.add_resource(Update, '/update')
except Exception as e:
    logging.error("Not able to handle the API: " + str(e))


if __name__ == '__main__':
     app.run(host=GetIP(), port=8090)
