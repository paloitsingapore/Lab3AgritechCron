from crate import client


#connection = client.connect("http://172.16.13.50:4200", username="crate")
#cursor = connection.cursor()
#query = "CREATE TABLE TH_DATA (MAC_ADD TEXT PRIMARY KEY, TIME timestamp PRIMARY KEY, TEMPERATURE float, HUMIDITY float) WITH (number_of_replicas = 1)"
#cursor.execute(query)
#cursor.close()
#connection.close()

def InsertDB(mac_add, time, temperature, humidity):
    query = "INSERT INTO TH_DATA (MAC_ADD, TIME, TEMPERATURE, HUMIDITY) VALUES ('{}','{}','{}','{}')".format(mac_add,time,temperature, humidity)
    try:
        connection = client.connect("http://localhost:4200", username="crate")
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Exception as e:
        print ("Error: " + e)

