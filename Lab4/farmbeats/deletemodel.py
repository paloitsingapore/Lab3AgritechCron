import requests
import msal
import json
import gentoken
import os

with open('deviceModel.json', 'r') as f:
    json_dict = json.load(f)
payload = json.dumps(json_dict) #to convert as JSON attribute from single quote to double quote
DEVICE= "ebfe6460-6666-42ff-baa5-5c010b8bc53e"
url = gentoken.ENDPOINT + "/Sensor/" + DEVICE
r = requests.delete(url=url,headers=gentoken.headers) #, auth=HTTPBasicAuth(access_token, 'api_token'))
print(r.text)
print(r.status_code)
