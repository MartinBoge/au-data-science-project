from dotenv import load_dotenv
from .utils import upsert_df_to_sql_table
from datetime import datetime
from collections import defaultdict
import pandas as pd
import os
import requests


def etl_bronze_weather() -> None:
    print("Running ETL - bronze_weather")
    # API spec: https://opendatadocs.dmi.govcloud.dk/en/APIs/Meteorological_Observation_API
    dmi_api_url = "https://dmigw.govcloud.dk/v2/metObs/collections/observation/items"

    load_dotenv()
    api_key = os.environ.get("DMI_API_KEY")

    from_date = "2024-02-01"
    to_date = "2024-02-01"

    station_id = "06074"

    parameters = {
        "api-key": api_key,
        "datetime": f"{from_date}T00:00:00Z/{to_date}T06:00:00Z",
        "stationId": station_id,
    }

    response = requests.get(url=dmi_api_url, params=parameters)

    if response.status_code != 200:
        print(response.json()["message"])
        raise Exception(
            f"DMI API - responded with status code {
                response.status_code}. Message: {response.json()['message']}"
        )

    data = defaultdict(list)

    for feature in response.json()["features"]:
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
