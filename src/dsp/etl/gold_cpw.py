import pandas as pd

from .utils import read_sql_table, upsert_df_to_sql_table


def etl_gold_cpw() -> None:
    print("Running ETL - gold_cpw - (consumption, prices, & weather)")

    # Extract
    df_consumption = read_sql_table("silver_consumption")
    df_prices = read_sql_table("silver_prices")
    df_weather = read_sql_table("silver_weather")

    # Transform - weather to prepare for merge
    df_weather = df_weather.rename(columns={"observed": "hour_utc"})
    df_weather = df_weather.pivot(
        index="hour_utc",
        columns="parameter_id",
        values="value",
    ).reset_index()

    # Transform - build dataset
    df_transformed = pd.merge(df_consumption, df_prices, on="hour_utc")
    df_transformed = pd.merge(df_transformed, df_weather, on="hour_utc")

    # Load
    upsert_df_to_sql_table("gold_cpw", df_transformed)
