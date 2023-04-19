
#get all the keys https://dev.fitbit.com/apps/details/23QR73
#Fill in implicit grant flow https://dev.fitbit.com/build/reference/web-api/authorization/authorize/
#in browser https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=23QR73&redirect_uri=http://localhost:8080&expires_in=31536000&scope=activity%20sleep%20heartrate%20location%20Profile
#get http://localhost:8080/#access_token=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1FSNzMiLCJzdWIiOiJCSFlDUEYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJybG9jIHJhY3QgcmhyIHJzbGUiLCJleHAiOjE3MTI3Mjg2OTUsImlhdCI6MTY4MTE5MjY5NX0.AyBW-Qfeye5tTHF5TyVp41hFDYpx9p_JUKJSUUwzmEE&user_id=BHYCPF&scope=activity+sleep+heartrate+location&token_type=Bearer&expires_in=31536000


import requests
import datetime
import time
import serial
from pprint import pprint as pp

import numpy as np
import pandas as pd
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing

import warnings
import seaborn as sns 
from itertools import cycle
import matplotlib.pyplot as plt
%matplotlib inline

####################################
microsteps =16
today = datetime.date.today()
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1FSNzMiLCJzdWIiOiJCSFlDUEYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJybG9jIHJociByYWN0IHJwcm8gcnNsZSIsImV4cCI6MTcxMjc3Mzk5OCwiaWF0IjoxNjgxMjM3OTk4fQ.ZUis2vDaDXPzplCLuXpXaOKO_tIHODypTIzW5cMO4Jc"
header = {'Authorization' : 'Bearer ' + access_token, 'Content-Type':'application/json'}
current_time_unix = int(time.time())

####################################
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
print("Initializing connection....")
time.sleep(3)
ser.reset_input_buffer()
print("connected to: " + ser.portstr)
print("moving")
####################################

def date():
    today = datetime.date.today()
    return (today)

def datetime_to_unix(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
    return int(time.mktime(dt.timetuple()))

    
def get_sleep_time_df():
    API_key = '38ca058a77bcc7e906c1c6adb7e49e35'
    url = 'https://api.fitbit.com/1.2/user/-/sleep/list.json?beforeDate={date}&sort=asc&offset=0&limit=100'
    url = url.format(date=date())
    r = requests.get(url, headers=header)    
    data = r.json()

    if r.status_code == 200:
        # Check the content of the response
        print(r.text)

        # Extract required fields from JSON data
        date_sleep = [item["dateOfSleep"] for item in data['sleep']]
        length_sleep = [item["sleep"]["minutesAsleep"] for item in sleep_time_data]
        length_sleep_sec = [minutes * 60 for minutes in length_sleep]
        begin_sleep_full = [item['startTime'] for item in data['sleep']]
        unix_begin_sleep = [datetime_to_unix(dt_str) for dt_str in begin_sleep_full]
        begin_sleep_utc = [item['startTime'][11:19] for item in data['sleep']]

    


        # Create DataFrame
        df = pd.DataFrame({
            "Date of Sleep": date_sleep,
            "Length of Sleep (sec)": length_sleep_sec,
            "Start Time of Sleep (unix)": unix_begin_sleep,
            "Start Time of Sleep (utc)": begin_sleep_utc
        })

        return(df)

    else:
        print(f"Error: {r.status_code}")

def sleep_begin_predict():
    alpha = 0.2
    model = SimpleExpSmoothing(get_sleep_time_df()['Start Time of Sleep']).fit(smoothing_level=alpha)
    forecast = model.forecast(1)
    return(forecast)

##how the forcast like? do we need to call the last row of df?  should be 1 number

def sleep_lenght_predict():
    alpha = 0.2
    model = SimpleExpSmoothing(get_sleep_time_df()['Length of Sleep (sec)']).fit(smoothing_level=alpha)
    forecast = model.forecast(1)
    return(forecast)
##how the forcast like? do we need to call the last row of df? should be 1 number


def awake_lenght_predict():
    awake_time = 86400-sleep_lenght_predict()
    return(awake_time)


def get_step_angle():
    if sleep_begin_predict() <= current_time_unix:
        stepangle = int((current_time_unix - sleep_begin_predict()) / sleep_lenght_predict() * 400.0 * microsteps)
    else:
        stepangle = int((current_time_unix - sunset_unix_time / awake_lenght_predict() * 400.0 * microsteps) + (400 * microsteps))
        get_sleep_time_df()
    return (stepangle)



####################################

while True :
    serial.write(('DAY_MOVE ' + str(get_step_angle()) + '\n').encode())
    time.sleep(1)

####################################