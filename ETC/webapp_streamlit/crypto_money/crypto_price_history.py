import streamlit as st
from cryptocmd import CmcScraper
import plotly.express as px

st.write('# 비트코인 BTC ')

# https://coinmarketcap.com
# 코인데이터를 크롤링
scraper = CmcScraper('BTC', '01-01-2021', '07-01-2021') 
# '%d-%m-%Y'형태로 날짜를 역순으로 기입

df = scraper.get_dataframe()

fig_close = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title='가격')
fig_volume = px.line(df, x='Date', y=['Volume'], title='거래량')

st.plotly_chart(fig_close)
st.plotly_chart(fig_volume)