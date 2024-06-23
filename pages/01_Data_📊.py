import streamlit as st
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


# Set page configuration
st.set_page_config(page_title="Data", page_icon="📊",  layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status,username = authenticator.login(location='sidebar')


if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')

    st.title('Customer Data')
    def filter_columns(data):
        # Allow the user to select the data type to display
        data_type = st.selectbox('Select Data type', [
                                'All', 'Numeric Columns', 'Categorical Columns'])

        if data_type == 'Numeric Columns':
            data = data.select_dtypes(include=['number'])
        elif data_type == 'Categorical Columns':
            data = data.select_dtypes(include=['object', 'category'])

        # Display the filtered data in Streamlit
        st.write('Filtered Data:', data)


    # Define the path to the dataset
    dataset_path = 'Data/train.csv'

    # Check if the file exists
    if not os.path.isfile(dataset_path):
        st.error(
            f"The file '{dataset_path}' does not exist. Please check the path.")
    else:
        try:
            # Load the dataset
            data = pd.read_csv(dataset_path)
            # st.write('Loaded Data:', data)
            # Call the function to filter and display columns
            filter_columns(data)
        except Exception as e:
            st.error(f"Error loading the file '{dataset_path}': {e}")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            # st.write('Loaded Data:', data)
            # Call the function to filter and display columns
            filter_columns(data)
        except Exception as e:
            st.error(f"Error loading the uploaded file: {e}")


elif st.session_state['authentication_status'] is False:
    st.error('Wrong username/password')
elif st.session_state['authentication_status'] is None:
    st.info('Login to get access to the app')
    st.code("""
    Test Account
    Username: valiant
    Password: 123456
    """)

# st.write(st.session_state)


