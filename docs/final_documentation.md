# Final documentation for Customer Intelligence Labs - implemented steps

This file lists each lab step from the Customer Intelligence Labs PDF and where it is implemented in this repository. Phase 4 (React) has been intentionally skipped per project instructions.

1) Data ingestion & engineering
- Evidence: DataEngineering.ipynb, load.py, scripts/customer_cleaner.py
- Status: Implemented. I added scripts/customer_cleaner.py which standardizes and cleans the raw CSV and load.py now uses it to load cleaned data into the DB table 'main1'.

2) Data exploration & EDA
- Evidence: DataAnalyzing.ipynb, FeatureEngineering.ipynb
- Status: Implemented (notebook-based exploration present).

3) Feature engineering
- Evidence: FeatureEngineering.ipynb, Load_Features.py, customer_features.csv
- Status: Implemented. Load_Features.py was adjusted to read (or assume) cleaned features and load them to the 'customer_features' table.

4) Model development & evaluation
- Evidence: ML_prep.ipynb, UsingModel.ipynb, models/
- Status: Implemented in notebooks; models/ contains trained artifacts (pkl files). The API predict endpoint will attempt to load models from models/ (including .pkl files).

5) Model usage & API
- Evidence: main.py, routers.py
- Status: Implemented. routers.py now includes a model loader that scans models/ for common artifact names (.joblib/.pkl) and uses them for /predict_churn if available; otherwise falls back to the original stub.

6) React frontend
- Status: SKIPPED per instructions.

7) Documentation & tests
- Evidence: docs/USAGE.md, docs/final_documentation.md, tests/test_customer_cleaner.py
- Status: docs and a unit test for the new CustomerCleaner were added.

Notes & local actions required:
- ORM vs DB schema for MonthlyCharges/TotalCharges: I changed the SQLAlchemy ORM types to Float. If your local DB table was created with VARCHAR/Text for these columns, you'll need to re-import the table (drop and recreate) or ALTER the columns to numeric types locally.
- routers.py import: you previously asked to skip changing datetime import; that import remains as originally (it may cause import errors depending on Python environment). If you want me to fix it so the API runs, I can apply that fix.

If you'd like, I can open a PR from ci-lab/finalize to main containing these changes and a full diff; or I can apply additional small fixes per your direction.
