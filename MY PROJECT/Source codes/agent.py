import ollama
import zipfile
import os
import shutil

# Explicit client configuration for stable connection
client = ollama.Client(host='http://127.0.0.1:11434')

def audit_submission(roll_no):
    # 1. Path Setup
    folder_path = os.path.join("submissions_vault", roll_no)
    extract_path = os.path.join(folder_path, "extracted")
    
    zip_file = os.path.join(folder_path, "repo.zip")
    if not os.path.exists(zip_file):
        return f"ERROR: repo.zip not found in {folder_path}"

    if os.path.exists(extract_path): shutil.rmtree(extract_path)
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(extract_path)
    
    # 2. Gather Project Content
    content = ""
    for root, dirs, files in os.walk(extract_path):
        for file in files:
            if file.endswith((".py", ".md")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        snippet = f.read()
                        content += f"\n--- File: {file} ---\n{snippet[:1000]}\n"
                except Exception:
                    continue
    
    # 3. Master Prompt (With Summary Addition)
    prompt = f"""
    ROLE: Official Grader for Vibe Coding Challenge 2026.
    TASK: Analyze this project and provide a grading table and a brief summary.
    
    TABLE SCHEMA:
    | Criteria | Status | Marks |
    | :--- | :---: | :---: |
    | Working Solution | [✅/❌] | 25 |
    | Creativity/Originality | [✅/❌] | 20 |
    | AI Usage | [✅/❌] | 15 |
    | User Interface | [✅/❌] | 10 |
    | GitHub Repo Quality | [✅/❌] | 10 |
    | Development Log | [✅/❌] | 10 |
    | Demo Video | [✅/❌] | 10 |
    
    | Bonus Criteria | Status | Marks |
    | :--- | :---: | :---: |
    | Local LLM | [+/-] | 5 |
    | Ollama | [+/-] | 5 |
    | RAG | [+/-] | 5 |
    | Agentic Workflows | [+/-] | 5 |
    | Voice I/O | [+/-] | 5 |
    | Auth | [+/-] | 5 |
    | Database | [+/-] | 5 |

    INSTRUCTIONS:
    - You must output the table exactly as requested.
    - For Main Criteria, use only [✅] for PASS and [❌] for FAIL.
    - For Bonus Criteria, use only [+] for PASS and [-] for FAIL. Do not use any other symbols.
    - Provide a 3-sentence project summary.

    PROJECT CONTENT: {content}
    """
    
    try:
        response = client.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        analysis = response['message']['content']
        
        # 4. Deterministic Parser (Strict)
        main_marks = {"Working Solution": 25, "Creativity/Originality": 20, "AI Usage": 15, "User Interface": 10, "GitHub Repo Quality": 10, "Development Log": 10, "Demo Video": 10}
        bonus_marks = {"Local LLM": 5, "Ollama": 5, "RAG": 5, "Agentic Workflows": 5, "Voice I/O": 5, "Auth": 5, "Database": 5}
        
        total_marks = 0
        lines = analysis.split('\n')
        
        for line in lines:
            for feature, mark in main_marks.items():
                if feature in line and "[✅]" in line:
                    total_marks += mark
            for feature, mark in bonus_marks.items():
                if feature in line and "[+]" in line:
                    total_marks += mark
        
        final_report = f"{analysis}\n\n**Total Marks Earned: {total_marks}/135**"
        return final_report
        
    except Exception as e:
        return f"CRITICAL ERROR during analysis: {str(e)}"