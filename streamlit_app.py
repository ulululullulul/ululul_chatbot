import streamlit as st
from openai import OpenAI

# 페이지 제목
st.title("🌸 탄생화 추천 AI 챗봇")

st.write(
    "생년월일을 입력하면 당신의 탄생화와 꽃말을 알려드립니다!"
)

# OpenAI API 키 입력
openai_api_key = st.text_input(
    "OpenAI API 키",
    type="password"
)

if not openai_api_key:
    st.info(
        "계속하려면 OpenAI API 키를 입력해주세요.",
        icon="🗝️"
    )

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 사용자의 생년월일을 기반으로 "
                    "탄생화를 알려주는 AI 챗봇이야. "
                    "사용자가 생년월일을 입력하면 "
                    "탄생화 이름, 꽃말, 특징을 "
                    "친절하고 감성적으로 설명해줘. "
                    "답변은 항상 한국어로 해줘."
                ),
            }
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":

            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input(
        "생년월일을 입력해주세요! 예: 2004년 3월 15일"
    ):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )

        # 응답 가져오기
        bot_reply = response.choices[0].message.content

        # 응답 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_reply
            }
        )

        # 챗봇 메시지 출력
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
