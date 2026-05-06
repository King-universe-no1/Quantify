import streamlit as st
from Helper import check_user_id,GetShortName
from DatabaseConnection import GetUserAssets,DeleteAsset
st.header("Remove Asset")
st.text("Easily remove an asset from your portfolio by selecting it from the list. Keep your dashboard organized and up-to-date with just a few clicks.")

user_stocks=[]
symbol_list=[]
check_user_id(st.session_state.userid)
try:
    userid=st.session_state.userid[0]
    
    # st.write(userid)
    if userid:
        assets=GetUserAssets(userid)
        
except Exception as e:
    st.warning(f"Error fetching user assets {e}",icon="⚠️")
# for asset in assets:
#     symbol=asset[1]
#     name=GetShortName(symbol)
#     user_stocks.append(name)

# st.multiselect("Select stocks to remove : ",options=user_stocks)
for asset in assets:
            symbol=asset[1]
            name=GetShortName(symbol)
            user_stocks.append(name)
            symbol_list.append(symbol)
deletingassets=st.multiselect("Select stocks to remove : ",options=user_stocks)
col1,col2,col3=st.columns([3,4,1])
with col2:
    if deletingassets:
        delete_asset=st.button("Delete Selected Assets ",width=200)
        # sure=st.checkbox("Are you sure ?",help="This action cannot be undone, please make sure you have selected the correct assets before proceeding")
        if delete_asset: 
                for asset in deletingassets:
                    symbol=symbol_list[user_stocks.index(asset)]
                    #gets the index of the asset in user stocks and gets the symbol of that asset based on index
                    #not sure how stable this logic is but works tbh so np for now
                    DeleteAsset(userid,symbol)
                    st.switch_page("pages/HomePage.py")
col1,col2,col3=st.columns([3,4,1])
with col2:
    if st.button("Go Back",width=200):
        st.switch_page("pages/HomePage.py")