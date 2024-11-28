import streamlit as st
import firebase_config as fb
def app():
    st.title("Login")
    if(not getState()):
        st.session_state['authflag'] = False
    # Create a form for login
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

    if submit_button:
        try:
            # Authenticate user with Firebase
            user = fb.auth.sign_in_with_email_and_password(username, password)
            # Store user's authentication status in session state
            st.session_state['authflag'] = True
            st.success("Logged in successfully!")
            # Redirect to main page
            st.write("Go to main page...")
        except Exception as e:
            st.error(f"Error: {e}")
            # Set authentication status to False

def getState():
    try:
        return st.session_state['authflag']
    except Exception as e:
        st.session_state['authflag'] = False

def setState(flag):
        st.session_state['authflag'] = flag