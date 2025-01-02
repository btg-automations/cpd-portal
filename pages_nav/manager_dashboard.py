import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils import load_data
from .dashboard import dashboard
from defaults import cpd_file, users_file

users = load_data(users_file)

# Show only reports of the manager
if "user_profile" in st.session_state:
    if st.session_state.user_profile['user_type'] == 'manager':
        user_data = [record for record in users if record.get('email', '') == st.session_state.user_profile["userPrincipalName"]]
        index = users.index(user_data[0])
        reports = users[index]['reports']
        users = [record for record in users if record.get('email', '') in reports]
    elif st.session_state.user_profile['user_type'] == 'user':
        st.error("You do not have permission to view this page.")

def manager_dashboard():
    st.title("Manager Dashboard")

    data = load_data(cpd_file)

    if not data:
        st.write("No CPD records found.")
        return

    users_df = pd.DataFrame(users)

    user_cpd_hours = []
    for user in users_df['email']:
        user_data = pd.DataFrame([record for record in data if record.get('email', '') == user])
        total_cpd_hours = user_data['Hours'].sum() if not user_data.empty else 0
        user_cpd_hours.append(total_cpd_hours)

    users_df['Total CPD Hours'] = user_cpd_hours
    users_df['Target Hours'] = users_df['yearly_hours_goal']
    users_df['Percentage Completed'] = (users_df['Total CPD Hours'] / users_df['Target Hours']) * 100

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        fig, ax = plt.subplots()
        ax.bar(users_df['full_name'], users_df['Total CPD Hours'], color='skyblue')
        ax.set_xlabel("User")
        ax.set_ylabel("Total CPD Hours")
        ax.set_title("Total CPD Hours Per User")
        st.pyplot(fig)

    st.subheader("CPD Data Table")
    st.table(users_df[['full_name', 'Total CPD Hours', 'Target Hours', 'Percentage Completed']])

def manager_view_dashboard():

    user_data = [{'full_name': record["full_name"], "email": record["email"]} for record in users]

    if not user_data:
        st.write("No users found.")
        return
    
    # Mapping username to fullname
    full_name_to_email = {record['full_name']: record['email'] for record in user_data}
    selected_full_name = st.selectbox("Select a user to view", options=list(full_name_to_email.keys()))
    st.text("")
    selected_email = full_name_to_email[selected_full_name]

    dashboard(selected_email)
    