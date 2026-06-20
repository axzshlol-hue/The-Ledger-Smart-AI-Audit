# The Ledger: AI-Powered Auditing Portal
## Vibe Coding Challenge 2026 | Applied AI Summer Internship

The Ledger is an intelligent, agentic auditing platform designed for automated code analysis, secure transaction tracking, and voice-controlled interaction.

---

## 🚀 Technical Architecture & Features
* **Agentic Audit Engine (`agent.py`)**: Uses a custom grading agent powered by **Ollama (Llama 3.2)** to autonomously analyze project structures, parse code snippets, and calculate deterministic scores based on a rubric.
* **Semantic Ledger System**: Built using **SQLite** to manage project metadata and transaction history, accessible via natural language queries.
* **Voice-First Interaction**: Integrated `speech_recognition` (input) and `pyttsx3` (output) for hands-on, accessible administrative reporting.
* **Admin Security**: Features robust **Custom Authentication** middleware to protect sensitive auditing panels.
* **Local-First Processing**: The entire RAG and LLM workflow runs locally, ensuring data privacy and offline capability.

---

## 💎 Bonus Criteria Compliance
We have implemented the following features to qualify for the **Bonus Marks**:

| Feature | Implementation Details |
| :--- | :--- |
| **Local LLM** | Fully offline Llama 3.2 integration via Ollama. |
| **Ollama** | Native API communication for prompt-driven auditing. |
| **RAG Systems** | Semantic query integration with SQLite ledger database. |
| **Agentic Workflows** | Automated grading agent with multi-step logic. |
| **Voice I/O** | `speech_recognition` for commands, `pyttsx3` for reports. |
| **Authentication** | Secure session-state password protection for Admin access. |
| **Database** | SQLite-based persistence for audit and transaction records. |

---

## 📝 Compliance & Evaluation
As required by the **Evaluation Rule**, this project is built for transparency:
1. **Application Logic**: Automates rubric-based grading via autonomous agents.
2. **Architecture**: Streamlit UI -> Agentic Logic -> Ollama API -> Local Database.
3. **Prompting Strategy**: Focused on strict, deterministic schema output for grading.
4. **Challenges Faced**: Resolved local socket binding conflicts and Streamlit session state volatility.
5. **Future Improvements**: Planned migration to multi-agent swarm architecture for deeper code-base analysis.

---

## 🎥 Project Demo
**[▶️ Watch the Live Demo Here (YouTube/Drive Link)](https://drive.google.com/file/d/1E5mbcaha9YGZu3TzZI7XURpi0zxm0lrH/view?usp=drivesdk)**

---

## 🛠 Installation & Deployment
1. **Clone**: `git clone [https://github.com/axzshlol-hue/The-Ledger-Smart-AI-Audit.git]`
2. **Install**: `pip install -r requirements.txt`
3. **Run**: `streamlit run app.py`

---

## 📂 Documentation
- **`development_log.md`**: Tracks the progression of the AI assistant setup, challenges, and lessons.
- **`requirements.txt`**: Complete dependency environment.
