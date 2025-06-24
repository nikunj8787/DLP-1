import streamlit as st
from database_manager import check_user, add_user

def login_form(role):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_user(email, password, role):
            st.session_state["user_email"] = email
            st.session_state["user_role"] = role
            st.success("Logged in as {}!".format(role))
            st.experimental_rerun()
        else:
            st.error("Invalid credentials or not verified.")
    if st.button("Register"):
        add_user(email, password, role)
        st.success("Registered. Awaiting admin verification.")
