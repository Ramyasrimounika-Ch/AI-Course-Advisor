import streamlit as st
import sqlite3
import hashlib

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

st.title("🔐 Login / Register")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)
""")

if st.button("Login / Register"):
    hashed = hash_password(password)
    user = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

    if user:
        if user[1] == hashed:
            st.session_state["user"] = email
            st.success("Logged in!")
            st.switch_page("main.py")
        else:
            st.error("Wrong password")
    else:
        c.execute("INSERT INTO users VALUES (?,?)", (email, hashed))
        conn.commit()
        st.session_state["user"] = email
        st.success("Account created!")
        st.switch_page("main.py")
