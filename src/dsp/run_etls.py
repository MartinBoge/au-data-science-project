from etl.bronze_consumption import etl_bronze_consumption
from etl.bronze_prices import etl_bronze_prices
from etl.bronze_weather import etl_bronze_weather

from etl.silver_consumption import etl_silver_consumption
from etl.silver_prices import etl_silver_prices
from etl.silver_weather import etl_silver_weather

from etl.gold_cpw import etl_gold_cpw

# Bronze
etl_bronze_consumption()
etl_bronze_prices()
etl_bronze_weather()


# Silver
etl_silver_consumption()
etl_silver_prices()
etl_silver_weather()

# Gold
etl_gold_cpw()
