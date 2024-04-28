import json
from collections import defaultdict
from datetime import datetime

import pandas as pd
import requests

from .utils import upsert_df_to_sql_table


def etl_bronze_prices(
    start_date: str,
    end_date: str,
) -> None:
    print("Running ETL - bronze_prices")
    # API spec: https://www.energidataservice.dk/guides/api-guides
    # Dataset: https://www.energidataservice.dk/tso-electricity/PrivIndustryConsumptionHour
    energi_data_service_api_url = (
        "https://api.energidataservice.dk/dataset/Elspotprices"
    )

    parameters = {
        "start": start_date,
        "end": end_date,
        "filter": json.dumps(
            {
                "PriceArea": ["DK1"],  # Aarhus is in area DK1
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
        price_area = str(data_point["PriceArea"])
        spot_price_dkk = str(data_point["SpotPriceDKK"])
        spot_price_eur = str(data_point["SpotPriceEUR"])

        data["hour_utc"].append(hour_utc)
        data["hour_dk"].append(hour_dk)
        data["price_area"].append(price_area)
        data["spot_price_dkk"].append(spot_price_dkk)
        data["spot_price_eur"].append(spot_price_eur)

    df_api = pd.DataFrame(data)

    upsert_df_to_sql_table("bronze_prices", df_api)
