import pandas as pd
from sql_connection import engine
from scripts.customer_cleaner import CustomerCleaner

# Use the existing local CSV path (left as-is per repository's original behavior)
raw_path = r"C:\Users\aniruddh.singh\OneDrive - Prodapt Solutions Private Limited\Documents\Project_prac\WA_Fn-UseC_-Telco-Customer-Churn(in).csv"

# Create a cleaner instance and clean the data
cleaner = CustomerCleaner.from_csv(raw_path)
df = cleaner.clean()

# Write to DB table 'main1' to match ORM (lowercase)
df.to_sql(
    "main1",
    con=engine,
    if_exists="append",
    index=False
)

print("Data loaded successfully to table 'main1'")
