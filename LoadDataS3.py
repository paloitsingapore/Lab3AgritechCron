import boto3
import os
from zipfile import ZipFile
from datetime import datetime



# Create an S3 client
S3 = boto3.client('s3')
BUCKET_NAME = 'lab3agritechpaloit'
directory = '/home/pi/logs'
zip_log = (datetime.now()+'-'+'logs.zip','w')
zip_data =(datetime.now()+'-'+'data.zip','w')

for file in os.listdir(directory):
    print('in dir',directory)
    filename = directory + '/' + file
    print("new filename:\t",filename)
    if filename.endswith(".log"):
          #print('file',directory+'/'+filename)
        DEST='logs/'+file
        print("destination",DEST)
        s3.upload_file(filename, BUCKET_NAME, DEST)
    elif ".gz" in filename:
        DEST='data/'+file
        print("elif:\t",DEST)
        s3.upload_file(filename, BUCKET_NAME,DEST)

