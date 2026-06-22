# Development Log - Vibe Coding Challenge 2026
**Project: The Ledger (AI-Powered Auditing Portal)**
### AI Coding Assistant
 * **Assistant Used:** Gemini
 * **Model:** Gemini 1.5 Pro
### Development Process
 * **AI Prompts Used:** "Create a strict schema output for grading tables in agent.py," "Enhance Streamlit dashboard layout using container-based styling," and "Refactor project architecture to include a modular agentic audit engine."
 * **Manual Modifications:** Manually integrated custom CSS for a professional "card-based" UI, implemented dynamic column configuration for teacher notes, and hard-coded the automatic rubric discovery logic for the submissions_vault.
 * **Challenges Faced:** Resolving Mermaid.js rendering errors in the README and managing session state volatility when switching between Admin and Student roles in the dashboard.
 * **Lessons Learned:** Mastered the integration of multi-modal vision models (LLAVA) for rubric extraction and the importance of deterministic prompt engineering for grading accuracy.
### Features Implemented
 * **Local LLM (Ollama):** Full integration with llama3.2 and llava for local, private auditing.
 * **RAG System:** Contextual snippet extraction from zipped student repositories.
 * **Agentic Workflow (Automated Auditor):** Autonomous agent with strict schema-constrained output.
 * **Voice I/O (Input/Output):** Integrated pyttsx3 for hands-free report generation.
 * **Authentication:** Secure session-state password protection for Admin access.
 * **Database Integration (SQLite):** Persistent data storage for audit history and teacher overrides.
 * **Pro-Grade Editor:** Dynamic manual override table with Teacher Notes justification column.
