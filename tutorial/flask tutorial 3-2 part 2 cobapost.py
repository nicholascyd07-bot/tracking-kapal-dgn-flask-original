import requests

req = requests.post("http://127.0.0.1:5002/cobarequest")

print(req.text)