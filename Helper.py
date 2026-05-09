import streamlit as st
from DatabaseConnection import GetUserAssets
import yfinance as yf
from forex_python.converter import CurrencyCodes
import requests
from DatabaseConnection import AddNewAsset,GetUserAssets
# if "user_currency" not in st.session_state:
#             st.session_state.user_currency='INR'
# st.write(st.session_state.user_currency)
#!Delete when bug fixes

# ConvertCurrency("USD",st.session_state.user_currency,430)
e=''
# def ConvertCurrency(original_currency, convert_to, amount):
#     for _ in range(5):
#         try:
#             c = CurrencyRates()

#             converted_amount = c.convert(original_currency, convert_to, amount)

#             if converted_amount is None:
#                 raise ValueError("Conversion returned None")

#             return converted_amount
# #!REMOVE ALL INSTANCESOF THIS
# #TODO Rewrite the currency system with a better api
#         except Exception as e:
#             time.sleep(1)
#             st.warning(f"Conversion problem: {e}")
#             #!FIX FROM HERE

#             #  fallback so app doesn't crash
#     return amount  # return original value instead of None
# @st.cache_data(ttl=3600)
# def ConvertCurrency(amount,from_currency:str,to_currency:str):
#     if to_currency == "Default":
#         return amount
#     if from_currency == to_currency:
#         return amount
#     #same currency not converted
#     url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
#     # try:
#     response = requests.get(url)
#     data = response.json()
#     exchange_rate = data['rates'][to_currency]
#     st.write(f"Converting {amount} from {from_currency} to {to_currency} at rate {exchange_rate} Amount is {type(amount)}")
#     try:
#         amount=float(amount)
#     except Exception as e:
#         st.warning(f"Amount conversion error: {e}")
#         return amount
#     #!REMOVE ALL INSTANCESOF THIS AFTER BUG RESOLVES
#     converted_amount = amount* exchange_rate
#     return converted_amount
#     # except Exception as e:
#     #     return f"Error: {e}"
# #coverted=ConvertCurrency(100,"USD","INR")
@st.cache_data(ttl=3600)
def GetCurrencySymbol(currency_code):
    # if currency_code == "Default" or None:
    #     return None
    # st.write(f"Getting symbol for {currency_code}")
    #!REMOVE AFTER BUG FIXES
    c=CurrencyCodes()
    code=c.get_symbol(currency_code)
    return code
import time
time.sleep(20)
def SetLoginState():
    st.session_state['logged_in'] = True

def CheckLoginState():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.stop("Tried to acces page without proper login")
        st.switch_page("Main.py")
        
@st.cache_data(ttl=300)
def get_data(assets):
    # st.write('Currency in get data',st.session_state.user_currency)
    results=[]
    for stock in assets:
        Atype=stock[0]
        #getting the type of asset from the tuple
        symbol=stock[1]
        #getting the symbol of the asset from the tuple
        pricebought=stock[-2]
        quantity=stock[-1]
        # st.write("My stock",stock)
        if Atype=="Stock":
            print("Stock")
            data,currency=GetStockData(symbol)
            time.sleep(1)
            #avoiding rate limits
            #st.write(f"Currency: {currency}")
            if data.empty:
                # st.warning(f"Error fetching data for {symbol}")
                continue
                #skips it
            # st.write(type(data["Close"].iloc[-1]))
            # results.append({
            #     "symbol": symbol,
            #     "latest": ConvertCurrency(data["Close"].iloc[-1],st.session_state.user_currency,currency),
            #     "open": ConvertCurrency(data["Open"].iloc[0],st.session_state.user_currency,currency),
            #     "high": ConvertCurrency(data["High"].iloc[-1],st.session_state.user_currency,currency),
            #     "low": ConvertCurrency(data["Low"].iloc[-1],st.session_state.user_currency,currency),
            #     #co pilot exchange position of currency and user currency in conversion function, check if it works correctly
            #     "close_series": data["Close"],
            #     "open_series": data["Open"],
            #     "index": data.index,
            #     'currency':currency,
            #     'pricebought':pricebought,
            #     'quantity':quantity,
            #     })
            else:
                try:
                #     st.write("Data before conversion",data)
                    results.append({
                    "symbol": symbol,
                    "latest": data["Close"].iloc[-1],
                    "open": data["Open"].iloc[0],
                    "high": data["High"].iloc[-1],
                    "low": data["Low"].iloc[-1],
                    #the second arg is the third arg and third arg is second arg fix it
                    "close_series": data["Close"],
                    "open_series": data["Open"],
                    "index": data.index,
                    "currency": currency,
                    "pricebought": pricebought,
                    "quantity": quantity,
                })
                    # st.write("Results",results)
                except Exception as e:
                    st.warning(f"Error in data for {symbol}: {e}")  
            # for item in results:
            #     for key,value in item.items():
            #         for i in range(5):
            #             if key=='symbol':
            #                 continue
            #             st.write(value)
            #             converted_value=ConvertCurrency(currency,st.session_state.user_currency,value)
            #             item[key]=converted_value
        elif Atype=="Crypto":
            print("Crypto")
            continue
            #TODO Add crypto support
        #st.write(data)
        # st.write(yf.ticker(symbol).info)
    # st.write("Returning data")
    #!REMOVE AFTR BUG FIXES
    # return data
    return results
@st.cache_data(ttl=300)
#reduced caching time to 5 minutes
def GetStockData(symbol,period="1d",interval="10m"):
    print(f"Getting data for {symbol}")
    try:
        stock=yf.Ticker(symbol)
    except Exception as e:
        st.warning(f"Error fetching data for {symbol}: {e}")
        return None,None
    #st.write(stock.info)
    try:
        data=stock.history(period=period,interval=interval)
        try:
            if data:
                currency=stock.fast_info.get("currency","USD")
                return data,currency
            else:
                st.warning(f"No currency info found for {symbol}, defaulting to USD")
                return data,"USD"
        except Exception as e:
            st.warning(f"Error fetching currency for {symbol}: {e}")
            return data,"USD"
        # except Exception as e:
        #     st.warning(f"Error extracting data from {symbol}: {e}",icon="⚠️")
            return None,None
    except Exception as e:
        st.warning(f"Error extracting  data from {symbol}: {e}",icon="⚠️")
        return None,None
@st.cache_data(ttl=3600)
def SmartSearch(query):
    top5list=[]
    try:
        search=yf.Search(query).quotes
        #only getting the quotes from the search results as it contains the symbol and the type of asset
        print(f"Search results for {query}:")
        print(search)
        # top5=search[:5]
        i=1
        for result in search:
            if result["symbol"].isdigit():
                continue
            else:
                top5list.append((result["symbol"],result["longname"]))
                i+=1
        return top5list
    except Exception as e:
        st.warning(f"Error fetching search results for {query}: {e}")
# SmartSearch("Tesla")
# get_data([["Stock","TSLA"]])

# def AddNewAssetwithCurrency(userid,assettype,symbol,MovementType,PriceBought,Quantity,SMSAlert,EmailAlert):
#     # PriceBought=PriceBought,st.session_state.user_currency,"INR")
#     #converts data into INR before adding to DB so that all data is in same currency and can be easily compared and calculated with
#     result,reason=AddNewAsset(userid,assettype,symbol,MovementType,PriceBought,Quantity,SMSAlert,EmailAlert)
#     return result,reason
# def GetUserAssetswithCurrency(userid):
#     assets=GetUserAssets(userid)
#     #assets is a list of tuples with each tuple containing the asset details
#     for asset in assets:
#         asset=list(asset)
#         # asset.insert(2, ConvertCurrency(asset[2], "INR", st.session_state.user_currency))
#         asset=tuple(asset)
#         #inserting after conversion cause tuple are immutable
#     #converts data into user's currency before showing on dashboard 

#     return assets
def check_user_id(userid):
    if userid is None:
        st.error("User not logged in")
        st.stop()
        st.switch_page("Main.py")
@st.cache_data(ttl=3600)
def GetShortName(symbol):
    stock=yf.Search(symbol).quotes
    # try:
    shortname=stock[0]['shortname']
    return shortname
    # except Exception as e:
    #     st.warning(f"Could not find {e}")
    