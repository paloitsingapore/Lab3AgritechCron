import os
import json
from datetime import datetime
from azure.cosmosdb.table.tableservice import TableService
import access
import logging
import sys
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("azure_ml_faucets")

account_name= access.get_name('1')
account_key = access.get_key('1')
table_service = TableService(account_name, account_key)
table_name = 'Faucets'

def run():
  for file in os.listdir("/home/pi/crate-4.0.6/data/az"):
    if file.startswith("faucets"):
         filename = os.path.join("/home/pi/crate-4.0.6/data/az", file)
         with open(filename, 'r') as f:
            for line in f:
               fc = json.loads(line)
               exist_flag = 0
               fc['PartitionKey'] = table_name
               fc['RowKey'] = str(fc["mac_id"]) 
               fc['time']   = datetime.fromtimestamp(fc["time"]// 1000) 
               try:
                     entities = table_service.query_entities(table_name, filter="PartitionKey eq 'Faucets'", select='mac_id')
                     for entity in entities:
                           if entity['mac_id'] == fc['mac_id']:
                              exist_flag = 1
                              exit                  
               except Exception as err:
                     logging.info("Error while query the entries " +  str(err))
               if exist_flag == 0:
                  try:
                     table_service.insert_entity(table_name, fc)
                     logging.info("New faucet is inserted - RowKey: " + fc['RowKey'])
                  except Exception as err:
                     logging.info("Error while insert the entries " +  str(err))
               elif exist_flag == 1:
                    table_service.update_entity(table_name, fc)
 
if __name__ == '__main__':
   try:
      run()
   except Exception as err:
      logging.info("Error while extracting Faucet " +  str(err))
