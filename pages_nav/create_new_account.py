import streamlit as st
import pandas as pd

from utils import add_data
from defaults import users_file

# Sample data for users

# Function to add a new user
def add_user(df, username, temp_password, user_type):
    new_user = {'Username': username, 'User Type': user_type}
    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    return df

def create_new_account():
    st.title('Manage Users')

    st.subheader('Create New User')
    with st.form(key='create_user_form'):
        username = st.text_input('Username')
        full_name = st.text_input('Full Name')
        user_type = st.selectbox('User Type', ['user', 'manager'])
        temp_password = st.text_input('Temporary Password', type='password')
        submit_button = st.form_submit_button(label='Create User')

        if submit_button:
            # Load existing users
            existing_users = pd.read_json(users_file)

            # Check if username already exists
            if username in existing_users['username'].values:
                st.error(f"Failed Creating new user. Username {username} already in use")
            else:
                new_record = {
                    "username": username,
                    "password": temp_password,
                    "full_name": full_name,
                    "user_type": user_type
                }
                add_data(users_file, new_record)
                st.success(f"User {username} created successfully!")

    # if user_type == 'Manager':
    #     with st.form(key='Add Reports'):
    #         st.subheader('Add Reports')
    #         reports = []
    #         report = st.selectbox('Select Report', df[df['User Type'] == 'User']['Username'])
    #         add_report_button = st.form_submit_button(label='Add Report')
    #         if add_report_button:
    #             reports.append(report)
    #             st.write('Reports:', reports)
        # if user_type == 'Manager':
        #     st.subheader('Add Reports')
        #     reports = []
            
        #     # Move the button outside the form
        #     add_report_button = st.button('Add Report')
        #     if add_report_button:
        #         report = st.selectbox('Select Report', df[df['User Type'] == 'User']['Username'])
        #         reports.append(report)
        #         st.write('Reports:', reports)

