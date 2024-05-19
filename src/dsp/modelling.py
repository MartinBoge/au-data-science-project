#Script for modelling

#Libraries
import pandas as pd
import numpy as np
from etl.utils import read_sql_table
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import root_mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
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

#Converting spot price to float64
df['spot_price_dkk'] = df['spot_price_dkk'].astype('float64')

#Dummy encoding 'hour'
hour_dummies = pd.get_dummies(df['hour'], prefix='hour').astype('float64')

#Concatenate this with original dataframe
df = pd.concat([df, hour_dummies], axis=1)

#Drop hour
df = df.drop('hour', axis=1)

#print(df.head().to_string(), "\n")
#print(df.info())

##Splitting dataset
X = df.drop('consumption_kwh', axis=1)
y = df[['consumption_kwh']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)
#print(y_train)

####Linear Regression####
##Training and evaluating linear regression model without preprocessing
est = sm.OLS(y_train, sm.add_constant(X_train)) #model with constant
est_fit = est.fit()
#print(est_fit.summary()) #All but hour and precip_past1h are significant
#In a zero-intercept model, all but precip_past1h and spot_price_dkk are significant

#Linear regression with scaling
X_train_scale = StandardScaler().fit_transform(X_train)
est = sm.OLS(y_train, sm.add_constant(X_train_scale))
est_fit = est.fit()
#print(est_fit.summary())

###Prediction accuracy - linear regression
X_test_scale = StandardScaler().fit_transform(X_test)
y_pred_lm = est_fit.predict(sm.add_constant(X_test_scale))
rmse_lm = root_mean_squared_error(y_test, y_pred_lm)
#print(round(rmse_lm))

###Random Forest
#Documentation: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
rf_model = RandomForestRegressor(n_estimators = 200, bootstrap=True) #200 trees
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test) #Test
rmse_rf = root_mean_squared_error(y_test, y_pred_rf)
#print(round(rmse_rf))


###Support Vector Machines
#Documentation: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html
svm_model = SVR(kernel='linear', C=1000)
svm_model.fit(X_train, y_train) #Train
y_pred_svm = svm_model.predict(X_test) #Test
rmse_svm = root_mean_squared_error(y_test, y_pred_svm) #RMSE
#print(round(rmse_svm))

#Comparing models
rmse_values = [rmse_lm, rmse_rf, rmse_svm]
rmse_data = {'Model': ['Linear Model', 'Random Forrest', 'Support Vector Machine'],
            'RMSE': [round(value) for value in rmse_values]
    }

rmse_df = pd.DataFrame(rmse_data) #Make dataframe of RMSE data


###Linear model CV
# Define a pipeline with StandardScaler and LinearRegression
pipeline = make_pipeline(StandardScaler(), LinearRegression())

# Perform cross-validation
rmse_scores_lm = -cross_val_score(pipeline, X_train, y_train, cv=10, scoring='neg_root_mean_squared_error')

# Calculate mean and standard deviation of RMSE scores
mean_rmse_lm = np.mean(rmse_scores_lm)
std_rmse_lm = np.std(rmse_scores_lm)

# Print mean squared error from cross-validation
#print("Root Mean Squared Error (Cross-validation):", round(mean_rmse_lm))
#print("Standard Deviation of RMSE (Cross-validation):", round(std_rmse_lm))


###Random forest CV
rf_model = RandomForestRegressor(n_estimators=200, bootstrap=True)

#Cross-validation
rmse_scores_rf = -cross_val_score(rf_model, X, y, cv=10, scoring='neg_root_mean_squared_error')

# Calculate mean and standard deviation of RMSE scores
mean_rmse_rf = np.mean(rmse_scores_rf)
std_rmse_rf = np.std(rmse_scores_rf)

# Train model on full training data
rf_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_rf = rf_model.predict(X_test)

# Calculate rmse on the test set
rmse_rf = root_mean_squared_error(y_test, y_pred_rf)

# Print rmse from cv and on test set
#print("Root Mean Squared Error (Cross-validation):", round(mean_rmse_rf))
#print("Standard Deviation of RMSE (Cross-validation):", round(std_rmse_rf)) #Large variation in rmse scores.
#Suggests that the splits from the small dataset has large influence on performance.
#print("Root Mean Squared Error (Test set):", round(rmse_rf))


###Support Vector Machines CV
svm_model = SVR(C=1000)

#CV
rmse_scores_svm = -cross_val_score(svm_model, X, y, cv=10, scoring='neg_root_mean_squared_error')

#Calculate mean and standard deviation of RMSE scores
mean_rmse_svm = np.mean(rmse_scores_svm)
std_rmse_svm = np.std(rmse_scores_svm)


#Comparing CV models
mean_rmse_values = [mean_rmse_lm, mean_rmse_rf, mean_rmse_svm]
mean_std_values = [std_rmse_lm, std_rmse_rf, std_rmse_svm]
rmse_data = {'CV Model': ['Linear Model', 'Random Forrest', 'Support Vector Machine'],
            'Mean RMSE': [round(value) for value in mean_rmse_values],
            'Std': [round(value) for value in mean_std_values]
        }

rmse_df = pd.DataFrame(rmse_data) #Make dataframe of RMSE and std data