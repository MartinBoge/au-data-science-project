# At first we import the libraries installed in our requirements.txt

import requests
import pandas as pd

# Unlike other API's where params can be specified in addition to the URL
# The documentation for Energinets API emply that all parameters are specified in the URL.

response = requests.get(
    url="https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?offset=0&start=2024-01-01T00:00&end=2024-03-31T00:00&filter=%7B%22MunicipalityNo%22:[%22751%22]%7D&sort=HourDK%20ASC"
)


# Params:
# dataset/PrivIndustryConsumptionHour --> From which database we want to retrive data
# offset=0&start=2024-01-01T00:00  --> Using offset, we define start as first of januar at 0 o'clock danish time
# end=2024-03-31T00:00  --> Enddate is the last hour of the 31 marts
# filter=%7B%22MunicipalityNo%22:[%22751%22]%7D --> We only get data from Århus
# sort=HourDK%20ASC') --> Data i ordered by the our Danish time.

# We interpret the json repsonse and save it as "result"
result = response.json()

# Extract records
records = result.get("records", [])

# Save our data in a DataFrame
df = pd.DataFrame(records)

# Write DataFrame to Excel
df.to_excel("data.xlsx", index=False)