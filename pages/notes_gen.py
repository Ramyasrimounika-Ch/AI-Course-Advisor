from src.notes import notes_generate
from src.download import pdf
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from src.progress import mark_notes_completed

load_dotenv()

if "Notes" not in st.session_state:
    st.session_state["Notes"]=None
if "Notes_subtopic" not in st.session_state:
    st.session_state["Notes_subtopic"] = None
if "Notes_style" not in st.session_state:
    st.session_state["Notes_style"] = ""   
if "download_name" not in st.session_state:
    st.session_state["download_name"] = "notes.pdf"       

st.title("Notes generation page")
sub = st.session_state.get("subtopic")
key = st.session_state.get("last_clicked") 
 
if sub is None:
    st.warning("no topic to generate note")
else:
    note_type = st.selectbox(
        "Select Note Type",
        [
            "Revision Notes",
            "Reference Notes",
            "Linear Notes",
            "Practical Notes"
        ],
        key=f"{sub}_note_type"
    )
    explain_style = st.selectbox(
        "Explain As",
        [
            "Simple",
            "Exam-Oriented",
            "Interview-Focused"
        ],
        key=f"{sub}_explain_style"
    )
    current_style = {
       "note_type": note_type,
       "explain_style": explain_style
    }
    st.info("If their is notes before clicking the generate notes button,then it is previous topic notes for this topic notes enter the notes_style and click the below button")
    if st.button("generate notes") and (st.session_state["Notes"] is None or st.session_state["Notes_subtopic"] != sub or st.session_state["Notes_style"] != current_style):
        st.session_state["Notes_subtopic"] = sub 
        st.session_state["Notes_style"] = current_style
        st.session_state["Notes"] = notes_generate(st.session_state["main_topic"],st.session_state["Notes_subtopic"],note_type,explain_style,st.session_state["level"])

    if st.session_state["Notes"]:    
        st.write(st.session_state["Notes"])
        
        st.session_state["download_name"] = st.text_input(
            "Enter PDF file name",
            value=st.session_state["download_name"],
            key=f"{sub}_filename"
        )
        if not st.session_state["download_name"].endswith(".pdf"):
            st.session_state["download_name"] += ".pdf"
        
        pdf_file = pdf(st.session_state["Notes"])
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name=st.session_state["download_name"],
            mime="application/pdf"
        )
        mark_notes_completed(
            email=st.session_state["user"],
            main_topic=st.session_state["main_topic"],
            chapter=st.session_state["chapter"],
            subtopic=sub
        )
    if st.button("quiz"):
        st.session_state["message_to_quiz"]=sub
        #st.session_state["quiz_level"]=st.session_state["level"]
        st.switch_page("pages/quiz_platform.py")

want_chatbot = st.sidebar.checkbox("🤖 Chat with AI")

if want_chatbot:
    st.sidebar.write("Clarify doubts with Chatbot")
    ques = st.sidebar.text_area("Enter your question:")

    if ques:
        llm = ChatGroq(
            model="llama-3.1-8b-instant"
        )
        res = llm.invoke(ques)
        st.sidebar.write("### 🤖 Chatbot Answer:")
        st.sidebar.write(res.content)  # display clean text
        