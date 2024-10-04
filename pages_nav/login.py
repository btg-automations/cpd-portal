import streamlit as st

from defaults import users_file
from utils import load_data

def login():
    st.title("Login")

    users = load_data(users_file)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.button("Login")

    if submit:
        for user in users:
            if user['username'] == username and user['password'] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.full_name = user['full_name']
                st.session_state.user_type = user['user_type']
                st.session_state.page = "Dashboard"  # Redirect to the dashboard after login
                st.rerun()
                return
        st.error("Invalid username or password")