from etl.utils import read_sql_table

df = read_sql_table("gold_cpw")

print(df)
