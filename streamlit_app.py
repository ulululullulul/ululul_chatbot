import streamlit as st
from openai import OpenAI

# 페이지 제목
st.title("🌸 탄생화 추천 AI 챗봇")
st.write(
    "생년월일을 입력하면 당신의 탄생화를 알려주는 AI 챗봇입니다. "
    "탄생화의 의미와 꽃말도 함께 설명해드립니다."
)

# API 키 입력
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 사용자의 생년월일을 기반으로 탄생화를 알려주는 AI 챗봇이야. "
                    "사용자가 생년월일을 입력하면 해당 날짜의 탄생화를 알려주고, "
                    "꽃말과 특징, 어울리는 분위기를 친절하고 감성적으로 설명해줘. "
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
    if prompt := st.chat_input("생년월일을 입력해주세요! 예: 2004년 3월 15일"):

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
        )

        # 응답 내용 가져오기
        bot_reply = response.choices[0].message.content

        # 답변 끝에 해바라기 추가
        bot_reply += " 🌻"

        # 챗봇 메시지 출력
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        # 응답 저장
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )
