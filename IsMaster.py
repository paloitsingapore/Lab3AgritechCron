import os
import sys
module_path = os.path.abspath(os.getcwd() + '\\..')
if module_path not in sys.path:
    sys.path.append(module_path)
from crate import client


#connection = client.connect("http://172.16.13.50:4200", username="crate")
#cursor = connection.cursor()
#query = "CREATE TABLE TH_DATA (MAC_ADD TEXT PRIMARY KEY, TIME timestamp PRIMARY KEY, TEMPERATURE float, HUMIDITY float) WITH (number_of_replicas = 1)"
#cursor.execute(query)
#cursor.close()
#connection.close()

query = "select id ,rest_url from sys.nodes a where id =(select master_node from sys.cluster)"
try:
 connection = client.connect("http://172.16.12.203:4200", username="crate")
 cursor = connection.cursor()
 cursor.execute(query)
 result = cursor.fetchone()
 result_str = str(result)
 result_str= result_str.split(",") 
 print (result_str[1])
 cursor.close()
 connection.close()
except Exception as e:
 print ("Error: " + e)

