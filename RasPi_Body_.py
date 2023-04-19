
#get all the keys https://dev.fitbit.com/apps/details/23QR73
#Fill in implicit grant flow https://dev.fitbit.com/build/reference/web-api/authorization/authorize/
#in browser https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=23QR73&redirect_uri=http://localhost:8080&expires_in=31536000&scope=activity%20sleep%20heartrate%20location%20Profile
#get http://localhost:8080/#access_token=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1FSNzMiLCJzdWIiOiJCSFlDUEYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJybG9jIHJhY3QgcmhyIHJzbGUiLCJleHAiOjE3MTI3Mjg2OTUsImlhdCI6MTY4MTE5MjY5NX0.AyBW-Qfeye5tTHF5TyVp41hFDYpx9p_JUKJSUUwzmEE&user_id=BHYCPF&scope=activity+sleep+heartrate+location&token_type=Bearer&expires_in=31536000


import requests
import datetime
import time
import serial
from pprint import pprint as pp


access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1FSNzMiLCJzdWIiOiJCSFlDUEYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJybG9jIHJociByYWN0IHJwcm8gcnNsZSIsImV4cCI6MTcxMjc3Mzk5OCwiaWF0IjoxNjgxMjM3OTk4fQ.ZUis2vDaDXPzplCLuXpXaOKO_tIHODypTIzW5cMO4Jc"
header = {'Authorization' : 'Bearer ' + access_token, 'Content-Type':'application/json'}


ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
print("Initializing connection....")
time.sleep(3)
ser.reset_input_buffer()


def date():
    today = datetime.date.today()
    return (today)

    
def Sleep_time():
    API_key = '38ca058a77bcc7e906c1c6adb7e49e35'
    url = 'https://api.fitbit.com/1.2/user/-/sleep/date/{date}.json'
    url = url.format(date=date())
    print(url)
    r = requests.get("https://api.fitbit.com/1/user/-/profile.json", headers=header).json()    
    Sleep_time_data = r.json()['']['']
    return (Sleep_time_data)

