import streamlit as st

from defaults import users_file
from utils import load_data, save_data

def edit_profile():
    st.title("Settings")

    # Load user data
    user_data = load_data(users_file)
    user_info = [record for record in user_data if record.get('email', '') == st.session_state.user_profile['mail']][0]

    with st.form(key='edit_form'):
        # full_name = st.text_input("Name", user_info.get('full_name', ''))
        yearly_hours_goal = st.number_input("Yearly CPD Hours Goal", value=user_info.get('yearly_hours_goal', 0.0), min_value=40, max_value=5000, step=1)

        # Submit
        submit_button = st.form_submit_button(label='Save')

        if submit_button:
            index = user_data.index(user_info)
            user_data[index] = {
                "email": user_info.get('email', ''),
                "password": user_info.get('password', ''),
                "yearly_hours_goal": yearly_hours_goal,
                "user_type": user_info.get('user_type', '')
            }
            save_data(user_data, users_file)
            st.success("User information updated successfully!")

    # Finalize authentication handling first
    # with st.form(key='change_password_form'):
    #     st.write("Change Password")
    #     old_password = st.text_input("Old Password", type="password")
    #     new_password = st.text_input("New Password", type="password")
    #     new_password_confirm = st.text_input("Confirm New Password", type="password")
    #     if st.form_submit_button("Submit"):
    #         # handle password change
    #         st.success("Password changed successfully!")