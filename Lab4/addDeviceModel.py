import requests
import msal
import json
import os
import gentoken

with open('deviceModel.json', 'r') as f:
    json_dict = json.load(f)
payload = json.dumps(json_dict)

response = requests.post(gentoken.ENDPOINT + "/DeviceModel", data=payload, headers=gentoken.headers)
json_r = response.json()
print(response.text)
print(json_r['id'])
#print(response2.text)
if (response.status_code == 200):
    print("Hello")
    filename = 'device.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        data['deviceModelId'] = json_r["id"]# <--- add `id` value.
    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    with open(filename, 'r') as f:
        data = json.load(f)      
    a = json.dumps(data) 
    print(a)
    print("Successsfullyy updates device.json")
