# app.py

import streamlit as st
from rag_app import ask_rag

# 페이지 설정
st.set_page_config(
    page_title="폐쇄망 로컬 AI 코딩 어시스턴트",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 폐쇄망 로컬 AI 코딩 어시스턴트")
st.caption("LCEL 기반 RAG · 내부 문서 우선")


# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_question" not in st.session_state:
    st.session_state.last_question = None


# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# 사용자 입력
user_input = st.chat_input("코딩 또는 내부 문서에 대해 질문해보세요")

if user_input:
    # 사용자 메시지 기록
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner("AI가 답변을 생성 중입니다..."):

            # 일반 설명 요청
            if user_input == "일반 설명" :
                if st.session_state.last_question:
                    answer = ask_rag(
                        st.session_state.last_question,
                        allow_general=True
                        )
                else:
                    answer = "일반 설명을 요청할 질문이 없습니다."
            else:
                st.session_state.last_question = user_input
                answer = ask_rag(user_input, allow_general=False)

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
