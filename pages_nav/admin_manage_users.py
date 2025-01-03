import streamlit as st
import pandas as pd

from utils import add_data, load_data, save_data
from defaults import users_file

# Convert the reports list to a string of full names
    
def admin_manage_users():
    st.title("Admin Manage Users")

    # Load user data
    users_data = load_data(users_file)
    users_df = pd.DataFrame(users_data)

    #dictionary to map emails to full names
    email_to_full_name = dict(zip(users_df['email'], users_df['full_name']))

    if "reports" not in users_df.columns:
        users_df['reports'] = ""

    users_df.loc[users_df["user_type"] == "manager", "reports"] = users_df.loc[users_df['user_type'] == 'manager', 'reports'].apply(lambda reports: [email_to_full_name.get(email, email) for email in (reports if isinstance(reports, list) else [])])
    # users_df.loc[users_df["user_type"] == "user", "reports"] = [["Not Applicable"]]
    # users_df.loc[users_df["user_type"] == "admin", "reports"] = [["All Access"]]

    st.dataframe(users_df[['full_name', 'user_type', 'reports']], width=1000)

    # Add a new user
    with st.expander("Add a new user"):
        with st.form("add_user_form"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email")

            if st.form_submit_button("Add User"):
                if email in users_df['email'].values:
                    st.error("A user with this email already exists.")
                else:
                    new_user = {
                        "full_name": full_name,
                        "email": email,
                        "user_type": "user",
                        "yearly_hours_goal": 40
                    }
                    users_data.append(new_user)
                    save_data(users_data, users_file)
                    st.success("User added successfully!")
                    st.rerun()

    # Select a user to edit
    with st.expander("Edit a user"):
        selected_user = st.selectbox("Select a user to edit", users_df['full_name'])

        if selected_user:
            user_data = [record for record in users_data if record.get('full_name', '') == selected_user][0]
            index = users_data.index(user_data)

            with st.form("edit_user_form"):
                user_type = st.selectbox("User Type", ["user", "manager", "admin"], index=["user", "manager", "admin"].index(user_data['user_type']), key="user_type")

                if st.form_submit_button("Save Changes"):
                    users_data[index]["user_type"] = user_type
                    if user_type in ["user", "admin"]:
                        users_data[index].pop("reports", None)
                    elif user_type == "manager":
                        users_data[index]["reports"] = user_data.get('reports', [])

                    save_data(users_data, users_file)
                    if (user_type != user_data['user_type']) & (user_type == "manager"):
                        st.rerun()
                    st.success("User data updated successfully!")

            if user_type == "manager":
                with st.form("Reports"):
                    choices = [name for email, name in email_to_full_name.items() if name != selected_user]
                    if 'reports' in user_data.keys():
                        reports_list = [email_to_full_name.get(email, email) for email in user_data['reports']]
                        reports = st.multiselect("Reports", choices, default=reports_list, key="reports")
                    else:
                        reports = st.multiselect("Reports", choices, key="reports")
                    if st.form_submit_button("Save Reports"):
                        users_data[index]["reports"] = [email for email, name in email_to_full_name.items() if name in reports]
                        save_data(users_data, users_file)
                        st.rerun()
                        st.success("Reports updated successfully!")
