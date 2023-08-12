import streamlit as st
import streamlit_authenticator as stauth
import datetime
import re
from deta import Deta
DATA_KEY='d0j6euzkhxu_zPjEC6kYCvndvoDsV6bGaFGmQp7gyVgk'
deta=Deta(DATA_KEY)

db=deta.Base('signin')

def insert_user(email,username,password):
    date_joined=str(datetime.datetime.now())

    return db.put({'key':email,'username':username,'password':password,'date_joined':date_joined})

def fetch_users():

    users=db.fetch()

    return users.items
#insert_user('a123@gmail.com','abc123','1234567')
#print(fetch_users())
def get_user_email():
    users=db.fetch()
    emails=[]
    for user in users.items:
        emails.append(user['key'])
    return emails

def get_user_email():
    users=db.fetch()
    emails=[]
    for user in users.items:
        emails.append(user['key'])
    return emails
def get_username():
    users=db.fetch()
    username=[]
    for user in users.items:
        username.append(user['key'])
    return username
def validate_email(email):
    pattern="^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"

    if re.match(pattern,email):
        return True
    return False

def validate_username(username):
    pattern="^[a-zA-Z0-9]*$"
    if re.match(pattern,username):
        return True
    return False

def signup():
    st.write('hello')
    st.title('Hello EVERYone')
    st.write("Signin for more content")
    with st.form(key='signup',clear_on_submit=True):
        st.subheader(':green[Sign Up]')
        email=st.text_input(':blue[Email]',placeholder='Enter your email')
        username=st.text_input(':blue:[user name]',placeholder='Enter your username')
        password=st.text_input(':blue[Password]',type='password',placeholder='Enter your password')
        cpassword=st.text_input('Confrim Password',placeholder='Confirm your password')
        st.form_submit_button('Sign Up')

        if email:
            if validate_email(email):
                if email not in get_user_email():
                    if validate_username(username):
                        if username not in get_username():
                            if len(username)>2:
                                if len(password)>=6:
                                    if password==cpassword:
                                        pass
                                        hashed_password=stauth.Hasher([password]).generate()
                                        insert_user(email,username,hashed_password[0])
                                        st.success("Account Created Successully")
                                        st.balloons()
                                    else:
                                        st.warning('Password didnt match')
                                else:
                                    st.warning('Password is short')
                            else:
                                st.warning('Username is too short')
                        else:
                            st.warning('Username Exist')    
                else:
                    st.warning('Email Already exist')
            else:
                st.warning('Invalid Email')
#sign_up()