# core/portfolio.py

def get_user_holdings():
    # This will eventually query DB
    return {
        "RELIANCE": {"quantity": 10, "avg_price": 2600},
        "TCS": {"quantity": 5, "avg_price": 3500},
        "HDFCBANK": {"quantity": 15, "avg_price": 1550}
    }

def calculate_portfolio_metrics():
    # You can put aggregated return calculations here if needed
    pass
