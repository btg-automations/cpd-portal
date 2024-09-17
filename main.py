import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

from utils import login, logout, dashboard, log_or_edit_cpd, edit_cpd


# Session state para makeep track si login status
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'full_name' not in st.session_state:
    st.session_state.full_name = ""

if 'page' not in st.session_state:
    st.session_state.page = "Login"

# Navigation
if st.session_state.authenticated:
    # Show/Disply welcome message and logout
    st.sidebar.write(f"Welcome {st.session_state.full_name}")
    if st.sidebar.button("Logout"):
        logout()

    # Display the navigation options (you can change this to a button if you want or other form instead of radio pero ok na din as is for now)
    st.session_state.page = st.sidebar.radio("Go to", ["Dashboard", "Log New CPD", "Edit CPD"])
    # Very basic naming option, pwede mo change name if you want but do check kung san sila nakalink sa taas.
    if st.session_state.page == "Dashboard":
        dashboard()
    elif st.session_state.page == "Log New CPD":
        log_or_edit_cpd()
    elif st.session_state.page == "Edit CPD":
        edit_cpd()
else:
    login()