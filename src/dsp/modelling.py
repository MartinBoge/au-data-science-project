#Script for modelling

import pandas as pd
import numpy as np
from etl.utils import read_sql_table
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

df = read_sql_table("gold_cpw")

###Variable manipulation
# Convert HourDK to datetime if it's not already in datetime format
df['hour_utc'] = pd.to_datetime(df['hour_utc'])

# Extract the hour from the HourDK column
df['hour'] = df['hour_utc'].dt.hour

#Subsetting variables
df = df[['hour', 'consumption_kwh', 'spot_price_dkk', 'temp_mean_past1h', 'wind_speed_past1h',
    'humidity_past1h', 'precip_past1h']]
#Converting variables to float64
df['hour'] = df['hour'].astype('float64')
df['spot_price_dkk'] = df['spot_price_dkk'].astype('float64')

#print(df.head().to_string())
#print(df.info())

##Checking for missing values
#print(df.isna().any())
#No missing values


##Splitting dataset
X = df[['hour', 'spot_price_dkk', 'temp_mean_past1h', 'wind_speed_past1h', 'humidity_past1h', 'precip_past1h']]
y = df[['consumption_kwh']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
#print(X_train)

####Linear Regression####
##Training and evaluating linear regression model without preprocessing
est = sm.OLS(y_train, X_train)
est_fit = est.fit()
print(est_fit.summary()) #All but precip_past1h and spot_price_dkk are significant

##Training and evaluating linear regression model with scaling of price
#StandardScaler().fit_transform(X_train['spot_price_dkk'])
#print(X_train)

#est = sm.OLS(y_train, X_train)
#est_fit = est.fit()
#print(est_fit.summary()) #

