import os
import streamlit as st
from datetime import datetime

from defaults import cpd_file
from utils import load_data, upload_to_s3, save_data

data = load_data(cpd_file)

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
        certificate = st.file_uploader("Upload Certificate", type=["pdf", "jpg", "jpeg", "png"])

        submit = st.form_submit_button("Submit")

        if submit:

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

            if certificate:
                bucket_name = os.getenv('AWS_S3_BUCKET_NAME')
                folder_name = os.getenv('AWS_S3_FOLDER_NAME')
                object_name = f"{folder_name}/{username}-{certificate.name}"

                upload_to_s3(certificate, bucket_name, object_name)

            save_data(data, cpd_file)

def edit_cpd():
    st.title("Edit CPD Activity")

    username = st.session_state.username
    user_data = [record for record in data if record.get("Username") == username]

    if not user_data:
        st.write("No CPD records found.")
        return

    cpd_titles = [f"{record['Title']} ({record['Date']})" for record in user_data]
    selected_cpd = st.selectbox("Select a CPD record to edit", cpd_titles)

    cpd_to_edit = user_data[cpd_titles.index(selected_cpd)]

    log_or_edit_cpd(edit_mode=True, cpd_to_edit=cpd_to_edit)