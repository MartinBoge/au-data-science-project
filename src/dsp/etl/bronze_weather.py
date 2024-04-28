import os
from collections import defaultdict
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from .utils import upsert_df_to_sql_table


def etl_bronze_weather(
    start_date: str,
    end_date: str,
) -> None:
    print("Running ETL - bronze_weather")
    # API spec: https://opendatadocs.dmi.govcloud.dk/en/APIs/Meteorological_Observation_API
    dmi_api_url = "https://dmigw.govcloud.dk/v2/metObs/collections/observation/items"

    load_dotenv()
    api_key = os.environ.get("DMI_API_KEY")

    station_id = "06074"
    limit = 300_000

    parameters = {
        "api-key": api_key,
        "limit": limit,
        "datetime": f"{start_date}T00:00:00Z/{end_date}T00:00:00Z",
        "stationId": station_id,
    }

    response = requests.get(url=dmi_api_url, params=parameters)

    if response.status_code != 200:
        print(response.json()["message"])
        raise Exception(
            f"DMI API - responded with status code {response.status_code}. Message: {response.json()['message']}"
        )

    data = defaultdict(list)

    features = response.json()["features"]

    if len(features) == limit:
        raise Exception(
            "The request limit of 300000 observations for the DMI API was reached."
        )

    for feature in features:
        properties = feature["properties"]

        observed = datetime.strptime(
            properties["observed"], "%Y-%m-%dT%H:%M:%SZ"
        ).isoformat()
        parameter_id = properties["parameterId"]
        station_id = properties["stationId"]
        value = properties["value"]

        data["observed"].append(observed)
        data["parameter_id"].append(parameter_id)
        data["station_id"].append(station_id)
        data["value"].append(value)

    df_api = pd.DataFrame(data)

    upsert_df_to_sql_table("bronze_weather", df_api)
