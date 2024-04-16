
# At first we import the libraries installed in our requirements.txt

import requests
import pandas

# Unlike other API's where params can be specified in addition to the URL
# The documentation for Energinets API emply that all parameters are specified in the URL.

response = requests.get(
    url='https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?offset=0&start=2024-01-01T00:00&end=2024-03-31T00:00&filter=%7B%22MunicipalityNo%22:[%22751%22]%7D&sort=HourDK%20ASC')


# Params:
# dataset/PrivIndustryConsumptionHour --> From which database we want to retrive data
# offset=0&start=2024-01-01T00:00  --> Using offset, we define start as first of januar at 0 o'clock danish time
# end=2024-03-31T00:00  --> Enddate is the last hour of the 31 marts
# filter=%7B%22MunicipalityNo%22:[%22751%22]%7D --> We only get data from Århus
# sort=HourDK%20ASC') --> Data i ordered by the our Danish time.

# We interpret the json repsonse and save it as "result"
result = response.json()

# Extract records
records = result.get('records', [])

# Save our data in a DataFrame
df = pd.DataFrame(records)



# Inspecting the Dataframe, we can tell that we still have data regarding "erhverv".
# We have however limited our scope to private consumption, we will exclude observation where Heating- or Housingcategory = "erhverv"
print(df)

# Deleting erhverv:
filtered_df = df[(df['HousingCategory'] != 'Erhverv') & (df['HeatingCategory'] != 'Erhverv')]

# Checking that there is no erhverv left.
print(filtered_df)


# As we do not care whether private consumption is for heating or general consumption.
# We sum all consumption irespectable of the category.

# Group by HourDK and sum the ConsumptionkWh
total_consumption = df.groupby('HourDK')['ConsumptionkWh'].sum().reset_index()

# Display the resulting DataFrame
print(total_consumption)

# As we want to use the time of day as a predictor, we extract this.

# Convert HourDK to datetime if it's not already in datetime format
total_consumption['HourDK'] = pd.to_datetime(total_consumption['HourDK'])

# Extract the hour from the HourDK column
total_consumption['Hour'] = total_consumption['HourDK'].dt.hour

# Display the resulting DataFrame
print(total_consumption)


# Once again we use the API from Energinet to get the reel spotprices

response = requests.get(
    url='https://api.energidataservice.dk/dataset/Elspotprices?offset=0&start=2024-01-01T00:00&end=2024-03-31T00:00&filter=%7B%22PriceArea%22:[%22DK1%22]%7D&sort=HourDK%20ASC')


# Params:
# dataset/PrivIndustryConsumptionHour --> From which database we want to retrive data
# offset=0&start=2024-01-01T00:00  --> Using offset, we define start as first of januar at 0 o'clock danish time
# end=2024-03-31T00:00  --> Enddate is the last hour of the 31 marts
# filter=%7B%22PriceArea%22:[%22DK1%22]%7D&sort=HourDK%20ASC') --> we only get DK1 prices
# sort=HourDK%20ASC') --> Data i ordered by the our Danish time.

# We interpret the json repsonse and save it as "result"
result = response.json()

# Extract records
records = result.get('records', [])

# Save our data in a DataFrame
df = pd.DataFrame(records)

# Inspect data
print(df)


# We now merge the collum SpotPriceDKK into the consumption dataframe

# Convert HourDK column in the df DataFrame to datetime format
df['HourDK'] = pd.to_datetime(df['HourDK'])

# Merge the DataFrames based on the 'HourDK' column
merged_df = pd.merge(total_consumption, df[['HourDK', 'SpotPriceDKK']], on='HourDK', how='left')

# Display the resulting DataFrame
print(merged_df)


# API for Lukas data.

import requests
import pandas as pd

# Save API key
DMI_URL = 'https://dmigw.govcloud.dk/v2/metObs/collections/observation/items'
api_key = '479e3248-d629-4b80-85de-b7ab638b59e8'
stationId = '06074'
parameterId = ['temp_mean_past1h', 'humidity_past1h', 'wind_speed_past1h', 'sun_last1h_glob', 'precip_past1h']

from_date = '2024-01-01'
to_date = '2024-03-31'

datetimeId = f'{from_date}T00:00:00/{to_date}T00:00:00'

parameter_ids = ['temp_mean_past1h', 'humidity_past1h', 'wind_speed_past1h', 'sun_last1h_glob', 'precip_past1h']

for param_id in parameter_ids:
  response = requests.get(DMI_URL, params={'api-key': api_key, "stationId": '06074', 'parameterId': param_id, 'datetime': '2024-01-01T00:00:00Z/2024-03-31T00:00:00Z'})
  print(response)
  result = response.json()
  for feature in result['features']:
    print(feature)


