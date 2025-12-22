import streamlit as st

st.subheader(f"You just completed quiz on {st.session_state.get("message_to_last")}") 

marks=st.session_state.get("mes")

if marks<5:
    st.error(f"Based on the quiz you are advised to read the topic {st.session_state.get("message_to_last")} again.")
elif marks>5 and marks<8:
    st.info(f"Based on the quiz you are ok in the topic {st.session_state.get("message_to_last")}.But it is better to read it again.") 
else:
    st.success(f"Based on the quiz you are now good at the topic {st.session_state.get("message_to_last")}.You can continue with the next topics.")       

st.subheader("Thank you")
if st.button("Back to Home"):
    st.switch_page("main.py")