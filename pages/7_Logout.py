import streamlit as st
from auth.auth_helper import load_authenticator

# Page setup
st.set_page_config(page_title="Logout - IndexIQ", page_icon="🚪", layout="centered")

try:
    authenticator, config = load_authenticator()
    
    # Check if user is logged in first
    if 'authentication_status' in st.session_state and st.session_state['authentication_status']:
        # User is logged in, show logout option
        st.title("🚪 Logout from IndexIQ")
        st.markdown("Are you sure you want to logout?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Yes, Logout", type="primary", use_container_width=True):
                try:
                    authenticator.logout(location="main")
                    st.success("✅ You have been logged out successfully!")
                    st.info("👋 Thank you for using IndexIQ. See you next time!")
                    st.balloons()
                except Exception as e:
                    # Manual logout if authenticator fails
                    st.session_state['authentication_status'] = None
                    st.session_state['name'] = None
                    st.session_state['username'] = None
                    st.success("✅ You have been logged out successfully!")
                    st.info("👋 Thank you for using IndexIQ. See you next time!")
        
        with col2:
            if st.button("Cancel", type="secondary", use_container_width=True):
                st.info("Logout cancelled. You remain logged in.")
    else:
        # User is not logged in
        st.title("🚪 Already Logged Out")
        st.info("You are not currently logged in.")
        st.markdown("---")
        st.markdown("**Want to login?** Use the sidebar to access the login page.")
        
        if st.button("Go to Login", type="primary"):
            st.switch_page("pages/0_Login.py")

except Exception as e:
    st.error(f"Error with logout: {str(e)}")
    st.info("Clearing session manually...")
    
    # Manual session clearing
    if st.button("Clear Session", type="primary"):
        st.session_state.clear()
        st.success("Session cleared successfully!")