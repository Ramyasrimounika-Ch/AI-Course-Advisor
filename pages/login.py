import streamlit as st
import bcrypt

from src.db import get_connection


# -----------------------------
# Password hashing
# -----------------------------

def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )


# -----------------------------
# Password verification
# -----------------------------

def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password
    )


# -----------------------------
# Create users table
# -----------------------------

def create_users_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email VARCHAR(255) PRIMARY KEY,
            password VARCHAR(255) NOT NULL
        )
    """)

    conn.commit()

    cursor.close()
    conn.close()


# -----------------------------
# Register user
# -----------------------------

def register_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    # Check whether user already exists
    cursor.execute(
        "SELECT email FROM users WHERE email = %s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return False, "User already exists."

    # Hash password
    hashed_password = hash_password(password)

    # Insert user
    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (%s, %s)
        """,
        (email, hashed_password.decode("utf-8"))
    )

    conn.commit()

    cursor.close()
    conn.close()

    return True, "Account created successfully."


# -----------------------------
# Login user
# -----------------------------

def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email, password FROM users WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return False

    stored_hash = user[1].encode("utf-8")

    return verify_password(password, stored_hash)


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("🔐 AI Course Advisor")

create_users_table()

email = st.text_input("Email")
password = st.text_input(
    "Password",
    type="password"
)

col1, col2 = st.columns(2)

with col1:

    if st.button("Register"):

        if not email or not password:
            st.error("Please enter email and password.")

        else:

            success, message = register_user(
                email,
                password
            )

            if success:

                st.session_state["user"] = email

                st.success(message)

                st.switch_page("main.py")

            else:
                st.error(message)


with col2:

    if st.button("Login"):

        if not email or not password:
            st.error("Please enter email and password.")

        else:

            success = login_user(
                email,
                password
            )

            if success:

                st.session_state["user"] = email

                st.success("Logged in successfully!")

                st.switch_page("main.py")

            else:
                st.error("Invalid email or password.")
