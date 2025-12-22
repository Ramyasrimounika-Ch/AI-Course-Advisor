# 🤖 AI Course Advisor

An AI-powered personalized learning platform that helps students go from beginner to mastery in any topic using skill gap analysis, dynamic course generation, AI-powered notes, quizzes, and progress tracking.

# 🚀 Features
# 🔐 User Authentication

-Secure login & registration system

-Password hashing

-Session-based authentication using Streamlit

# 🧠 Skill Gap Analyzer

-Asks diagnostic questions before course generation

-Uses AI to analyze learner responses

-Dynamically adjusts the effective learning level

-Prevents over/under-estimation of skill level

# 🗺️ AI-Generated Course Roadmap

-Generates chapters and subtopics based on:

-Selected topic

-Target mastery level

-Skill gap analysis

-Structured and progressive learning path

# 📝 AI Notes Generator

Generate notes for every subtopic with:

📌 Note Styles

Revision Notes

Reference Notes

Linear Notes

Practical Notes

📌 Explanation Modes

Simple (ELI5)

Exam-Oriented

Interview-Focused

📌 Smart Code Handling

If the main topic is a programming language, code examples follow that language

If code appears inside a non-programming topic, Python is used by default

Code snippets are placed exactly where relevant

📌 Extra

Download notes as PDF

Notes generation is tracked as completed learning

# 📺 YouTube Resource Generator

-Generates relevant YouTube learning links per subtopic

-Helps visual learners alongside notes

# 🤖 AI Chatbot for Doubts

-Available while studying notes

-Context-aware doubt solving

-Acts like a personal tutor inside the platform

# 📝 AI Quiz System
🔹 Subtopic Quizzes

MCQs generated directly from notes

Difficulty selection: Easy / Medium / Hard

AI explanations for wrong answers

Scores stored per subtopic

🔹 Chapter-Level Quizzes

Tests understanding of all subtopics in a chapter

Stores overall chapter quiz score

# 💾 Persistent Progress Tracking

Tracks:

-Completed subtopics

-Subtopic quiz scores

-Chapter quiz scores

Stored using a database-backed architecture

Users can resume learning across sessions

🧰 Tech Stack

Frontend: Streamlit (Multi-page app)

LLMs: Groq (LLaMA 3.1)

Framework: LangChain

Database: SQLite / MySQL

Backend Logic: Python

Auth: Password hashing + session state

# 🏗️ Project Architecture

ai_course/

│

├── main.py                ← Application Controller

│

├── pages/                 ← UI Layer (Streamlit Pages)

│     ├── login.py           ← Authentication

│     ├── notes_gen.py       ← AI Notes Generator

│     ├── quiz_platform.py  ← Subtopic Quiz Engine

│     ├── quiz_overall.py   ← Chapter-Level Quiz

│     ├── youtube_gen.py    ← YouTube Resource Generator

│     ├── progress_dashboard.py ← User Progress Viewer

│     └── last.py            ← Completion / Summary Page

│

├── src/                   ← Core Logic Layer

│     ├── topics.py          ← Skill Gap + Course Roadmap

│     ├── notes.py           ← Notes Prompt & Formatting

│     ├── quiz.py            ← MCQ Generation Logic

│     ├── progress.py        ← Progress Persistence

│     ├── youtube.py         ← Resource Generation

│     ├── download.py        ← PDF Generator

│     └── db.py              ← Database Abstraction

│

├── users.db               ← User Credentials

├── progress.db            ← Learning Progress

├── .env                   ← API Keys

└── requirements.txt

# 👩‍💻 Author

Ch. Mounika

B.Tech Student | AI & Full Stack Enthusiast
