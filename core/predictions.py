# core/predictions.py

import pandas as pd
from datetime import datetime, timedelta
import random

def get_prediction_for_stock(symbol: str):
    today = datetime.today()
    
    # Mock historical
    historical = pd.DataFrame({
        "Date": [today - timedelta(days=i) for i in range(30)][::-1],
        "Price": [round(1000 + i + random.uniform(-10, 10), 2) for i in range(30)]
    })

    # Mock forecast
    forecast = pd.DataFrame({
        "Date": [today + timedelta(days=i) for i in range(1, 11)],
        "Forecast": [round(historical["Price"].iloc[-1] + i*5 + random.uniform(-5, 5), 2) for i in range(1, 11)]
    })

    return historical, forecast

def get_prediction_summary(symbol: str):
    return pd.DataFrame({
        "Metric": ["Next Day", "5-Day Avg", "10-Day Target"],
        "Forecast Price (₹)": [
            round(1050 + random.uniform(-10, 10), 2),
            round(1075 + random.uniform(-10, 10), 2),
            round(1100 + random.uniform(-10, 10), 2)
        ],
        "Confidence": ["High", "Medium", "Medium"]
    })
