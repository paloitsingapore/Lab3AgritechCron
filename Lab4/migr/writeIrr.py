from crate import client
import time
import os
f = open("/home/pi/crate-4.0.6/data/irr/irr_set.sql", "r")
tab = f.read()
tab1 = tab.split(':')
connection = client.connect("http://localhost:4200", username="crate")
cursor = connection.cursor()
for t in tab1:
    t1 = t.replace("number_of_replicas = '1'","number_of_replicas = '0-1'")
    print(t1)
    if 'CREATE' in t1:
       print("Execute")
       cursor.execute(str(t1))

for file in os.listdir('/home/pi/crate-4.0.6/data/irr/'): 
    if 'irr_set_hist' in file: 
        file_len = (len(file))
        tab = file[0:file_len-7]
        ins_q =  'COPY ' + tab +' FROM  ' + "'file:///home/crate/crate/data/irr/"  + file + "'" + ';'
        print(ins_q)
        cursor.execute(ins_q)

