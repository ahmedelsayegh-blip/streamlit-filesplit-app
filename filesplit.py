import streamlit as st
import pandas as pd
import pyreadstat  # For reading and writing SAS XPT files
from io import BytesIO
import tempfile  # For creating temporary files

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

# Function to handle SAS XPT files
def process_xpt(uploaded_file):
    df, meta = pyreadstat.read_xport(uploaded_file)
    return df.head(500), meta

# Function to handle SAS7BDAT files
def process_sas7bdat(uploaded_file):
    # Write the file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    # Read the SAS7BDAT file from the temporary path
    df, meta = pyreadstat.read_sas7bdat(tmp_path)
    
    return df.head(500), meta

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
    
    elif file_extension == 'xpt':
        # Process SAS XPT file
        df, meta = process_xpt(uploaded_file)
        
        # Display the first few rows of the dataframe
        st.write("Here are the first 500 rows of the SAS XPT file:")
        st.write(df)

        # Convert the processed dataframe back to SAS XPT
        output = BytesIO()
        pyreadstat.write_xport(df, output, metadata=meta)
        
        # Download button for SAS XPT
        st.download_button("Download SAS XPT", data=output.getvalue(), file_name="first_500_rows.xpt")
    
    elif file_extension == 'sas7bdat':
        # Process SAS7BDAT file
        df, meta = process_sas7bdat(uploaded_file)
        
        # Display the first few rows of the dataframe
        st.write("Here are the first 500 rows of the SAS7BDAT file:")
        st.write(df)

        # **Since pyreadstat can't write SAS7BDAT, we provide alternative formats:**
        # Fallback: Convert the processed dataframe to CSV
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.write("Note: Exporting to SAS7BDAT format is not supported. Download as CSV instead.")
        
        # Download button for CSV
        st.download_button("Download CSV (Fallback for SAS7BDAT)", data=csv, file_name="first_500_rows.csv")

        # Optionally, you can offer XPT format as well
        output = BytesIO()
        pyreadstat.write_xport(df, output, metadata=meta)
        st.download_button("Download SAS XPT (Fallback for SAS7BDAT)", data=output.getvalue(), file_name="first_500_rows.xpt")
