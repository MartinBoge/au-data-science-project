from .utils import read_sql_table, upsert_df_to_sql_table


def etl_silver_consumption() -> None:
    print("Running ETL - silver_consumption")

    df_bronze = read_sql_table("bronze_consumption")

    df_transformed = df_bronze.groupby("hour_utc").sum("consumption_kwh").reset_index()

    upsert_df_to_sql_table("silver_consumption", df_transformed)
