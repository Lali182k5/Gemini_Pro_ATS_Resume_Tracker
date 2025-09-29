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
try:
    from pyrebase import initialize_app
except ImportError:
    from pyrebase4 import initialize_app
import login
import signup
from firebase_config import firebaseConfig, firebase, auth, db

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#genai.configure(api_key="AIzaSyBwDgcn8cpV0x7DjtivK0o9iXi8lk9Q-KM")
model = genai.GenerativeModel('gemini-pro')
# Configure tesseract path based on OS
import platform
import shutil

# Auto-detect tesseract installation
tesseract_path = shutil.which('tesseract')
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
elif platform.system() == 'Windows':
    # Windows default installation paths
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    ]
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break
else:
    # For Linux/Mac, tesseract should be in PATH
    pass

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text()
    return extracted_text

def extract_text_from_docx(file):
    doc = Document(file)
    extracted_text = ""
    for para in doc.paragraphs:
        extracted_text += para.text + "\n"
    return extracted_text

def extract_text_from_image(file):
    image = Image.open(file)
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

def calculate_tfidf(jd, resume):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([jd, resume])
    feature_names = vectorizer.get_feature_names_out()
    dense = vectors.todense()
    denselist = dense.tolist()
    return denselist, feature_names

def find_missing_keywords(jd, resume):
    jd_keywords = set(jd.split())
    resume_keywords = set(resume.split())
    missing_keywords = jd_keywords - resume_keywords
    return missing_keywords

def app():
    col1, col2, col3 = st.columns([3,2,1])
    def logout():
        login.setState(False)
        signup.setState(False)
    with col3:
        st.button("Logout", on_click=logout)
    #st.set_page_config(page_title="Gemini Pro ATS Resume Tracker", page_icon=":robot:")
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://e0.pxfuel.com/wallpapers/219/656/desktop-wallpaper-purple-color-background-best-for-your-mobile-tablet-explore-color-cool-color-colored-background-one-color-aesthetic-one-color.jpg");
    background-size: 450%;
    background-position: top left;
    background-repeat: no repeat;
    background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}

    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    [data-testid="stAppViewBlockContainer"] {{
    max-width: 76rem;
    }}
    </style>
    """
    #C:\Users\micro\ATS22\Demo\robo.png
    st.markdown(page_bg_img, unsafe_allow_html=True)
    # Prompt Template
    input_prompt = """
    You are a skilled and very experienced ATS (Application Tracking System) with a deep understanding of tech fields, software engineering,
    data science, data analysis, and big data engineering. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide the best assistance for improving the resumes. 
    Assign the percentage Matching based on Job description and the missing keywords with high accuracy.
    Resume: {extracted_text}
    Description: {jd}

    I want the only response in 3 sectors as follows:
    • Job Description Match: \n
    • Missing Keywords: \n
    • Profile Summary: \n
    """

    # HTML and CSS for centering the title
    html_code = """
    <style>
        .centered-title {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 60vh;
            font-family: Arial, sans-serif;
            font-size: 2em;
            color: yellow;
            font-family: 'Arial', sans-serif; 
            font-weight:bold;
    # font-size: 24px;  
    # color: #007bff; /* Blue color */  
        }
    </style>
    <div class="centered-title"><h1>🔥GEMINI PRO ATS RESUME TRACKER🔥</h1></div>
    """
    # Display the HTML code in Streamlit
    st.markdown(html_code, unsafe_allow_html=True)
    col1, col2 = st.columns([3, 2])
    with col1:
        st.header(" Revolutionize Your Job Search!")
        st.markdown("""<p style='text-align: justify;'>
                    Introducing GEMINI PRO, your ultimate tool for crafting the perfect job application. Harnessing cutting-edge ATS technology, GEMINI PRO offers deep insights into how well your resume matches job descriptions, ensuring you always stand out. From refining your resume to boosting your skill set and providing clear career guidance, GEMINI PRO equips you to excel in today's competitive job market. Simplify your job search, elevate your qualifications, and confidently navigate your career path. Join GEMINI PRO today and unlock new heights in your professional journey! With features like resume optimization, skill enhancement, career progression guidance, and real-time feedback, GEMINI PRO is designed to streamline your job application process and help you achieve professional success. Discover the difference with GEMINI PRO and take the first step towards your dream job. Get started with GEMINI PRO today and discover new heights in your professional journey!</p>""", unsafe_allow_html=True)
    with col2:
        st.image('https://cdn.dribbble.com/userupload/12500996/file/original-b458fe398a6d7f4e9999ce66ec856ff9.gif', use_column_width=True)

    avs.add_vertical_space(10)

    col1, col2 = st.columns([3,2])
    with col2:
        st.header("Wide Range of Offerings")
        st.write('ATS-Optimized Resume Analysis')
        st.write('Resume Optimization')
        st.write('Skill Enhancement')
        st.write('Career progression Guidance')
        st.write('Tailored profile Summaries')
        st.write('Streamlined Application Process')
        st.write('Personalized Recommendations')
        st.write('Efficient Career Navigation')

    with col1:
        imgl = Image.open("robo.png")
        st.image(imgl, width=500)
    avs.add_vertical_space(10)
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown("<h1 style='text-align: left; '>Embark on Your Career Adventure</h1>", unsafe_allow_html=True)
        jd = st.text_area("Paste the Job Description")
        uploaded_file = st.file_uploader("Upload your Resume", type=["pdf", "docx", "png", "jpeg"])
        submit = st.button("Submit", key="submit_button")
    with col2:
        imgl = Image.open("Logo.jfif")
        st.image(imgl, width=400)

    if submit:
        if uploaded_file is not None:
            file_type = uploaded_file.type
            if file_type == "application/pdf":
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                extracted_text = extract_text_from_docx(uploaded_file)
            elif file_type in ["image/png", "image/jpeg"]:
                extracted_text = extract_text_from_image(uploaded_file)
            else:
                st.error("Unsupported file type")
                return
            tfidf_values, feature_names = calculate_tfidf(jd, extracted_text)
            missing_keywords = find_missing_keywords(jd, extracted_text)
       
            try:
                response = model.generate_content(input_prompt.format(extracted_text=extracted_text, jd=jd))
                st.markdown('<h8 style="color: lightgreen;text-align: center;">File uploaded successfully!</h8>', unsafe_allow_html=True)
                st.write(response.text)
                #st.write("Missing Keywords:", missing_keywords)
            except InvalidArgument as e:
                st.error(f"InvalidArgument error: {e}")
                # Log more details if needed
                print(f"Error details: {e}")
           # st.markdown('<h8 style="color: lightgreen;text-align: center;">File uploaded successfully!</h8>', unsafe_allow_html=True)
        else:
            st.error("Please upload a file")
            st.markdown('<h8 style="color: red;text-align: center;">Please upload your Resume!</h8>', unsafe_allow_html=True)

    avs.add_vertical_space(15)
    col1, col2 = st.columns([2, 3])
    with col2:
        st.markdown("<h1 style='text-align: center;'>FAQ</h1>", unsafe_allow_html=True)
        with  st.expander("Question: How does ATS analyze resumes and job descriptions?"):
            st.write('''Answer: Gemini Pro uses advanced algorithms to analyze resumes and job descriptions, identifying keywords and assessing compatibility between the two.''')
        with  st.expander("Question: Can Gemini Pro ATS suggest improvements for my resume?"):
            st.write('''Answer: Yes, It provides personalized recommendations to optimize your resume for specific job openings, including suggestions for missing keywords and alignment with desired job roles.''')
        with  st.expander("Question: Is Gemini Pro Resume tracker suitable for both entry-level and experienced professionals?"):
            st.write('''Answer: Absolutely! It caters to job seekers at all career stages, offering tailored insights and guidance to enhance their resumes and advance their careers.''')
        
    with col1:
        file_ = open("resume2.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="resume2.gif">',unsafe_allow_html=True)
