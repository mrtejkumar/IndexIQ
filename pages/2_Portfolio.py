import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import time
from core.portfolio import get_user_holdings, calculate_portfolio_metrics
from core.angel_api import get_live_price

from core.logo import show_logo_sidebar_top 
from core.search_bar import setup_stock_search_bar



# Show Logo at Top of Sidebar
show_logo_sidebar_top()

# -------------------------
# Redirect if Not Logged In
# -------------------------
if not st.session_state.get("authenticated"):
    st.warning("🔒 You are not logged in. Redirecting to login page in 10 seconds...")

    if st.button("🔑 Go to Login Now"):
        st.switch_page("Welcome_Trader.py")

    with st.empty():
        for seconds in range(10, 0, -1):
            st.info(f"Redirecting in {seconds} seconds...")
            time.sleep(1)
        st.switch_page("Welcome_Trader.py")
# -------------------------
# Sidebar Logout Button
# -------------------------
with st.sidebar:
    if st.session_state.get("authenticated"):
        if st.button("🚪 Logout"):
            username = st.session_state.get("username", "User")
            for key in ["authenticated", "user_id", "username", "show_register"]:
                st.session_state.pop(key, None)
            st.success(f"✅ {username}, you have been logged out successfully.")
            time.sleep(5)
            st.switch_page("Welcome_Trader.py")
#adding search bar
setup_stock_search_bar(location="sidebar", show_history=True)
# Page setup
st.set_page_config(page_title="Portfolio - IndexIQ", layout="wide")
st.title("💼 My Portfolio")

# Fetch user's portfolio (for now: session state or mock)
holdings = get_user_holdings()

if not holdings:
    st.warning("No holdings found. Start paper trading to build your portfolio.")
    st.stop()

portfolio_data = []

total_value = 0
total_invested = 0

for symbol, data in holdings.items():
    live_price_data = get_live_price(symbol)
    live_price = live_price_data['price']
    quantity = data["quantity"]
    avg_price = data["avg_price"]
    current_value = live_price * quantity
    invested = avg_price * quantity
    pnl = current_value - invested
    pnl_pct = (pnl / invested) * 100 if invested else 0

    total_value += current_value
    total_invested += invested

    portfolio_data.append({
        "Symbol": symbol,
        "Qty": quantity,
        "Avg Buy Price": round(avg_price, 2),
        "Live Price": round(live_price, 2),
        "Invested (₹)": round(invested, 2),
        "Current Value (₹)": round(current_value, 2),
        "PnL (₹)": round(pnl, 2),
        "PnL (%)": round(pnl_pct, 2)
    })

df = pd.DataFrame(portfolio_data)

# Metrics
st.subheader("📊 Portfolio Summary")

col1, col2, col3 = st.columns(3)
col1.metric("Total Invested", f"₹{total_invested:,.2f}")
col2.metric("Current Value", f"₹{total_value:,.2f}")
col3.metric("Total PnL", f"₹{total_value - total_invested:,.2f}", delta=f"{((total_value - total_invested) / total_invested) * 100:.2f}%" if total_invested else "0%")

# Display table
st.dataframe(df, use_container_width=True)

# Trendline (Mocked for now)
st.subheader("📈 Portfolio Value Over Time")

df_trend = pd.DataFrame({
    "Date": pd.date_range(end=pd.Timestamp.today(), periods=10),
    "Portfolio Value": [total_invested * (1 + 0.01 * i) for i in range(10)]
})

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_trend["Date"], y=df_trend["Portfolio Value"], mode="lines+markers"))
fig.update_layout(height=300, margin=dict(t=10, b=10))
st.plotly_chart(fig, use_container_width=True)