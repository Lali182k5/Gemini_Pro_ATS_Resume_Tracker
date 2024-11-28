    
import pyrebase
firebaseConfig = {
  'apiKey': "AIzaSyD92wCZBT50YChBc2eIVvVwUs7_1_XqO0A",
  'authDomain': "gemini-pro-ats-resumetracker.firebaseapp.com",
  'databaseURL': "https://gemini-pro-ats-resumetracker-default-rtdb.firebaseio.com",
  'projectId': "gemini-pro-ats-resumetracker",
  'storageBucket': "gemini-pro-ats-resumetracker.firebasestorage.app",
  'messagingSenderId': "466058490166",
  'appId': "1:466058490166:web:76d73846ee61c579eac397",
  'measurementId': "G-KB8WKFC4B8"
};

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()
