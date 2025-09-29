import streamlit as st
import firebase_admin 
from firebase_admin import auth
from firebase_admin import credentials
import re
import time

# Initialize Firebase Admin (with error handling)
try:
    if not firebase_admin._apps:
        # Try to load service account key
        try:
            cred = credentials.Certificate('serviceAccountKey.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://gemini-pro-ats-resumetracker-default-rtdb.firebaseio.com'
            })
        except FileNotFoundError:
            st.warning("⚠️ Firebase service account key not found. Some features may be limited.")
        except Exception as e:
            st.warning(f"⚠️ Firebase Admin initialization issue: {str(e)}")
except Exception as e:
    st.write("ℹ️ Using existing Firebase app instance")

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
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"

def app():
    st.markdown("### 📝 Create Your Account")
    st.markdown("Join thousands of job seekers who have improved their resumes with AI")
    
    if not getState():
        st.session_state['authflag'] = False
    
    # Enhanced signup form
    with st.form("signup_form", clear_on_submit=False):
        st.markdown("#### Fill in your details")
        
        # Personal information
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "👤 First Name",
                placeholder="John",
                help="Enter your first name"
            )
        
        with col2:
            last_name = st.text_input(
                "👤 Last Name",
                placeholder="Doe",
                help="Enter your last name"
            )
        
        # Email
        email = st.text_input(
            "📧 Email Address",
            placeholder="john.doe@example.com",
            help="We'll use this for your login and notifications"
        )
        
        # Real-time email validation
        if email:
            if validate_email(email):
                st.success("✅ Valid email format")
            else:
                st.error("❌ Please enter a valid email address")
        
        # Password
        password = st.text_input(
            "🔒 Password",
            type="password",
            placeholder="Create a strong password",
            help="Password must be at least 8 characters with uppercase, lowercase, and numbers"
        )
        
        # Real-time password validation
        if password:
            is_valid, message = validate_password(password)
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
        
        # Confirm password
        confirm_password = st.text_input(
            "🔒 Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            help="Must match the password above"
        )
        
        # Real-time password match validation
        if password and confirm_password:
            if password == confirm_password:
                st.success("✅ Passwords match")
            else:
                st.error("❌ Passwords do not match")
        
        # Terms and conditions
        agree_terms = st.checkbox(
            "I agree to the Terms of Service and Privacy Policy",
            help="You must agree to continue"
        )
        
        # Newsletter subscription
        subscribe_newsletter = st.checkbox(
            "📧 Subscribe to career tips and updates",
            value=True,
            help="Get helpful resume tips and job market insights"
        )
        
        # Submit button
        col1, col2 = st.columns([2, 1])
        
        with col1:
            submit_button = st.form_submit_button(
                "🚀 Create Account",
                use_container_width=True,
                help="Click to create your account"
            )
        
        with col2:
            demo_button = st.form_submit_button(
                "👀 Try Demo",
                use_container_width=True,
                help="Explore without creating an account"
            )
    
    # Handle form submission
    if submit_button:
        # Validation checks
        errors = []
        
        if not first_name.strip():
            errors.append("First name is required")
        
        if not last_name.strip():
            errors.append("Last name is required")
        
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
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if not agree_terms:
            errors.append("You must agree to the Terms of Service")
        
        # Display errors or proceed with registration
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Proceed with account creation
            with st.spinner("🔄 Creating your account..."):
                time.sleep(1)  # Brief delay for better UX
                
                try:
                    # Create user with Firebase Admin
                    user = auth.create_user(
                        email=email,
                        password=password,
                        display_name=f"{first_name} {last_name}"
                    )
                    
                    # Store additional user data (if database is available)
                    user_data = {
                        'email': email,
                        'first_name': first_name,
                        'last_name': last_name,
                        'subscribe_newsletter': subscribe_newsletter,
                        'created_at': time.time(),
                        'analysis_count': 0
                    }
                    
                    # Set authentication state
                    st.session_state['authflag'] = True
                    st.session_state['user_email'] = email
                    st.session_state['user_id'] = user.uid
                    st.session_state['user_name'] = f"{first_name} {last_name}"
                    
                    st.success("🎉 Account created successfully!")
                    st.balloons()
                    
                    # Welcome message
                    st.info(f"Welcome aboard, {first_name}! 🚀 You can now start analyzing your resumes.")
                    
                    # Auto-redirect after success
                    time.sleep(3)
                    st.rerun()
                    
                except Exception as e:
                    error_message = str(e)
                    
                    if "EMAIL_ALREADY_EXISTS" in error_message:
                        st.error("❌ An account with this email already exists. Please try logging in instead.")
                    elif "WEAK_PASSWORD" in error_message:
                        st.error("❌ Password is too weak. Please choose a stronger password.")
                    else:
                        st.error(f"❌ Account creation failed: {error_message}")
                        
                        # Provide helpful suggestions
                        st.info("💡 **Troubleshooting tips:**")
                        st.info("• Make sure your email is not already registered")
                        st.info("• Use a stronger password with mixed characters")
                        st.info("• Check your internet connection")
    
    # Handle demo mode
    if demo_button:
        st.info("🎭 **Demo Mode Activated!**")
        st.session_state['authflag'] = True
        st.session_state['user_email'] = 'demo@atsresume.com'
        st.session_state['user_id'] = 'demo_user'
        st.session_state['user_name'] = 'Demo User'
        st.success("You're now using the demo version. Some features may be limited.")
        time.sleep(2)
        st.rerun()
    
    # Additional options
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("##### 🔐 Already have an account?")
        if st.button("🚪 Sign In", use_container_width=True):
            st.session_state.redirect_to_login = True
            st.rerun()
    
    with col2:
        st.markdown("##### 🏠 Go Back")
        if st.button("⬅️ Home", use_container_width=True):
            st.session_state.redirect_to_home = True
            st.rerun()
    
    # Features preview for signup encouragement
    with st.expander("🌟 What you'll get with your account", expanded=False):
        features = [
            "🎯 Unlimited resume analysis",
            "📊 Detailed match scoring",
            "📈 Progress tracking over time",
            "💾 Analysis history and reports",
            "🔔 Job market insights",
            "🆓 Always free to use"
        ]
        
        for feature in features:
            st.markdown(f"• {feature}")

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
            keys_to_clear = ['user_email', 'user_id', 'user_name', 'analysis_count']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
    except Exception as e:
        st.error(f"Error setting auth state: {e}")

def get_user_name():
    """Get current user's full name"""
    return st.session_state.get('user_name', '')

def is_demo_user():
    """Check if current user is using demo mode"""
    return st.session_state.get('user_email', '') == 'demo@atsresume.com'