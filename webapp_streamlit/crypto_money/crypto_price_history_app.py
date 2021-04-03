import streamlit as st
from cryptocmd import CmcScraper
import plotly.express as px
from datetime import datetime

st.write('# cryptomoney Web App')

st.sidebar.header('Menu')
# 사이드바 메뉴를 설정

name = st.sidebar.selectbox('Name', ['BTC', 'ETH', 'USDT'])
# 코인의 종류를 선택하는 selectbox

start_date = st.sidebar.date_input('Start date', datetime(2021, 1, 1))
end_date = st.sidebar.date_input('End date', datetime(2021, 4, 2))

# https://coinmarketcap.com
scraper = CmcScraper(name, start_date.strftime('%d-%m-%Y'), end_date.strftime('%d-%m-%Y')) # '%d-%m-%Y'
#datatime은 일-월-연 순서로 변경하여 입력
df = scraper.get_dataframe()

fig_close = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title='가격')
fig_volume = px.line(df, x='Date', y=['Volume'], title='거래량')

st.plotly_chart(fig_close)
st.plotly_chart(fig_volume)

# streamlit run [filename] 형태로 실행
# http://localhost:8501/