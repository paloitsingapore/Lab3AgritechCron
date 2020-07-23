import os
import json
from datetime import datetime
from azure.cosmosdb.table.tableservice import TableService
import access
import logging
import sys
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("azure_ml_soil_data")

account_name= access.get_name('1')
account_key = access.get_key('1')
table_service = TableService(account_name, account_key)
table_name = 'SoilData'

def run():
  for file in os.listdir("/home/pi/crate-4.0.6/data/az"):
    if file.startswith("soil"):
         filename = os.path.join("/home/pi/crate-4.0.6/data/az", file)
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
                     logging.info("Error while query the entries " +  str(err))
               if exist_flag == 0:
                  try:
                     table_service.insert_entity(table_name, sd)
                     logging.info("New Soil data inserted - RowKey: " + sd['RowKey'])
                  except Exception as err:
                     logging.info("Error while insert the entries " +  str(err))

if __name__ == '__main__':
   try:
      run()
   except Exception as err:
      logging.info("Error while extracting soil Data " +  str(err))
