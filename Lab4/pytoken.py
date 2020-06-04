import requests


url = "https://login.microsoftonline.com/7a1df1b4-6447-42e5-a909-9856defa1164/oauth2/token"

payload = {'grant_type': 'client_credentials',
'client_id': '43fe8c33-02cf-43fb-8156-fd9ac7c38936',
'client_secret': 'YTdmOTdhYTYtN2IzZS00Y2MxLWI3NjAtYTRmOWI4NmNkOTkz=',
'resource': 'https://management.azure.com/'}
files = [

]
headers = {
  'Cookie': 'stsservicecookie=estsfd; x-ms-gateway-slice=estsfd; fpc=AoLpVDUit61GvM_Vdmq9oFDONg5DAQAAAKBPO9YOAAAA'
}

r = requests.post(url, data=payload)
r.status_code
r.headers = headers
jsonResp = r.json()         # To get response dictionary as JSON 
print(jsonResp['token_type'] , jsonResp['access_token'], sep = ' : ')  # output: Python Requests : Requests are awesome 
bearercode = jsonResp['access_token']
g = requests.get('https://farmbeats-palo-lab-dev-site-api.azurewebsites.net/Device',data= {'access_code': bearercode})
print(g.text)
