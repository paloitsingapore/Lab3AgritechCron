import os
import json

from azure.cosmosdb.table.tableservice import TableService
table_service = TableService(account_name='irrigation6862843155', account_key='ANCWDTPTsnseCsZGyibl53f5IwMl6UJOzFqVkBzxsZjhjxgw+wfV1P+m+ndJQ73lD2MdM8wE/d9M7gNJQNkORA==')

table_name = 'SoilData'

#import pandas as pd
#pd.to_datetime(sd['time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Phnom_Penh')

#table_service.delete_table(table_name)

table_service.create_table(table_name)
"""
print('Delete the entity')
table_service.delete_entity(table_name, 'PK')
print('Successfully deleted the entity')"""


                
               
"""
customer = { "temperature":27.8,"humidity":22.1,"time":1594746552382,"mac_add":"17200005",'PartitionKey': 'PK', 'RowKey': 1594746552382}

try:
    entities = table_service.query_entities(table_name, filter="PartitionKey eq 'SoilData'", select='RowKey')
    for entity in entities:
       print(entity['RowKey'])
    #table_service.delete_table(table_name)
except Exception as err:
    print('Error creating table, ' + table_name + 'check if it already exists')

#ntity = table_service.get_entity(table_name, 'PK', '2')
#print(entity)
#table_service.insert_entity(table_name, customer)


"""