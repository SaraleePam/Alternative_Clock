import serial
import time
import datetime
import requests
from datetime import datetime, timedelta
from pprint import pprint as pp

microsteps = 16
lat = 40.807537
lon = -73.962570
today = datetime.date.today()
tomorrow = today + timedelta(days=1)
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

sunrise_obj = datetime.datetime.strptime(sunrise, "%I:%M:%S %p")
sunrise_datetime_obj = datetime.datetime.combine(today, sunrise_obj.time())
sunrise_unix_time = sunrise_datetime_obj.timestamp()

sunset_obj = datetime.datetime.strptime(sunset, "%I:%M:%S %p")
sunset_datetime_obj = datetime.datetime.combine(today, sunrise_obj.time())
sunset_unix_time = sunrise_datetime_obj.timestamp()


def get_daylenght():
    daylenght = sunset_unix_time - sunrise_unix_time
    return daylenght


def get_nightlenght():

    url = 'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={date}'
    url = url.format(lat=lat, lon=lon, date=tomorrow)
    r_tomorrow = requests.get(url)
    next_sunrise = r_tomorrow.json()['results']['sunrise']

    next_sunrise_obj = datetime.datetime.strptime(next_sunrise, "%I:%M:%S %p")
    next_sunrise_datetime_obj = datetime.datetime.combine(tomorrow, sunrise_obj.time())
    next_sunrise_unix_time = sunrise_datetime_obj.timestamp()

    nightlenght = next_sunrise_unix_time - sunset_unix_time

    return nightlenght

#########################################


while True:

    if sunrise_unix_time <= current_time_unix <= sunset_unix_time:
        stepangle = int((current_time_unix-sunrise_unix_time) / get_daylenght() * 400.0 * microsteps)

    else:
        stepangle = int((current_time_unix - sunset_unix_time / get_nightlenght() * 400.0 * microsteps) + (400 * microsteps))


    serial.write(('DAY_MOVE ' + str(stepangle) + '\n').encode())
    time.sleep(1)

#########################################


