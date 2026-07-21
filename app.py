import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(
    page_title="Crypto Dashboard",
    page_icon="📈",
    layout="wide"
)

st.sidebar.title("⚙️ Settings")
currency = st.sidebar.selectbox(
    "Select Currency",
    ["usd", "inr", "eur", "gbp"]
)

available_coins = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Solana": "solana",
    "Dogecoin": "dogecoin",
    "Cardano": "cardano",
    "Litecoin": "litecoin",
    "Ripple (XRP)": "ripple",
    "Binance Coin": "binancecoin"
}

selected_coins = st.sidebar.multiselect(
    "Select Crytocurrencies",
    list(available_coins.keys()),
    default=["Bitcoin", "Ethereum", "Solana", "Dogecoin"]
)

coin_ids = ",".join(
    available_coins[coin]
    for coin in selected_coins
)

st_autorefresh(interval=30000, key="crypto_refresh")

st.title("📈 Live Cryptocurrency Dashboard")
st.write("Real-time cryptocurrency prices using the CoinGecko API")

url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies={currency}"

response = requests.get(url)
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    
if response.status_code == 200:
    st.success("🟢 Connected to CoinGecko API")
else:
    st.success("🔴 Unable to connect to CoinGeko API")
    st.stop()

data = response.json()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

crypto_names = []
crypto_prices = []

for coin in selected_coins:
    coin_id = available_coins[coin]
    crypto_names.append(coin)
    crypto_prices.append(data[coin_id][currency])

df = pd.DataFrame({
    "Cryptocurrency": crypto_names,
    f"Price ({currency.upper()})": crypto_prices,
    "Timestamp": [current_time] * len(crypto_names)
})

currency_symbols = {
    "usd": "$",
    "inr": "₹",
    "eur": "€",
    "gbp": "£"
}

symbol = currency_symbols[currency]

if not selected_coins:
    st.warning("Please select at least one cryptocurrency.")
    st.stop()

cols = st.columns(len(selected_coins))

for col, coin in zip(cols, selected_coins):

    coin_id = available_coins[coin]

    with col:
        st.metric(
            coin,
            f"{symbol}{data[coin_id][currency]:,.2f}"
        )

st.write(f"🕒 Last Update: {current_time}")

st.subheader("Current Prices")
st.dataframe(
    df.style.format({
        "Price ({currency})": "${:,.2f}"
    }),
    use_container_width=True
)
