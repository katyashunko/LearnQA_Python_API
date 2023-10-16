import requests
import time
import json

response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
token = json.loads(response.text)
print(token)
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job",  params=token)
print(response.text)
time.sleep(token['seconds'])
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params=token)
print(response.text)
