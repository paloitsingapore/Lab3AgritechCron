import os
import json
from datetime import datetime
from azure.cosmosdb.table.tableservice import TableService
import access
account_name= 'irrigation6862843155'
account_key = access.get_key(account_name)
table_service = TableService(account_name, account_key)
table_name = 'SoilData'

def run():
  for file in os.listdir("/home/pi/data/azdata"):
    if file.startswith("soil"):
         filename = os.path.join("/home/pi/data/azdata", file)
         with open(filename, 'r') as f:
            for line in f:
               sd = json.loads(line)
               exist_flag = 0
               sd['PartitionKey'] = table_name
               sd['RowKey'] = sd["mac_add"] + str(sd["time"]) 
               sd['time']   = datetime.fromtimestamp(sd["time"]// 1000) 
               try:
                     entities = table_service.query_entities(table_name, filter="PartitionKey eq 'SoilData'", select='RowKey')
                     for entity in entities:
                           if entity['RowKey'] == sd['RowKey']:
                              exist_flag = 1
                              exit 
               except Exception as err:
                     print("Error while query the entries " +  str(err))
               if exist_flag == 0:
                  try:
                     table_service.insert_entity(table_name, sd)
                     print("New Soil data inserted - RowKey: " + sd['RowKey'])
                  except Exception as err:
                     print("Error while insert the entries " +  str(err))

if __name__ == '__main__':
   try:
      run()
   except Exception as err:
      print("Error while extracting soil Data " +  str(err))
