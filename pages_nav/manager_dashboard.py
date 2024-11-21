import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from utils import load_data
from .dashboard import dashboard
from defaults import cpd_file, users_file

users = load_data(users_file)

def manager_dashboard():
    st.title("Manager Dashboard")

    data = load_data(cpd_file)

    if not data:
        st.write("No CPD records found.")
        return

    users_df = pd.DataFrame(users)
    user_only_df = users_df[users_df['user_type'] == 'user']

    user_cpd_hours = []
    for user in user_only_df['email']:
        user_data = pd.DataFrame([record for record in data if record.get('email', '') == user])
        total_cpd_hours = user_data['Hours'].sum() if not user_data.empty else 0
        user_cpd_hours.append(total_cpd_hours)

    user_only_df['Total CPD Hours'] = user_cpd_hours
    user_only_df['Target Hours'] = user_only_df['yearly_hours_goal']
    user_only_df['Percentage Completed'] = (user_only_df['Total CPD Hours'] / user_only_df['Target Hours']) * 100

    col1, col2, col3 = st.columns([1, 3, 1])

    with col2:
        fig, ax = plt.subplots()
        ax.bar(user_only_df['full_name'], user_only_df['Total CPD Hours'], color='skyblue')
        ax.set_xlabel("User")
        ax.set_ylabel("Total CPD Hours")
        ax.set_title("Total CPD Hours Per User")
        st.pyplot(fig)

    st.subheader("CPD Data Table")
    st.table(user_only_df[['full_name', 'Total CPD Hours', 'Target Hours', 'Percentage Completed']])

def manager_view_dashboard():
    # users = load_data(users_file)

    user_data = [{'full_name': record["full_name"], "email": record["email"]} for record in users if record["user_type"] == "user"]

    if not user_data:
        st.write("No users found.")
        return
    
    # Mapping username to fullname
    full_name_to_email = {record['full_name']: record['email'] for record in user_data}
    selected_full_name = st.selectbox("Select a user to view", options=list(full_name_to_email.keys()))
    st.text("")
    selected_email = full_name_to_email[selected_full_name]

    dashboard(selected_email)
    