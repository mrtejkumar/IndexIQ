# core/trading.py

import pandas as pd
import random
from datetime import datetime

# Simulated storage (to be replaced with DB in real app)
holdings = {}
trade_history = []

def place_order(symbol, action, quantity, price):
    global holdings, trade_history

    if action == "Buy":
        if symbol in holdings:
            holdings[symbol]["quantity"] += quantity
            holdings[symbol]["avg_price"] = (
                (holdings[symbol]["avg_price"] * holdings[symbol]["quantity"] + price * quantity) /
                (holdings[symbol]["quantity"] + quantity)
            )
        else:
            holdings[symbol] = {"quantity": quantity, "avg_price": price}
    elif action == "Sell":
        if symbol not in holdings or holdings[symbol]["quantity"] < quantity:
            return f"❌ Not enough shares of {symbol} to sell"
        holdings[symbol]["quantity"] -= quantity
        if holdings[symbol]["quantity"] == 0:
            del holdings[symbol]

    # Add to trade history
    trade_history.append({
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Symbol": symbol,
        "Action": action,
        "Qty": quantity,
        "Price": price
    })

    return f"✅ {action} order for {quantity} shares of {symbol} at ₹{price} executed."

def get_holdings():
    data = []
    for symbol, details in holdings.items():
        data.append({
            "Symbol": symbol,
            "Quantity": details["quantity"],
            "Avg Buy Price (₹)": round(details["avg_price"], 2),
            "Current Price (₹)": round(details["avg_price"] * random.uniform(0.95, 1.05), 2),  # Mock
        })
    return pd.DataFrame(data)

def get_trade_history():
    return pd.DataFrame(trade_history[::-1])  # Most recent first
