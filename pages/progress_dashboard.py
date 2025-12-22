import streamlit as st
import pandas as pd
from src.db import get_connection

st.title("📊 Your Learning Progress")

conn = get_connection()
df = pd.read_sql("""
SELECT main_topic, chapter, subtopic,
       notes_completed,
       subtopic_quiz_score,
       chapter_quiz_score
FROM user_progress
WHERE email = %s
""", conn, params=(st.session_state["user"],))
conn.close()

st.dataframe(df)
