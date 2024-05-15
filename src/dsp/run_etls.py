from etl.bronze_consumption import etl_bronze_consumption
from etl.bronze_prices import etl_bronze_prices
from etl.bronze_weather import etl_bronze_weather
from etl.gold_cpw import etl_gold_cpw
from etl.silver_consumption import etl_silver_consumption
from etl.silver_prices import etl_silver_prices
from etl.silver_weather import etl_silver_weather


def etl():
    # Bronze
    start_date = "2024-01-01"
    end_date = "2024-04-30"

    etl_bronze_consumption(start_date, end_date)
    etl_bronze_prices(start_date, end_date)
    etl_bronze_weather(start_date, end_date)

    # Silver
    etl_silver_consumption()
    etl_silver_prices()
    etl_silver_weather()

    # Gold
    etl_gold_cpw()


if __name__ == "__main__":
    etl()
