from crate import client
import json
import datetime
data_path ='/home/pi/data'
print (datetime.datetime.now())
current_timestamp = datetime.datetime.now()
status_ok ='OK'
status_nok='NOK'
query_max_time ="select max(load_time) from activity_s3_load where status='OK' "
query_load ="INSERT INTO activity_s3_load (load_time, status) VALUES ('{}','{}')".format(current_timestamp,status_ok)
query_load_nok="INSERT INTO activity_s3_load (load_time, status,remark) VALUES ('{}','{}' ,'{}')".format(current_timestamp,'NOK','NO DATA to EXTRACT')
query_sensors= "SELECT * from SENSORS"
try:
    connection = client.connect("http://localhost:4200", username="crate")
    cursor = connection.cursor()
    #Getting MAX TIMESTAMP

    cursor.execute(query_max_time)
    max_time = cursor.fetchone()
    max_time = max_time[0]
    print(max_time)

    #GETTING DATA BASED ON MAX TIME 
    if max_time is None:
        query = "select * from activities"
    else:
        query = "select * from activities where end_time is not null and end_time > '{}'".format(max_time)
    
    cursor.execute(query)
    rowcount = cursor.rowcount
    print(rowcount)
    result = cursor.fetchall()
    print(result)
    if rowcount > 0:
        json_string = json.dumps(result)
        file = open(data_path + '/' + datetime.datetime.today().strftime('%Y-%m-%d') + '-ACTIVITIES.txt',"a+")
        file.write(json.dumps(json_string) + '\n')
        file.close  
        cursor.execute(query_load)
    else:
        cursor.execute(query_load_nok)

    #EXTRACTING SENSOR DATA
    rowcount =0 
    cursor.execute(query_sensors)
    rowcount = cursor.rowcount
    print(rowcount)
    result = cursor.fetchall()
    print(result)
    if rowcount > 0:
        json_string = json.dumps(result)
        file = open(data_path + 'SENSORS.txt',"a+")
        file.write(json.dumps(json_string) + '\n')
        file.close    

    cursor.close()
    connection.close()
except Exception as e:
     print ("Data Extraction Failed")

