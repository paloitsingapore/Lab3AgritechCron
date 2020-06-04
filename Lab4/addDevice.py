import requests
import msal
import json
import gentoken
import os

filename = 'device.json'

with open(filename, 'r') as f:
    data = json.load(f)      
payload = json.dumps(data) 
response = requests.post(gentoken.ENDPOINT + "/Device", data=payload, headers=gentoken.headers)

print(response.text)


