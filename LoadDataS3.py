import boto3
import os
import zipfile
from datetime import datetime
import subprocess 
from myip import GetIP 
# Create an S3 client
print("uploading to cloud on ")
print (GetIP())
S3 = boto3.client('s3')
BUCKET_NAME = 'lab3agritechtest'
log_directory = '/home/pi/logs/'
data_directory ='/home/pi/data/'
zip_log = (str(datetime.now())+'-'+'logs.zip')
zip_data =(str(datetime.now())+'-'+'data.zip')
zip_log =  zip_log.replace(" ", "_")
zip_data = zip_data.replace(" ","_")

with zipfile.ZipFile(log_directory+zip_log, mode='w') as zf:
    for file in os.listdir(log_directory):
        filename = log_directory + '/' + file
        if filename.endswith(".log"):
            print('Zipping File' + filename)
            zf.write(filename)
print("Log Files zipped in "+zip_log)

with zipfile.ZipFile(data_directory+zip_data, mode='w') as zf:
    for file in os.listdir(data_directory):
        filename = data_directory + '/' + file
        if filename.endswith(".tar.gz"):
            print("zipping file "+filename)
            zf.write(filename)
print("data file zipped in "+zip_data)

print("uploading files to s3....")
S3.upload_file(log_directory+zip_log, BUCKET_NAME, 'logs/'+str(GetIP())+zip_log)
S3.upload_file(data_directory+zip_data, BUCKET_NAME, 'data/'+str(GetIP())+zip_data)
print("s3 upload finished")


print("Removing Zipped File .....")

log_file  = os.listdir(log_directory)
data_file = os.listdir(data_directory)

for item in log_file:
    if item.endswith(".zip"):
        os.remove( os.path.join( log_directory, item ) )

for item in data_file:
    if item.endswith(".zip"):
        os.remove( os.path.join( data_directory, item ) )

print("Zip files removed")

subprocess.call('mv  /home/pi/logs/* /home/pi/backup/logs',shell=True)

subprocess.call('mv /home/pi/data/* /home/pi/backup/data',shell=True)

