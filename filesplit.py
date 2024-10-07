import streamlit as st
import pandas as pd
import readstat  # Replacing pyreadstat with readstat-py for reading SAS files
from io import BytesIO
import tempfile  # For handling temporary files

# Title of the app
st.title('File Upload and Split to First 500 Rows (CSV, SAS XPT, & SAS7BDAT)')

# Instructions
st.write("Upload a CSV, SAS XPT, or SAS7BDAT file. The app will select the first 500 rows and allow you to download the processed file in the same format.")

# File upload
uploaded_file = st.file_uploader("Choose a CSV, SAS XPT, or SAS7BDAT file", type=["csv", "xpt", "sas7bdat"])

# Function to handle CSV files
def process_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df.head(500)

# Function to handle SAS XPT and SAS7BDAT files using readstat-py
def process_sas_file(uploaded_file):
    # Write the file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Read the SAS file using readstat
    df = pd.DataFrame(readstat.read_sas7bdat(tmp_path))  # or readstat.read_xport(tmp_path)
    
    return df.head(500)

# File processing and download
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == 'csv':
        # Process CSV file
        df = process_csv(uploaded_file)
        
        # Display the first few rows of the dataframe
        st.write("Here are the first 500 rows of the CSV file:")
        st.write(df)

        # Convert the processed dataframe back to CSV
        csv = df.to_csv(index=False).encode('utf-8')
        
        # Download button for CSV
        st.download_button("Download CSV", data=csv, file_name="first_500_rows.csv")
    
    elif file_extension in ['xpt', 'sas7bdat']:
        # Process SAS XPT or SAS7BDAT file
        df = process_sas_file(uploaded_file)
        
        # Display the first few rows of the dataframe
        st.write(f"Here are the first 500 rows of the {file_extension} file:")
        st.write(df)

        # Fallback: Convert the processed dataframe to CSV for download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(f"Download CSV (converted from {file_extension})", data=csv, file_name=f"first_500_rows_{file_extension}.csv")

