import boto3
import os
from zipfile import ZipFile
from datetime import datetime

# Create an S3 client
S3 = boto3.client('s3')
BUCKET_NAME = 'lab3agritechpaloit'
log_directory = '/home/pi/logs'
data_directory ='/home/pi/data'
zip_log = (datetime.now()+'-'+'logs.zip','w')
zip_data =(datetime.now()+'-'+'data.zip','w')

for file in os.listdir(log_directory):
    print('in dir',directory)
    filename = directory + '/' + file
    print("new filename:\t",filename)
    if filename.endswith(".log"):
        DEST='logs/'+file
        print("destination",DEST)
        s3.upload_file(filename, BUCKET_NAME, DEST)
for file in os.listdir(data_directory):
    print('in dir',directory)
    filename = directory + '/' + file
    print("new filename:\t",filename)
    if filename.endswith(".tar.gz"):
        DEST='data/'+file
        print("destination",DEST)
        s3.upload_file(filename, BUCKET_NAME, DEST)

