import json
from collections import defaultdict
from datetime import datetime

import pandas as pd
import requests

from .utils import upsert_df_to_sql_table


def etl_bronze_consumption(
    start_date: str,
    end_date: str,
) -> None:
    print("Running ETL - bronze_consumption")
    # API spec: https://www.energidataservice.dk/guides/api-guides
    # Dataset: https://www.energidataservice.dk/tso-electricity/PrivIndustryConsumptionHour
    energi_data_service_api_url = (
        "https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour"
    )

    parameters = {
        "start": start_date,
        "end": end_date,
        "filter": json.dumps(
            {
                "MunicipalityNo": ["751"],  # Aarhus is 751
            }
        ),
    }

    response = requests.get(url=energi_data_service_api_url, params=parameters)

    if response.status_code != 200:
        raise Exception(
            f"Energi Data Service API - responded with status code {
                response.status_code}"
        )

    data = defaultdict(list)

    for data_point in response.json()["records"]:
        hour_utc = datetime.strptime(
            data_point["HourUTC"], "%Y-%m-%dT%H:%M:%S"
        ).isoformat()
        hour_dk = datetime.strptime(
            data_point["HourDK"], "%Y-%m-%dT%H:%M:%S"
        ).isoformat()
        municipality_no = str(data_point["MunicipalityNo"])
        housing_category = str(data_point["HousingCategory"])
        heating_category = str(data_point["HeatingCategory"])
        consumption_kwh = float(data_point["ConsumptionkWh"])

        data["hour_utc"].append(hour_utc)
        data["hour_dk"].append(hour_dk)
        data["municipality_no"].append(municipality_no)
        data["housing_category"].append(housing_category)
        data["heating_category"].append(heating_category)
        data["consumption_kwh"].append(consumption_kwh)

    df_api = pd.DataFrame(data)

    upsert_df_to_sql_table("bronze_consumption", df_api)
