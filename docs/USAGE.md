# Usage notes — Customer Intelligence Labs project

This file shows basic commands to run the data cleaning and loading scripts locally on your machine. These commands assume you have the same local paths and MySQL instance used in the original project.

1) Clean the raw CSV and write cleaned CSV:

python scripts/customer_cleaner.py --input "WA_Fn-UseC_-Telco-Customer-Churn(in).csv" --output data/cleaned_customer.csv

2) Load cleaned data to the database table 'main1' (this script uses your existing hard-coded path):

python load.py

3) Load features to the 'customer_features' table (reads customer_features.csv or the cleaned CSV as available):

python Load_Features.py

4) Run the FastAPI app locally (from repo root):

uvicorn main:app --reload

- Use header x-api-key: Aniruddh when calling endpoints (this is the API_KEY in routers.py)

Notes:
- I did not change any DB connection strings or logging paths — scripts use the same settings as existing files.
- After cleaning you may want to re-create the DB tables if the ORM expects numeric columns for MonthlyCharges/TotalCharges.
