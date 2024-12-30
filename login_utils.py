import streamlit as st
import msal
import os
import requests

# Azure AD app details
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_ClIENT_SECRET')
tenant_id = os.getenv('AZURE_TENANT_ID')
authority = f"https://login.microsoftonline.com/{tenant_id}"
redirect_uri = 'http://localhost:8501'
scope = ["User.Read"]

# print("Azure AD app starting")

# Initialize MSAL
app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret,
)

# print("Azure AD app initialized")

# Function to get Azure AD authentication URL
def get_auth_url():
    auth_url = app.get_authorization_request_url(scope, redirect_uri=redirect_uri)
    return auth_url

# Function to acquire a token from authorization code
def get_token_from_code(auth_code):
    token = app.acquire_token_by_authorization_code(auth_code, scopes=scope, redirect_uri=redirect_uri)
    return token

# Function to retrieve user profile using the token
def get_user_profile(token):
    headers = {
        'Authorization': 'Bearer ' + token['access_token']
    }
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()

# Page configuration
def set_page_config():
    st.set_page_config(page_title="CPD Portal", layout="centered")

# Add BTG logo
def add_logo():
    logo_url = "https://i.ibb.co/HrqxpBZ/logo.jpg"
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center;">
            <img src="{logo_url}" width="500">
        </div>
        """, unsafe_allow_html=True
    )

# Custom CSS
def custom_css():
    st.markdown("""
    <style>
    .stButton>button {
        width: 50%;
        #padding: 10px 20px 0px;
        background-color: transparent;
        color: #8B7355;  /* Brown color for the text */
        height: 3em;
        border-radius: 5px;
        border: 3px solid #1c2544;  /* Brown border */
        font-size: 16px;
        font-weight: bold;
        position: relative;
        left: 25%;

        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1c2544;  /* Brown background on hover */
        color: white;
        border: 3px solid #8B7355;
    }
    
    button[title="View fullscreen"]{
    visibility: hidden;}
    
    .css-m70y {display:none}

    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)


# Login page function
def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    add_logo()
    st.markdown("<h1 style='text-align: center; color: #1c2544;'>CPD Portal</h1>", unsafe_allow_html=True)

    auth_url = get_auth_url() 
    st.button("Login", on_click=lambda: st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True), )
    st.button("Go Back to BTG Apps Home", on_click=lambda: st.markdown(f'<meta http-equiv="refresh" content="0;url=https://apps.btgi.com.au">', unsafe_allow_html=True))

# Logout function
# def logout():
#     st.subheader("",divider="grey")
#     if st.button('Logout'):
#         # Clear session state
#         for key in list(st.session_state.keys()):
#             del st.session_state[key]

#         # Instead of using experimental_set_query_params, use st.markdown to simulate a redirect
#         st.markdown("<meta http-equiv='refresh' content='0; url=/' />", unsafe_allow_html=True)
