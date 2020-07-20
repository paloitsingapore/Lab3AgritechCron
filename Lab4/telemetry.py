import azure
from azure.eventhub import EventHubClient, Sender, EventData, Receiver, Offset
import json
import time
import os
import datetime
from tzlocal import get_localzone
import teleconfig
from random import random

ts = datetime.datetime.now().isoformat()
print(ts)


filename = 'teleTemp.json'

with open(filename, 'r') as f:
   json_dict = json.load(f)
   json_dict['timestamp'] = ts # <--- add `id` value.
   json_dict['sensors'][0]['sensordata'][0]['timestamp'] = ts
   if filename == 'teleTemp.json':
     json_dict['sensors'][0]['sensordata'][0]['temp'] = 36 + random()
   else:   
     json_dict['sensors'][0]['sensordata'][0]['humid'] = ts
#   json_dict['sensors'][1]['sensordata'][0]['timestamp'] = ts
os.remove(filename)
with open(filename, 'w') as f:
    json.dump(json_dict, f, indent=4)

with open(filename, 'r') as f:
    json_dict = json.load(f)      
jsondata = json.dumps(json_dict)


write_client = EventHubClient.from_connection_string(teleconfig.EVENTHUBCONNECTIONSTRING, eventhub=teleconfig.EVENTHUBNAME, debug=False)
sender = write_client.add_sender(partition="0")
write_client.run()
for i in range(5):
    telemetry = str(jsondata)
    print("Sending telemetry: " + telemetry)
    sender.send(EventData(telemetry))
    #time.sleep(20)
write_client.stop() 
