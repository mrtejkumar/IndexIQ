# pages/6_News.py

import streamlit as st
import time
from core.news import get_latest_news

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
