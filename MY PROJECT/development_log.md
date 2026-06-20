# Development Log - Vibe Coding Challenge 2026

## AI Coding Assistant
- **Assistant Used**: Gemini
- **Model**: Gemini 1.5 Pro

## Development Process
- **AI Prompts Used**: "Help me architect a RAG pipeline for SQLite," "Implement secure password hashing with bcrypt," "Draft a formal README for an auditing system."
- **Manual Modifications**: Hand-tuned the Streamlit CSS, configured the local Ollama API endpoints, and refined the prompt engineering for the Audit Agent.
- **Challenges Faced**: Resolving Python version compatibility issues with `speech_recognition` and configuring the local LLM environment.
- **Lessons Learned**: Learned how to effectively integrate local agents with SQLite for real-time auditing and the importance of dependency management in virtual environments.

## Features Implemented
- [x] Local LLM (Ollama)
- [x] RAG System
- [x] Agentic Workflow (Automated Auditor)
- [x] Voice I/O (Input/Output)
- [x] Authentication
- [x] Database Integration (SQLite)