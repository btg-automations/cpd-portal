import os
import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import pandas as pd
import json
from datetime import datetime
import matplotlib.pyplot as plt

from defaults import cpd_file, users_file

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Load CPD data from JSON file
def load_data(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save CPD data to JSON file
def save_data(data):
    with open(cpd_file, "w") as f:
        json.dump(data, f, indent=4)

# Add new entry in json
def add_data(file_name, new_entry):
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    data.append(new_entry)
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

def upload_to_s3(file, bucket_name, object_name):
    try:
        s3.upload_fileobj(file, bucket_name, object_name)
        st.success("File uploaded successfully!")
    except NoCredentialsError:
        st.error("Credentials not available")

def get_url(key):
    url = s3.generate_presigned_url('get_object',
                                    Params={
                                        'Bucket': 'cpd-portal-files',
                                        'Key': key,
                                    },                                  
                                    ExpiresIn=3600)
    return url

def generate_pie_chart(cpd_by_type, background_color='#f9f9f9'):
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # Set the background color for the figure and the axis
    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)
    
    colors = plt.get_cmap('Set3')(range(len(cpd_by_type)))
    ax.pie(cpd_by_type, labels=cpd_by_type.index, autopct='%1.1f%%', 
           startangle=90, wedgeprops={'width': 0.5}, colors=colors)
    
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
    plt.tight_layout()
    
    return fig

def encode_image_to_base64(fig):
    import io
    import base64
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    return img_str


# Logout
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.full_name = ""
    st.session_state.user_type = ""
    st.session_state.page = "Login"  # Redirect to login page after logout
    st.rerun()