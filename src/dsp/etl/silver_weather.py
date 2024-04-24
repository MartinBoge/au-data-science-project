from .utils import read_sql_table, upsert_df_to_sql_table


def etl_silver_weather() -> None:
    print("Running ETL - silver_weather")

    df_bronze = read_sql_table("bronze_weather")

    df_transformed = df_bronze[["observed", "parameter_id", "value"]]

    upsert_df_to_sql_table("silver_weather", df_transformed)
