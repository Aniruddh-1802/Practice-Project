import pandas as pd
from sql_connection import engine

df = pd.read_csv(r"C:\Users\aniruddh.singh\OneDrive - Prodapt Solutions Private Limited\Documents\Project_prac\WA_Fn-UseC_-Telco-Customer-Churn(in).csv")

df.to_sql(
    "Main1",
    con=engine,
    if_exists="append",
    index=False
)
