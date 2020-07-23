from crate import client
query = "show tables"
connection = client.connect("http://localhost:4200", username="crate")
cursor = connection.cursor()
cursor.execute(query)
result = cursor.fetchall()
for tab in result:
    if tab[0] in ['sensors','soil_data','irr_set_cust','faucets']:
        cp_data = "COPY " + str(tab[0]) +" TO DIRECTORY '/home/crate/crate/data/az'"
        cursor.execute(cp_data)
cursor.close()
connection.close()
