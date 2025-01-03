import streamlit as st

from dotenv import load_dotenv
import msal
import os
load_dotenv()
from defaults import users_file
from login_utils import custom_css, get_token_from_code, get_user_profile
from utils import logout, load_data

from pages_nav import (
    admin_manage_users,
    manager_dashboard,
    manager_view_dashboard,
    create_new_account,
    dashboard,
    edit_cpd,
    edit_profile,
    login_page,
    log_or_edit_cpd)

st.set_page_config(page_title="myCPD Portal", page_icon="static_files/Btg-icon.png", layout="wide", initial_sidebar_state="collapsed")
st.logo("static_files/Btg-Logo.png")

user_data = load_data(users_file)

def show_sidebar_navigation():
    user_info = [record for record in user_data if record.get('email', '') == st.session_state.user_profile['mail']][0]
    st.sidebar.title("Navigation")

    if user_info['user_type'] == 'manager':
        page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD", "Settings", "Manager - Overview", "Manager - Search"])
    elif user_info['user_type'] == 'admin':
        page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD", "Settings", "Manager - Overview", "Manager - Search", "Admin - Manage Users"])
    else:
        page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD", "Settings"])

    if page == "Manager - Overview":
        manager_dashboard()
    elif page == "Manager - Search":
        manager_view_dashboard()
    elif page == "Dashboard":
        dashboard(st.session_state.user_profile['mail'])
    elif page == "Log CPD":
        log_or_edit_cpd()
    elif page == "Edit CPD":
        edit_cpd()
    elif page == "Settings":
        edit_profile()
    elif page == "Admin - Manage Users":
        admin_manage_users()

# Main function to handle the app flow
def main():
    custom_css()

    if 'user_profile' in st.session_state:
        show_sidebar_navigation()
        if st.sidebar.button("Logout"):
            logout()
    elif 'code' in st.query_params:
        auth_code = st.query_params['code']
        if isinstance(auth_code, list):
            auth_code = auth_code[0]

        token = get_token_from_code(auth_code)
        if 'access_token' in token:
            st.session_state['access_token'] = token['access_token']
            user_profile = get_user_profile(token)

            email = user_profile["userPrincipalName"]
            if any(record.get('email', '') == email for record in user_data):
                user = [record for record in user_data if record.get('email', '') == email][0]
                index = user_data.index(user)

                st.session_state['user_profile'] = user_profile
                st.session_state.user_profile["user_type"] = user_data[index]["user_type"]
                st.session_state.user_profile["fulle_name"] = user_data[index]["full_name"]
                st.success(f"Logged in as {st.session_state.user_profile["fulle_name"]}")

                st.rerun()
            else:
                st.error("Email not found in user data. Please contact Data Team or an administrator for assistance.")
    else:
        login_page()

if __name__ == "__main__":
    main()