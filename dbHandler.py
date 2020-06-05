from crate import client


#connection = client.connect("http://192.168.1.101:4200", username="crate")
#cursor = connection.cursor()
#query = "CREATE TABLE TH_DATA (MAC_ADD TEXT PRIMARY KEY, TIME timestamp PRIMARY KEY, TEMPERATURE float, HUMIDITY float) WITH (number_of_replicas = 1)"
#cursor.execute(query)
#cursor.close()
#connection.close()

def InsertDB(table, mac_add, time, temperature, humidity):
    query = "INSERT INTO {} (MAC_ADD, TIME, TEMPERATURE, HUMIDITY) VALUES ('{}','{}','{}','{}')".format(table,mac_add,time,temperature, humidity)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("Error: " + e)


def GetSensorType(mac_add):
    query = "SELECT sensor_type FROM SENSOR_INFO WHERE MAC_ADD = '{}'".format(mac_add)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0]
    except Exception as e:
        print ("Error: " + e)
        
        
def GetListContainer():
    query = "select distinct id from containers"
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        print ("Error: " + str(e))

def GetContainerInfo(container_id):
    query = "SELECT humidity_setup - humidity_range start_point_humid ,  humidity_setup end_point_humid ,temperature_setup + temperature_range  start_point_temp , temperature_setup end_point_temp ,fan fan_switch ,mist mist_switch, fanning,auto_fanning,misting,auto_misting  FROM containers WHERE id = '{}'".format(container_id)     
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]
    except Exception as e:
        print ("Error: " + e)


def GetContainerHumidInfo(container_id):
    query = "SELECT humidity_setup end_point_humid, humidity_setup - humidity_range start_point_humid FROM containers WHERE id = '{}'".format(container_id)     
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0], result[1]
    except Exception as e:
        print ("Error: " + e)


def GetContainerTempInfo(container_id):
    query = "SELECT temperature_setup end_point_temp, temperature_setup + temperature_range  start_point_temp FROM containers WHERE id = '{}'".format(container_id)     
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0], result[1]
    except Exception as e:
        print ("Error: " + e)

def GetContainerStatus(container_id, system_type):
    query = "SELECT {} FROM containers WHERE id = '{}'".format(system_type, container_id)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor= connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    except Exception as e:
        print ("Error: " + e)

        
    
def GetAveTempHumid(container_id):
    query = "select avg(temperature) , avg(humidity), date_format('%d/%b/%Y %r', MAX(T1.TIME)) from th_data t1 , (select max(time)  time ,mac_Add from th_data  where mac_Add in (select macadd from  sensors where container  in ('{}'))group by mac_Add) t2  where t1.mac_add = t2.mac_Add and t1.time= t2.time;".format(container_id)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0], result[1], result[2]
    except Exception as e:
        print ("Error: " + e)
        

def UpdateContainerStatus(container_id, system_type, status):
    query = "update containers set {} = {} where id = '{}'".format(system_type, status, container_id)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("Error: " + e)      


def InsertActivity(Aid, sensor_id, timenow, Dtype, avetemp, avehumid):
    query = "INSERT INTO activities (activity_id, system_id, start_time, system_type, bfr_avg_temp, bfr_avg_humidity) VALUES ('{}','{}','{}','{}','{}','{}')".format(str(Aid), sensor_id, timenow, Dtype, avetemp, avehumid)
    print(query)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("Error: " + e)


def UpdateActivity(activity_id, sensor_id, endtime, avetemp, avehumi):
    query = "UPDATE activities set end_time = '{}', aftr_avg_temp = '{}', aft_avg_humidity = '{}' where activity_id = '{}' and system_id = '{}'".format(endtime, avetemp, avehumi, activity_id, sensor_id)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("Error: " + e)




def GetSystemStatus(system_type, container_id, status, active):
    query = "SELECT count(*) FROM user_action WHERE status in {} AND system_type = '{}' AND container_id = '{}' AND activating = '{}'".format(status, system_type, container_id, active)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0]
    except Exception as e:
        print ("Error: " + e)


def UpdateUserActions(status, system_type, activating, container_id, current_status):
    query = "UPDATE user_action set status = {} where system_type = '{}' and activating = '{}' and container_id = '{}' and status = '{}'".format(status, system_type, activating, container_id, current_status)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("Error: " + e)
        

def GetDelayTime(status, system_type, container_id, active):
    query = "SELECT delay FROM user_action WHERE status = {} AND system_type = '{}' AND container_id = '{}' AND activating = '{}'".format(status, system_type, container_id, active)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result[0]
    except Exception as e:
        print ("Error: " + e)
        
def GetRunningData(status, system_type, container_id):
    query = "SELECT id, delay, date_format('%Y%m%d%H%i', action_time) FROM user_action WHERE status = '{}' AND system_type = '{}' AND container_id = '{}' LIMIT 1".format(status, system_type, container_id)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        print ("Error: " + str(e))
        
        
def ClearUserActions(pid, status, remark):
    query = "UPDATE user_action set status = '{}' , remarks = '{}' where id = '{}'".format(status, remark, pid)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("Error: " + str(e))
        
def GetGraphData(date):
    query = "SELECT DATE_TRUNC('hour', time) AS day, avg(temperature) as temp, avg(humidity) as humidity FROM TH_data WHERE  time < '2020-02-19' and time > '2020-02-18' GROUP BY 1 ORDER BY 1 DESC"
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        print ("Error: " + str(e))
