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
table_name = 'lws'

def run():
  for file in os.listdir("/home/pi/crate-4.0.6/data/az"):
    if file.startswith("lws"):
         filename = os.path.join("/home/pi/crate-4.0.6/data/az", file)
         with open(filename, 'r') as f:
            for line in f:
               ws = json.loads(line)
               exist_flag = 0
               ws['PartitionKey'] = table_name
               ws['RowKey'] = str(ws["id"]) 
               try:
                     entities = table_service.query_entities(table_name, filter="PartitionKey eq 'lws'", select='id')
                     for entity in entities:
                           if entity['id'] == ws['id']:
                              exist_flag = 1
                              exit                  
               except Exception as err:
                     logging.info("Error while query the entries " +  str(err))
               if exist_flag == 0:
                  try:
                     table_service.insert_entity(table_name, ws)
                     logging.info("New sensor is inserted - RowKey: " + ws['RowKey'])
                  except Exception as err:
                     logging.info("Error while insert the entries " +  str(err))
               elif exist_flag == 1:
                    table_service.update_entity(table_name, ws)
 
if __name__ == '__main__':
   try:
      run()
   except Exception as err:
      logging.info("Error while extracting sensor " +  str(err))
