import pandas as pd
from sqlalchemy import create_engine

# Read CSV
df = pd.read_csv("C:/Users/aniruddh.singh/OneDrive - Prodapt Solutions Private Limited/Documents/Project_prac/customer_features.csv")

# Handle blank TotalCharges values
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# SQL Server connection
engine = create_engine(
    'mysql+pymysql://root:root@localhost:3306/project1'
)

# Load data
df.to_sql(
    "customer_features",
    con=engine,
    if_exists="replace",   # use "append" if table already exists
    index=False
)

print("Data loaded successfully")