import streamlit as st
import firebase_admin 
from firebase_admin import auth
from firebase_admin import credentials
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://gemini-pro-ats-resumetracker-default-rtdb.firebaseio.com'
        })
except Exception as e:
    st.write(firebase_admin.get_app())
# Sign up form and logic
def app():
    st.title("Sign Up")
    if(not getState()):
        st.session_state['authflag'] = False
    # Create a form for sign up
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        try:
            # Create new account with Firebase
            user = auth.create_user(email=username, password=password)
            st.success("Account created successfully!")
            # Redirect to login page
            st.write("Go to login page...")
            st.session_state['authflag'] = True
        except Exception as e:
            st.error(f"Error: {e}")

def getState():
    try:
        return st.session_state['authflag']
    except Exception as e:
        st.session_state['authflag'] = False

def setState(flag):
        st.session_state['authflag'] = flag
