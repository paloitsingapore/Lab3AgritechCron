import logging.handlers
import sys
import time
import logging
import os
import json
import subprocess
import time
from pathlib import Path
import atexit
import boto3
import requests
import datetime
import requests


handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE",
                   "/home/pi/logs/wechat" + datetime.datetime.today().strftime('%Y-%m-%d') + ".log"))
formatter = logging.Formatter('{asctime} {name} {levelname:8s} {message}', style='{')
handler.setFormatter(formatter)
root = logging.getLogger()
 
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)


ngrokDir="/home/pi" 
port='8090'

url = "http://54.255.187.114"

localhost_url = "http://localhost:4040/api/tunnels" 

def updateDB(ngrok_address):
    ngrok_address = ngrok_address.strip('https://')
    string_url = "{}/IP/{}/{}".format(url, ngrok_address, str(datetime.datetime.now()))
    logging.info(string_url)
    response = requests.get(string_url)

def is_running():
    try:
        ngrok_req = requests.get(localhost_url).text
        logging.info(ngrok_req)
        ngrok_address = get_ngrok_url(ngrok_req)
        logging.info("ngrok is already running {ngrok_address}".format(ngrok_address=ngrok_address))
        r=requests.get(ngrok_address)
        if r.status_code == 402:
            return _run_ngrok()
        return ngrok_address
    except Exception as e: 
        logging.info("exception",e)
        return _run_ngrok()

def get_ngrok_url(ngrok_req):
    j = json.loads(ngrok_req)
    tunnel_url = j['tunnels'][len(j['tunnels'])-1]['public_url']  
    return tunnel_url


def _run_ngrok():
    global ngrokDir
    command = "ngrok"
    executable = str(Path(ngrokDir, command))
    ngrok = subprocess.Popen([executable, 'http', '-inspect=false', port])
    atexit.register(ngrok.terminate)
    time.sleep(3)
    tunnel_url = requests.get(localhost_url).text 
    ngrok_address =get_ngrok_url(tunnel_url)
    logging.info("ngrok created  {ngrok_address}".format(ngrok_address=ngrok_address))
    updateDB(ngrok_address)
    time.sleep(3540) 
    return ngrok_address



is_running()
