import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from pages_nav import admin_dashboard, admin_view_dashboard, dashboard, log_or_edit_cpd, edit_cpd, login

from utils import logout

st.set_page_config(page_title="myCPD Portal", page_icon=None, layout="wide", initial_sidebar_state="collapsed")

# load environment
load_dotenv()

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
        
        if st.session_state.user_type == 'admin':
            page = st.sidebar.selectbox("Select Page", ["Overview", "Search"])
            if page == "Overview":
                admin_dashboard()
            elif page == "Search":
                admin_view_dashboard()
        else:
            page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD"])
            if page == "Dashboard":
                username = st.session_state.username
                dashboard(username)
            elif page == "Log CPD":
                log_or_edit_cpd()
            elif page == "Edit CPD":
                edit_cpd()

        # Logout button
        if st.sidebar.button("Logout"):
            logout()

if __name__ == "__main__":
    main()
