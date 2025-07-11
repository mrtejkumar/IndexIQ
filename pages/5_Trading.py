# pages/5_Trading.py

import streamlit as st
from core.trading import place_order, get_holdings, get_trade_history

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Paper Trading | IndexIQ", layout="wide")
st.title("💹 Paper Trading Simulator")
st.markdown("Simulate your stock trades, track portfolio performance, and learn without risk.")

# -------------------------
# Order Placement
# -------------------------
st.subheader("🛒 Place an Order")

col1, col2, col3 = st.columns(3)

with col1:
    symbol = st.selectbox("Select Stock", ["RELIANCE", "TCS", "INFY", "SBIN", "ICICIBANK", "NIFTY 50"])
with col2:
    action = st.radio("Action", ["Buy", "Sell"], horizontal=True)
with col3:
    quantity = st.number_input("Quantity", min_value=1, max_value=1000, value=10)

price = st.number_input("Price (₹)", min_value=1.0, value=1000.0, step=0.5)

if st.button("🚀 Execute Order"):
    result = place_order(symbol, action, quantity, price)
    st.success(result)

# -------------------------
# Holdings Display
# -------------------------
st.subheader("📊 Current Holdings")
holdings_df = get_holdings()
st.dataframe(holdings_df, use_container_width=True)

# -------------------------
# Trade History Display
# -------------------------
st.subheader("🧾 Trade History")
history_df = get_trade_history()
st.dataframe(history_df, use_container_width=True)

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("All trades are simulated. Paper trading helps improve discipline without risking capital.")
