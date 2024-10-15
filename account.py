import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
import os  # Import the os module for file operations

cred = credentials.Certificate("brain-analyser-3bf77a767a7a.json")

# Function to create a folder with the username as the folder name
def create_user_folder(username):
    try:
        folder_name = f"{username}"  # Generate folder name based on the username
        os.makedirs(folder_name, exist_ok=True)  # Create a new folder
        return folder_name  # Return the folder name if successful
    except Exception as e:
        st.warning(f'Failed to create user folder')
        return None
    
# Function to display folder contents including images
def d(folder_name):
    try:
        files = os.listdir(folder_name)  # Get the list of files in the folder
        if files:
            st.write(f"Contents of folder '{folder_name}':")
            for file in files:
                file_path = os.path.join(folder_name, file)
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    st.image(file_path, caption=file, use_column_width=True)
                else:
                    with open(file_path, "r") as f:
                        contents = f.read()  # Read file contents
                        st.write(f"File: {file}, Contents: {contents}")
        else:
            st.write(f"No files found in '{folder_name}'.")
    except Exception as e:
        st.warning(f'Failed to display folder contents: {e}')


# Function to grant access to the user for the created folder
def grant_folder_access(folder_name):
    try:
        os.chmod(folder_name, 0o777)  # Grant full access to the folder for the user
    except Exception as e:
        st.warning(f'Failed to grant access to user folder: {e}')

# Main application function
def app():
    st.title('Welcome to Analysis.Br')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    # Function to sign up with email and password
    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    # Function to sign in with email and password
    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    # Function to handle the login process
    def f():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']

            global Usernm
            Usernm = userinfo['username']

            st.session_state.signedout = True
            st.session_state.signout = True

            # Create user folder and grant access
            folder_name = create_user_folder(Usernm)
            if folder_name:
                grant_folder_access(folder_name)

        except:
            st.warning('Login Failed')

    # Function to handle the signout process
    def t():
        st.session_state.signout = False
        st.session_state.signedout = False
        st.session_state.username = ''

    # Initialize session state variables
    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    # User interface for login/signup
    if not st.session_state["signedout"]:
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password', type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username")

            if st.button('Create my account'):
                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')

        else:
            st.button('Login', on_click=f)

    # User interface after successful sign-in
    if st.session_state.signout:
        st.write('Welcome back ', st.session_state.username, '!')
        st.text('Email id: ' + st.session_state.useremail)
        st.button('Sign out', on_click=t)
        #st.button('Open Folder', on_click=d)
        folder_name = st.session_state.username  # Assuming folder name is the username
        st.button('Open Folder', on_click=lambda: d(folder_name))