# au-data-science-project

This repo contain the source code for the course Data Science Project at Aarhus University.

The source code serves a streamlit application with a dashboard that power suppliers can use to produce their demand forecast.

## How to run the app

Requirements:

- Python >= 3.11

Steps:

1. Install dependencies (recommended to use a virtual environment, see guide below): `pip install -r requirements.txt`
2. Create a file in the root of the project and call it `.env` - this is used for environment variables
3. Open the `.env` file and write the following `DMI_API_KEY=XXX` and replace `XXX` with an actual API key for the DMI Weather API. An API key can be acquired by subscribing to the metObsAPI from DMI at: https://dmiapi.govcloud.dk/#!/apis/48ed0c1b-ab40-473a-ad0c-1bab40073a51/detail
4. In your terminal go to the directory `src/dsp` via: `cd src/dsp`
5. Run ETL flows via: `python run_etls.py`
6. Now you can run the streamlit app via: `streamlit run application.py`

Note that running the ETL flows populate the following tables in a local SQLite db (file):

- bronze_consumption
- bronze_prices
- bronze_weather
- silver_consumption
- silver_prices
- silver_weather
- gold_cpw (consumption, prices, and weather data all in one dataset)

### Guide (Windows) - Python virtual environment

Steps:

1. Open a terminal in the root of the project
2. Ensure you are on the correct version of Python via: `python -V`
3. Create virtual environment via: `python -m venv .venv`
4. Activate the virtual environment via: `source .venv/scripts/activate.ps1`. Note that you can skip this step in VS Code if you select your `.venv` as the Python interpreter and then open a new terminal.

### Guide (Mac/Linux) - Python virtual environment

Steps:

1. Open a terminal in the root of the project
2. Ensure you are on the correct version of Python via: `python3 -V` (you can also use a specific version of Python via `python3.11 -V`)
3. Create virtual environment via: `python3 -m venv .venv`
4. Activate the virtual environment via: `source .venv/bin/activate`. Note that you can skip this step in VS Code if you select your `.venv` as the Python interpreter and then open a new terminal.

