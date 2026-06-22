import ollama
import zipfile
import os
import shutil

client = ollama.Client(host='http://127.0.0.1:11434')

def audit_submission(roll_no, scheme_text=None, scheme_image_path=None):
    folder_path = os.path.join("submissions_vault", roll_no)
    extract_path = os.path.join(folder_path, "extracted")
    zip_file = os.path.join(folder_path, "repo.zip")
    
    if not os.path.exists(zip_file):
        return "ERROR: Repository zip not found."

    # Extracting
    if os.path.exists(extract_path): shutil.rmtree(extract_path)
    with zipfile.ZipFile(zip_file, 'r') as z: z.extractall(extract_path)
    
    # Gathering code
    content = ""
    for root, _, files in os.walk(extract_path):
        for file in files:
            if file.endswith((".py", ".md")):
                with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                    content += f"\nFILE: {file}\n{f.read(1500)}\n"

    # Rubric Logic
    if scheme_image_path:
        with open(scheme_image_path, 'rb') as f:
            resp = client.chat(model='llava', messages=[{'role': 'user', 'content': 'List criteria and their maximum marks.', 'images': [f.read()]}])
            criteria_instructions = resp['message']['content']
    else:
        criteria_instructions = scheme_text or "Default Rubric: Total 135 marks. Divide into logical categories."

    # STRICT PROMPT ENGINEERING
    prompt = f"""
    You are an AI Auditor for Vibe Coding Challenge.
    Analyze the project content strictly against these criteria: {criteria_instructions}.
    
    TOTAL MARKS ALLOWED: 135.
    
    INSTRUCTIONS:
    1. Calculate marks only based on visible evidence in the code.
    2. Output a strictly formatted Markdown table with these columns: | Criteria | Max Marks | Awarded Marks | Reasoning |
    3. You MUST ensure the sum of 'Awarded Marks' does not exceed 135.
    4. Do not hallucinate features that are not in the code.
    5. Be critical. If a feature is missing, award 0.
    
    PROJECT CONTENT:
    {content}
    
    OUTPUT:
    [TABLE]
    [3-sentence summary]
    [Total Score: X/135]
    """
    
    try:
        response = client.chat(model='llama3.2', messages=[{'role': 'user', 'content': prompt}])
        return response['message']['content']
    except Exception as e:
        return f"Audit Failed: {str(e)}"
