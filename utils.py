import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

# Path to JSON files
cpd_file = "cpd_records.json"
user_credentials_file = "users.json"

# Load user credentials from JSON file
def load_user_credentials():
    try:
        with open(user_credentials_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Load CPD data from JSON file
def load_data():
    try:
        with open(cpd_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save CPD data to JSON file
def save_data(data):
    with open(cpd_file, "w") as f:
        json.dump(data, f, indent=4)

# Login Page
def login():
    st.title("Login")

    users = load_user_credentials()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.button("Login")

    if submit:
        for user in users:
            if user['username'] == username and user['password'] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.full_name = user['full_name']
                st.session_state.user_type = user['user_type']
                st.session_state.page = "Dashboard"  # Redirect to the dashboard after login
                st.rerun()
                return
        st.error("Invalid username or password")

# Page to log or edit a CPD
def log_or_edit_cpd(edit_mode=False, cpd_to_edit=None):
    if "username" not in st.session_state:
        st.error("No user is logged in. Please log in first.")
        return

    username = st.session_state.username
    st.title(f"Log CPD Activity for {username}")

    if edit_mode and cpd_to_edit:
        title = cpd_to_edit["Title"]
        cpd_type = cpd_to_edit["Type"]
        hours = cpd_to_edit["Hours"]
        date = datetime.strptime(cpd_to_edit["Date"], "%Y-%m-%d")
        organization = cpd_to_edit["Organization"]
        description = cpd_to_edit["Description"]
        learning_outcomes = cpd_to_edit["Learning outcomes"]
        links = cpd_to_edit["Links"]
        certificate = cpd_to_edit.get("Certificate", None)
    else:
        title = ""
        cpd_type = "Event"
        hours = 0.0
        date = datetime.today()
        organization = ""
        description = ""
        learning_outcomes = ""
        links = ""
        certificate = None

    with st.form("cpd_form"):
        title = st.text_input("CPD Title", value=title)
        cpd_type = st.selectbox("Type of CPD", ["Event", "Seminar", "Webinar", "Training Course", "Training Video"], index=["Event", "Seminar", "Webinar", "Training Course", "Training Video"].index(cpd_type))
        hours = st.number_input("Number of CPD Hours", min_value=0.0, step=0.5, value=hours)
        date = st.date_input("Date of CPD Activity", value=date)
        organization = st.text_input("Name of Organization Providing the Training", value=organization)
        description = st.text_area("Description", value=description)
        learning_outcomes = st.text_area("Learning Outcomes and Objectives", value=learning_outcomes)
        links = st.text_input("Supporting Links", value=links)
        certificate = st.file_uploader("Upload Certificate (PDF)", type=["pdf", "jpg", "jpeg"])

        submit = st.form_submit_button("Submit")

        if submit:
            data = load_data()

            username = st.session_state.username

            if edit_mode and cpd_to_edit:
                index = data.index(cpd_to_edit)
                data[index] = {
                    "Username": username,
                    "Title": title,
                    "Type": cpd_type,
                    "Hours": hours,
                    "Date": date.strftime("%Y-%m-%d"),
                    "Organization": organization,
                    "Description": description,
                    "Learning outcomes": learning_outcomes,
                    "Links": links,
                    "Certificate": certificate.name if certificate else cpd_to_edit.get("Certificate", None)
                }
                st.success("CPD activity updated successfully.")
            else:
                new_record = {
                    "Username": username,
                    "Title": title,
                    "Type": cpd_type,
                    "Hours": hours,
                    "Date": date.strftime("%Y-%m-%d"),
                    "Organization": organization,
                    "Description": description,
                    "Learning outcomes": learning_outcomes,
                    "Links": links,
                    "Certificate": certificate.name if certificate else None
                }
                data.append(new_record)
                st.success("CPD activity logged successfully.")

            save_data(data)

def edit_cpd():
    st.title("Edit CPD Activity")

    data = load_data()

    username = st.session_state.username
    user_data = [record for record in data if record.get("Username") == username]

    if not user_data:
        st.write("No CPD records found.")
        return

    cpd_titles = [f"{record['Title']} ({record['Date']})" for record in user_data]
    selected_cpd = st.selectbox("Select a CPD record to edit", cpd_titles)

    cpd_to_edit = user_data[cpd_titles.index(selected_cpd)]

    log_or_edit_cpd(edit_mode=True, cpd_to_edit=cpd_to_edit)

def admin_dashboard():
    st.title("Admin Dashboard")

    data = load_data()
    users = load_user_credentials()

    if not data:
        st.write("No CPD records found.")
        return

    users_df = pd.DataFrame(users)
    user_only_df = users_df[users_df['user_type'] == 'user']

    user_cpd_hours = []
    for user in user_only_df['username']:
        user_data = pd.DataFrame([record for record in data if record.get('Username', '') == user])

        total_cpd_hours = user_data['Hours'].sum() if not user_data.empty else 0
        user_cpd_hours.append(total_cpd_hours)

    user_only_df['Total CPD Hours'] = user_cpd_hours
    user_only_df['Target Hours'] = 40
    user_only_df['Percentage Completed'] = (user_only_df['Total CPD Hours'] / user_only_df['Target Hours']) * 100

    fig, ax = plt.subplots()
    ax.bar(user_only_df['full_name'], user_only_df['Total CPD Hours'], color='skyblue')
    ax.set_xlabel("User")
    ax.set_ylabel("Total CPD Hours")
    ax.set_title("Total CPD Hours Per User")
    st.pyplot(fig)

    st.subheader("CPD Data Table")
    st.table(user_only_df[['full_name', 'Total CPD Hours', 'Target Hours', 'Percentage Completed']])

# Dashboard Page
def dashboard():
    st.title(f"Welcome {st.session_state.full_name}")

    data = load_data()

    user_data = pd.DataFrame([record for record in data if record.get('Username', '') == st.session_state.username])

    if user_data.empty:
        st.write("No CPD records found for you.")
        return

    user_data['Date'] = pd.to_datetime(user_data['Date'], format="%Y-%m-%d")

    current_year = datetime.now().year
    this_year_df = user_data[user_data['Date'].dt.year == current_year]
    total_cpd_hours_year = this_year_df['Hours'].sum()
    percentage_completed = (total_cpd_hours_year / 40) * 100

    total_cpd_hours_lifetime = user_data['Hours'].sum()

    cpd_by_type = user_data['Type'].value_counts()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Total CPD Hours This Year")
        st.metric("Completed Hours", total_cpd_hours_year)
        st.metric("Yearly Goal (40 hrs)", f"{percentage_completed:.2f}%")
        st.progress(percentage_completed / 100)

    with col2:
        st.subheader("Total Lifetime CPD Hours")
        st.metric("Completed Hours", total_cpd_hours_lifetime)

    with col3:
        st.subheader("CPD Completed by Type")
        fig, ax = plt.subplots(figsize=(3, 3))
        colors = plt.get_cmap('Set3')(range(len(cpd_by_type)))
        ax.pie(cpd_by_type, labels=cpd_by_type.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.3}, colors=colors)
        ax.axis('equal')
        st.pyplot(fig)

    st.subheader("CPD Records Summary")
    st.write(user_data[['Title', 'Type', 'Hours', 'Date', 'Organization']])

# Logout
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.full_name = ""
    st.session_state.user_type = ""
    st.session_state.page = "Login"  # Redirect to login page after logout
    st.rerun()