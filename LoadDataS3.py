#To Upload Data to S3
#!/usr/bin/python3
import boto3
import os
import zipfile
from datetime import datetime
import time
import subprocess 
from myip import GetIP 
from datetime import datetime, timedelta

# Create an S3 client

print("uploading to cloud on ")
print (GetIP())
S3 = boto3.client('s3')
BUCKET_NAME = 'lab3agritechpaloit'
log_directory = '/home/pi/logs/'
data_directory ='/home/pi/data/'
zip_log = (str(datetime.now())+'-'+'logs.zip')
zip_data =(str(datetime.now())+'-'+'data.zip')
zip_log =  zip_log.replace(" ", "_")
zip_data = zip_data.replace(" ","_")
t_date =  (datetime.now()).strftime('%Y-%m-%d')

print(t_date)

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
        if  filename.endswith(".txt"):
            print("zipping file "+filename)
            zf.write(filename)

print("data file zipped in "+zip_data)

exit_code_log = 1
exit_code_data = 1
print("uploading files to s3....")
for x in range(2):
    print (x)
    if exit_code_log !=0:
        try:
            S3.upload_file(log_directory+zip_log, BUCKET_NAME, 'logs/'+str(GetIP())+zip_log)
            exit_code_log = 0
            
            current_path = "/home/pi/logs/" ## source path
            new_path = "/home/pi/backup/logs/" ## destination path
            for files in os.listdir(current_path):
                if files.endswith(".log") and t_date not in files:
                    subprocess.call("mv %s%s %s" % (current_path,files, new_path), shell=True)
                   
        except Exception as e:
            print("Error... "+str(e))
            exit_code_log = 1
            print("logs S3 Upload Failed Retrying in 10 min...")
    if exit_code_data != 0:
        try:          
            S3.upload_file(data_directory+zip_data, BUCKET_NAME, 'data/'+str(GetIP())+zip_data)
            exit_code_data = 0
            current_path = "/home/pi/data/" ## source path
            new_path = "/home/pi/backup/data/" ## destination path
            for files in os.listdir(current_path):
                if files.endswith(".txt") and t_date not in files:
                    subprocess.call("mv %s%s %s" % (current_path,files, new_path), shell=True)
        except Exception as e:
            print("Error... "+str(e))
            exit_code_data = 1
            print("data S3 Upload Failed Retrying in 10 min...")
    if exit_code_data == 0 and exit_code_log == 0:
        break
    else:
        time.sleep(60)


if exit_code_log ==1 or exit_code_data ==1:
    print("s3 upload failed")
else:
    print("s3 upload Finished Sucessfully")

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


