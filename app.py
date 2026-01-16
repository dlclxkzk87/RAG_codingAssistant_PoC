import streamlit as st
from rag_app import ask_rag

# 페이지 설정
st.set_page_config(
    page_title="로컬 AI 코딩 어시스트턴트",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 폐쇄망 로컬 AI 코딩 어시스트턴트")
st.caption("RAG 기반 · 내부 문서 참고")

# 세션 상태 초기화 (대화 히스토리)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
user_input = st.chat_input("코딩이나 문서에 대해 질문해보세요")

if user_input:
    # 사용자 메시지
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답
    with st.chat_message("assistant"):
        with st.spinner("AI가 답변을 생성 중입니다..."):
            answer = ask_rag(user_input)
            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
