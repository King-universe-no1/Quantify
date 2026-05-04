#*------------------------------------=-IMPORTS---------------------------------------------------------*
import streamlit as st
from Helper import CheckLoginState,get_data,GetCurrencySymbol,ConvertCurrency
try:
 userid=st.session_state.userid
except Exception as e:
    st.error(f"Error fetching user id {e}")
    st.switch_page("Main.py")
from Helper import GetUserAssetswithCurrency
import time


st.set_page_config(layout="wide")
# from streamlit_autofresh import st_autorefresh

# st_autorefresh(interval=10000)  # 10 seconds
#------------------------------------------Home page--------------------------------------------------------------
if "user_currency" not in st.session_state:
            st.session_state.user_currency='Default'
#Initially setting user currency to INR, can be changed by user from the dashboard
CheckLoginState()
if userid:
  print(f"User ID: {userid}")
  for i in userid:
      userid=int(i)
#----USER id is a tuple hence directly passing it gives an error
  time.sleep(3)
  try:
      st.write(userid)
      assets=GetUserAssetswithCurrency(userid)
  except Exception as e:
    st.error(f"Error fetching user assets {e}")
#!ERROR HERE
else:
    st.error("User not logged in")
    st.stop()
    assets=None
    st.switch_page("Main.py")

#use the get_data fn
if assets:
 results_home=get_data(assets)
 #!ERROR PROGRAM NOT EXECUTING AFTER THIS LINE
 #gives the complete data of asset and useful data is extracted in the fn instead of while giving
#  st.write(results_home)
col1,col2=st.columns([11,1.8])
with col1:
    # st.title("Financial Dashboard",text_alignment="center")
    # st.subheader("Track your assets and investments in one place",text_alignment="center")
    st.markdown("####")
with col2:
        if st.button("Refresh",use_container_width=True,help="Click to refresh the data on the dashboard"):
                st.rerun()
        if "user_currency" not in st.session_state:
            st.session_state.user_currency='Default'
        else:
            st.session_state.user_currency=st.session_state.user_currency
        # st.write(st.session_state.user_currency)
        # st.session_state.currency_symbol=GetCurrencySymbol(st.session_state.user_currency)
        # st.write("Here")
        #!REMOVE AFTER IT WORKS
        currency_list=["Default","INR", "USD", "EUR", "GBP", "CNY"]
        for i in currency_list:
            if st.session_state.user_currency in i:
                choosen=currency_list.pop(currency_list.index(i))
                currency_list.insert(0,choosen)
                #sends the selected currency to top of the list
                #this ensures that the selected currency is visible to user and also selected by default
                break
            
        
        st.selectbox('Choose Currency',currency_list,key="user_currency",)
        st.write("Selected Currency:", st.session_state.user_currency)
        # #!REMOVE AFTER BUG FIXES
        st.session_state.currency_symbol=GetCurrencySymbol(st.session_state.user_currency)
        
        
st.title("Your Financial Dashboard",text_alignment="center")
st.subheader("Track your assets and investments in one place",text_alignment="center")
st.space("large")
# st.metric(label="Total Portfolio Value", value="$12,345.67", delta="+5.67%")
try:
    if len(results_home)>0:
        cols=st.columns(len(results_home))
    for i,result in enumerate(results_home):
        with cols[i]:
    #    latest=ConvertCurrency(result['currency'],st.session_state.user_currency,result['latest'])
            latest=result['latest']
            if st.session_state.currency_symbol ==None:
                display_currency=GetCurrencySymbol(result['currency'])
            st.metric(label=result["symbol"],
                value=f"{st.session_state.currency_symbol}{latest}",
                delta=f"{(latest-result['pricebought'])*100/result['pricebought']:.3f} %",
                border=True,
            #   chart_data=result["close_series"],
            #   chart_type="line",
               )
            st.write(result['currency'])
    #    st.write(result['open'])
    #the i is the columns index
    # st.line_chart(result["close_series"])
except Exception as e:
    st.write("Start Tracking to see something!")

# for i,result in enumerate(results_home):
#     with cols[i]:
#     #    latest=ConvertCurrency(result['currency'],st.session_state.user_currency,result['latest'])
#          latest=result['latest']
#          st.metric(label=result["symbol"],
#               value=f"{st.session_state.currency_symbol}{latest}",
#               delta=f"{(latest-result['pricebought'])*100/result['pricebought']:.3f} %",
#               border=True,
            #   chart_data=result["close_series"],
            #   chart_type="line",
      #         )
    #    st.write(result['open'])
    #the i is the columns index
    # st.line_chart(result["close_series"])
col1, col2, col3 = st.columns([1,2,1])

with col2:
     if st.button("Track New Asset",use_container_width=True):
         st.switch_page("pages/AssetTracking.py")

while True:
    time.sleep(30)
    st.rerun()
    #automatic reloading