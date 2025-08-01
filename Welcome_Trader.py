import streamlit as st
import base64
import os
from db.database import get_db
from db.models import User
from auth.auth_manager import authenticate_user, get_password_hash
from sqlalchemy.orm import Session
from core.logo import show_logo_sidebar_top

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(page_title="Welcome to IndexIQ", layout="wide")

# ----------------------------
# Show Logo at Top of Sidebar
# ----------------------------

show_logo_sidebar_top()

# ----------------------------
# Session State Initialization
# ----------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "show_register" not in st.session_state:
    st.session_state.show_register = False

db: Session = next(get_db())

# ----------------------------
# Logout if Already Logged In
# ----------------------------
if st.session_state.authenticated:
    st.success(f"✅ You are already logged in as **{st.session_state.username}**.")
    if st.button("🚪 Logout"):
        for key in ["authenticated", "user_id", "username", "show_register"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ You have been logged out.")
        st.rerun()
    st.stop()

# Add this after imports
def encode_credentials():
    # Encoded version of "admin_tej" and "12345678"
    ENCODED_USERNAME = "YWRtaW5fdGVq"  # base64 encoded "admin_tej"
    ENCODED_PASSWORD = "MTIzNDU2Nzg="  # base64 encoded "12345678"
    return ENCODED_USERNAME, ENCODED_PASSWORD

# ----------------------------
# Login Form
# ----------------------------
def show_login_form():
    st.title("🔐 Login to IndexIQ")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        # Check encoded admin credentials
        encoded_user, encoded_pass = encode_credentials()
        try:
            is_admin = (base64.b64encode(username.encode()).decode() == encoded_user and 
                       base64.b64encode(password.encode()).decode() == encoded_pass)
        except:
            is_admin = False

        if is_admin:
            st.session_state.authenticated = True
            st.session_state.user_id = -1  # Special admin ID
            st.session_state.username = username
            st.success("✅ Admin login successful!")
            st.switch_page("pages/1_Home.py")
        else:
            # Regular user authentication
            user = authenticate_user(username, password, db)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user.id
                st.session_state.username = user.username
                st.success("✅ Login successful!")
                st.switch_page("pages/1_Home.py")
            else:
                st.error("❌ Invalid username or password")

    st.markdown("---")
    if st.button("Don't have an account? Register"):
        st.session_state.show_register = True
        st.rerun()

# ----------------------------
# Registration Form
# ----------------------------
def show_register_form():
    st.title("📝 Register for IndexIQ")
    username = st.text_input("New Username", key="reg_user")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register"):
        if password != confirm:
            st.error("❌ Passwords do not match.")
        elif db.query(User).filter((User.username == username) | (User.email == email)).first():
            st.error("❌ Username or email already exists.")
        else:
            new_user = User(
                username=username,
                email=email,
                hashed_password=get_password_hash(password)
            )
            db.add(new_user)
            db.commit()
            st.success("✅ Registered successfully! Please log in.")
            st.session_state.show_register = False
            st.rerun()

    st.markdown("---")
    if st.button("Already have an account? Login"):
        st.session_state.show_register = False
        st.rerun()

# ----------------------------
# Render Login or Register View
# ----------------------------
if st.session_state.show_register:
    show_register_form()
else:
    show_login_form()
