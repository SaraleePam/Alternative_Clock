
#get all the keys https://dev.fitbit.com/apps/details/23QR73
#Fill in implicit grant flow https://dev.fitbit.com/build/reference/web-api/authorization/authorize/
#in browser https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=23QR73&redirect_uri=http://localhost:8080&expires_in=31536000&scope=activity%20sleep%20heartrate%20location%20Profile
#get http://localhost:8080/#access_token=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1FSNzMiLCJzdWIiOiJCSFlDUEYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJybG9jIHJhY3QgcmhyIHJzbGUiLCJleHAiOjE3MTI3Mjg2OTUsImlhdCI6MTY4MTE5MjY5NX0.AyBW-Qfeye5tTHF5TyVp41hFDYpx9p_JUKJSUUwzmEE&user_id=BHYCPF&scope=activity+sleep+heartrate+location&token_type=Bearer&expires_in=31536000
# simplesmooth method https://medium.com/analytics-vidhya/time-series-forecasting-step-by-step-a06dac2293ff

import serial
import requests
import datetime
import time
import pytz

#import serial
from pprint import pprint as pp
from datetime import timedelta

import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.metrics import mean_squared_error
from statsmodels.tools.eval_measures import rmse
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, ExponentialSmoothing
############################

microsteps =16

local_timezone = pytz.timezone('America/New_York')
now = datetime.datetime.now(local_timezone)
timestamp = int(now.timestamp())


current_time_unix = int(now.timestamp())

today = datetime.datetime.now(local_timezone).date()
tomorrow = now + datetime.timedelta(days=1)
yesterday = now - datetime.timedelta(days=1)



print(current_time_unix)
print(now)
print(today)
print(tomorrow)
print(yesterday)

access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1FSNzMiLCJzdWIiOiJCSFlDUEYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJybG9jIHJociByYWN0IHJwcm8gcnNsZSIsImV4cCI6MTcxMjc3Mzk5OCwiaWF0IjoxNjgxMjM3OTk4fQ.ZUis2vDaDXPzplCLuXpXaOKO_tIHODypTIzW5cMO4Jc"
header = {'Authorization' : 'Bearer ' + access_token, 'Content-Type':'application/json'}

########################
ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
print("Initializing connection....")
time.sleep(3)
ser.reset_input_buffer()
print("connected to: " + ser.portstr)
print("moving")
########################
def date():
    today = datetime.date.today()
    return (today)

def datetime_to_unix(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f')
    return int(time.mktime(dt.timetuple()))

def time_to_seconds(time_string):
    hours, minutes, seconds = map(int, time_string.split(':'))
    total_seconds = (hours * 3600) + (minutes * 60) + seconds
    return total_seconds

def seconds_to_time(total_seconds):
    days, seconds = divmod(total_seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return time_string


def sleep_begin_sec(time_str):
    dt = datetime.datetime.strptime(time_str, "%H:%M:%S")
    seconds = (dt.hour * 3600) + (dt.minute * 60) + dt.second
    if seconds < 43200:
        seconds += 86400
    return seconds



def get_sleep_time_df():
    API_key = '38ca058a77bcc7e906c1c6adb7e49e35'
    url = 'https://api.fitbit.com/1.2/user/-/sleep/list.json?beforeDate={date}&sort=asc&offset=0&limit=100'
    url = url.format(date=date())
    r = requests.get(url, headers=header)    
    data = r.json()

    if r.status_code == 200:

        # Extract required fields from JSON data
        date_sleep = [item["dateOfSleep"] for item in data['sleep']]
        length_sleep = [item["minutesAsleep"] for item in data['sleep']]
        length_sleep_sec = [minutes * 60 for minutes in length_sleep]
        # begin_sleep = [item['startTime'] for item in data['sleep']]

        begin_sleep = [datetime.datetime.strptime(item['startTime'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%H:%M:%S') for item in data['sleep']]

        begin_sleep_sec = [sleep_begin_sec(item) for item in begin_sleep]

        # unix_begin_sleep = [datetime_to_unix(dt_str) for dt_str in begin_sleep]
        

        # Create DataFrame
        df = pd.DataFrame({
            "Date of Sleep": date_sleep,
            "Length of Sleep (sec)": length_sleep_sec,
            "Start Time of Sleep (UTC)": begin_sleep,
            "Start Time of Sleep (sec)": begin_sleep_sec,

        })



        # df['Start Time of Sleep (Seconds)'] = df['Start Time of Sleep (UTC)'].apply(time_to_seconds)


        return(df)
    

    else:
        print(f"Error: {r.status_code}")


########################


def sleep_begin_predict():
    average = get_sleep_time_df()["Start Time of Sleep (sec)"].mean()
    if average >= 86400:
       average -= 86400
    return int(average)




########################

sleep_time_str = seconds_to_time(sleep_begin_predict())
print(sleep_time_str)

# Convert the sleep time string to a datetime object
sleep_time = datetime.datetime.strptime(sleep_time_str, '%H:%M:%S').time()
print(sleep_time)

midnight = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
print(midnight)

# Combine the date and sleep time to get the sleep begin datetime object in the local timezone
if sleep_time > midnight.time():
  sleep_begin_local = local_timezone.localize(datetime.datetime.combine(tomorrow, sleep_time))
else:
  sleep_begin_local = local_timezone.localize(datetime.datetime.combine(today, sleep_time))


sleep_begin_unix = sleep_begin_local.timestamp()
print(sleep_begin_local)
print(sleep_begin_unix)

########################


def sleep_lenght_predict():
    alpha = 0.2
    model = SimpleExpSmoothing(get_sleep_time_df()['Length of Sleep (sec)']).fit(smoothing_level=alpha)
    forecast = model.forecast(1)
    sleep_lenght = int(forecast.iloc[0])
    return(sleep_lenght)

def awake_lenght_predict():
    awake_time = int(86400-sleep_lenght_predict())
    return(awake_time)

def awake_begin_predict():
    forecast = int(sleep_begin_predict() + sleep_lenght_predict())
    return(forecast)

##################################

awake_begin_str = seconds_to_time(awake_begin_predict())
print(awake_begin_str)

# Convert the awake time string to a datetime object
awake_time = datetime.datetime.strptime(awake_begin_str, '%H:%M:%S').time()
print(awake_time)

# Combine the date and awake time to get the awake begin datetime object in the local timezone
awake_begin_local = local_timezone.localize(datetime.datetime.combine(tomorrow, awake_time))
awake_begin_unix = awake_begin_local.timestamp()
print(tomorrow)
print(awake_begin_local)
print(awake_begin_unix)

dataframe = get_sleep_time_df()


# calculate last wake begin time
last_sleep_time = dataframe.iloc[-1, -1]
last_sleep_lenght = dataframe.iloc[-1,1]
last_awake_time = seconds_to_time(last_sleep_time + last_sleep_lenght)
print(last_awake_time)


last_awake_time_obj = datetime.datetime.strptime(last_awake_time, '%H:%M:%S').time()
last_awake_begin_local = local_timezone.localize(datetime.datetime.combine(today, last_awake_time_obj))
last_awake_begin_unix = last_awake_begin_local.timestamp()


########################
def get_step_angle():
    if awake_begin_unix <= current_time_unix <= sleep_begin_unix:
        stepangle = int((current_time_unix - last_awake_begin_unix) / awake_lenght_predict()  * 400.0 * microsteps)

    else:
        stepangle = int(((current_time_unix - sleep_begin_unix) / awake_lenght_predict() * 400.0 * microsteps) + (400 * microsteps))

    return(stepangle)
########################


while True :
    ser.write(('DAY_MOVE ' + str(get_step_angle()) + '\n').encode())
    time.sleep(5)