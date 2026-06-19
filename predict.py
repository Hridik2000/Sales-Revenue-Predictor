import pandas as pd
import numpy as np
import joblib

model = joblib.load("model/final_model.pkl")
feature_ranges = joblib.load("model/feature_ranges.pkl")


def predict_revenue(data):

    df = pd.DataFrame([{
        "Sales Quantity": data.Sales_Quantity,
        "Customers": data.Customers,
        "Margin": data.Margin,
        "Margin Goal": data.Margin_Goal,
        "Revenue Goal": data.Revenue_Goal,
        "Date": data.Date,
        "Department": data.Department,
        "Seller": data.Seller
    }])

    limits = {
        "Revenue Goal": (
            feature_ranges["Revenue Goal"]["min"],
            feature_ranges["Revenue Goal"]["max"]
        ),
        "Sales Quantity": (
            feature_ranges["Sales Quantity"]["min"],
            feature_ranges["Sales Quantity"]["max"]
        ),
        "Customers": (
            feature_ranges["Customers"]["min"],
            feature_ranges["Customers"]["max"]
        ),
        "Margin": (
            feature_ranges["Margin"]["min"],
            feature_ranges["Margin"]["max"]
        ),
        "Margin Goal": (
            feature_ranges["Margin Goal"]["min"],
            feature_ranges["Margin Goal"]["max"]
        )
    }

    for col, (low, high) in limits.items():
        value = df[col].iloc[0]

        if value < low or value > high:
            raise ValueError(
                f"{col} outside training range [{low}, {high}]"
            )

    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = df["Date"].dt.month
    df["DayOfWeek"] = df["Date"].dt.dayofweek
    df["Quarter"] = df["Date"].dt.quarter

    df = df.drop(columns=["Date"])

    pred = model.predict(df)

    revenue = np.expm1(pred)

    return float(revenue[0])
