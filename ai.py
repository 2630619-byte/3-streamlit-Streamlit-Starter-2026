import random

import streamlit as st

import time

st.title("뽑기 시뮬레이터")
st.write("1뽑 / 10뽑을 실제로 시뮬레이션합니다.")

choice = st.selectbox("몇 뽑할 건가요?", ["1", "10"])

if "one_draw_count" not in st.session_state:
    st.session_state.one_draw_count = 0
if "one_star_count" not in st.session_state:
    st.session_state.one_star_count = 0
if "two_star_count" not in st.session_state:
    st.session_state.two_star_count = 0
if "not_three_star_count" not in st.session_state:
    st.session_state.not_three_star_count = 0
if "three_star_count" not in st.session_state:
    st.session_state.three_star_count = 0
if "change_count" not in st.session_state:
    st.session_state.change_count = 0
st.write(f"1뽑 누적 횟수: {st.session_state.one_draw_count}회")

st.markdown(
    "- 픽업 3성 확률: 0.7%\n"
    "- 비픽업 3성 확률: 2.3%\n"
    "- 3성 확률: 3%\n"
    "- 2성 확률: 18.5%\n"
    "- 1성 확률: 78.5%"
)
button = st.button("뽑기 시작")
time.sleep(2)
if button and choice == "1":
    st.session_state.one_draw_count += 1
    value = round(random.random(), 4)
    if value < 0.007:
        st.session_state.three_star_count += 1
        st.markdown(
            '<span style="color:orchid;background-color:#f3e8ff;font-weight:bold;padding:4px 8px;border-radius:6px">픽업</span>',
            unsafe_allow_html=True,
        )
    elif value < 0.007 + 0.023:
        st.session_state.not_three_star_count += 1
        st.markdown(
            '<span style="color:orchid;background-color:#f3e8ff;padding:4px 8px;border-radius:6px">3성</span>',
            unsafe_allow_html=True,
        )
    elif value < 0.007 + 0.023 + 0.185:
        st.session_state.two_star_count += 1
        st.markdown(
            '<span style="color:#b58900;background-color:#fff8dc;padding:4px 8px;border-radius:6px">2성</span>',
            unsafe_allow_html=True,
        )
    else:
        if (st.session_state.one_draw_count) % 10 != 0:
            st.session_state.one_star_count += 1
            st.markdown(
                '<span style="color:skyblue;background-color:#e1f5fe;padding:4px 8px;border-radius:6px">1성</span>',
                unsafe_allow_html=True,
            )
        else:
            st.session_state.two_star_count += 1
            st.markdown(
                '<span style="color:#b58900;background-color:#fff8dc;padding:4px 8px;border-radius:6px">2성</span>',
                unsafe_allow_html=True,
            )
elif button and choice == "10":
    results = []
    for _ in range(10):
        st.session_state.one_draw_count += 1
        value = round(random.random(), 4)
        if value < 0.007:
            st.session_state.three_star_count += 1
            results.append(
                '<span style="color:orchid;background-color:#f3e8ff;font-weight:bold;padding:4px 8px;border-radius:6px">픽업</span>'
            )
        elif value < 0.007 + 0.023:
            st.session_state.not_three_star_count += 1
            results.append('<span style="color:orchid;background-color:#f3e8ff;padding:4px 8px;border-radius:6px">3성</span>')
        elif value < 0.007 + 0.023 + 0.185:
            st.session_state.two_star_count += 1
            results.append('<span style="color:#b58900;background-color:#fff8dc;padding:4px 8px;border-radius:6px">2성</span>')
        else:
            if (st.session_state.one_draw_count)% 10 != 0:
                st.session_state.one_star_count += 1
                results.append('<span style="color:skyblue;background-color:#e1f5fe;padding:4px 8px;border-radius:6px">1성</span>')
            else:
                st.session_state.two_star_count += 1
                results.append('<span style="color:#b58900;background-color:#fff8dc;padding:4px 8px;border-radius:6px">2성</span>')
    st.markdown("### 10뽑 결과")
    for i in range():
        st.markdown(" ".join(results[i:i+1]), unsafe_allow_html=True)
        time.sleep(0.5)

st.write(f"뽑기 스택 횟수: {st.session_state.one_draw_count}회")
if st.session_state.one_draw_count >= 200:
    if st.button("교환"):
        st.session_state.one_draw_count -= 200
        st.session_state.three_star_count += 1
        st.session_state.change_count += 1
        st.write(f"교환 완료!")
        st.write(f"☆픽업 3성 획득!☆ 즐겁다! 엉청난! ")
st.write(f'누적 뽑기 횟수: {st.session_state.one_draw_count+st.session_state.change_count*200}회')
st.write(f'<span style="color:orchid;font-weight:bold;padding:4px 8px;border-radius:6px"> 픽업 3성 횟수: {st.session_state.three_star_count}회</span> ', unsafe_allow_html=True)
st.write(f'<span style="color:orchid;padding:4px 8px;border-radius:6px"> 비픽업 3성 횟수: {st.session_state.not_three_star_count}회</span>', unsafe_allow_html=True)
st.write(f'<span style="color:#b58900;padding:4px 8px;border-radius:6px"> 2성 횟수: {st.session_state.two_star_count}회</span>', unsafe_allow_html=True)
st.write(f'<span style="color:skyblue;padding:4px 8px;border-radius:6px"> 1성 횟수: {st.session_state.one_star_count}회</span> ', unsafe_allow_html=True)
