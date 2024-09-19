import streamlit as st
import pandas as pd
from datetime import datetime

from utils import load_data, encode_image_to_base64, generate_pie_chart

def dashboard(username):
    # st.title(f"Welcome {st.session_state.full_name}")

    data = load_data()

    user_data = pd.DataFrame([record for record in data if record.get('Username', '') == username])

    if user_data.empty:
        st.write("No CPD records found.")
        return

    user_data['Date'] = pd.to_datetime(user_data['Date'], format="%Y-%m-%d")

    current_year = datetime.now().year
    this_year_df = user_data[user_data['Date'].dt.year == current_year]
    total_cpd_hours_year = this_year_df['Hours'].sum()
    percentage_completed = (total_cpd_hours_year / 40) * 100

    total_cpd_hours_lifetime = user_data['Hours'].sum()

    cpd_by_type = user_data['Type'].value_counts()

    # Create a container with a white background, gap, and shadow
    with st.container():
        st.markdown(
            """
                <div style="display: flex; gap: 20px;">
                    <div style="flex: 1; background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                        <h3>Total CPD Hours This Year</h3>
                        <p><strong>Completed Hours:</strong> {}</p>
                        <p><strong>Yearly Goal (40 hrs):</strong> {:.2f}%</p>
                        <div style="width: 100%; background-color: #e0e0e0; border-radius: 5px; height: 20px;">
                            <div style="width: {:.2f}%; background-color: #4caf50; height: 100%; border-radius: 5px;"></div>
                        </div>
                    </div>
                    <div style="flex: 1; background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                        <h3>Total Lifetime CPD Hours</h3>
                        <p><strong>Completed Hours:</strong> {}</p>
                    </div>
                    <div style="flex: 1; background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);">
                        <h3>CPD Completed by Type</h3>
                        <img src="data:image/png;base64,{}" style="max-width: 100%;"/>
                    </div>
                </div>
            """.format(
                total_cpd_hours_year,
                percentage_completed,
                percentage_completed,
                total_cpd_hours_lifetime,
                encode_image_to_base64(generate_pie_chart(cpd_by_type))
            ),
            unsafe_allow_html=True
        )

    st.title("CPD Activities")
    st.write(user_data[['Title', 'Type', 'Hours', 'Date', 'Organization', 'Description', 'Learning outcomes', 'Links']])

    # Include Font Awesome for icons
    st.markdown('''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    ''', unsafe_allow_html=True)

    # Display three cards per row
    page_bg_img = f"""
            <style>
            /* Stretch the content to fit the window size */
            [data-testid="stAppViewContainer"] > .main {{
                padding-left: 10px;
                padding-right: 10px;
                max-width: 100%;
                width: 100%;
                margin: 0;
            }}

            /* Adjust the scaling box to have a fixed height and handle overflow */
            .scaling-box {{
                background-color: #F9F9F9;
                border: 1px solid #ddd;
                padding: 10px;
                margin: 10px;
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                transition: 0.3s;
                border-radius: 5px;
                text-align: left;
                height: 500px; /* Fixed height */
                display: flex;
                flex-direction: column;
                overflow: hidden; /* Hide overflowing content */
            }}

            .scaling-box:hover {{
                transform: scale(1.05);
            }}

            /* Handle expandable content within the box */
            .scaling-box .scaling-box-inner {{
                overflow-y: auto; /* Scrollable content */
                flex: 1; /* Take remaining space */
            }}

            /* Reduce margins between columns */
            .stColumn {{
                padding-left: 5px;
                padding-right: 5px;
            }}

            /* Hide the Streamlit top padding */
            .css-1d391kg {{
                padding-top: 0 !important;
            }}

            h3 {{
                --tw-text-opacity: 1;
                color: rgb(102 102 102/var(--tw-text-opacity));
                line-height: 1.5;
                font-weight: 600;
                font-size: 1.525rem;
                white-space: wrap;
                overflow: hidden;
                text-overflow: ellipsis;
                margin: 0;
            }}
            </style>
        """

    st.markdown(page_bg_img, unsafe_allow_html=True)

    # Show CPD activities in 3 columns
    st.title("CPD Activities")

    # Number of columns for each row
    num_cols = 3
    applist = st.container()

    # Assuming 'user_data' is the dataframe you're working with
    for i in range(0, len(user_data), num_cols):
        row = applist.columns(num_cols)
        for j in range(num_cols):
            if i + j < len(user_data):
                activity = user_data.iloc[i + j]
                # activity_cert_key = f"{os.getenv("AWS_S3_FOLDER_NAME")}/{username}-{activity["Certificate"]}"
                
                # url = s3.generate_presigned_url('get_object',
                #                 Params={
                #                     'Bucket': 'cpd-portal-files',
                #                     'Key': activity_cert_key,
                #                 },                                  
                #                 ExpiresIn=3600)
                
                # if activity['Certificate']:
                #     download_cert_button = f'''
                #         <a href="{url}" style="
                #             display: inline-block; 
                #             padding: 8px 16px; 
                #             border: 1px solid #6200ee; 
                #             border-radius: 5px; 
                #             color: #6200ee; 
                #             text-decoration: none;">
                #             Download certificate
                #         </a>
                #     '''
                # else:
                #     download_cert_button = ""
                
                with row[j]:
                    st.markdown(f'''
                        <div class="scaling-box">
                            <h3>{activity["Title"]}</h3>
                            <div class="scaling-box-inner">
                                <p><i class="fas fa-calendar-day"></i> <strong>Date of CPD Activity: </strong>{activity["Date"].strftime("%Y-%m-%d")}</p>
                                <p><i class="fas fa-tag"></i> <strong>Type:</strong> {activity["Type"]}</p>
                                <p><i class="fas fa-building"></i> <strong>Organization:</strong> {activity["Organization"]}</p>
                                <p><i class="fas fa-file-alt"></i> <strong>Description:</strong><p> {activity["Description"]}</p>
                                <p><i class="fas fa-bullhorn"></i> <strong>Outcomes & Objectives:</strong><p> {activity["Learning outcomes"]}</p>
                                <p><i class="fas fa-link"></i> <strong>Links:</strong><p><a href="{activity['Links']}" target="_blank">{activity['Links']}</a></p>
                            </div>
                            <p class="scaling-box-description">
                                <i class="fas fa-clock"></i> <strong>{activity["Hours"]} hours logged</strong>
                                <br>
                            </p>
                        </div>
                    ''', unsafe_allow_html=True)