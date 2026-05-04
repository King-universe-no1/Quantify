import streamlit as st
import pathlib
base=pathlib.Path(__file__).parent.parent
from DatabaseConnection import signup_user
from Helper import SetLoginState
def error_msg(msg):
    st.error(msg)
    col1, col2, col3 = st.columns([2,2,2])
    with col2:
       if st.button("Try Again"):
        st.rerun()
col1, col2, col3 = st.columns([1,2,1])
with col2:
 st.image(str(base/"Logo.png"),width=200,use_container_width=True)

# st.text("Real Time Market Alerts",text_alignment="center")
st.subheader("Signup",text_alignment="center")
userphone=st.text_input("Enter your phone number",placeholder="98*******71")
useremail=st.text_input("Enter your email id",placeholder="me123@gmail.com")
userpassword=st.text_input("Enter your password",placeholder="MyPassword123$")
reenterpassword=st.text_input("Re-enter your password",placeholder="MyPassword123$")
col1, col2, col3 = st.columns([1,2.5,1])
with col2:
 if st.button("SIGN UP!",use_container_width=True):
    if userphone and useremail and userpassword:
        print("Valid details")
        if  not userpassword==reenterpassword:
            error_msg("Passwords do not match")
        else:
            result,statement=signup_user(userphone,useremail,userpassword)
            if result:
                st.success("Account created successfully!")
                st.balloons()
                SetLoginState()
                st.session_state.userid=statement
                st.switch_page("pages/HomePage.py")
            else:
                error_msg(statement)
                
            
    else:
        error_msg("Enter all details")

col1, col2, col3 = st.columns([3,4,3])
with col2:
 if st.button("Already Have an Account? Login!"):
     st.switch_page("Main.py")
