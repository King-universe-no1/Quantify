# import requests
# def CurrencyConverter(amount,from_currency,to_currency):
#     url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
#     try:
#         response = requests.get(url)
#         data = response.json()
#         exchange_rate = data['rates'][to_currency]
#         converted_amount = amount * exchange_rate
#         return converted_amount
#     except Exception as e:
#         return f"Error: {e}"
# coverted=CurrencyConverter(100,"USD","INR")
# print(coverted)
from Helper import get_data
import streamlit as st
st.session_state.user_currency="Default"
data=get_data([("Stock","WRTH",20.0,10),("Stock","AAPL",200.0,5),("Stock","TCS.NS",300.0,2),])
print(data)
st.write(data)