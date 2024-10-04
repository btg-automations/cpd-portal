import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from pages_nav import (
    admin_dashboard,
    admin_view_dashboard,
    create_new_account,
    dashboard,
    edit_cpd,
    login,
    log_or_edit_cpd)

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

def main():
    if st.session_state.page == "Login":
        login()
    elif st.session_state.authenticated:
        show_sidebar_navigation()
        if st.sidebar.button("Logout"):
            logout()

def show_sidebar_navigation():
    st.sidebar.title("Navigation")
    
    if st.session_state.user_type == 'admin':
        page = st.sidebar.selectbox("Select Page", ["Overview", "Search"])
        if page == "Overview":
            admin_dashboard()
        elif page == "Search":
            admin_view_dashboard()
    elif st.session_state.user_type == 'super_admin':
        page = st.sidebar.selectbox("Select Page", ["Create New Account"])
        if page == "Create New Account":
            create_new_account()
    else:
        page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD"])
        if page == "Dashboard":
            username = st.session_state.username
            dashboard(username)
        elif page == "Log CPD":
            log_or_edit_cpd()
        elif page == "Edit CPD":
            edit_cpd()
            
if __name__ == "__main__":
    main()
