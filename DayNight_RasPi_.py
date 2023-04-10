Python3


import requests
from pprint import pprint as pp
lat = 40.807537
lon = -73.962570
API_key = '38ca058a77bcc7e906c1c6adb7e49e35'
url = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'

r = requests.get(url)
r.status_code

Sunrise = r.json()['sys']['sunrise']
Sunset = r.json()['sys']['sunset']
Dayleng = Sunset - Sunrise

pp(Dayleng)


    