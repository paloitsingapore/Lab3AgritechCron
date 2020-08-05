from crate import client
import os
import time
connection = client.connect("http://localhost:4200", username="crate")
cursor = connection.cursor()

for file in os.listdir('/home/pi/crate-ce-4.1/data/'): 
    if 'json' in file: 
        file_len = (len(file))
        tab = file[0:file_len-8]
        ins_q =  'DROP TABLE IF EXISTS ' + tab + ';'     
        print(ins_q)
        cursor.execute(ins_q)