import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

from dotenv import load_dotenv

from pages_nav import (
    manager_dashboard,
    manager_view_dashboard,
    create_new_account,
    dashboard,
    edit_cpd,
    edit_profile,
    login,
    log_or_edit_cpd)

from utils import logout

st.set_page_config(page_title="myCPD Portal", page_icon="static_files/Btg-icon.png", layout="wide", initial_sidebar_state="collapsed")
st.logo("static_files/Btg-Logo.png")

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
    
    if st.session_state.user_type == 'manager':
        page = st.sidebar.selectbox("Select Page", ["Overview", "Search"])
        if page == "Overview":
            manager_dashboard()
        elif page == "Search":
            manager_view_dashboard()
    elif st.session_state.user_type == 'super_admin':
        page = st.sidebar.selectbox("Select Page", ["Create New Account"])
        if page == "Create New Account":
            create_new_account()
    else:
        page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD", "Edit Profile"])
        if page == "Dashboard":
            username = st.session_state.username
            dashboard(username)
        elif page == "Log CPD":
            log_or_edit_cpd()
        elif page == "Edit CPD":
            edit_cpd()
        elif page == "Edit Profile":
            edit_profile()
            
if __name__ == "__main__":
    main()
