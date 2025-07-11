import streamlit as st
from passlib.hash import bcrypt
from auth.auth_helper import load_authenticator
import yaml
from pathlib import Path
import re
import time

config_path = Path(__file__).parent.parent / "auth/auth_config.yaml"

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
    return True, "Password is strong"

def validate_username(username):
    """Validate username format"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 20:
        return False, "Username must be less than 20 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    if username[0].isdigit():
        return False, "Username cannot start with a number"
    return True, "Username is valid"

def check_username_exists(username):
    """Check if username already exists"""
    try:
        with config_path.open("r") as f:
            config = yaml.safe_load(f)
        return username in config.get('credentials', {}).get('usernames', {})
    except FileNotFoundError:
        return False

def save_user_to_config(username, email, password, full_name):
    """Save user to config file"""
    try:
        # Load existing config or create new one
        if config_path.exists():
            with config_path.open("r") as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}
        
        # Initialize structure if needed
        if 'credentials' not in config:
            config['credentials'] = {'usernames': {}}
        if 'usernames' not in config['credentials']:
            config['credentials']['usernames'] = {}

        # Add new user
        config['credentials']['usernames'][username] = {
            "email": email,
            "name": full_name,
            "password": bcrypt.hash(password),
            "registered_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save config
        with config_path.open("w") as f:
            yaml.dump(config, f, default_flow_style=False)

        return True, "User registered successfully!"
    except Exception as e:
        return False, f"Error saving user: {str(e)}"

def get_password_strength_color(password):
    """Get color based on password strength"""
    is_valid, _ = validate_password(password)
    if not password:
        return "gray"
    elif is_valid:
        return "green"
    else:
        score = 0
        if len(password) >= 8:
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        
        if score >= 4:
            return "orange"
        elif score >= 2:
            return "yellow"
        else:
            return "red"

# Page setup
st.set_page_config(page_title="Register - IndexIQ", page_icon="📝", layout="centered")

# Header
st.title("📝 Create Your IndexIQ Account")
st.markdown("Join thousands of investors tracking their portfolio with IndexIQ")

# Create form
with st.form("registration_form", clear_on_submit=False):
    st.markdown("### Personal Information")
    
    # Full Name
    col1, col2 = st.columns([3, 1])
    with col1:
        full_name = st.text_input(
            "Full Name *",
            placeholder="Enter your full name",
            help="This will be displayed in your profile"
        )
    with col2:
        if full_name:
            if len(full_name.strip()) >= 2:
                st.success("✓")
            else:
                st.error("✗")
    
    # Username
    col1, col2 = st.columns([3, 1])
    with col1:
        username = st.text_input(
            "Username *",
            placeholder="Choose a unique username",
            help="3-20 characters, letters, numbers, and underscores only. Cannot start with a number."
        )
    with col2:
        if username:
            is_valid, message = validate_username(username)
            if is_valid and not check_username_exists(username):
                st.success("✓")
            else:
                st.error("✗")
    
    # Show username validation message
    if username:
        is_valid, message = validate_username(username)
        if not is_valid:
            st.error(f"❌ {message}")
        elif check_username_exists(username):
            st.error("❌ Username already taken")
        else:
            st.success("✅ Username is available")
    
    # Email
    col1, col2 = st.columns([3, 1])
    with col1:
        email = st.text_input(
            "Email Address *",
            placeholder="your.email@example.com",
            help="We'll use this for account recovery and important notifications"
        )
    with col2:
        if email:
            if validate_email(email):
                st.success("✓")
            else:
                st.error("✗")
    
    # Show email validation message
    if email and not validate_email(email):
        st.error("❌ Please enter a valid email address")
    
    st.markdown("### Security")
    
    # Password
    col1, col2 = st.columns([3, 1])
    with col1:
        password = st.text_input(
            "Password *",
            type="password",
            placeholder="Create a strong password",
            help="At least 8 characters with uppercase, lowercase, number, and special character"
        )
    with col2:
        if password:
            color = get_password_strength_color(password)
            if color == "green":
                st.success("✓")
            elif color == "orange":
                st.warning("○")
            else:
                st.error("✗")
    
    # Password strength indicator
    if password:
        is_valid, message = validate_password(password)
        if is_valid:
            st.success("✅ Strong password")
        else:
            st.error(f"❌ {message}")
        
        # Password requirements checklist
        with st.expander("Password Requirements", expanded=not is_valid):
            st.markdown("**Your password must contain:**")
            
            checks = [
                (len(password) >= 8, "At least 8 characters"),
                (re.search(r'[A-Z]', password), "One uppercase letter (A-Z)"),
                (re.search(r'[a-z]', password), "One lowercase letter (a-z)"),
                (re.search(r'\d', password), "One number (0-9)"),
                (re.search(r'[!@#$%^&*(),.?":{}|<>]', password), "One special character (!@#$%^&*)")
            ]
            
            for check, description in checks:
                if check:
                    st.success(f"✅ {description}")
                else:
                    st.error(f"❌ {description}")
    
    # Confirm Password
    col1, col2 = st.columns([3, 1])
    with col1:
        confirm_password = st.text_input(
            "Confirm Password *",
            type="password",
            placeholder="Re-enter your password",
            help="Must match the password above"
        )
    with col2:
        if confirm_password:
            if password == confirm_password:
                st.success("✓")
            else:
                st.error("✗")
    
    # Show password match validation
    if confirm_password and password != confirm_password:
        st.error("❌ Passwords do not match")
    
    st.markdown("### Terms & Conditions")
    
    # Terms and conditions
    terms_accepted = st.checkbox(
        "I agree to the Terms of Service and Privacy Policy *",
        help="Please read and accept our terms to continue"
    )
    
    # Newsletter subscription
    newsletter = st.checkbox(
        "Subscribe to IndexIQ newsletter (optional)",
        help="Get market insights and portfolio tips delivered to your inbox"
    )
    
    # Submit button
    st.markdown("---")
    submitted = st.form_submit_button(
        "Create Account",
        type="primary",
        use_container_width=True
    )
    
    # Form validation and submission
    if submitted:
        # Collect all validation errors
        errors = []
        
        if not full_name or len(full_name.strip()) < 2:
            errors.append("Full name is required (minimum 2 characters)")
        
        if not username:
            errors.append("Username is required")
        else:
            is_valid, message = validate_username(username)
            if not is_valid:
                errors.append(message)
            elif check_username_exists(username):
                errors.append("Username already exists")
        
        if not email:
            errors.append("Email is required")
        elif not validate_email(email):
            errors.append("Please enter a valid email address")
        
        if not password:
            errors.append("Password is required")
        else:
            is_valid, message = validate_password(password)
            if not is_valid:
                errors.append(message)
        
        if not confirm_password:
            errors.append("Please confirm your password")
        elif password != confirm_password:
            errors.append("Passwords do not match")
        
        if not terms_accepted:
            errors.append("Please accept the Terms of Service and Privacy Policy")
        
        # Display errors or proceed with registration
        if errors:
            st.error("Please fix the following errors:")
            for error in errors:
                st.error(f"• {error}")
        else:
            # Attempt to save user
            with st.spinner("Creating your account..."):
                success, message = save_user_to_config(username, email, password, full_name.strip())
                
                if success:
                    st.success("🎉 Account created successfully!")
                    st.info("You can now login with your credentials")
                    st.balloons()
                    
                    # Optional: Auto-redirect to login page after delay
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"Registration failed: {message}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        Already have an account? <a href='/' style='color: #1f77b4;'>Login here</a><br>
        By creating an account, you agree to our 
        <a href='#' style='color: #1f77b4;'>Terms of Service</a> and 
        <a href='#' style='color: #1f77b4;'>Privacy Policy</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Add some CSS for better styling
st.markdown("""
<style>
.stTextInput > div > div > input {
    border-radius: 8px;
}
.stButton > button {
    border-radius: 8px;
    height: 3em;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)