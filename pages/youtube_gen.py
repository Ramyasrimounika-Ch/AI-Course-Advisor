import streamlit as st
from src.youtube import get_youtube_links

st.title("YOUTUBE VIDEOS ADVISOR")
sub = st.session_state.get("message_to_youtube_gen")

if "youtube_links" not in st.session_state:
    st.session_state["youtube_links"] = []

if st.button("Generate"):
    if sub:
        st.session_state["youtube_links"] = get_youtube_links(sub, st.session_state.get("level", "beginner"))
    else:
        st.warning("No topic selected for generating YouTube links.")

if st.session_state["youtube_links"]:
    st.subheader(f"Recommended YouTube videos for: {sub}")
    for title, link in st.session_state["youtube_links"]:
        st.write(f"- {title}: {link}")
