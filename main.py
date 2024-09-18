import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

from utils import (
    login,
    log_or_edit_cpd,
    edit_cpd,
    admin_dashboard,
    dashboard,
    logout
)

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = ""

if 'full_name' not in st.session_state:
    st.session_state.full_name = ""

if 'user_type' not in st.session_state:
    st.session_state.user_type = ""

if 'page' not in st.session_state:
    st.session_state.page = "Login"

# Main app logic
def main():
    if st.session_state.page == "Login":
        login()
    elif st.session_state.authenticated:
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD"])

        if st.session_state.user_type == 'admin':
            if page == "Dashboard":
                admin_dashboard()
            elif page == "Log CPD":
                log_or_edit_cpd()
            elif page == "Edit CPD":
                edit_cpd()
        else:
            if page == "Dashboard":
                dashboard()
            elif page == "Log CPD":
                log_or_edit_cpd()
            elif page == "Edit CPD":
                edit_cpd()

        # Logout button
        if st.sidebar.button("Logout"):
            logout()

if __name__ == "__main__":
    main()
