import streamlit as st
import os
import pandas as pd
import pyttsx3
from agent import audit_submission

# --- CONFIGURATION ---
st.set_page_config(page_title="The Ledger", layout="wide")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 8px; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- UTILITIES ---
def check_password():
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if st.session_state.authenticated: return True
    pwd = st.sidebar.text_input("Admin Password", type="password")
    if pwd == "password123":
        st.session_state.authenticated = True
        return True
    return False

def read_aloud(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# --- APP LOGIC ---
if not os.path.exists("submissions_vault"): os.makedirs("submissions_vault")

if 'main_df' not in st.session_state: st.session_state.main_df = None
if 'bonus_df' not in st.session_state: st.session_state.bonus_df = None

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
                with open(os.path.join(student_path, "repo.zip"), "wb") as f: f.write(repo_zip.getbuffer())
                st.success(f"Project submitted for {name}!")

elif role == "Admin":
    if check_password():
        tab1, tab2, tab3 = st.tabs(["🚀 Audit Student", "📊 Analytics", "📜 History Log"])
        
        with tab1:
            st.subheader("Automated Grading Engine")
            col_up1, col_up2 = st.columns(2)
            with col_up1:
                students = [d for d in os.listdir("submissions_vault") if os.path.isdir(os.path.join("submissions_vault", d))]
                selected = st.selectbox("Select Student", students)
            with col_up2:
                scheme_file = st.file_uploader("Upload Rubric (Txt/JPG/PNG)", type=["txt", "jpg", "png", "jpeg"])
            
            if st.button("Run AI Audit"):
                with st.spinner('Analyzing code via Vision AI...'):
                    scheme_text, temp_path = None, None
                    if scheme_file:
                        if scheme_file.type == "text/plain":
                            scheme_text = scheme_file.read().decode("utf-8")
                        else:
                            temp_path = f"temp_{selected}.png"
                            with open(temp_path, "wb") as f: f.write(scheme_file.getbuffer())
                    
                    report = audit_submission(roll_no=selected, scheme_text=scheme_text, scheme_image_path=temp_path)
                    st.session_state.last_report = report
                    
                    if temp_path and os.path.exists(temp_path): os.remove(temp_path)
                    
                    # Initialize with Notes column for teacher justifications
                    st.session_state.main_df = pd.DataFrame({"Criteria": ["Working Solution", "Creativity", "AI Usage", "UI", "Repo", "Log", "Video"], "Status": ["✅"]*7, "Marks": [25, 20, 15, 10, 10, 10, 10], "Notes": [""]*7})
                    st.session_state.bonus_df = pd.DataFrame({"Criteria": ["Local LLM", "Ollama", "RAG", "Agentic", "Voice", "Auth", "DB"], "Status": ["+"]*7, "Marks": [5, 5, 5, 5, 5, 5, 5], "Notes": [""]*7})
            
            if st.session_state.main_df is not None:
                st.write("### ✍️ Manual Grading Override")
                col1, col2 = st.columns(2)
                with col1: 
                    st.session_state.main_df = st.data_editor(st.session_state.main_df, column_config={"Notes": st.column_config.TextColumn("Teacher Notes")}, use_container_width=True)
                with col2: 
                    st.session_state.bonus_df = st.data_editor(st.session_state.bonus_df, column_config={"Notes": st.column_config.TextColumn("Teacher Notes")}, use_container_width=True)
                
                # Real-time score calculation
                total = st.session_state.main_df['Marks'].sum() + st.session_state.bonus_df['Marks'].sum()
                st.metric("Final Adjusted Score", f"{total} / 135")
                
                if st.button("💾 Save Final Grades"): st.success(f"Final grade {total} saved for {selected}!")
                st.markdown("---")
                st.subheader("AI Feedback Summary")
                st.markdown(st.session_state.last_report)
                if st.button("🔊 Read Summary"): read_aloud(st.session_state.last_report)

        with tab2:
            st.subheader("Performance Analytics")
            if st.session_state.main_df is not None: st.bar_chart(pd.concat([st.session_state.main_df, st.session_state.bonus_df]).set_index("Criteria")["Marks"])
        
        with tab3:
            st.subheader("Transaction Ledger")
            if st.session_state.main_df is not None: st.table(pd.concat([st.session_state.main_df, st.session_state.bonus_df]))
    else:
        st.warning("Enter password to access Admin Panel.")
