# core/sentiment.py

import random
import pandas as pd
from datetime import datetime, timedelta

def get_overall_sentiment():
    score = random.randint(40, 80)
    label = "Bullish" if score >= 60 else "Bearish" if score <= 45 else "Neutral"
    return score, label

def get_sentiment_trends():
    today = datetime.now()
    return pd.DataFrame({
        "Date": [today - timedelta(days=i) for i in range(7)][::-1],
        "Sentiment Score": [random.randint(40, 80) for _ in range(7)]
    })

def get_trending_keywords():
    return ["Nifty", "Buyback", "Bullish", "Support", "Breakout", "RBI", "Inflation"]
