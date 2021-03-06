import os
import json
from datetime import datetime
from azure.cosmosdb.table.tableservice import TableService
import access
import logging
import sys
sys.path.insert(1, '/home/pi/Lab3AgritechCron/')
import logHandler 
logHandler.run("azure_ml_settings")

account_name= access.get_name('1')
account_key = access.get_key('1')
table_service = TableService(account_name, account_key)
table_name = 'CurrentConstraints'

def run():
  for file in os.listdir("/home/pi/crate-4.0.6/data/az"):
    if file.startswith("irr_set_cust"):
         filename = os.path.join("/home/pi/crate-4.0.6/data/az", file)
         with open(filename, 'r') as f:
            for line in f:
               cc = json.loads(line)
               exist_flag = 0
               cc['PartitionKey'] = "CC"
               cc['RowKey'] = str(cc["field_id"]) 
               cc['last_updated']   = datetime.fromtimestamp(cc["last_updated"]// 1000) 
               try:
                     entities = table_service.query_entities(table_name, filter="PartitionKey eq 'CC'", select='field_id')
                     for entity in entities:
                           if entity['field_id'] == cc['field_id']:
                              exist_flag = 1
                              exit                  
               except Exception as err:
                     logging.info("Error while query the entries " +  str(err))
               if exist_flag == 0:
                  try:
                     table_service.insert_entity(table_name, cc)
                     logging.info("New field Setting inserted - RowKey: " + cc['RowKey'])
                  except Exception as err:
                     logging.info("Error while insert the entries " +  str(err))
               elif exist_flag == 1:
                    table_service.update_entity(table_name, cc)

if __name__ == '__main__':
   try:
      run()
   except Exception as err:
      logging.info("Error while extracting Irrigation custom settings " +  str(err))
