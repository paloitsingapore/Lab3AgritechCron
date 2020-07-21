import requests
import msal
import json
import gentoken
import os

filename = 'sensor.json'
with open(filename, 'r') as f:
    data = json.load(f)      
payload = json.dumps(data) 
print(payload)
response = requests.post(gentoken.ENDPOINT + "/Sensor", data=payload, headers=gentoken.headers)

print(response.text)