import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import time

# Page configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-container {
        background-color: #566cba;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .positive { color: #00C851; }
    .negative { color: #ff4444; }
    .stSelectbox > div > div > div > div { background-color: #7a1515; }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📈 Indian Stock Market Dashboard")
st.markdown("Real-time stock prices and candlestick charts")

# Indian market indices with their Yahoo Finance symbols
INDIAN_INDICES = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN", 
    "BANK NIFTY": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY AUTO": "^CNXAUTO"
}

def get_stock_data(symbol, period="1d", interval="5m"):
    """Fetch stock data using yfinance"""
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period=period, interval=interval)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def get_current_price(symbol):
    """Get current price and change"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        current_price = info.get('currentPrice', 0)
        previous_close = info.get('previousClose', 0)
        
        if current_price == 0:
            # Fallback to recent data
            data = stock.history(period="2d", interval="1d")
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                previous_close = data['Close'].iloc[-2] if len(data) > 1 else current_price
        
        change = current_price - previous_close
        change_percent = (change / previous_close) * 100 if previous_close != 0 else 0
        
        return current_price, change, change_percent
    except Exception as e:
        st.error(f"Error getting current price for {symbol}: {str(e)}")
        return 0, 0, 0

def format_price_display(price, change, change_percent):
    """Format price display with colors"""
    color = "positive" if change >= 0 else "negative"
    arrow = "↑" if change >= 0 else "↓"
    sign = "+" if change >= 0 else ""
    
    return f"""
    <div class="metric-container">
        <h3>₹{price:.2f}</h3>
        <p class="{color}">
            {arrow} {sign}{change:.2f} ({sign}{change_percent:.2f}%)
        </p>
    </div>
    """

def create_candlestick_chart(data, title):
    """Create candlestick chart using Plotly"""
    if data is None or data.empty:
        return None
    
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=[title, 'Volume'],
        row_width=[0.7, 0.3]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Price"
        ),
        row=1, col=1
    )
    
    # Volume chart
    colors = ['red' if close < open else 'green' 
             for close, open in zip(data['Close'], data['Open'])]
    
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name="Volume",
            marker_color=colors,
            opacity=0.7
        ),
        row=2, col=1
    )
    
    fig.update_layout(
        title=title,
        yaxis_title="Price (₹)",
        yaxis2_title="Volume",
        xaxis_rangeslider_visible=False,
        height=600,
        showlegend=False
    )
    
    return fig

# Sidebar for settings
st.sidebar.header("Settings")
auto_refresh = st.sidebar.checkbox("Auto Refresh (30s)", value=False)
time_period = st.sidebar.selectbox(
    "Chart Time Period",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y"],
    index=0
)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔍 Stock Search")
    
    # Search input
    search_symbol = st.text_input(
        "Enter stock symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS)",
        placeholder="Type stock symbol..."
    )
    
    if search_symbol:
        # Clean the symbol
        symbol = search_symbol.upper().strip()
        if not symbol.endswith('.NS') and not symbol.endswith('.BO'):
            symbol += '.NS'  # Default to NSE
        
        st.subheader(f"📊 {symbol}")
        
        # Get current price
        current_price, change, change_percent = get_current_price(symbol)
        
        if current_price > 0:
            # Display current price
            st.markdown(
                format_price_display(current_price, change, change_percent),
                unsafe_allow_html=True
            )
            
            # Get historical data for chart
            chart_data = get_stock_data(symbol, period=time_period, interval="1h" if time_period == "1d" else "1d")
            
            if chart_data is not None and not chart_data.empty:
                # Create and display candlestick chart
                fig = create_candlestick_chart(chart_data, f"{symbol} - {time_period.upper()}")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No chart data available for this symbol")
        else:
            st.error("Invalid symbol or no data available")

with col2:
    st.header("📈 Indian Market Indices")
    
    # Display indices in a container
    indices_container = st.container()
    
    with indices_container:
        for index_name, symbol in INDIAN_INDICES.items():
            with st.expander(f"{index_name}", expanded=True):
                current_price, change, change_percent = get_current_price(symbol)
                
                if current_price > 0:
                    st.markdown(
                        format_price_display(current_price, change, change_percent),
                        unsafe_allow_html=True
                    )
                else:
                    st.warning(f"Data not available for {index_name}")

# Auto refresh functionality
if auto_refresh:
    time.sleep(30)
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
**Instructions:**
- For NSE stocks, use format: `RELIANCE.NS`, `TCS.NS`, `HDFCBANK.NS`
- For BSE stocks, use format: `RELIANCE.BO`, `TCS.BO`
- Popular stocks: RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, ICICIBANK.NS, ADANIPORTS.NS
- Data is fetched from Yahoo Finance with ~15-20 minute delay
""")

st.markdown("*Last updated: {}*".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))