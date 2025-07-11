import random
import time
from datetime import datetime

def get_live_price(symbol):
    """
    Dummy function to get live price for a stock symbol
    Returns mock price data
    """
    # Simulate some processing time
    time.sleep(0.1)
    
    # Mock price data based on symbol
    base_prices = {
        'RELIANCE': 2500.00,
        'TCS': 3200.00,
        'INFY': 1450.00,
        'HDFCBANK': 1650.00,
        'ICICIBANK': 950.00,
        'SBIN': 580.00,
        'ITC': 420.00,
        'HINDUNILVR': 2300.00,
        'BHARTIARTL': 850.00,
        'KOTAKBANK': 1800.00,
        'NIFTY50': 19500.00,
        'SENSEX': 65000.00
    }
    
    # Get base price or use a random price if symbol not found
    base_price = base_prices.get(symbol.upper(), random.uniform(100, 3000))
    
    # Add some random fluctuation (+/- 2%)
    fluctuation = random.uniform(-0.02, 0.02)
    current_price = base_price * (1 + fluctuation)
    
    # Calculate change
    change = current_price - base_price
    change_percent = (change / base_price) * 100
    
    return {
        'symbol': symbol.upper(),
        'price': round(current_price, 2),
        'change': round(change, 2),
        'change_percent': round(change_percent, 2),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def get_portfolio_data():
    """
    Dummy function to get portfolio data
    """
    stocks = ['RELIANCE', 'TCS', 'INFY', 'HDFCBANK', 'ICICIBANK']
    portfolio = []
    
    for stock in stocks:
        price_data = get_live_price(stock)
        portfolio.append({
            'symbol': stock,
            'quantity': random.randint(10, 100),
            'avg_price': round(price_data['price'] * random.uniform(0.8, 1.2), 2),
            'current_price': price_data['price'],
            'change': price_data['change'],
            'change_percent': price_data['change_percent']
        })
    
    return portfolio

def get_market_data():
    """
    Dummy function to get market indices data
    """
    return {
        'NIFTY50': get_live_price('NIFTY50'),
        'SENSEX': get_live_price('SENSEX')
    }

def authenticate():
    """
    Dummy authentication function
    """
    return {
        'status': 'success',
        'message': 'Connected to mock API',
        'session_id': 'mock_session_' + str(int(time.time()))
    }

# You can add more functions as needed
def get_holdings():
    """
    Dummy holdings data
    """
    return get_portfolio_data()

def place_order(symbol, quantity, order_type='BUY'):
    """
    Dummy order placement function
    """
    return {
        'status': 'success',
        'order_id': f'ORD_{int(time.time())}',
        'symbol': symbol,
        'quantity': quantity,
        'order_type': order_type,
        'message': f'Mock order placed for {quantity} shares of {symbol}'
    }