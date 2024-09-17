import streamlit as st
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

# Hard-coded user credentials for now, you can make it in to a json as well. tapos hardcode na muna users, chaka na usermanagement for adding.
# hence kaya pati password non-encrypted. again for the purpose lang of simple login.
USER_CREDENTIALS = {
    "mark.torres": {
        "password": "pass123",
        "full_name": "Mark Torres"
    }
}

# Load CPD data from JSON file
def load_data():
    try:
        with open(cpd_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Json containing the data
cpd_file = "cpd_records.json"

# Save CPD data to JSON file
def save_data(data):
    with open(cpd_file, "w") as f:
        json.dump(data, f, indent=4)

# Login Page
def login():
    st.title("Login to BTG myCPD Portal")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.full_name = USER_CREDENTIALS[username]["full_name"]
            st.session_state.page = "Dashboard"
            st.success("Login successful!")
            # Refresh the page to reflect changes
            st.rerun()
        else:
            st.error("Invalid username or password.")

# Dashboard Page kunwari
def dashboard():
    st.title("CPD Dashboard")

    data = load_data()

    if not data:
        st.write("No CPD records found.")
        return

    # Load and Put that sa dataframe
    df = pd.DataFrame(data)

    # Disregard this --> Convert lang to proper case column names pd tanggalin
    df.columns = [col.replace('_', ' ').title() for col in df.columns]

    # Calc total CPD hours completed this year
    current_year = datetime.now().year
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
    this_year_df = df[df['Date'].dt.year == current_year]
    total_cpd_hours_year = this_year_df['Hours'].sum()
    percentage_completed = (total_cpd_hours_year / 40) * 100

    # Total lifetime CPD hours
    total_cpd_hours_lifetime = df['Hours'].sum()

    # Donut chart of CPD by type
    cpd_by_type = df['Type'].value_counts()

    # Create three columns for the boxes
    col1, col2, col3 = st.columns(3)

    # First Box: Total CPD Hours Completed This Year with Percentage Bar
    with col1:
        st.subheader("Total CPD Hours This Year")
        st.metric("Completed Hours", total_cpd_hours_year)
        st.metric("Yearly Goal (40 hrs)", f"{percentage_completed:.2f}%")
        st.progress(percentage_completed / 100)  # Horizontal bar showing completion

    # Second Box: Total Lifetime CPD Completion
    with col2:
        st.subheader("Total Lifetime CPD Hours")
        st.metric("Completed Hours", total_cpd_hours_lifetime)

    # Third Box: Donut Chart of CPD by Type
    with col3:
        st.subheader("CPD Completed by Type")
        
        # Set the size ng chart
        fig, ax = plt.subplots(figsize=(3, 3))  # 300x300 pixels 

        # Plot the pie chart with a 'donut' style
        colors = plt.get_cmap('Set3')(range(len(cpd_by_type)))  # Get distinct colors for the chart
        ax.pie(cpd_by_type, labels=cpd_by_type.index, autopct='%1.1f%%', startangle=90, wedgeprops={'width':0.3}, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle

        # Create a custom legend with color squares next to the labels, <-- you can change or remove this para may extra space kasi redundant na yung legend.
        legend_labels = [f"{label} ({value})" for label, value in zip(cpd_by_type.index, cpd_by_type)]
        handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in colors]
        ax.legend(handles, legend_labels, title="CPD Type", loc="center left", bbox_to_anchor=(1, 0.5))

        # Display the chart
        st.pyplot(fig)

    # Summary Table 
    st.subheader("CPD Records Summary")
    st.write(df[['Title', 'Type', 'Hours', 'Date', 'Organization', 'Description', 'Learning Outcomes', 'Links', 'Certificate']])

# Page to log or edit a CPD
def log_or_edit_cpd(edit_mode=False, cpd_to_edit=None):
    st.title("Log CPD Activity")

    # If in edit mode, pre-populate the fields with the selected record's data
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

    # Form to input CPD data
    with st.form("cpd_form"):
        title = st.text_input("CPD Title", value=title)
        cpd_type = st.selectbox("Type of CPD", ["Event", "Seminar", "Webinar", "Training Course", "Training Video"], index=["Event", "Seminar", "Webinar", "Training Course", "Training Video"].index(cpd_type))
        hours = st.number_input("Number of CPD Hours", min_value=0.0, step=0.5, value=hours)
        date = st.date_input("Date of CPD Activity", value=date)
        organization = st.text_input("Name of Organization Providing the Training", value=organization)
        description = st.text_area("Description", value=description)
        learning_outcomes = st.text_area("Learning Outcomes and Objectives", value=learning_outcomes)
        links = st.text_input("Supporting Links", value=links)
        certificate = st.file_uploader("Upload Certificate (PDF)", type=["pdf"])

        submit = st.form_submit_button("Submit")

        if submit:
            # Load existing data
            data = load_data()

            # If in edit mode, update the record instead of adding a new one
            if edit_mode and cpd_to_edit:
                index = data.index(cpd_to_edit)
                data[index] = {
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
                # Save new CPD record
                new_record = {
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

            # Save data back to the JSON file
            save_data(data)

# Page to edit CPD
def edit_cpd():
    st.title("Edit CPD Activity")

    # Load CPD data
    data = load_data()

    if not data:
        st.write("No CPD records found.")
        return

    # Create a dropdown for selecting a CPD record to edit, for now nakaset sa title and date, there should've been an ID. 
    # This might be a problem or matter later pag per user na yung table.
    cpd_titles = [f"{record['Title']} ({record['Date']})" for record in data]
    selected_cpd = st.selectbox("Select a CPD record to edit", cpd_titles)

    # Find the selected CPD record
    cpd_to_edit = data[cpd_titles.index(selected_cpd)]

    # Redirect to the edit form pre-populated with the selected record
    log_or_edit_cpd(edit_mode=True, cpd_to_edit=cpd_to_edit)

# Logout
def logout():
    st.session_state.authenticated = False
    st.session_state.full_name = ""
    st.session_state.page = "Login"