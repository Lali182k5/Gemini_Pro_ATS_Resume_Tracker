import streamlit as st
import signup, login, enhanced_fb
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
from PIL import Image
import os

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
        # Enhanced page configuration
        st.set_page_config(
            page_title="🚀 Gemini Pro ATS Resume Tracker",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Enhanced custom CSS
        st.markdown("""
            <style>
            /* Sidebar styling */
            [data-testid=stSidebar] {
                background: linear-gradient(180deg, 
                    rgba(75,0,130,0.9) 0%, 
                    rgba(138,43,226,0.8) 50%, 
                    rgba(72,61,139,0.7) 100%);
                border-radius: 0 25px 25px 0;
                border-right: 2px solid rgba(255,255,255,0.3);
            }
            
            [data-testid=stSidebar] .sidebar-content {
                padding: 1rem;
            }
            
            /* Main content area */
            .stApp > header {
                background-color: transparent;
            }
            
            .main .block-container {
                padding-top: 2rem;
                max-width: 95%;
            }
            
            /* Sidebar image styling */
            [data-testid=stImage] {
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                transition: transform 0.3s ease;
            }
            
            [data-testid=stImage]:hover {
                transform: scale(1.05);
            }
            
            /* Option menu styling */
            .nav-link {
                font-weight: 600 !important;
                transition: all 0.3s ease !important;
                border-radius: 10px !important;
                margin: 5px 0 !important;
            }
            
            .nav-link:hover {
                background-color: rgba(255,255,255,0.2) !important;
                transform: translateX(10px);
            }
            
            .nav-link-selected {
                background: linear-gradient(90deg, #FF6B6B, #4ECDC4) !important;
                font-weight: bold !important;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            }
            
            /* Welcome message */
            .welcome-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 15px;
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            
            /* Animated background */
            .stApp {
                background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
            }
            
            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            /* Content overlay */
            .main {
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                margin: 1rem;
                box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            }
            
            /* Button styling */
            .stButton > button {
                background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
                color: white;
                border: none;
                border-radius: 25px;
                padding: 0.75rem 2rem;
                font-weight: 600;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }
            
            /* Authentication status indicator */
            .auth-status {
                position: fixed;
                top: 1rem;
                right: 1rem;
                background: rgba(76, 175, 80, 0.9);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                font-size: 0.8rem;
                z-index: 1000;
                backdrop-filter: blur(5px);
            }
            
            .auth-status.logged-out {
                background: rgba(244, 67, 54, 0.9);
            }
            
            /* Footer */
            .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background: rgba(0,0,0,0.8);
                color: white;
                text-align: center;
                padding: 0.5rem;
                font-size: 0.8rem;
                backdrop-filter: blur(5px);
            }
            </style>
        """, unsafe_allow_html=True)
        
        # Authentication status indicator
        auth_status = "✅ Logged In" if (signup.getState() or login.getState()) else "🔒 Not Authenticated"
        auth_class = "auth-status" if (signup.getState() or login.getState()) else "auth-status logged-out"
        st.markdown(f'<div class="{auth_class}">{auth_status}</div>', unsafe_allow_html=True)
        
        # Sidebar configuration
        with st.sidebar:
            # Logo/Header image
            try:
                if os.path.exists("Gemini.jpeg"):
                    logo_img = Image.open("Gemini.jpeg")
                    st.image(logo_img, width=300, caption="Powered by Gemini Pro AI")
                else:
                    st.markdown("### 🚀 ATS Resume Tracker")
            except Exception as e:
                st.markdown("### 🚀 ATS Resume Tracker")
            
            st.markdown("---")
            
            # Enhanced navigation menu
            app = option_menu(
                menu_title='Navigation',
                options=['🏠 Home', '📝 Sign Up', '🔐 Login'],
                icons=['house-fill', 'person-plus-fill', 'box-arrow-in-right'],
                menu_icon='compass',
                default_index=0,
                styles={
                    'container': {
                        'padding': '0px',
                        'background-color': 'transparent'
                    },
                    'icon': {
                        'color': '#FFFFFF',
                        'font-size': '18px'
                    },
                    'nav-link': {
                        'color': '#FFFFFF',
                        'font-size': '16px',
                        'text-align': 'left',
                        'margin': '5px 0px',
                        'padding': '10px 15px',
                        'border-radius': '10px',
                        'background-color': 'rgba(255,255,255,0.1)'
                    },
                    'nav-link-selected': {
                        'background': 'linear-gradient(90deg, #FF6B6B, #4ECDC4)',
                        'font-weight': 'bold',
                        'box-shadow': '0 4px 15px rgba(0,0,0,0.2)'
                    }
                }
            )
            
            st.markdown("---")
            
            # Feature highlights
            st.markdown("### ✨ Features")
            features = [
                "🎯 AI-Powered Analysis",
                "📊 Real-time Match Scoring",
                "🔍 Keyword Gap Analysis",
                "📈 Improvement Suggestions",
                "💾 Analysis History",
                "🔒 Secure & Private"
            ]
            
            for feature in features:
                st.markdown(f"• {feature}")
            
            st.markdown("---")
            
            # Quick stats (if logged in)
            if signup.getState() or login.getState():
                st.markdown("### 📊 Your Stats")
                if 'analysis_count' not in st.session_state:
                    st.session_state.analysis_count = 0
                
                st.metric("Analyses Done", st.session_state.analysis_count)
                
                # Progress towards goals
                progress = min(st.session_state.analysis_count / 10, 1.0)  # Goal of 10 analyses
                st.progress(progress)
                st.caption(f"Goal: 10 analyses ({st.session_state.analysis_count}/10)")
        
        # Main content area based on navigation
        if app == "🏠 Home":
            if signup.getState() or login.getState():
                # Welcome message for authenticated users
                user_email = st.session_state.get('user_email', 'User')
                st.markdown(f"""
                <div class="welcome-header">
                    <h2>🎉 Welcome back, {user_email.split('@')[0].title()}!</h2>
                    <p>Ready to optimize your resume for your dream job?</p>
                </div>
                """, unsafe_allow_html=True)
                
                enhanced_fb.app()
            else:
                # Landing page for non-authenticated users
                self.show_landing_page()
        
        elif app == "📝 Sign Up":
            st.markdown('<div class="welcome-header"><h2>📝 Create Your Account</h2></div>', unsafe_allow_html=True)
            signup.app()
        
        elif app == "🔐 Login":
            st.markdown('<div class="welcome-header"><h2>🔐 Welcome Back</h2></div>', unsafe_allow_html=True)
            login.app()
        
        # Footer
        st.markdown("""
        <div class="footer">
            🚀 Gemini Pro ATS Resume Tracker | Powered by Google Gemini AI | Made with ❤️ using Streamlit
        </div>
        """, unsafe_allow_html=True)

    def show_landing_page(self):
        """Display an engaging landing page for non-authenticated users"""
        
        # Hero Section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("# 🚀 Transform Your Job Search with AI")
            st.markdown("""
            ### Boost Your Resume's ATS Score with Gemini Pro AI
            
            🎯 **Get hired faster** by optimizing your resume for Applicant Tracking Systems (ATS)
            
            🤖 **AI-powered analysis** provides instant feedback and improvement suggestions
            
            📊 **Real-time scoring** shows exactly how well your resume matches job descriptions
            
            🔍 **Keyword optimization** helps you include the right skills and terms employers are looking for
            """)
            
            st.markdown("### 🌟 Why Choose Our ATS Tracker?")
            
            benefits = [
                ("⚡", "Instant Analysis", "Get results in seconds, not hours"),
                ("🎯", "Precision Matching", "Advanced AI understands context and relevance"),
                ("📈", "Improvement Tracking", "Monitor your progress over time"),
                ("🔒", "Privacy First", "Your data is secure and never shared"),
                ("💼", "Industry Expertise", "Trained on thousands of successful resumes"),
                ("🆓", "Free to Start", "No credit card required to begin")
            ]
            
            for icon, title, description in benefits:
                with st.container():
                    benefit_col1, benefit_col2 = st.columns([1, 6])
                    with benefit_col1:
                        st.markdown(f"<div style='font-size: 2rem; text-align: center;'>{icon}</div>", 
                                  unsafe_allow_html=True)
                    with benefit_col2:
                        st.markdown(f"**{title}**")
                        st.caption(description)
        
        with col2:
            # Demo metrics or image
            try:
                if os.path.exists("robo.png"):
                    demo_img = Image.open("robo.png")
                    st.image(demo_img, caption="AI-Powered Resume Analysis", use_column_width=True)
            except:
                # Fallback to text-based demo
                st.markdown("### 📊 Sample Results")
                st.success("Match Score: 89%")
                st.info("Missing Keywords: 3")
                st.warning("Suggestions: 5")
        
        # Call-to-action section
        st.markdown("---")
        st.markdown("### 🚀 Ready to Get Started?")
        
        cta_col1, cta_col2, cta_col3 = st.columns([1, 2, 1])
        
        with cta_col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 border-radius: 15px; color: white; margin: 1rem 0;">
                <h3>Start Optimizing Your Resume Today!</h3>
                <p>Join thousands of job seekers who have improved their chances</p>
            </div>
            """, unsafe_allow_html=True)
            
            signup_col, login_col = st.columns(2)
            
            with signup_col:
                if st.button("📝 Sign Up Free", use_container_width=True):
                    st.session_state.redirect_to_signup = True
                    st.rerun()
            
            with login_col:
                if st.button("🔐 Login", use_container_width=True):
                    st.session_state.redirect_to_login = True
                    st.rerun()
        
        # Testimonials section
        st.markdown("---")
        st.markdown("### 💬 What Our Users Say")
        
        testimonials = [
            ("Sarah M.", "Software Engineer", "Increased my interview rate by 300%! The AI suggestions were spot-on."),
            ("David L.", "Marketing Manager", "Finally understood why my resume wasn't getting past ATS systems."),
            ("Priya K.", "Data Scientist", "The keyword analysis helped me tailor my resume perfectly.")
        ]
        
        test_cols = st.columns(len(testimonials))
        for i, (name, role, testimonial) in enumerate(testimonials):
            with test_cols[i]:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.9); padding: 1.5rem; border-radius: 10px; 
                     border-left: 4px solid #4CAF50; margin: 0.5rem 0;">
                    <p style="font-style: italic; margin-bottom: 1rem;">"{testimonial}"</p>
                    <p style="font-weight: bold; color: #333;">- {name}</p>
                    <p style="color: #666; font-size: 0.9rem;">{role}</p>
                </div>
                """, unsafe_allow_html=True)

# Run the application
if __name__ == "__main__":
    MultiApp().run()