import serial
import time
import datetime
import requests
from pprint import pprint as pp


#########################

ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
print("Initializing connection....")
time.sleep(3)
ser.reset_input_buffer()



def Dayleng_Angle():
    sec = 0
    lat = 40.807537
    lon = -73.962570
    API_key = '38ca058a77bcc7e906c1c6adb7e49e35'
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}'
    url = url.format(lat=lat, lon=lon, API_key=API_key)
    print(url)
    r = requests.get(url)
    r.status_code
    pp(r.json())
    Sunrise = r.json()['sys']['sunrise']
    Sunset = r.json()AccelStepper stepper1(AccelStepper::FULL2WIRE, 2, 5);['sys']['sunset']
    DaylengUnix = Sunset - Sunrise
    pp(DaylengUnix)
    #while sec < DaylengUnix:
    #    print(sec)
    #    sec += 1
    return (sec/DaylengUnix)*180


while True:

    time.sleep(1)
    stepangle = int(Dayleng_Angle()  /360.0 * 800.0)
    ser.write(('DAY_MOVE ' + str(stepangle) + '\n').encode())
    
    
    
"""

last_update = 0
dayleng = 0

while True:


    if current_time - last_update > 24h:
        update_Dayleng()
        current_time = now
    
    rotate_motor_to_current_angle()
    
    time.sleep(60)
    
"""
    
