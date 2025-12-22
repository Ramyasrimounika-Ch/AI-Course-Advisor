from src.quiz import generate_quiz
import streamlit as st
from langchain.prompts import PromptTemplate
from src.progress import save_subtopic_quiz_score
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
            model="llama-3.1-8b-instant"
        )

correct_template = """
You are an excellent explainer. You are given an MCQ question: {mcq}, 
with the options: {options}, and the correct answer: {correct}. 
The user has selected the wrong option {selected}. Your duty is to explain clearly 
why the correct answer is right and why the selected option is incorrect 
in a simple, step-by-step way that helps the user understand.
"""

prompt=PromptTemplate(
    input_variables=["mcq","options","correct","selected"],
    template=correct_template
)
chain=LLMChain(llm=llm,prompt=prompt)

def llm_response(mcq,options,correct,selected):
    res=chain.invoke({
        "mcq":mcq,
        "options":options,
        "correct":correct,
        'selected':selected
    })
    st.write(res['text'])

def generate_mcqs(Notes, level):
    """Generate quiz and reset session state."""
    with st.spinner("Generating MCQs..."):
        quiz = generate_quiz(Notes, level)
        st.session_state.data = quiz
        st.session_state.question_keys = list(quiz.keys())
        st.session_state.count = 0
        st.session_state.question_index = 0
        st.session_state.submitted = False
        st.session_state.selected_option = None


def render_quiz():
    """Render the quiz UI from stored session state."""
    if st.session_state.data and st.session_state.question_index < len(st.session_state.question_keys):
        key = st.session_state.question_keys[st.session_state.question_index]
        value = st.session_state.data[key]
        mcq = value["mcq"]

        st.subheader(f"Q{st.session_state.question_index + 1}: {mcq}")
        selected_option = st.radio(
            "Choose your answer:",
            options=list(value["options"].keys()),
            format_func=lambda x: f"{x}: {value['options'][x]}",
            key=f"q_{key}"
        )

        if st.button("Submit") and not st.session_state.submitted:  
            st.session_state.submitted = True
            if value["correct"] == selected_option:
                st.session_state.count += 1
                st.success("Correct ✅")
            else:
                st.error("Wrong ❌")
                st.info(f"Correct answer: {value['correct']}")
                st.subheader("Explanation:")
                llm_response(mcq,value['options'],value['correct'],selected_option)

        if st.session_state.submitted and st.button("Next Question"):
            st.session_state.question_index += 1
            st.session_state.submitted = False
            st.session_state.selected_option = None
        elif not st.session_state.submitted and st.button("Next Question"):
            st.write("You have to answer first")

    elif st.session_state.data:
        # Finished quiz
        if st.session_state.count < 5:
            st.subheader("You are still weak in this topic, try to read once again.")
        score = st.session_state.count
        total = len(st.session_state.question_keys)

        st.success(f"🎉 Quiz Finished! Your score is: {score} / {total}")
        save_subtopic_quiz_score(
            email=st.session_state["user"],
            main_topic=st.session_state["main_topic"],
            chapter=st.session_state["chapter"],
            subtopic=sub,
            score=score
        )

        if st.button("Finished quiz"):
            st.session_state["mes"]=st.session_state.count
            st.session_state.data = None
            st.session_state.question_keys = []
            st.session_state.count = 0
            st.session_state.question_index = 0
            st.session_state.submitted = False
            st.session_state.selected_option = None
            st.session_state["message_to_last"]=sub
            st.switch_page("pages/last.py")


# --------------------------
# Page main
# --------------------------
sub = st.session_state.get("message_to_quiz")
Notes = st.session_state.get("Notes")

if "data" not in st.session_state:
    st.session_state.data = None
if "question_keys" not in st.session_state:
    st.session_state.question_keys = []
if "count" not in st.session_state:
    st.session_state.count = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

st.title(f"Quiz on {sub}")
st.subheader("Note:")
st.info("After submitting the question or after clicking next, click on any option to change the question")
level=st.text_input("enter the quiz level you want?(easy,medium,hard)")

if st.button("Create MCQs"):
    if level:
        generate_mcqs(Notes, level)
    else:
        st.write("you have to decide level first")    

if st.session_state.get("data"):
    render_quiz()
