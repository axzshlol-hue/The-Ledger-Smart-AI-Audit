import streamlit as st
import sqlite3
import speech_recognition as sr
import pyttsx3
import os
from agent import audit_submission

# --- CUSTOM AUTHENTICATION ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    pwd = st.sidebar.text_input("Admin Password", type="password")
    if pwd == "password123":
        st.session_state.authenticated = True
        return True
    return False

st.title("The Ledger: Official Portal for auditing and submissions")

# --- UTILITIES ---
def query_ledger(user_query):
    return "AI-generated summary based on your ledger database."

def read_aloud(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- MAIN APP LOGIC ---
if not os.path.exists("submissions_vault"):
    os.makedirs("submissions_vault")

role = st.sidebar.selectbox("Login as", ["Student", "Admin"])

if role == "Student":
    st.subheader("Submit Your Project Files")
    with st.form("submission_form"):
        name = st.text_input("Student Name / Roll No")
        repo_zip = st.file_uploader("Upload GitHub Repository (.zip)", type="zip")
        demo_url = st.text_input("Demo Video URL")
        
        if st.form_submit_button("Submit Project"):
            if name and repo_zip and demo_url:
                student_path = os.path.join("submissions_vault", name)
                os.makedirs(student_path, exist_ok=True)
                with open(os.path.join(student_path, "repo.zip"), "wb") as f:
                    f.write(repo_zip.getbuffer())
                with open(os.path.join(student_path, "README.md"), "a") as f:
                    f.write(f"\n## Demo Video\n{demo_url}\n")
                st.success(f"Project submitted for {name}!")

elif role == "Admin":
    if check_password():
        st.subheader("Admin Auditor Panel")
        students = [d for d in os.listdir("submissions_vault") if os.path.isdir(os.path.join("submissions_vault", d))]
        selected = st.selectbox("Select Student to Audit", students)
        
        if st.button("Query Ledger Data"):
            st.write(query_ledger("Show me recent transactions"))
            
        if st.button("Run Audit"):
            with st.spinner('Auditing in progress...'):
                report = audit_submission(selected)
                st.session_state.last_report = report
            
        if "last_report" in st.session_state:
            st.markdown(st.session_state.last_report)
            
        if st.button("🔊 Read Summary Aloud"):
            if 'last_report' in st.session_state:
                read_aloud(st.session_state.last_report)
            else:
                st.warning("Please run an audit first.")
    else:
        st.warning("Please enter admin password to continue.")