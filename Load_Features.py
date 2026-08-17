import pandas as pd
from sqlalchemy import create_engine
from scripts.customer_cleaner import CustomerCleaner

# Use the original file location if available; otherwise this script can be adjusted to point elsewhere
raw_csv = r"C:/Users/aniruddh.singh/OneDrive - Prodapt Solutions Private Limited/Documents/Project_prac/customer_features.csv"

# If you want to regenerate features from the raw churn CSV, uncomment and point to the raw CSV
# from scripts.customer_cleaner import CustomerCleaner
# cleaner = CustomerCleaner.from_csv(<raw_csv_path>)
# df = cleaner.clean()

# Otherwise try to read the provided customer_features.csv
try:
    df = pd.read_csv(raw_csv)
except FileNotFoundError:
    raise

# Ensure TotalCharges numeric
if "TotalCharges" in df.columns:
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# SQL Server connection (left unchanged)
engine = create_engine(
    'mysql+pymysql://root:root@localhost:3306/project1'
)

# Load data into 'customer_features' table
df.to_sql(
    "customer_features",
    con=engine,
    if_exists="replace",   # use "append" if table already exists
    index=False
)

print("Data loaded successfully")
