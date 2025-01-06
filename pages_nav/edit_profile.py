import streamlit as st

from defaults import users_file
from utils import load_data, save_data

def edit_profile():
    st.title("Settings")

    # Load user data
    user_data = load_data(users_file)
    user_info = [record for record in user_data if record.get('email', '') == st.session_state.user_profile['mail']][0]

    with st.form(key='edit_form'):
        yearly_hours_goal = st.number_input("Yearly CPD Hours Goal", value=user_info.get('yearly_hours_goal', 0.0), min_value=40, max_value=5000, step=1)

        # Submit
        submit_button = st.form_submit_button(label='Save')

        if submit_button:
            index = user_data.index(user_info)
            user_data[index]["yearly_hours_goal"] = yearly_hours_goal
            print(user_data[index]["yearly_hours_goal"])
            save_data(user_data, users_file)
            st.success("User information updated successfully!")