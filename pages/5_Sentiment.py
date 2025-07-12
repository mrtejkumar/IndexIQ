# pages/3_Sentiment.py

import streamlit as st
import pandas as pd
import time
import plotly.express as px
from core.sentiment import get_overall_sentiment, get_sentiment_trends, get_trending_keywords

from core.logo import show_logo_sidebar_top  # Ensure logo function is defined properly

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
            time.sleep(1)
            st.switch_page("Welcome_Trader.py")


# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Sentiment Analysis | IndexIQ", layout="wide")
st.title("🧠 Sentiment Analysis")
st.markdown("Live market sentiment from social media and financial news.")

# -------------------------
# Overall Sentiment Summary
# -------------------------
sentiment_score, sentiment_label = get_overall_sentiment()

st.metric(label="Overall Market Sentiment", value=f"{sentiment_score}%", delta=sentiment_label)

# -------------------------
# Sentiment Trend (Mock Data from NLP or API)
# -------------------------
st.subheader("📊 Sentiment Over Time")

trend_data = get_sentiment_trends()

fig = px.line(trend_data, x="Date", y="Sentiment Score", title="7-Day Sentiment Trend", markers=True)
fig.update_layout(margin=dict(l=20, r=20, t=40, b=10), height=350)
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Trending Topics
# -------------------------
st.subheader("🔥 Trending Financial Keywords")

keywords = get_trending_keywords()

st.markdown(
    " ".join([f"`{kw}`" for kw in keywords])
)

# -------------------------
# Example Tweets / Headlines (Optional Section)
# -------------------------
with st.expander("📰 Sample News & Tweets"):
    st.write("- \"Markets expected to rebound as earnings season starts.\"")
    st.write("- \"Retail investors showing strong bullish behavior this week.\"")
    st.write("- \"Volatility spikes as FIIs exit positions.\"")

# -------------------------
# Footer
# -------------------------
st.markdown("---")
st.caption("Sentiment data is AI-processed from real-time sources like news, Reddit, Twitter.")

