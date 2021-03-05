import logging

import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import json,csv

CONNECT_STR="DefaultEndpointsProtocol=https;AccountName=lab3agritechpaloit;AccountKey=7y9wfjL59CGOGJWgWVno8L2XTaDoHjT1ASgIJaEEJlASVAWcQMZxKj/RaB4h/Q/WnRNw3NNBVjHtVX29labzuA==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(CONNECT_STR)
# Create a unique name for the container
container_json = "lab3agritechpaloit/json"
container_csv  = "lab3agritechpaloit/csv"

def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size shobhit1: {myblob.length} bytes")
    file_name = myblob.name
    file_name = file_name.split("/")[-1].split(".")[0]
    logging.info(file_name)
    stream_data = myblob.read()
    logging.info(stream_data);
    with open("temp.json" , "wb") as my_blob:
        logging.info(stream_data)
        my_blob.write(stream_data)
        my_blob.close()
    logging.info("file saved")
    data = []
    logging.info("open new file")
    logging.info(file_name)
    f = open("temp.json", "r")
    logging.info("file opend")
    for line in f:
        try:
            logging.info(line)
            value = json.loads(json.loads(json.loads(json.dumps(line))))
            logging.info(value)
            data.append(value)
            logging.info(data)
        except Exception as e:
            logging.info("" +str(e))
            logging.info("Remove Unhealthy Data")
    
    file_json = str(file_name) + '.json'   
    file_csv =  str(file_name) + '.csv'
    logging.info(file_json)
    logging.info(file_csv)
    with open("temp.json",'w') as out:
       json.dump(data, out)
    logging.info("JSON Converted")   
    logging.info(data)    
    #Converting File to CSV
    inputFile = open("temp.json") #open json file
    outputFile = open("temp.csv", 'w') #load csv file
    data = json.load(inputFile) #load json content
    inputFile.close() #close the input file
    output = csv.writer(outputFile) #create a csv.write
    output.writerow(data[0].keys())  # header row
    for row in data:
        output.writerow(row.values())  # values row
    logging.info("csv_converted")
    logging.info("i am here ") 
    try:
        blob_client = blob_service_client.get_blob_client(container=container_json, blob=file_json)
        logging.info("hello")
        with open("temp.json", "rb") as data:
            blob_client.upload_blob(data)
    except Exception as e:
        logging.info(e)
    logging.info("json saved")
    try:
        blob_client = blob_service_client.get_blob_client(container=container_csv, blob=file_csv)
        with open("temp.csv", "rb") as data:
            blob_client.upload_blob(data)
    except Exception as e:
        print(e)
    logging.info("CSV Saved")

