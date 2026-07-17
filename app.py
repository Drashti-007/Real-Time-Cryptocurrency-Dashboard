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

st_autorefresh(interval=30000, key="crypto_refresh")

st.title("📈 Live Cryptocurrency Dashboard")
st.write("Real-time cryptocurrency prices using the CoinGecko API")

url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,dogecoin&vs_currencies=usd"

response = requests.get(url)

if response.status_code == 200:
    st.success("🟢 Connected to CoinGecko API")
else:
    st.success("🔴 Unable to connect to CoinGeko API")
    st.stop()

data = response.json()

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

crypto_names = []
crypto_prices = []

for crypto in data:
    crypto_names.append(crypto.capitalize())
    crypto_prices.append(data[crypto]['usd'])

df = pd.DataFrame({
    "Cryptocurrency": crypto_names,
    "Price (USD)": crypto_prices,
    "Timestamp": [current_time] * len(crypto_names)
})

df["Price (USD)"] = df["Price (USD)"].round(2)

df = df.sort_values(
    by="Price (USD)",
    ascending=False
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("₿ Bitcoin", f"${data['bitcoin']['usd']:,}")

with col2:
    st.metric("Ξ Ethereum", f"${data['ethereum']['usd']:,}")

with col3:
    st.metric("◎ Solana", f"${data['solana']['usd']:,}")

with col4:
    st.metric("🐶 Dogecoin", f"${data['dogecoin']['usd']}")

st.write(f"🕒 Last Update: {current_time}")

st.subheader("Current Prices")
st.dataframe(
    df.style.format({
        "Price (USD)": "${:,.2f}"
    }),
    use_container_width=True
)
