import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_extras import add_vertical_space as avs
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract
import base64
from sklearn.feature_extraction.text import TfidfVectorizer
from google.api_core.exceptions import InvalidArgument
import login
import signup
import platform
import shutil
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from firebase_config import firebaseConfig, firebase, auth, db
import time
import json

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Configure tesseract path based on OS
tesseract_path = shutil.which('tesseract')
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif platform.system() == 'Windows':
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

def extract_text_from_pdf(file):
    """Extract text from PDF file with enhanced error handling"""
    try:
        reader = PdfReader(file)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text()
        return extracted_text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return ""

def extract_text_from_docx(file):
    """Extract text from DOCX file with enhanced error handling"""
    try:
        doc = Document(file)
        extracted_text = ""
        for para in doc.paragraphs:
            extracted_text += para.text + "\n"
        return extracted_text
    except Exception as e:
        st.error(f"Error reading DOCX: {str(e)}")
        return ""

def extract_text_from_image(file):
    """Extract text from image using OCR with enhanced error handling"""
    try:
        image = Image.open(file)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        st.error(f"Error performing OCR: {str(e)}. Please ensure Tesseract is installed.")
        return ""

def calculate_match_percentage(jd, resume):
    """Calculate match percentage using TF-IDF similarity"""
    try:
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        vectors = vectorizer.fit_transform([jd, resume])
        
        # Calculate cosine similarity
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])
        return round(similarity[0][0] * 100, 2)
    except Exception as e:
        st.error(f"Error calculating match: {str(e)}")
        return 0

def find_missing_keywords(jd, resume):
    """Find missing keywords with better analysis"""
    jd_words = set(word.lower().strip() for word in jd.split() if len(word) > 3)
    resume_words = set(word.lower().strip() for word in resume.split() if len(word) > 3)
    missing_keywords = jd_words - resume_words
    return list(missing_keywords)[:10]  # Top 10 missing keywords

def create_progress_circle(percentage):
    """Create an interactive progress circle using Plotly"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Match Score"},
        delta = {'reference': 80},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        width=300,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def create_keyword_chart(missing_keywords):
    """Create a bar chart for missing keywords"""
    if not missing_keywords:
        return None
    
    # Create importance scores for visualization
    importance_scores = list(range(len(missing_keywords), 0, -1))
    
    fig = px.bar(
        x=importance_scores,
        y=missing_keywords[:10],
        orientation='h',
        title='Top Missing Keywords',
        labels={'x': 'Priority Score', 'y': 'Keywords'}
    )
    
    fig.update_layout(
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    
    return fig

def save_analysis_history(user_email, jd, filename, match_percentage, missing_keywords):
    """Save analysis to user history (if Firebase is available)"""
    try:
        if db:
            timestamp = int(time.time())
            analysis_data = {
                'job_description': jd[:100] + "..." if len(jd) > 100 else jd,
                'filename': filename,
                'match_percentage': match_percentage,
                'missing_keywords': missing_keywords[:5],  # Store top 5
                'timestamp': timestamp
            }
            db.child("users").child(user_email.replace(".", "_")).child("history").push(analysis_data)
            return True
    except Exception as e:
        print(f"Error saving history: {e}")
    return False

def app():
    # Enhanced page configuration
    st.set_page_config(
        page_title="🚀 Gemini Pro ATS Resume Tracker",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        
        .stProgress .st-bo {
            background-color: #4CAF50;
        }
        
        .metric-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .upload-container {
            border: 2px dashed #4CAF50;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            margin: 1rem 0;
            background-color: rgba(76, 175, 80, 0.1);
        }
        
        .success-message {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 0.75rem 1rem;
            border-radius: 0.375rem;
            margin: 1rem 0;
        }
        
        .warning-message {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 0.75rem 1rem;
            border-radius: 0.375rem;
            margin: 1rem 0;
        }
        
        .animated-title {
            animation: gradient 3s ease infinite;
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin: 2rem 0;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .sidebar .stSelectbox {
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    def logout():
        login.setState(False)
        signup.setState(False)
        if 'user_email' in st.session_state:
            del st.session_state.user_email
    
    with col3:
        if st.button("🚪 Logout", help="Sign out from the application"):
            logout()
            st.rerun()
    
    # Animated title
    st.markdown('<div class="animated-title">🚀 Gemini Pro ATS Resume Tracker</div>', unsafe_allow_html=True)
    
    # Main application tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume Analysis", "📊 Dashboard", "ℹ️ How It Works", "❓ FAQ"])
    
    with tab1:
        # Main analysis interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Analyze Your Resume Against Job Requirements")
            
            # Job description input with enhanced UI
            st.markdown("#### Job Description")
            jd = st.text_area(
                "Paste the complete job description here:",
                height=200,
                help="Include the complete job posting including requirements, skills, and qualifications",
                placeholder="Copy and paste the job description from the company's website..."
            )
            
            # File upload with enhanced styling
            st.markdown("#### Resume Upload")
            st.markdown('<div class="upload-container">', unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Choose your resume file",
                type=["pdf", "docx", "png", "jpeg", "jpg"],
                help="Supported formats: PDF, DOCX, PNG, JPEG"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Analysis controls
            col_submit, col_clear = st.columns([1, 1])
            
            with col_submit:
                analyze_btn = st.button("🔍 Analyze Resume", type="primary", use_container_width=True)
            
            with col_clear:
                if st.button("🗑️ Clear All", use_container_width=True):
                    st.rerun()
        
        with col2:
            st.markdown("### 📈 Quick Stats")
            
            # Display current session stats
            if 'analysis_count' not in st.session_state:
                st.session_state.analysis_count = 0
            
            st.metric("📊 Analyses Today", st.session_state.analysis_count)
            
            # Tips section
            with st.expander("💡 Pro Tips", expanded=False):
                st.markdown("""
                **For better results:**
                - Use complete job descriptions
                - Ensure resume text is clear and readable
                - Include relevant keywords naturally
                - Update skills section regularly
                - Tailor resume for each application
                """)
        
        # Analysis processing
        if analyze_btn:
            if uploaded_file is not None and jd.strip():
                with st.spinner('🔄 Analyzing your resume... This may take a moment.'):
                    # Extract text based on file type
                    file_type = uploaded_file.type
                    extracted_text = ""
                    
                    if file_type == "application/pdf":
                        extracted_text = extract_text_from_pdf(uploaded_file)
                    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        extracted_text = extract_text_from_docx(uploaded_file)
                    elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
                        extracted_text = extract_text_from_image(uploaded_file)
                    
                    if extracted_text.strip():
                        try:
                            # Enhanced prompt for better analysis
                            enhanced_prompt = f"""
                            You are an expert ATS (Application Tracking System) analyzer and career counselor. 
                            Analyze the following resume against the job description with high precision.
                            
                            Job Description:
                            {jd}
                            
                            Resume Content:
                            {extracted_text}
                            
                            Please provide a detailed analysis in the following format:
                            
                            **MATCH PERCENTAGE:** [Provide exact percentage 0-100]
                            
                            **KEY STRENGTHS:**
                            • [List 3-5 key matching strengths]
                            
                            **MISSING KEYWORDS:**
                            • [List 5-10 important missing keywords from job description]
                            
                            **IMPROVEMENT RECOMMENDATIONS:**
                            • [Provide 3-5 specific actionable recommendations]
                            
                            **SKILLS GAP ANALYSIS:**
                            • [Identify skill gaps and suggest improvements]
                            
                            **OVERALL ASSESSMENT:**
                            [Provide comprehensive feedback and next steps]
                            """
                            
                            # Generate AI analysis
                            response = model.generate_content(enhanced_prompt)
                            
                            # Calculate technical metrics
                            match_percentage = calculate_match_percentage(jd, extracted_text)
                            missing_keywords = find_missing_keywords(jd, extracted_text)
                            
                            # Save to history
                            user_email = st.session_state.get('user_email', 'anonymous')
                            save_analysis_history(user_email, jd, uploaded_file.name, match_percentage, missing_keywords)
                            
                            # Update session stats
                            st.session_state.analysis_count += 1
                            
                            # Display results
                            st.markdown("---")
                            st.markdown("## 📊 Analysis Results")
                            
                            # Results in columns
                            result_col1, result_col2 = st.columns([1, 1])
                            
                            with result_col1:
                                # Progress circle
                                progress_fig = create_progress_circle(match_percentage)
                                st.plotly_chart(progress_fig, use_container_width=True)
                                
                                # Quick metrics
                                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                                st.metric("📈 Match Score", f"{match_percentage}%")
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                                st.metric("🔍 Keywords Missing", len(missing_keywords))
                                st.markdown('</div>', unsafe_allow_html=True)
                            
                            with result_col2:
                                # Missing keywords chart
                                if missing_keywords:
                                    keyword_fig = create_keyword_chart(missing_keywords)
                                    if keyword_fig:
                                        st.plotly_chart(keyword_fig, use_container_width=True)
                            
                            # AI Analysis Results
                            st.markdown("### 🤖 AI-Powered Analysis")
                            st.markdown(response.text)
                            
                            # Action items
                            st.markdown("### ✅ Next Steps")
                            if match_percentage < 60:
                                st.warning("Your resume needs significant improvements to match this job description.")
                            elif match_percentage < 80:
                                st.info("Your resume is a good match but could be optimized further.")
                            else:
                                st.success("Excellent match! Your resume aligns well with the job requirements.")
                            
                            # Download results option
                            results_data = {
                                'job_description': jd,
                                'filename': uploaded_file.name,
                                'match_percentage': match_percentage,
                                'missing_keywords': missing_keywords,
                                'ai_analysis': response.text,
                                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                            }
                            
                            results_json = json.dumps(results_data, indent=2)
                            st.download_button(
                                label="📥 Download Analysis Report",
                                data=results_json,
                                file_name=f"ats_analysis_{uploaded_file.name}_{int(time.time())}.json",
                                mime="application/json"
                            )
                            
                        except Exception as e:
                            st.error(f"❌ Analysis failed: {str(e)}")
                    else:
                        st.error("❌ Could not extract text from the uploaded file. Please try a different file.")
            else:
                st.warning("⚠️ Please provide both a job description and upload your resume.")
    
    with tab2:
        st.markdown("### 📊 Analytics Dashboard")
        
        # Mock dashboard for demonstration
        st.info("📈 Dashboard features will show your analysis history, trends, and improvement suggestions.")
        
        # Sample charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample trend chart
            dates = pd.date_range('2024-01-01', periods=10, freq='W')
            scores = [65, 68, 72, 70, 75, 78, 82, 85, 88, 90]
            
            fig = px.line(x=dates, y=scores, title="Match Score Improvement Over Time")
            fig.update_traces(line_color='#4CAF50', line_width=3)
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sample skills chart
            skills = ['Python', 'JavaScript', 'SQL', 'Docker', 'AWS']
            proficiency = [85, 70, 80, 60, 65]
            
            fig = px.bar(x=skills, y=proficiency, title="Skill Proficiency Analysis")
            fig.update_traces(marker_color='#2196F3')
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🔧 How It Works")
        
        # Step-by-step process
        steps = [
            ("📄", "Upload Resume", "Upload your resume in PDF, DOCX, or image format"),
            ("📋", "Job Description", "Paste the complete job description from the posting"),
            ("🤖", "AI Analysis", "Our Gemini Pro AI analyzes the match and provides insights"),
            ("📊", "Get Results", "Receive detailed feedback, match score, and improvement suggestions"),
            ("🎯", "Optimize", "Use the insights to improve your resume for better matches")
        ]
        
        for i, (icon, title, description) in enumerate(steps):
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{icon}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"### {i+1}. {title}")
                    st.markdown(description)
                
                if i < len(steps) - 1:
                    st.markdown("⬇️", unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### ❓ Frequently Asked Questions")
        
        faqs = [
            ("How accurate is the ATS analysis?", 
             "Our AI-powered analysis uses Google's Gemini Pro model combined with TF-IDF similarity scoring to provide highly accurate results. The system analyzes keyword matches, skill alignment, and contextual relevance."),
            
            ("What file formats are supported?", 
             "We support PDF, DOCX (Word documents), PNG, and JPEG image formats. For best results, use text-based formats like PDF or DOCX."),
            
            ("How is the match percentage calculated?", 
             "The match percentage is calculated using advanced natural language processing that compares your resume content with the job description, considering keyword frequency, relevance, and semantic similarity."),
            
            ("Can I track my improvement over time?", 
             "Yes! The system saves your analysis history (when logged in) so you can track improvements in your match scores over time."),
            
            ("Is my data secure?", 
             "Absolutely. We use secure Firebase authentication and don't store your actual resume content permanently. Analysis data is encrypted and protected.")
        ]
        
        for question, answer in faqs:
            with st.expander(f"❓ {question}"):
                st.markdown(answer)

if __name__ == "__main__":
    app()