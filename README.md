# au-data-science-project

## Developer notes

### Requirements

- python >= 3.11

### Virtual environment

To setup local development environment:

1. Ensure python version: `python -V`.
2. Setup virtual env: `python -m venv .venv`.
3. Open a new terminal and run `pip install -r requirements.txt`.

### Workflow - how to add a feature

1. Open Fork
2. Checkout main (double click the main branch)
3. Pull
4. Create a branch
5. Checkout the new branch (double click on the branch on the left-hand side)
6. Open VS Code and write your code
7. When done coding, open Fork and go into the all commits section (left-hand side)
8. Stage all the files that you wish to commit
9. Commit
10. Push
11. Open Github and create pull request
12. Merge pull request

### Running ETLs

To run ETLs:

1. Ensure you have created a file called ".env" file in the root of the project. This file can also be refered to as the dotenv file. This file is under gitignore, thus you can safely put any secrets or api keys in here.
2. Ensure that the dotenv file contains a line specifying your DMI API key like so: `DMI_API_KEY=###` - that is of course with your actual key instead of `###`. To see how the code reads this key have a look at the `bronze_weather.py` file inside the `etl` directory - in here we use the function `load_dotenv()`, which sets all of the variables from the dotenv file as environment variables. Then we're then able to call `os.environ.get("DMI_API_KEY")` to grab the key.
3. Ensure that you have all requirements (dependencies) installed in your virtual environment: `pip install -r requirements.txt`.
4. Now you can run: `python src/dsp/run_etls.py`. Note that inside the `run_etls.py` file you can specify the date ranges in which you wish to extract data for.
5. See the file `src/dsp/example_select.py` on how to read a table from SQLite to a Pandas dataframe.

Note that running the ETLs populate the following tables in the SQLite db:

- bronze_consumption
- bronze_prices
- bronze_weather
- silver_consumption
- silver_prices
- silver_weather
- gold_cpw (consumption, prices, and weather data all in one dataset)

### Running the application
1. Ensure you have streamlit installed. You can install streamlit writing `pip install streamlit` in your terminal.
2. Ensure that you have all requirements (dependencies) installed in your virtual environment: `pip install -r requirements.txt`.
3. Run the application `streamlit run src\dsp\etl\application.py`