import os
import json
from datetime import datetime
from azure.cosmosdb.table.tableservice import TableService
import access
import logging
import sys
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("azure_ml_sensors")

account_name= access.get_name('1')
account_key = access.get_key('1')
table_service = TableService(account_name, account_key)
table_name = 'Sensors'

def run():
  for file in os.listdir("/home/pi/crate-4.0.6/data/az"):
    if file.startswith("sensors"):
         filename = os.path.join("/home/pi/crate-4.0.6/data/az", file)
         with open(filename, 'r') as f:
            for line in f:
               se = json.loads(line)
               exist_flag = 0
               se['PartitionKey'] = table_name
               se['RowKey'] = str(se["macadd"]) 
               try:
                     entities = table_service.query_entities(table_name, filter="PartitionKey eq 'Sensors'", select='macadd')
                     for entity in entities:
                           if entity['macadd'] == se['macadd']:
                              exist_flag = 1
                              exit                  
               except Exception as err:
                     logging.info("Error while query the entries " +  str(err))
               if exist_flag == 0:
                  try:
                     table_service.insert_entity(table_name, se)
                     logging.info("New sensor is inserted - RowKey: " + se['RowKey'])
                  except Exception as err:
                     logging.info("Error while insert the entries " +  str(err))
               elif exist_flag == 1:
                    table_service.update_entity(table_name, se)
 
if __name__ == '__main__':
   try:
      run()
   except Exception as err:
      logging.info("Error while extracting sensor " +  str(err))
