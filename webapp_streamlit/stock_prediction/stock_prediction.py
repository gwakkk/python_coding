import streamlit as st
import pandas_datareader as pdr

# markdown형식의 문법 사용가능
st.write('''
# 삼성전자 주식 
마감 가격과 거래량을 도표로 표시
''')

# https://finance.yahoo.com/quote/005930.KS?p=005930.KS
df = pdr.get_data_yahoo('005930.KS', '2020-01-01', '2021-03-30')
# 야후 주식 historical 데이터를 df형태로 반환한다.

st.line_chart(df.Open)
# 시작가격
st.line_chart(df.Close)
# 마감가격
st.line_chart(df.Volume)
#거래량

# streamlit run [filename] 형태로 실행
# http://localhost:8501/