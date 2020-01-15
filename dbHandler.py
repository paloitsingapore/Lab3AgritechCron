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

        
