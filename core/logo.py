import os
import base64
import streamlit as st

def show_logo_sidebar_top():
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()

        st.markdown(
            f"""
            <style>
            [data-testid="stSidebar"]::before {{
                content: "";
                display: block;
                margin-top: 0px;
                margin-bottom: 0px;
                height: 100px;
                background-image: url("data:image/png;base64,{encoded}");
                background-repeat: no-repeat;
                background-position: center center;
                background-size: 170px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
