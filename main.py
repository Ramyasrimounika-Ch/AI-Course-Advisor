import streamlit as st
from langchain_groq import ChatGroq
from src.topics import topic_chain, change_format, skill_gap_questions, generate_student_profile
from dotenv import load_dotenv
import os
load_dotenv()

if "user" not in st.session_state:
    st.switch_page("pages/login.py")

# ---------------- SESSION STATE ----------------
if "level" not in st.session_state:
    st.session_state["level"] = None
if "main_topic" not in st.session_state:
    st.session_state["main_topic"] = None    
if "effective_level" not in st.session_state:
    st.session_state["effective_level"] = None
if "structured_chapters" not in st.session_state:
    st.session_state["structured_chapters"] = None
if "assessment_done" not in st.session_state:
    st.session_state["assessment_done"] = False

# ---------------- UI ----------------
st.header("🤖 AI COURSE ADVISOR")

topic = st.text_input("Enter the topic you want to learn")
st.session_state["main_topic"] = topic
st.session_state["level"] = st.selectbox(
    "Select the level you want to master",
    ["Beginner", "Intermediate", "Advanced"]
)
if st.sidebar.button("📊 View Progress"):
    st.switch_page("pages/progress_dashboard.py")

# ---------------- SKILL GAP ANALYZER ----------------
st.subheader("🧠 Skill Gap Assessment (Recommended)")

questions = skill_gap_questions(topic)

answers = []
for i, q in enumerate(questions):
    ans = st.text_area(q, key=f"q_{i}")
    answers.append(ans)

if st.button("Assess My Level"):
    st.session_state["effective_level"] = generate_student_profile(
        st.session_state["level"], answers
    )
    st.session_state["assessment_done"] = True

if st.session_state["assessment_done"]:
    st.success(
        f"Personalized learning level identified: "
        f"**{st.session_state['effective_level']}**"
    )

# ---------------- GENERATE TOPICS ----------------
if st.session_state["assessment_done"]:
    if st.button("Generate Topics"):
        response = topic_chain.invoke(
            {
                "topic": topic,
                "target_level": st.session_state["level"],
                "student_profile":st.session_state['effective_level']
            }
        )

        llm_response = response["chapters"]
        st.session_state["structured_chapters"] = change_format(llm_response)

# ---------------- DISPLAY CONTENT ----------------
if st.session_state["structured_chapters"]:
    structured_chapters = st.session_state["structured_chapters"]

    for chap in structured_chapters:
        st.subheader(f"{chap['chapter']}. {chap['title']}")

        for sub in chap["subtopics"]:
            st.write(f"- {sub}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Generate notes for {sub}", key=f"notes_{sub}"):
                    st.session_state["chapter"]=chap['title']
                    st.session_state["subtopic"] = sub
                    st.switch_page("pages/notes_gen.py")

            with col2:
                if st.button(f"YouTube resources for {sub}", key=f"yt_{sub}"):
                    st.session_state["chapter"]=chap['title']
                    st.session_state["subtopic"] = sub
                    st.switch_page("pages/youtube_gen.py")

        st.subheader(f"Overall quiz on {chap['title']}")
        if st.button("Take Quiz", key=f"quiz_{chap['chapter']}"):
            st.session_state["message_to_overall"] = chap["title"]
            st.switch_page("pages/overall.py")

# ---------------- CHATBOT ----------------
want_chatbot = st.sidebar.checkbox("🤖 Chat with AI")

if want_chatbot:
    ques = st.sidebar.text_area("Ask your doubt")

    if ques:
        llm=ChatGroq( api_key="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", model="llama-3.1-8b-instant" )
        res = llm.invoke(ques)
        st.sidebar.write(res.content)

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/login.py")
