import streamlit as st
import yaml
from pathlib import Path
from passlib.hash import bcrypt

def load_users():
    """Load users from config file"""
    config_path = Path(__file__).parent.parent / "auth/auth_config.yaml"
    
    if not config_path.exists():
        return {}
    
    try:
        with config_path.open("r") as f:
            config = yaml.safe_load(f)
            return config.get('credentials', {}).get('usernames', {})
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return {}

def verify_password(password, hashed_password):
    """Verify password against hash"""
    try:
        return bcrypt.verify(password, hashed_password)
    except Exception:
        return False

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users = load_users()
    
    if not users:
        return False, "No users found. Please register first."
    
    if username not in users:
        return False, "Username not found"
    
    user_data = users[username]
    if verify_password(password, user_data['password']):
        return True, user_data
    else:
        return False, "Invalid password"

# Page setup
st.set_page_config(page_title="Login - IndexIQ", page_icon="🔐", layout="centered")

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# Header
st.title("🔐 Welcome to IndexIQ")
st.markdown("Sign in to access your portfolio dashboard")

# Check if already logged in
if st.session_state.authenticated:
    user_name = st.session_state.user_data.get('name', st.session_state.username)
    st.success(f"✅ Welcome back, {user_name}!")
    st.markdown("🎉 You are already logged in. Use the sidebar to explore IndexIQ.")
    
    # Show user info
    st.markdown("---")
    st.markdown("**Account Information:**")
    st.write(f"**Name:** {user_name}")
    st.write(f"**Username:** {st.session_state.username}")
    st.write(f"**Email:** {st.session_state.user_data.get('email', 'N/A')}")
    
    # Add logout button
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Logout", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.user_data = None
            st.success("Successfully logged out!")
            st.rerun()
    
    with col2:
        if st.button("Go to Portfolio", type="primary", use_container_width=True):
            st.switch_page("pages/1_Portfolio.py")

else:
    # Login form
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### Login to Your Account")
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            help="Use the username you created during registration"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            help="Enter your account password"
        )
        
        # Remember me checkbox
        remember_me = st.checkbox("Remember me", help="Keep me logged in")
        
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submitted:
            if not username or not password:
                st.error("❌ Please enter both username and password")
            else:
                with st.spinner("Logging in..."):
                    success, result = authenticate_user(username, password)
                    
                    if success:
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.user_data = result
                        st.success("✅ Login successful!")
                        st.balloons()
                        
                        # Show success message and redirect
                        st.markdown("**Redirecting to your dashboard...**")
                        st.rerun()
                    else:
                        st.error(f"❌ Login failed: {result}")
                        
                        # Show helpful hints
                        if "Username not found" in result:
                            st.info("💡 **Tip:** Make sure you've registered first")
                        elif "Invalid password" in result:
                            st.info("💡 **Tip:** Check your password and try again")
    
    # Additional sections
    st.markdown("---")
    
    # Quick access buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Register New Account", use_container_width=True):
            st.switch_page("pages/Register.py")
    
    with col2:
        if st.button("❓ Need Help?", use_container_width=True):
            st.info("Contact support at support@indexiq.com")
    
    # Demo credentials (for testing)
    with st.expander("🧪 Demo Credentials (for testing)"):
        st.code("""
Demo Username: demo_user
Demo Password: Demo123!
        """)
        st.caption("*These credentials are for demonstration purposes only*")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p><strong>IndexIQ</strong> - Your Personal Portfolio Tracker</p>
        <p>🔒 Secure • 📊 Smart • 🚀 Simple</p>
        <p><em>Track • Analyze • Grow</em></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Add custom CSS for better styling
st.markdown("""
<style>
.stButton > button {
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.stTextInput > div > div > input {
    border-radius: 8px;
    border: 2px solid #e0e0e0;
    padding: 0.75rem;
    font-size: 1rem;
}

.stTextInput > div > div > input:focus {
    border-color: #1f77b4;
    box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1);
}

.stForm {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid #e9ecef;
}
</style>
""", unsafe_allow_html=True)