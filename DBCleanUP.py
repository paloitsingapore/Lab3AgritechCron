import os
import sys
import datetime
import subprocess
from crate import client
from myip import GetIP 

timestamp_s = datetime.datetime.now()-datetime.timedelta(days=7)
timestamp_s = timestamp_s.strftime('%Y-%m-%d')
query = "delete  FROM ""doc"".""th_data"" where ""time"" < '" + str(timestamp_s) + "'"
print(query) 

masterip = str(subprocess.run(["python3", "IsMaster.py"], stdout=subprocess.PIPE).stdout)
masterip = masterip[2:-3]
myip = GetIP()
if masterip == myip:
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        #out=cursor.execute(query)
        #print(out)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("0.0.0.0" + str(e))

else:
    print("I am not master")
