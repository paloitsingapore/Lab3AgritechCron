from crate import client
import os
import time
connection = client.connect("http://localhost:4200", username="crate")
cursor = connection.cursor()

for file in os.listdir('/home/pi/crate-4.0.6/data/'): 
    if 'json' in file: 
        file_len = (len(file))
        tab = file[0:file_len-8]
        alt_q = 'alter table ' + tab + ' set ' + '("blocks.read_only_allow_delete" = false)' + ';'
        print(alt_q)
        cursor.execute(alt_q)
