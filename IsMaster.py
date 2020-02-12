import os
import sys
from crate import client

query = "select id ,rest_url from sys.nodes a where id =(select master_node from sys.cluster)"
try:
 connection = client.connect("http://localhost:4200", username="crate")
 cursor = connection.cursor()
 cursor.execute(query)
 result = cursor.fetchone()
 result_str = str(result)
 result_str= result_str.split(",") 
 ip=result_str[1]
 if ip[2:-7] == '192.168.1.103':
     print('192.168.1.102')
 else:
     print(ip[2:-7]) 
 cursor.close()
 connection.close()
except Exception as e:
 print ("0.0.0.0")

