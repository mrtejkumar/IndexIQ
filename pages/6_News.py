# pages/6_News.py

import streamlit as st
from core.news import get_latest_news

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Financial News | IndexIQ", layout="wide")
st.title("📰 Financial Market News")
st.markdown("Stay updated with real-time financial and stock market headlines.")

# -------------------------
# News Section
# -------------------------
news_items = get_latest_news()

for article in news_items:
    st.markdown(f"### [{article['title']}]({article['url']})")
    st.markdown(f"**Source:** {article['source']} &nbsp; | &nbsp; 🕒 {article['published']}")
    st.markdown(article["summary"])
    st.markdown("---")
