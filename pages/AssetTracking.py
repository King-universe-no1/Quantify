import streamlit as st
#-------TRACK NEW ASSET-----------
from Helper import SmartSearch,get_data,check_user_id
from DatabaseConnection import AddNewAsset
import time
#------Setting variables
assetpl='AAPL'
asset='Apple'
# i=0
if "userid" not in st.session_state:
    check_user_id(None)
if "currentasset" not in st.session_state:
    st.session_state.currentasset = None
#checks if current asset has already been set and if not sets it to None
if "data" not  in st.session_state:
        st.session_state.data=[{"latest":0.0,"currency":"Default"},]
        st.session_state .buyprice = st.session_state.data[0]['latest']
#using makeshift data untill real data is fetched
if "data" in st.session_state:
    data = st.session_state.data
   
    st.session_state.user_currency = (
    data[0].get("currency")
    if type(data)==list and len(data) > 0 and isinstance(data[0], dict)
    else "Default"
    # if data and isinstance(data[0], dict)
    # else "Default"
    #!SMTH FEELS FISHY HERE CHECK IT OUT
)
    # st.session_state.data=[{"latest":0.0,"currency":"USD"},{}]
if "assetpl" not in st.session_state:
    st.session_state.assetpl = "AAPL"
if "buyprice" not in st.session_state:
    price=st.session_state.data[0]['latest']
    st.session_state.buyprice = price
    
else:
    price=st.session_state.buyprice
    # st.session_state.buyprice = price
#-----------CODE START-------
st.title("Track A New Asset",text_alignment="center")
st.space(15)
st.text("Easily track a new stock, cryptocurrency, or other financial asset by entering its symbol and type. Stay updated on your investments with real-time data and insights.")
st.space("small")
st.subheader("Add a New Asset to Your Portfolio",text_alignment="center")
st.markdown("""
<style>

/* Center the main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 800px;
    margin: auto;
}

/* Title styling */
h1 {
    text-align: center;
    font-size: 3rem;
    margin-bottom: 0.5rem;
}

/* Subtitle text */
p {
    text-align: center;
    font-size: 1.1rem;
    color: #aaa;
    margin-bottom: 2rem;
}

/* Section heading */
h2 {
    margin-top: 2rem;
    text-align: left;
}

/* Input + form spacing */
.stTextInput, .stSelectbox {
    margin-bottom: 1rem;
}

/* Button styling */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    padding: 0.6rem;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)
st.selectbox("Select Asset Type", options=["Stock"], index=0, key="asset_type",help="Currently only stocks are supported, more asset types coming soon!")

#--key is used to store the value of the selectbox in session state--
#--index is used to set the default value of the selectbox--
assetinput=st.text_input(f"Enter {st.session_state.asset_type} Name",placeholder=asset,key="asset")
asset=st.session_state.asset
assetpl=st.session_state.assetpl
assettype=st.session_state.asset_type
st.caption("Press Enter for Results to update")
def add(i): 
    return i+1
def button(result):
    asset=result[1]
    st.session_state.assetpl=result[0]
    assetpl=result[0]
    st.session_state.asset=asset
    assets=[[assettype,assetpl,asset],]
    # st.write("Before get data",assets)
    # st.write(st.session_state.user_currency)
    st.session_state.data=get_data(assets)
    #data comes here when stock name is entered
    
    #!remove after bug fixes
    price=st.session_state.data[0]['latest']
    #!BUG HERE
    st.session_state.buyprice = price
    #asset pl refers to its symbol
    #*this ensures to update all the relevant data when user chooses a new stock
    return asset
# while True:
#     time.sleep(0.1)

if asset:
    # if st.session_state.buyprice != price:
    #     st.session_state.buyprice = price
    st.write("Did you mean -")
    i=0
    # st.write(st.session_state.asset,st.session_state.currentasset)
    #!!REMOVE AFTER BUG FIXED
    # st.session_state.currentasset = asset
    if st.session_state.currentasset != asset:
        # st.rerun()
        st.session_state.currentasset = asset
        
        # price=st.session_state.data[0]['latest']
        # st.session_state.buyprice = price
        #!!BUG HERE
        # price=st.session_state.buyprice
        #changing price to latest price when asset changes
        # st.write("Changed asset, resetting price to latest price")
    top5list=SmartSearch(asset)
    # st.write("Got result")
    col1,col2,col3=st.columns([2,4,2])
    with col2:
        # st.write("Creating buttons")
        if top5list:
            for result in top5list:
                if i<=5:
                    st.button(f"{result[0]} ({result[1]})",help="Click to include this asset",width='stretch',key=f"Asset{add(i)}",on_click=button,args=(result,))
                    #*RESULT contains codename and long name of the stock rest details come through the get data fn
                    i=add(i)
                    # st.write(result)
                    #!!REMOVE AFTER BUG FIXED
    # assets=[[assettype,assetpl,asset],]
    # st.session_state.data=get_data(assets)
    
    # st.write(assets)
           

    # st.radio("When should we notify you about price changes?",options=["Small Movements","Medium Movements","High Movements"])
    # st.button("Next ",help="Click to proceed to the next step of the asset tracking process",width='stretch',on_click=lambda: st.switch_page("AssetTracking2"))
    if "data" not  in st.session_state:
        st.session_state.data=[{"latest":0.0,}]
        st.session_state .buyprice = st.session_state.data[0]['latest']
    #changes buyprice when stock changes
    # st.write(data[0]['latest'])
    #st.number_input("Set the price at which stock bought",value=st.session_state.data[0]['latest'],step=0.01,key="buy_price")
    # st.rerun()
else:
    st.write("Find recommendations for your asset")
if "data" not in st.session_state:
        st.session_state.data=[{"latest":0.0,}]
# st.session_state.buy_price = data[0]['latest']
if asset:
    if st.session_state.user_currency == "Default":
        #st.write(st.session_state.data)
        #!REMOV AFTER BUG FIXES
        currency_for_price=st.session_state.data[0]['currency']
    else:
        currency_for_price=st.session_state.user_currency
    num_input=st.number_input(f"Set the price at which stock bought (In {currency_for_price})",value=price,step=1.00,key="buyprice")
    st.number_input("Select Quantity Bought",value=1,step=1,key="quantity")
    # st.write(st.session_state.data)
    # st.write(st.session_state.buyprice,price)
    st.toggle('Enable Price Alerts on SMS',key="alerts")
    st.toggle('Enable Daily Summary Emails',key="emails")
    if st.session_state.alerts:
        st.radio("When should we notify you about price changes?",options=["Small Movements","Medium Movements","High Movements"])
    # st.session_state.buyprice=price
    # userid=st.session_state.userid
    # st.write(userid[0])
    if st.button("Track Asset",help="Click to start tracking asset",width='stretch'):
        time.sleep(0.5)
        userid=st.session_state.userid[0]
        # CurrencyRates(st.session_state.user_currency,"INR",st.session_state.buyprice)
        result,reason=AddNewAsset(userid,assettype,assetpl,MovementType="Medium Movements",PriceBought=st.session_state.buyprice,Quantity=st.session_state.quantity,SMSAlert=st.session_state.alerts,EmailAlert=st.session_state.emails)
        if result:
            # st.success(reason)
            st.success(f"Now tracking {assetpl} ({asset})")
            st.balloons()
            time.sleep(0.5)
            st.switch_page("pages/HomePage.py")
        else:
            st.warning(reason)
            st.error(reason)
        # st.write("Redirecting to Home Page...")
        # time.sleep(2)
    