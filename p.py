import streamlit as st

st.title("두근♡두근♡ 확률계산기")
st.write("뽑기 재화와 가진 티켓 개수 입력")
q=0
t=0
q = st.text_input("재화개수")
t = st.text_input("티켓개수")
st.success(1-0.993**((q//120)+t))