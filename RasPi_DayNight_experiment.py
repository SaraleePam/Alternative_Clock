import serial
import time
import datetime
import requests
from datetime import  timedelta
from pprint import pprint as pp

microsteps = 16
lat = 40.807537
lon = -73.962570
today = datetime.date.today()
tomorrow = today + timedelta(days=1)
yesterday = today + timedelta(days=-1)
current_time_unix = int(time.time())

#########################################

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
print("Initializing connection....")
time.sleep(3)
ser.reset_input_buffer()
print("HELLO!")
print("connected to: " + ser.portstr)
print("moving")

#########################################

url = 'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}'
url = url.format(lat=lat, lon=lon, date=today)
r = requests.get(url)
sunrise = r.json()['results']['sunrise']
sunset = r.json()['results']['sunset']


url2 = url.format(lat=lat, lon=lon, date=tomorrow)
r_tomorrow = requests.get(url2)
next_sunrise = r_tomorrow.json()['results']['sunrise']


url3 = url.format(lat=lat, lon=lon, date=yesterday)
r_yesterday = requests.get(url3)
last_sunset = r_yesterday.json()['results']['sunset']

#############

sunrise_obj = datetime.datetime.strptime(sunrise, "%I:%M:%S %p")
sunrise_datetime_obj = datetime.datetime.combine(today, sunrise_obj.time())
sunrise_unix_time = sunrise_datetime_obj.timestamp()

sunset_obj = datetime.datetime.strptime(sunset, "%I:%M:%S %p")
sunset_datetime_obj = datetime.datetime.combine(today, sunset_obj.time())
sunset_unix_time = sunset_datetime_obj.timestamp()

next_sunrise_obj = datetime.datetime.strptime(next_sunrise, "%I:%M:%S %p")
next_sunrise_datetime_obj = datetime.datetime.combine(tomorrow, next_sunrise_obj.time())
next_sunrise_unix_time = next_sunrise_datetime_obj.timestamp()


last_sunset_obj = datetime.datetime.strptime(last_sunset, "%I:%M:%S %p")
last_sunset_datetime_obj = datetime.datetime.combine(yesterday, last_sunset_obj.time())
last_sunset_unix_time = last_sunset_datetime_obj.timestamp()

#######################

def get_daylenght():
    daylenght = sunset_unix_time - sunrise_unix_time
    return daylenght


def get_nightlenght():
    nightlenght = next_sunrise_unix_time - sunset_unix_time
    return nightlenght

def get_step_angle():
    if sunrise_unix_time <= current_time_unix <= sunset_unix_time:
        stepangle = int((current_time_unix - sunrise_unix_time) / get_daylenght() * 400.0 * microsteps)

   #for night time after midnight (the today sunset&sunrise is not the same)
    if (current_time_unix < sunrise_unix_time) and (current_time_unix < sunset_unix_time):
        stepangle = int(((current_time_unix - last_sunset_unix_time) / get_nightlenght() * 400.0 * microsteps) + (400 * microsteps))

    else:
        stepangle = int(((current_time_unix - sunset_unix_time) / get_nightlenght() * 400.0 * microsteps) + (400 * microsteps))

    return(stepangle)

#########################################



while True:
    time.sleep(5)   
    stepangle= get_step_angle()
    print(stepangle)
    ser.write(('DAY_MOVE ' + str(stepangle) + '\n').encode())
    


#########################################


