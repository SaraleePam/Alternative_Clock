import serial
import time
import datetime
import requests
from pprint import pprint as pp

microsteps = 16
sec = 0
lat = 40.807537
lon = -73.962570
API_key = '38ca058a77bcc7e906c1c6adb7e49e35'
sec = int(time.time())
#########################

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
print("Initializing connection....")
time.sleep(3)
ser.reset_input_buffer()


""""""
import requests
from pprint import pprint as pp
url = 'https://api.sunrise-sunset.org/json?lat=36.7201600&lng=-4.4203400'
r = requests.get(url)
pp(r.json())
""""""


def Sunrise():
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'
    url = url.format(lat=lat, lon=lon, API_key=API_key)
    print(url)
    r = requests.get(url)
    pp(r.json())
    Sunrise = r.json()['sys']['sunrise']
    return (Sunrise)

def Sunset():
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'
    url = url.format(lat=lat, lon=lon, API_key=API_key)
    print(url)
    r = requests.get(url)
    pp(r.json())
    Sunset = r.json()['sys']['sunset']
    return (Sunset)

while True:

    if sec <= Sunrise():??
        stepangle = int(sec / (Sunset()-Sunrise()) * 400.0 * microsteps)

    else:
        stepangle = int((sec / (Sunrise()-Sunset()) * 400.0 * microsteps) + (400 * microsteps))

    sec += 1
    print(sec)

    ser.write(('DAY_MOVE ' + str(stepangle) + '\n').encode())
    time.sleep(3)



"""
last_update = 0
dayleng = 0

while True:

    if current_time - last_update > 24h:
        update_Dayleng()
        current_time = now

    # while sec < DaylengUnix:
    #    print(sec)
    #    sec += 1

    rotate_motor_to_current_angle()
    ser.write(('DAY_MOVE ' + str(stepangle) + '\n').encode())
    
    time.sleep(60)
    
    while True:

    time.sleep(1)
    stepangle = int(Dayleng_Angle()  /360.0 * 800.0)
    ser.write(('DAY_MOVE ' + str(stepangle) + '\n').encode())
"""
    

"""
#https://pypi.org/project/suntime/


import datetime
from datetime import datetime
from suntime import Sun

lat = 40.807537
lon = -73.962570
abd = datetime.date(2014, 10, 3)
sun = Sun(lat, lon)

today_sr = sun.get_sunrise_time()
today_ss = sun.get_sunset_time()

ts = datetime.timestamp(today_sr)
"""
"""

#install library https://pypi.org/project/daylight/


import serial
import time
import datetime
from datetime import datetime
import requests
import pytz
import daylight
from pprint import pprint as pp

lat = 40.807537
lon = -73.962570


def epoch(year, month, day, hour=0, minute=0, second=0, tz=pytz.UTC):
    return int(tz.localize(datetime.datetime(year, month, day, hour, minute, second)).timestamp())

tz = pytz.timezone('US/Eastern')
tz_offset = tz.utcoffset(datetime.datetime.utcnow()).total_seconds() / 3600

# Example with GPS coords for Hyderabad, India, in Indian timezone (IST)
sun = daylight.Sunclock(lat, lon)

# Know the sunrise time for a given date
# Returns unix timestamp for 5:42 AM
sun.sunrise(epoch(2020, 5, 21, tz=tz))

# Know the sunset time for a given date
# Returns unix timestamp for 18:42 PM
sun.sunset(epoch(2020, 5, 21, tz=tz))

 sunrise_unix_time = sunrise_datetime.replace(tzinfo=timezone.utc).timestamp()

"""