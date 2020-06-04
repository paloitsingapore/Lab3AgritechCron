import requests
import msal
import json

CLIENT_ID = '43fe8c33-02cf-43fb-8156-fd9ac7c38936' # Your service principal App ID
CLIENT_SECRET = 'YTdmOTdhYTYtN2IzZS00Y2MxLWI3NjAtYTRmOWI4NmNkOTkz=' # Your service principal password
TENANT_ID = "7a1df1b4-6447-42e5-a909-9856defa1164" # Tenant ID for your Azure subscription
AUTHORITY= 'https://login.microsoftonline.com/' + TENANT_ID
ENDPOINT ='https://farmbeats-palo-lab-dev-site-api.azurewebsites.net'
SCOPE = ENDPOINT + "/.default"

context = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = context.acquire_token_for_client(SCOPE)
access_token = token_response.get('access_token') # We should get an access token here
print(access_token)

headers = {"Authorization": "Bearer " + access_token,"Content-Type" : "application/json"}