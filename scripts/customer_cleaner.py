from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np

class CustomerCleaner:
    """
    Minimal reusable cleaner for the Telco churn dataset.

    Usage:
      cleaner = CustomerCleaner.from_csv("WA_Fn-UseC_-Telco-Customer-Churn(in).csv")
      df = cleaner.clean()
      cleaner.to_csv("data/cleaned_customers.csv")
    """

    DEFAULT_COLS = [
        "customerID", "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
        "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
        "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
        "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
        "MonthlyCharges", "TotalCharges", "Churn"
    ]

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    @staticmethod
    def from_csv(path: str, encoding: Optional[str] = None) -> "CustomerCleaner":
        df = pd.read_csv(path, encoding=encoding)
        return CustomerCleaner(df)

    def _standardize_column_names(self):
        # Trim and normalize column names
        col_map = {c: c.strip() for c in self.df.columns}
        self.df.rename(columns=col_map, inplace=True)

    def _coerce_numeric(self):
        # Convert MonthlyCharges & TotalCharges to floats, coerce errors to NaN
        for c in ["MonthlyCharges", "TotalCharges"]:
            if c in self.df.columns:
                self.df[c] = pd.to_numeric(self.df[c], errors="coerce")

    def _fill_total_charges(self):
        # If TotalCharges is missing or zero-like, set to MonthlyCharges * tenure where appropriate
        if "TotalCharges" in self.df.columns and "MonthlyCharges" in self.df.columns and "tenure" in self.df.columns:
            # Replace blank strings or NaN already coerced above
            # If tenure==0 and TotalCharges is NaN -> set to MonthlyCharges (or 0)
            mask_zero_tenure = (self.df["tenure"] == 0) & (self.df["TotalCharges"].isna())
            self.df.loc[mask_zero_tenure, "TotalCharges"] = self.df.loc[mask_zero_tenure, "MonthlyCharges"].fillna(0)
            # For other rows missing TotalCharges, approximate by MonthlyCharges * tenure
            mask = self.df["TotalCharges"].isna()
            self.df.loc[mask, "TotalCharges"] = (self.df.loc[mask, "MonthlyCharges"].fillna(0)
                                                  * self.df.loc[mask, "tenure"].fillna(0))

    def _derive_features(self):
        # churn_flag: 1 if Churn == "Yes"
        if "Churn" in self.df.columns:
            self.df["churn_flag"] = self.df["Churn"].apply(lambda x: 1 if str(x).strip().lower() == "yes" else 0)
        # service_count: simple count of positive services
        services = ["PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
                    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
        for s in services:
            if s in self.df.columns:
                # treat 'Yes' as 1, others as 0
                self.df[s + "_flag"] = self.df[s].apply(lambda v: 1 if str(v).strip().lower() == "yes" else 0)
        existing_flags = [c for c in self.df.columns if c.endswith("_flag")]
        if existing_flags:
            self.df["service_count"] = self.df[existing_flags].sum(axis=1).astype(int)
        # tenure_bucket example
        if "tenure" in self.df.columns:
            bins = [-1, 6, 12, 24, 48, 9999]
            labels = ["0-6", "7-12", "13-24", "25-48", "48+"]
            self.df["tenure_bucket"] = pd.cut(self.df["tenure"].fillna(0), bins=bins, labels=labels)

    def _drop_unused_columns(self):
        # keep only DEFAULT_COLS + derived columns
        keep = set(self.DEFAULT_COLS)
        derived = {"churn_flag", "service_count", "tenure_bucket"}
        keep |= derived
        keep_cols = [c for c in self.df.columns if c in keep or c.endswith("_flag")]
        self.df = self.df[keep_cols]

    def clean(self) -> pd.DataFrame:
        self._standardize_column_names()
        self._coerce_numeric()
        self._fill_total_charges()
        self._derive_features()
        self._drop_unused_columns()
        return self.df

    def to_csv(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(path, index=False)

    def to_sql(self, engine, table_name="main1", if_exists="replace"):
        # uses pandas to_sql; index=False to match ORM expectations
        self.df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="raw CSV path")
    parser.add_argument("--output", default="data/cleaned_customer.csv", help="cleaned CSV path")
    args = parser.parse_args()
    cleaner = CustomerCleaner.from_csv(args.input)
    df = cleaner.clean()
    cleaner.to_csv(args.output)
    print(f"Wrote cleaned data to {args.output}")
