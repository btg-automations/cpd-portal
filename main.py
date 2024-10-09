from dotenv import load_dotenv
load_dotenv()
from login_utils import *
from utils import logout

from pages_nav import (
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

def show_sidebar_navigation():
    st.sidebar.title("Navigation")
    
    # if st.session_state.user_type == 'manager':
    #     page = st.sidebar.selectbox("Select Page", ["Overview", "Search"])
    #     if page == "Overview":
    #         manager_dashboard()
    #     elif page == "Search":
    #         manager_view_dashboard()
    # elif st.session_state.user_type == 'super_admin':
    #     page = st.sidebar.selectbox("Select Page", ["Create New Account"])
    #     if page == "Create New Account":
    #         create_new_account()
    # else:
    page = st.sidebar.selectbox("Select Page", ["Dashboard", "Log CPD", "Edit CPD", "Edit Profile"])
    if page == "Dashboard":
        dashboard(st.session_state.user_profile['mail'])
    elif page == "Log CPD":
        log_or_edit_cpd()
    elif page == "Edit CPD":
        edit_cpd()
    elif page == "Edit Profile":
        edit_profile()

# Main function to handle the app flow
def main():
    custom_css()

    if 'user_profile' in st.session_state:
        show_sidebar_navigation()
        if st.sidebar.button("Logout"):
            logout()
    elif 'code' in st.query_params:
        print(st.query_params)
        auth_code = st.query_params['code']
        if isinstance(auth_code, list):
            auth_code = auth_code[0]

        token = get_token_from_code(auth_code)
        print(f"Token: {token}")
        if 'access_token' in token:
            st.session_state['access_token'] = token['access_token']
            user_profile = get_user_profile(token)

            st.session_state['user_profile'] = user_profile
            st.success(f"Logged in as {user_profile['displayName']}")
            st.rerun()
    else:
        login_page() 

if __name__ == "__main__":
    main()