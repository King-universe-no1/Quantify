import streamlit as st
# st.title("Quantify",text_alignment="center")
import pathlib
from DatabaseConnection import check_user_info
from Helper import SetLoginState
base=pathlib.Path(__file__).parent
st.set_page_config(initial_sidebar_state="collapsed")
hide_sidebar_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)
def error_msg(msg):
    st.error(msg)
    col1, col2, col3 = st.columns([2,2,2])
    with col2:
       if st.button("Try Again"):
        st.rerun()
col1, col2, col3 = st.columns([1,2,1])
with col2:
 st.image(str(base/"Logo.png"),width=200,use_column_width=True)

# st.text("Real Time Market Alerts",text_alignment="center")
st.subheader("Login",text_alignment="center")
userphone=st.text_input("Enter your phone number",placeholder="98*******71")
useremail=st.text_input("Enter your email id",placeholder="me123@gmail.com")
userpassword=st.text_input("Enter your password",placeholder="MyPassword123$")
col1, col2, col3 = st.columns([1,2.5,1])
with col2:
 if st.button("LOGIN",use_container_width=True):
    if userphone and useremail and userpassword:
        print("Valid details")
        result,statement=check_user_info(userphone,useremail,userpassword)
        if result:
            st.success("User Log in Sucessful!")
            SetLoginState()
            st.session_state.userid=statement
            st.switch_page("pages/HomePage.py")
        else:
            error_msg(statement)
    else:
        error_msg("Enter all details")

col1, col2, col3 = st.columns([3,4,3])
with col2:
 if st.button("Don't have an account? Sign Up!"):
     st.switch_page("pages/signup.py")

