import random
import time

import streamlit as st

# 확률 상수
PICKUP_3STAR_PROB = 0.007
NON_PICKUP_3STAR_PROB = 0.03
TWO_STAR_PROB = 0.215

# 색상 상수
CARD_COLORS = {
    "픽업": ("orchid", "#f3e8ff"),
    "3성": ("orchid", "#f3e8ff"),
    "2성": ("#b58900", "#fff8dc"),
    "1성": ("skyblue", "#e1f5fe"),
}

# 앱 제목과 간단한 설명
st.title("뽑기 시뮬레이터")

@st.cache_resource
def load_css():
    return '''
<style>
@keyframes grow-shrink {
    0% { font-size: 60px; }
    100% { font-size: 50px; }
}
</style>
'''

st.markdown(load_css(), unsafe_allow_html=True)
st.write("1뽑 / 10뽑을 실제로 시뮬레이션합니다.")

# 1회 또는 10회 뽑기 선택
choice = st.selectbox("몇 뽑할 건가요?", ["1", "10"])

# 기본 상태를 한 번에 초기화
default_state = {
    "one_draw_count": 0,
    "one_star_count": 0,
    "two_star_count": 0,
    "not_three_star_count": 0,
    "three_star_count": 0,
    "change_count": 0,
    "sign_input": "",
    "draw_results": [],
    "phase": "idle",
    "preview_done": False,
}
for key, default in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = default

# 확률 정보 출력
st.write(f"1뽑 누적 횟수: {st.session_state.one_draw_count}회")
st.markdown(
    "- 픽업 3성 확률: 0.07%\n"
    "- 비픽업 3성 확률: 2.93%\n"
    "- 3성 확률: 3%\n"
    "- 2성 확률: 18.5%\n"
    "- 1성 확률: 78.5%"
)


def get_card_html(name, color, bg_color, pickup=False, animate=False, element_id=""):
    """결과 카드를 HTML 문자열로 반환합니다."""
    animation = "animation: grow-shrink 0.6s ease-in-out 0s 1 both;" if animate else ""
    bold = "font-weight:bold;" if pickup else ""
    id_attr = f' id="{element_id}"' if element_id else ""
    # 애니메이션이 적용될 때마다 고유한 data 속성을 추가하여 DOM 변경을 강제
    data_attr = f' data-animation-id="{int(time.time() * 1000)}"' if animate else ""
    return (
        f'<p{id_attr}{data_attr} style="display:inline-block; font-size: 50px; {animation}">'
        f'<span style="color:{color};background-color:{bg_color};padding:6px 12px;'
        f'border-radius:8px;{bold}">{name}</span></p>'
    )


def draw_once():
    """한 번 뽑기를 실행하고 결과를 반환합니다."""
    st.session_state.one_draw_count += 1
    value = random.random()
    
    if value < PICKUP_3STAR_PROB:
        st.session_state.three_star_count += 1
        result = "픽업"
    elif value < NON_PICKUP_3STAR_PROB:
        st.session_state.not_three_star_count += 1
        result = "3성"
    elif value < TWO_STAR_PROB:
        st.session_state.two_star_count += 1
        result = "2성"
    elif st.session_state.one_draw_count % 10 != 0:
        st.session_state.one_star_count += 1
        result = "1성"
    else:
        st.session_state.two_star_count += 1
        result = "2성"
    
    color, bg_color = CARD_COLORS[result]
    pickup = result == "픽업"
    return result, color, bg_color, pickup


def reset_draw_state():
    """새 뽑기를 시작할 때 필요한 상태를 초기화합니다."""
    st.session_state.phase = "sign"
    st.session_state.preview_done = False
    st.session_state.sign_input = ""
    st.session_state.next_index = 0
    st.session_state.draw_results = []


def has_good_result(results):
    return any(name in ("픽업", "3성") for name, *_ in results)


def show_preview_results(results):
    cols = st.columns(5)
    for idx, item in enumerate(results):
        col = cols[idx % 5]
        name, color, bg_color, pickup = item
        with col:
            st.markdown(
                get_card_html(name, color, bg_color, pickup=pickup, animate=True, element_id=f"preview-{idx}"),
                unsafe_allow_html=True,
            )
        time.sleep(0.2)


if st.button("뽑기 시작"):
    reset_draw_state()
    for _ in range(int(choice)):
        st.session_state.draw_results.append(draw_once())

result = st.session_state.draw_results
text_holder = st.empty()
sign_holder = st.empty()
name_holder = st.empty()

if st.session_state.phase != "idle" and result:
    if st.session_state.phase == "sign":
        # 3성/픽업이 있으면 90% 확률로 orchid, 10% 확률로 skyblue
        if has_good_result(result):
            st.session_state.sign_color = "orchid" if random.random() < 0.9 else "skyblue"
        else:
            st.session_state.sign_color = "skyblue"
        
        text_holder.markdown(
            f'<span style="color:{st.session_state.sign_color};font-weight:bold">싸인해주세요 선생님!</span>',
            unsafe_allow_html=True,
        )
        sign_value = sign_holder.text_input("", key="sign_widget")
        if sign_value.strip():
            st.session_state.sign_input = sign_value.strip()
            st.session_state.phase = "preview"
            st.rerun()

    elif st.session_state.phase == "preview":
        text_holder.empty()
        sign_holder.empty()
        name_holder.markdown(
            f'<span style="color:{st.session_state.sign_color};font-weight:bold">{st.session_state.sign_input}</span>',
            unsafe_allow_html=True,
        )
        if not st.session_state.preview_done:
            show_preview_results(result)
            st.session_state.preview_done = True

    elif st.session_state.phase == "view":
        text_holder.empty()
        sign_holder.empty()
        name_holder.markdown(
            f'<span style="color:{st.session_state.sign_color};font-weight:bold">{st.session_state.sign_input}</span>',
            unsafe_allow_html=True,
        )



def display_stats():
    """통계를 화면에 출력합니다."""
    st.write(f"뽑기 스택 횟수: {st.session_state.one_draw_count}회")
    if st.session_state.one_draw_count >= 200:
        if st.button("교환"):
            st.session_state.one_draw_count -= 200
            st.session_state.three_star_count += 1
            st.session_state.change_count += 1
            st.write("교환 완료! ☆픽업 3성 획득!☆")
    
    st.write(f'누적 뽑기 횟수: {st.session_state.one_draw_count + st.session_state.change_count * 200}회')
    
    stats = [
        ("픽업 3성 횟수", st.session_state.three_star_count, "orchid"),
        ("비픽업 3성 횟수", st.session_state.not_three_star_count, "orchid"),
        ("2성 횟수", st.session_state.two_star_count, "#b58900"),
        ("1성 횟수", st.session_state.one_star_count, "skyblue"),
    ]
    
    for label, count, color in stats:
        st.write(f'<span style="color:{color};font-weight:bold;padding:4px 8px;border-radius:6px"> {label}: {count}회</span>', unsafe_allow_html=True)

display_stats()
