import streamlit as st
import signup, login, fb
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
from PIL import Image
load_dotenv()

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
       # st.title("Gemini Pro ATS Resume Tracker")
        st.sidebar.markdown("""
            <style>
            [data-testid = stSidebar] {
                background-image: url("https://e0.pxfuel.com/wallpapers/219/656/desktop-wallpaper-purple-color-background-best-for-your-mobile-tablet-explore-color-cool-color-colored-background-one-color-aesthetic-one-color.jpg");
                border-radius: 25px;
                background-size: 500%;
            }
            [data-testid = stImage] {
                border-radius: 25px;
            }
            </style>
        """, unsafe_allow_html=True)
        imgl = Image.open("Gemini.jpeg")
        st.sidebar.image(imgl, width=350)
        with st.sidebar:
            app = option_menu(
                menu_title='ATS Resume Tracking',
                options=['Signup', 'Login', 'Home'],
                icons=['trophy-fill', 'person-circle', 'house-fill'],
                menu_icon='info-circle-fill',
                default_index=0,
                styles={
                    'container': {'padding': '0px', 'background-color': '#000000'},
                    'icon': {'color': '#FFFFFF'},
                    'nav-link': {'color': '#FFFFFF'},
                    'nav-link-selected': {'background-color': '#4F4F4F'}

                }
            )
        if app == "Home":
            if(signup.getState() == True or login.getState() == True):
                fb.app()
            else:
                signup.app()
        elif app == "Signup":
            signup.app()
        elif app == "Login":
            login.app()

MultiApp().run()