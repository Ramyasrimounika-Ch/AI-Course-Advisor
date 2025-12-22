import streamlit as st

chapter=st.session_state.get("message_to_overall")
level=st.session_state.get("level")

st.subheader("Note:")

st.info(
    f"""**Overall Quiz Info:**

- 📘 Chapter: **{chapter}**
- To answer this quiz you also need knowledge beyond the generated notes.
- This quiz will be generated at your chosen **{level}** only.
"""
)
start=st.checkbox("i am aware of the points given in note")

if start and st.button("Start quiz"):
    st.session_state["Notes"]=chapter
    st.session_state["quiz_level"]=level
    st.session_state["message_to_quiz"]=chapter
    st.switch_page("pages/quiz_overall.py")
