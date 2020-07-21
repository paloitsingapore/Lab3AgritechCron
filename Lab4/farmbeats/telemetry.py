import azure
from azure.eventhub import EventHubClient, Sender, EventData, Receiver, Offset
import json
import os
from datetime import datetime
import teleconfig

def fpath(input):
  if input == "humid":
    filename = 'teleHumid.json'
  elif input == "temp":
    filename = 'teleTemp.json'
  filepath = '/home/pi/Lab3AgritechCron/Lab4/farmbeats/json/'
  dest = os.path.join(str(filepath) + str(filename))
  return dest
 
def conv(ts):
    date_time = datetime.fromtimestamp(ts // 1000)
    return date_time.strftime("%Y-%m-%dT%H:%M:%S")

def loadHistorical(input):
  for file in os.listdir("/home/pi/data/azdata"):
    if file.startswith("soil"):
         filename = os.path.join("/home/pi/data/azdata", file)
         with open(filename, 'r') as f:
            for line in f:
               sd = json.loads(line)
               print(sd)
               exist_flag = 0
               #logic to handle duplicates to be added here
               with open(fpath(input), 'r') as f:
                  json_dict = json.load(f)
                  json_dict['timestamp'] = conv(sd["time"])
                  json_dict['sensors'][0]['sensordata'][0]['timestamp'] = conv(sd["time"])
                  if input == "humid":
                    json_dict['sensors'][0]['sensordata'][0]['humid'] = sd["humidity"]
                  elif input == "temp":
                    json_dict['sensors'][0]['sensordata'][0]['temp'] = sd["temperature"]
 
               with open(fpath(input), 'w') as f:
                  json.dump(json_dict, f, indent=4)

               with open(fpath(input), 'r') as f:
                  json_dict = json.load(f)      
                  jsondata = json.dumps(json_dict)

               if exist_flag == 0:
                  try:
                      write_client = EventHubClient.from_connection_string(teleconfig.EVENTHUBCONNECTIONSTRING, eventhub=teleconfig.EVENTHUBNAME, debug=False)
                      sender = write_client.add_sender(partition="0")
                      write_client.run()
                      telemetry = str(jsondata)
                      print("Sending telemetry: " + telemetry)
                      sender.send(EventData(telemetry))
                      write_client.stop() 
                      print("New Soil data inserted" )
                  except Exception as err:
                     print("Error while insert the entries " +  str(err))


if __name__ == '__main__':
   try:
      loadHistorical("humid") 
      loadHistorical("temp")
   except Exception as err:
      print("Error while extracting soil Data " +  str(err))

