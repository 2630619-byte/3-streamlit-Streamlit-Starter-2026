st.markdown("""
<style>
@keyframes one_animation {
    0% {
        color: black;
        font-size: 24px;
    }
    100% {
        color: blue;
        font-size: 16px;
    }
}
.animated-one {
    animation: one_animation 0.8s ease-in-out forwards;
    display: inline;
}
</style>
""", unsafe_allow_html=True)
st.write(f'<span style="color:skyblue;padding:4px 8px;border-radius:6px"> <span class="animated-one">1</span>성 횟수: {st.session_state.one_star_count}회</span> ', unsafe_allow_html=True)
