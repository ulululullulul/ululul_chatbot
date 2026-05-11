import streamlit as st
from openai import OpenAI

# 봄 느낌 스타일 적용
st.markdown("""
    <style>

    /* 전체 배경 */
    .stApp {
        background: linear-gradient(
            to bottom,
            #FFF4F8,
            #FFE8F0,
            #FFF9E6
        );
    }

    /* 제목 */
    h1 {
        color: #E26D9F;
        text-align: center;
        font-weight: 700;
    }

    /* 설명 텍스트 */
    p {
        color: #6B5B66;
    }

    /* 채팅 메시지 */
    .stChatMessage {
        background-color: rgba(255,255,255,0.72);
        border-radius: 18px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid rgba(255,255,255,0.5);
        backdrop-filter: blur(6px);
    }

    /* 입력창 */
    .stChatInputContainer {
        background-color: transparent;
        border-top: none;
    }

    .stChatInputContainer > div {
        background: rgba(255,255,255,0.72);
        border: 2px solid #F4BCD3;
        border-radius: 20px;
        padding: 6px 12px;
        box-shadow: 0 4px 12px rgba(226,109,159,0.12);
    }

    /* 텍스트 입력 필드 */
    textarea {
        color: #6B5B66 !important;
        font-size: 15px !important;
    }

    textarea::placeholder {
        color: #C597AE !important;
    }

    /* API 키 입력 필드 */
    .stTextInput input {
        background-color: rgba(255,255,255,0.75);
        border: 2px solid #F4BCD3;
        border-radius: 14px;
        color: #6B5B66;
        padding: 10px;
    }

    /* 포커스 시 */
    .stTextInput input:focus,
    textarea:focus {
        border-color: #E26D9F !important;
        box-shadow: 0 0 0 0.15rem rgba(226,109,159,0.2);
    }

    </style>
""", unsafe_allow_html=True)

# 페이지 제목
st.title("🌸 탄생화 추천 AI 챗봇")

st.write(
    "생년월일을 입력하면 당신의 탄생화와 꽃말을 알려드립니다!"
)

# API 키 입력
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
