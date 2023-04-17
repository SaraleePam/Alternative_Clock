
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


today = datetime.date.today()
access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1FSNzMiLCJzdWIiOiJCSFlDUEYiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJybG9jIHJociByYWN0IHJwcm8gcnNsZSIsImV4cCI6MTcxMjc3Mzk5OCwiaWF0IjoxNjgxMjM3OTk4fQ.ZUis2vDaDXPzplCLuXpXaOKO_tIHODypTIzW5cMO4Jc"
header = {'Authorization' : 'Bearer ' + access_token, 'Content-Type':'application/json'}


ser = serial.Serial(port='/dev/ttyACM0', baudrate=9600)
print("Initializing connection....")
time.sleep(3)
ser.reset_input_buffer()


def date():
    today = datetime.date.today()
    return (today)

    
def sleep_time():
    API_key = '38ca058a77bcc7e906c1c6adb7e49e35'
    url = 'https://api.fitbit.com/1.2/user/-/sleep/list.json?beforeDate={date}&sort=asc&offset=0&limit=100'
    url = url.format(date=date())
    r = requests.get(url, headers=header)    
    sleep_time_data = r.json()
    return (sleep_time_data)



##make data fram from api data
new_df = pd.DataFrame()

new_df['day'] = sleep_time()['sleep']['startTime'].dt.date
new_df['year'] = sleep_time()['sleep']['startTime'].dt.year
new_df['month'] = sleep_time()['sleep']['startTime'].dt.month
new_df['date'] = pd.to_datetime(new_df[['day', 'year', 'month']])

new_df['begin'] = sleep_time()['sleep']['startTime'].dt.time
new_df['lenght'] = sleep_time()['sleep']['timeInBed']


new_df = new_df.set_index('date')
new_df.head()


train_data = new_df.iloc[:96]
test_data = new_df.iloc[96:]
 


span = 12
alpha = 2/(span+1)
simpleExpSmooth_model = SimpleExpSmoothing(train_data['begin']).fit(smoothing_level=alpha,optimized=False)
doubleExpSmooth_model = ExponentialSmoothing(train_data['begin'],trend='add',seasonal_periods=12).fit()
tripleExpSmooth_model = ExponentialSmoothing(train_data['begin'],trend='add',seasonal='add',seasonal_periods=12).fit()

predictions_simpleExpSmooth_model = simpleExpSmooth_model.forecast(24)
predictions_doubleExpSmooth_model = doubleExpSmooth_model.forecast(24)
predictions_tripleExpSmooth_model = tripleExpSmooth_model.forecast(24)


train_data['begin'].plot(legend=True,label='TRAIN')
test_data['begin'].plot(legend=True,label='TEST',figsize=(15,6))
# predictions_simpleExpSmooth_model.plot(legend=True,label='Simple Exponential Forecast')
# predictions_doubleExpSmooth_model.plot(legend=True,label='Double Exponential Forecast')
# predictions_tripleExpSmooth_model.plot(legend=True,label='Triple Exponential Forecast')


print('Simple Exponential Smoothing RMSE: {:.4f}'.format(np.sqrt(mean_squared_error(test_data,predictions_simpleExpSmooth_model))))
print('Double Exponential Smoothing RMSE: {:.4f}'.format(np.sqrt(mean_squared_error(test_data,predictions_doubleExpSmooth_model))))
print('Triple Exponential Smoothing RMSE: {:.4f}'.format(np.sqrt(mean_squared_error(test_data,predictions_tripleExpSmooth_model))))

test_data.std()


model = ExponentialSmoothing(new_df['begin'],trend='add',seasonal='add',seasonal_periods=12)
results = model.fit()
fcast = results.predict(len(new_df),len(new_df)+12).rename('Triple Exponential Forecast')

fcast.head()


next_fcast_begintim = fcast.loc[today(), ['begin']]
next_fcast_lenght = fcast.loc[today(), ['lenght']]


#do it again to trainign the lenght
#The code is using a fixed value for the span variable, but it is not clear what this value should be. A better approach would be to use cross-validation to determine the optimal value for this hyperparameter.

