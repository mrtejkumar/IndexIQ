# indexiq_dashboard.py
import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd
import random

# -------------------------
# Set Page Config
# -------------------------
st.set_page_config(page_title="IndexIQ Dashboard", layout="wide")

# -------------------------
# Header
# -------------------------
st.title("📈 IndexIQ - Smart Market Dashboard")
st.markdown("A modern, data-driven dashboard with sentiment, prediction & financial insights.Designed by Tej Kumar Sahu")

# -------------------------
# Sidebar Navigation
# -------------------------
# with st.sidebar:
#     st.header("📂 Navigation")
#     pages = ["Dashboard", "Portfolio", "Watchlist", "Screener", "Sentiment Analysis", "Predictions", "News"]
#     selected_page = st.radio("Go to", pages)

# -------------------------
# Market Overview
# -------------------------
st.subheader("🌐 Market Overview with Sentiment")

cols = st.columns(3)
index_data = {
    "Nifty 50": {"symbol": "^NSEI", "sentiment": random.choice(["Bullish", "Bearish"])},
    "Sensex": {"symbol": "^BSESN", "sentiment": random.choice(["Bullish", "Bearish"])},
    "Nasdaq": {"symbol": "^IXIC", "sentiment": random.choice(["Bullish", "Bearish"])}
}

for i, (name, info) in enumerate(index_data.items()):
    index = yf.Ticker(info["symbol"])
    df = index.history(period="1d")
    price = df["Close"].iloc[-1]
    change = df["Close"].iloc[-1] - df["Open"].iloc[-1]
    pct_change = (change / df["Open"].iloc[-1]) * 100
    sentiment_color = "green" if info["sentiment"] == "Bullish" else "red"

    with cols[i]:
        st.metric(label=f"{name}", value=f"{price:,.2f}", delta=f"{pct_change:.2f}%", delta_color="normal")
        st.markdown(f"Sentiment: **:{sentiment_color}[{info['sentiment']}]**")

# -------------------------
# Portfolio Performance (Sample Data)
# -------------------------
st.subheader("📊 Portfolio Performance")
portfolio_data = pd.DataFrame({
    "Date": pd.date_range("2024-06-01", periods=30),
    "Value": [100000 + random.uniform(-5000, 5000) * i for i in range(30)]
})
fig = go.Figure()
fig.add_trace(go.Scatter(x=portfolio_data["Date"], y=portfolio_data["Value"], mode='lines+markers', name='Portfolio'))
fig.update_layout(margin=dict(l=10, r=10, t=30, b=10), height=300)
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Sentiment Analysis Summary (Static Example)
# -------------------------
st.subheader("🧠 Sentiment Analysis (From Social & News)")
col1, col2 = st.columns([1, 1])

with col1:
    st.metric(label="Sentiment Score", value="76%", delta="Bullish")
    st.markdown("Based on Twitter, Reddit & financial news sentiment.")
with col2:
    st.write("**Trending Keywords**")
    st.markdown(
        "`investors` `market` `growth` `earnings` `rise` `outlook` `stock`")

# -------------------------
# AI Stock Prediction (Sample Data)
# -------------------------
st.subheader("🔮 AI Stock Prediction")
pred_col = st.columns(3)
predictions = [
    {"ticker": "INFY", "prediction": "+3.2%", "confidence": "87%"},
    {"ticker": "TCS", "prediction": "+1.1%", "confidence": "73%"},
    {"ticker": "HDFCBANK", "prediction": "-0.8%", "confidence": "68%"},
]

for i, pred in enumerate(predictions):
    with pred_col[i]:
        st.metric(f"{pred['ticker']}", pred["prediction"], help=f"Confidence: {pred['confidence']}")

# -------------------------
# Financial News (Static Placeholder)
# -------------------------
st.subheader("🗞️ Financial News")
news = [
    {"source": "Reuters", "title": "U.S. Fed declines to cut rates", "time": "2h ago"},
    {"source": "MarketWatch", "title": "Amazon hit with EU antitrust case", "time": "3h ago"},
    {"source": "Bloomberg", "title": "Gold gains as inflation rises", "time": "4h ago"}
]
for article in news:
    st.markdown(f"- **{article['source']}** · {article['title']} _(Posted {article['time']})_")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("IndexIQ © 2025. Powered by Streamlit + Yahoo Finance + AI.")
