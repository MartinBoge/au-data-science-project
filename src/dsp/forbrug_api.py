import requests
import sqlite3

# Unlike other API's where params can be specified in addition to the URL
# The documentation for Energinets API emply that all parameters are specified in the URL.


def main() -> None:
    # Step 1: Connect to database
    # see documentation for sqlite3 here:
    # https://docs.python.org/3/library/sqlite3.html
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # Step 2: Ensure table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS forbrug(
            hour_utc,
            hour_dk,
            municipality_no,
            housing_category,
            heating_category,
            consumption_kwh
        )
    """)

    con.commit()

    # Params:
    # dataset/PrivIndustryConsumptionHour --> From which database we want to retrive data
    # offset=0&start=2024-01-01T00:00  --> Using offset, we define start as first of januar at 0 o'clock danish time
    # end=2024-03-31T00:00  --> Enddate is the last hour of the 31 marts
    # filter=%7B%22MunicipalityNo%22:[%22751%22]%7D --> We only get data from Århus
    # sort=HourDK%20ASC') --> Data i ordered by the our Danish time.
    response = requests.get(
        url="https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?offset=0&start=2024-01-01T00:00&end=2024-03-31T00:00&filter=%7B%22MunicipalityNo%22:[%22751%22]%7D&sort=HourDK%20ASC"
    )

    # We interpret the json repsonse and save it as "result"
    result = response.json()

    for obj in result.get("records"):
        hour_utc = obj["HourUTC"]
        hour_dk = obj["HourDK"]
        municipality_no = obj["MunicipalityNo"]
        housing_category = obj["HousingCategory"]
        heating_category = obj["HeatingCategory"]
        consumption_kwh = obj["ConsumptionkWh"]
        con = sqlite3.connect("database.db")
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO forbrug VALUES
                (?, ?, ?, ?, ?, ?)
        """,
            (
                hour_utc,
                hour_dk,
                municipality_no,
                housing_category,
                heating_category,
                consumption_kwh,
            ),
        )
        con.commit()


if __name__ == "__main__":
    main()
