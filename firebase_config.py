import os
from dotenv import load_dotenv
try:
    import pyrebase
except ImportError:
    import pyrebase4 as pyrebase

load_dotenv()

# Use environment variables for security
firebaseConfig = {
    'apiKey': os.getenv('FIREBASE_API_KEY', "AIzaSyD92wCZBT50YChBc2eIVvVwUs7_1_XqO0A"),
    'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN', "gemini-pro-ats-resumetracker.firebaseapp.com"),
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL', "https://gemini-pro-ats-resumetracker-default-rtdb.firebaseio.com"),
    'projectId': os.getenv('FIREBASE_PROJECT_ID', "gemini-pro-ats-resumetracker"),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET', "gemini-pro-ats-resumetracker.firebasestorage.app"),
    'messagingSenderId': os.getenv('FIREBASE_MESSAGING_SENDER_ID', "466058490166"),
    'appId': os.getenv('FIREBASE_APP_ID', "1:466058490166:web:76d73846ee61c579eac397"),
    'measurementId': os.getenv('FIREBASE_MEASUREMENT_ID', "G-KB8WKFC4B8")
}

try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    db = firebase.database()
    auth = firebase.auth()
except Exception as e:
    print(f"Firebase initialization error: {e}")
    firebase = None
    db = None
    auth = None