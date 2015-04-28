import requests

token = '9WlGWF035I7TlUmIy2hYKyRW36AvrSVo'
headers = {'Authorization: Bearer ' + token}
response = requests.get("https://api.box.com/2.0/files/bmb0dhzzi9zx87isny6pr2bo99ja5q9w/content")

print response.status_code
for chunk in response.iter_content(1000):
    print chunk