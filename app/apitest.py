import requests
 
url = "https://emailapi.netcorecloud.net/v5/mail/send"
 
payload = "{\"from\":{\"email\":\"confirmation@pepisandbox.com\",\"name\":\"Flight confirmation\"},\"subject\":\"Your Barcelona flight e-ticket : BCN2118050657714\",\"content\":[{\"type\":\"html\",\"value\":\"Hello Lionel, Your flight for Barcelona is confirmed.\"}],\"personalizations\":[{\"to\":[{\"email\":\"lionel@gmail.com\",\"name\":\"Lionel Messi\"}]}]}"
headers = {
	'api_key': "27692da1594047c6f5e46db25403aee5",
	'content-type': "application/json"
	}
 
response = requests.request("POST", url, data=payload, headers=headers)
 
print(response.text)