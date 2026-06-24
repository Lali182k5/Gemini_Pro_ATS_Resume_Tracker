# 🔍 Gemini Pro ATS Resume Tracker

## 📌 Overview
**Gemini Pro ATS Resume Tracker** is a Python and Streamlit-based tool that allows users to upload resumes and analyze them against a job description. It uses rule-based processing and an AI backend to extract insights such as keyword relevance and match scores.

This project is designed to demonstrate an end-to-end resume analysis pipeline using Python, Streamlit, and AI-assisted scoring logic.

## 🎯 Purpose
Traditional resume screening can be time-consuming. This tool aims to provide *structured, explainable feedback* on how well a resume aligns with a given job description.

## 🧠 How It Works
1. The app runs a Streamlit interface (`streamlit_app.py` or `enhanced_streamlit_app.py`) which accepts:
   - Resume file (e.g., PDF, DOCX)
   - Job description text
2. Uploaded resumes are parsed and converted to text format.
3. Basic text preprocessing (lowercasing, tokenization, cleaning) is applied.
4. Rule-based keyword matching is performed between resume and job description.
5. Optional integration with an AI/LLM backend (e.g., Gemini Pro API) assists with semantic comparison and feedback generation.
6. Results are displayed on the Streamlit interface.

## 🛠️ Tech Stack
- **Python**
- **Streamlit** (UI)
- **Text processing libraries**
- **Optional AI integration (Gemini Pro)**

## 🏗 Repository Structure

    Gemini_Pro_ATS_Resume_Tracker/
    ├── streamlit_app.py # Main Streamlit UI entry point
    ├── enhanced_streamlit_app.py # Enhanced UI logic
    ├── fb.py # Firebase configuration
    ├── firebase_config.py # Firebase settings
    ├── login.py # Login flow
    ├── requirements.txt # Dependencies
    ├── logo.png / Title.jpg / Gemini.jpeg # UI assets
    ├── .env.example # Example environment config
    └── other python modules # Shared backend logic


Each module is organized to separate frontend (Streamlit) from backend logic and configuration.

## 📥 Installation & Usage

### Clone the repository
```
git clone https://github.com/Lali182k5/Gemini_Pro_ATS_Resume_Tracker.git

cd Gemini_Pro_ATS_Resume_Tracker
```

### Create and activate a virtual environment
```
python -m venv venv
```
#### macOS / Linux
```
source venv/bin/activate
```
#### Windows PowerShell
```
venv\Scripts\Activate.ps1
```

### Install dependencies
```
pip install -r requirements.txt
```

### Set up environment variables
1. Create a `.env` file (based on `.env.example`)
2. Add any required API keys (e.g., for AI backend) or config values

### Run the app
```
streamlit run streamlit_app.py
```

Open the browser link printed by Streamlit to interact with the ATS interface.

## ⚠️ Limitations
- Resume parsing depends on file formatting and may fail on poorly structured documents.
- Some modules (e.g., AI backend) may require API keys or external service setup.
- No database or backend persistence is implemented.

## 🚀 Future Improvements
- Add support for **PDF/DOCX parsing** with libraries like `PyPDF2` or `python-docx`.
- Add **backend API integration** for scoring without requiring local compute.
- Add **unit tests** for backend logic.
- Improve semantic matching by fine-tuning LLM prompts.
- Add **downloadable feedback report** (PDF/CSV).

## 📌 Key Learnings
- Building UI with Streamlit
- Isolating business logic from presentation
- Basic resume to text conversion workflows
- Designing explainable ATS analysis (keywords + scoring)

## 🤝 Contributions
Contributions are welcome.  
Fork the repository, make changes, and submit pull requests. Suggestions and issues are also appreciated.




