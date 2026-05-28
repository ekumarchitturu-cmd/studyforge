# 🎓 StudyForge - AI Study Planner

## Overview
StudyForge is a universal AI-powered study planner that creates personalized learning plans for students of all ages, fields, and levels.

## Features
- ✅ Universal support (Law, Medicine, Engineering, Commerce, Arts, Design, etc.)
- ✅ Adaptive AI (adjusts to age, field, level)
- ✅ Credit system (100 free credits)
- ✅ Beautiful web interface
- ✅ Download study plans

## Tech Stack
- Frontend: Streamlit
- Backend: Python
- AI: OpenAI GPT-4
- Database: SQLite
- Hosting: Streamlit Cloud

## Local Setup

1. Clone repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create `.env` file with:
   ```
   OPENAI_API_KEY=your-key-here
   ```
5. Run app:
   ```bash
   streamlit run app.py
   ```

## Deployment

Deployed on Streamlit Cloud

## Contact
support@studyforge.com

## License
MIT License
