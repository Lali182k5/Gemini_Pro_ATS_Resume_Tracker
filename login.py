import streamlit as st
import firebase_config as fb
import time

def app():
    st.markdown("### 🔐 Sign In to Your Account")
    
    if not getState():
        st.session_state['authflag'] = False
    
    # Enhanced login form with better styling
    with st.form("login_form", clear_on_submit=False):
        st.markdown("#### Enter your credentials")
        
        username = st.text_input(
            "📧 Email Address",
            placeholder="your.email@example.com",
            help="Enter the email address you used to sign up"
        )
        
        password = st.text_input(
            "🔒 Password", 
            type="password",
            placeholder="Enter your password",
            help="Enter your account password"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit_button = st.form_submit_button("🔐 Sign In", use_container_width=True)
        
        with col2:
            forgot_password = st.form_submit_button("🔄 Forgot Password?", use_container_width=True)
    
    # Handle login
    if submit_button:
        if username and password:
            with st.spinner("🔄 Signing you in..."):
                time.sleep(1)  # Brief delay for better UX
                try:
                    if fb.auth:
                        # Authenticate user with Firebase
                        user = fb.auth.sign_in_with_email_and_password(username, password)
                        
                        # Store user's authentication status and info
                        st.session_state['authflag'] = True
                        st.session_state['user_email'] = username
                        st.session_state['user_id'] = user['localId']
                        
                        st.success("✅ Logged in successfully!")
                        st.balloons()
                        
                        # Auto-redirect after a brief moment
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("🔥 Firebase authentication is not available. Please check configuration.")
                
                except Exception as e:
                    error_message = str(e)
                    if "INVALID_EMAIL" in error_message:
                        st.error("❌ Invalid email format. Please check your email address.")
                    elif "EMAIL_NOT_FOUND" in error_message:
                        st.error("❌ No account found with this email. Please sign up first.")
                    elif "INVALID_PASSWORD" in error_message:
                        st.error("❌ Incorrect password. Please try again.")
                    elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error_message:
                        st.error("❌ Too many failed attempts. Please try again later.")
                    else:
                        st.error(f"❌ Login failed: {error_message}")
        else:
            st.warning("⚠️ Please fill in both email and password fields.")
    
    # Handle forgot password
    if forgot_password:
        if username:
            try:
                if fb.auth:
                    fb.auth.send_password_reset_email(username)
                    st.success(f"📧 Password reset email sent to {username}")
                    st.info("Please check your email and follow the instructions to reset your password.")
                else:
                    st.error("🔥 Firebase authentication is not available.")
            except Exception as e:
                st.error(f"❌ Error sending reset email: {str(e)}")
        else:
            st.warning("⚠️ Please enter your email address first, then click 'Forgot Password?'")
    
    # Additional options
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("##### 🆕 New User?")
        if st.button("📝 Create Account", use_container_width=True):
            st.session_state.redirect_to_signup = True
            st.rerun()
    
    with col2:
        st.markdown("##### 🏠 Go Back")
        if st.button("⬅️ Home", use_container_width=True):
            st.session_state.redirect_to_home = True
            st.rerun()
    
    # Show current authentication status for debugging
    if st.checkbox("🔍 Show Debug Info", help="For troubleshooting purposes"):
        st.json({
            "Authentication Status": getState(),
            "Firebase Auth Available": fb.auth is not None,
            "Session Keys": list(st.session_state.keys()) if hasattr(st, 'session_state') else []
        })

def getState():
    """Get current authentication state"""
    try:
        return st.session_state.get('authflag', False)
    except Exception as e:
        st.session_state['authflag'] = False
        return False

def setState(flag):
    """Set authentication state"""
    try:
        st.session_state['authflag'] = flag
        if not flag:
            # Clear user data when logging out
            keys_to_clear = ['user_email', 'user_id', 'analysis_count']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
    except Exception as e:
        st.error(f"Error setting auth state: {e}")

def get_user_email():
    """Get current user's email"""
    return st.session_state.get('user_email', '')

def get_user_id():
    """Get current user's ID"""
    return st.session_state.get('user_id', '')