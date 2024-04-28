from .utils import read_sql_table, upsert_df_to_sql_table


def etl_silver_prices() -> None:
    print("Running ETL - silver_prices")

    df_bronze = read_sql_table("bronze_prices")

    df_transformed = df_bronze[["hour_utc", "spot_price_dkk", "spot_price_eur"]]

    upsert_df_to_sql_table("silver_prices", df_transformed)
