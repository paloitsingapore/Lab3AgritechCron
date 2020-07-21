import requests
import msal
import json
import os

# Your service principal App ID
CLIENT_ID = '43fe8c33-02cf-43fb-8156-fd9ac7c38936'
# Your service principal password
CLIENT_SECRET = 'YTdmOTdhYTYtN2IzZS00Y2MxLWI3NjAtYTRmOWI4NmNkOTkz='
# Tenant ID for your Azure subscription
TENANT_ID = "7a1df1b4-6447-42e5-a909-9856defa1164"

AUTHORITY= 'https://login.microsoftonline.com/' + TENANT_ID
ENDPOINT ='https://farmbeats-palo-lab-dev-site-api.azurewebsites.net'

filepath = '/home/pi/Lab3AgritechCron/Lab4/farmbeats/json/'
filename = 'sensorModel.json'
dest = os.path.join(str(filepath) + str(filename))
SCOPE = ENDPOINT + "/.default"

context = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = context.acquire_token_for_client(SCOPE)
# We should get an access token here
access_token = token_response.get('access_token')
print(access_token)


headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type" : "application/json"
    }

with open(dest, 'r') as f:
    json_dict = json.load(f)
payload = json.dumps(json_dict)
#response = requests.delete(ENDPOINT + "/SensorModel/b63b69d0-93ea-4355-bd5a-959130004e8d", data=payload, headers=headers)
response2 = requests.get(ENDPOINT + "/SensorModel", headers=headers)


#print(response.text)
print(response2.text)
