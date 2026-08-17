import pandas as pd
from scripts.customer_cleaner import CustomerCleaner

def test_totalcharges_and_flags():
    # create a tiny dataframe with edge cases
    df = pd.DataFrame([
        {"customerID": "A", "tenure": 0, "MonthlyCharges": 29.85, "TotalCharges": " ", "Churn": "No", "PhoneService": "No", "MultipleLines": "No", "OnlineSecurity": "No", "OnlineBackup": "No", "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No", "StreamingMovies": "No"},
        {"customerID": "B", "tenure": 2, "MonthlyCharges": "53.85", "TotalCharges": "108.15", "Churn": "Yes", "PhoneService": "Yes", "MultipleLines": "No", "OnlineSecurity": "Yes", "OnlineBackup": "No", "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No", "StreamingMovies": "No"}
    ])

    cleaner = CustomerCleaner(df)
    out = cleaner.clean()

    # TotalCharges should be numeric and non-null
    assert out.loc[out['customerID']=='A','TotalCharges'].astype(float).notnull().all()
    assert out.loc[out['customerID']=='B','TotalCharges'].astype(float).notnull().all()

    # churn_flag should be 0 for A and 1 for B
    assert int(out.loc[out['customerID']=='A','churn_flag'].iloc[0]) == 0
    assert int(out.loc[out['customerID']=='B','churn_flag'].iloc[0]) == 1

    # service_count should be integer (B has PhoneService and OnlineSecurity => at least 2 flags)
    assert out.loc[out['customerID']=='B','service_count'].iloc[0] >= 1
