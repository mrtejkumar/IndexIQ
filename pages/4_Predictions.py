# pages/4_Predictions.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.predictions import get_prediction_for_stock, get_prediction_summary

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Stock Predictions | IndexIQ", layout="wide")
st.title("🔮 Stock Price Predictions")
st.markdown("AI/ML-based stock price forecasting for key stocks and indexes.")

# -------------------------
# Stock Selector
# -------------------------
selected_stock = st.selectbox("📈 Choose a stock or index", ["RELIANCE", "INFY", "HDFCBANK", "ICICIBANK", "NIFTY 50"])

# -------------------------
# Prediction Data
# -------------------------
historical_df, forecast_df = get_prediction_for_stock(selected_stock)

# -------------------------
# Line Chart
# -------------------------
st.subheader(f"📊 Predicted vs Historical Price - {selected_stock}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=historical_df['Date'], y=historical_df['Price'], name="Historical", mode="lines"))
fig.add_trace(go.Scatter(x=forecast_df['Date'], y=forecast_df['Forecast'], name="Forecast", mode="lines", line=dict(dash='dash')))
fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=10))
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Prediction Summary Table
# -------------------------
st.subheader("📋 Prediction Summary")
summary_df = get_prediction_summary(selected_stock)
st.dataframe(summary_df, use_container_width=True)

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("Predictions are generated using mock models. You can replace with real ML models (e.g., LSTM, Prophet).")
