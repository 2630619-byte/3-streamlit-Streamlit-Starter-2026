import streamlit as st

st.title("두근♡두근♡ 확률계산기")
st.write("과연 당신은 이번 뽑기에서 몇퍼센트 확률로 뽑을 수 있을까요?")

q_input = st.text_input("재화개수")
t_input = st.text_input("티켓개수")

try:
    q = int(q_input) if q_input else 0
    t = int(t_input) if t_input else 0
    if (q // 120) + t < 200:
        probability = 100 * (1 - (0.993 ** ((q // 120) + t)))
        st.success(f"확률: {probability:.4f}")
    else:
        st.success("★경☆확률: 100.0000☆축★")
        st.success("무조건 뽑을 수 있는!")
        st.success("확정 뽑기 즐거운!")
except ValueError:
    st.error("재화개수와 티켓개수는 숫자로 입력해주세요.")
