from crate import client
import os
import time
connection = client.connect("http://localhost:4200", username="crate")
cursor = connection.cursor()

for file in os.listdir('/home/pi/crate-4.0.6/data/irr/'): 
    if 'irr_set_hist' in file: 
        print("Dropee")
        file_len = (len(file))
        tab = file[0:file_len-7]
        alt_q = 'alter table ' + tab + ' set ' + '("blocks.read_only_allow_delete" = false)' + ';'
        print(alt_q)
        cursor.execute(alt_q)
        time.sleep(1)
        ins_q =  'DROP TABLE ' + tab + ';'
        
        print(ins_q)
        cursor.execute(ins_q)