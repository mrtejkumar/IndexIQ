# indexiq_screener.py
import streamlit as st
import pandas as pd
import random

# -------------------------
# Mock Stock Data (Replace with live data as needed)
# -------------------------
@st.cache_data
def load_stock_data():
    symbols = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "ITC", "WIPRO", "LT", "SBIN", "MARUTI"]
    sectors = ["Energy", "IT", "Finance", "Consumer", "Auto"]
    data = []
    for sym in symbols:
        data.append({
            "Symbol": sym,
            "Sector": random.choice(sectors),
            "Price": round(random.uniform(100, 4000), 2),
            "Market Cap (Cr)": round(random.uniform(10000, 500000), 2),
            "Volume": round(random.uniform(0.5, 20), 2),
            "RSI": round(random.uniform(10, 90), 2),
            "Signal": random.choice(["Buy", "Hold", "Sell"])
        })
    return pd.DataFrame(data)

df = load_stock_data()

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(page_title="IndexIQ Screener", layout="wide")
st.title("📍 Stock Screener - IndexIQ")
st.markdown("Use filters below to screen Indian stocks by technical and financial indicators.")

# -------------------------
# Sidebar Filters
# -------------------------
with st.sidebar:
    st.header("📊 Screener Filters")
    sector_filter = st.multiselect("Sector", options=df["Sector"].unique(), default=df["Sector"].unique())
    price_range = st.slider("Price Range", 0.0, 5000.0, (0.0, 5000.0))
    mcap_range = st.slider("Market Cap Range (Cr)", 0.0, 500000.0, (0.0, 500000.0))
    rsi_range = st.slider("RSI Range", 0.0, 100.0, (0.0, 100.0))
    signal_filter = st.multiselect("Signal", options=["Buy", "Hold", "Sell"], default=["Buy", "Hold", "Sell"])

# -------------------------
# Filtered Data
# -------------------------
filtered_df = df[
    (df["Sector"].isin(sector_filter)) &
    (df["Price"] >= price_range[0]) & (df["Price"] <= price_range[1]) &
    (df["Market Cap (Cr)"] >= mcap_range[0]) & (df["Market Cap (Cr)"] <= mcap_range[1]) &
    (df["RSI"] >= rsi_range[0]) & (df["RSI"] <= rsi_range[1]) &
    (df["Signal"].isin(signal_filter))
]

# -------------------------
# Display Data Table
# -------------------------
st.subheader("📈 Screened Stocks")
st.dataframe(filtered_df.style
    .applymap(lambda val: 'color: green' if isinstance(val, float) and val > 70 else 'color: red' if isinstance(val, float) and val < 30 else '', subset=['RSI'])
    .applymap(lambda val: 'color: green' if val == 'Buy' else 'color: red' if val == 'Sell' else 'color: gray', subset=['Signal']),
    use_container_width=True
)

st.markdown(f"Showing **{filtered_df.shape[0]}** of **{df.shape[0]}** stocks.")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("IndexIQ Screener © 2025 - Powered by Streamlit")
