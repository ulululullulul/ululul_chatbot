import streamlit as st
from openai import OpenAI

# 제목과 설명 표시
st.title("💬 챗봇")
st.write(
    "이 챗봇은 OpenAI의 GPT-3.5 모델을 사용하여 응답을 생성합니다. "
    "이 앱을 사용하려면 OpenAI API 키가 필요합니다. "
    "API 키는 [여기](https://platform.openai.com/account/api-keys)에서 발급받을 수 있습니다. "
    "또한 이 앱을 단계별로 만드는 방법은 "
    "[공식 튜토리얼](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)에서 확인할 수 있습니다."
)

# 사용자에게 OpenAI API 키 입력받기
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요. 🌻", icon="🗝️")
else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 채팅 입력창 생성
    if prompt := st.chat_input("무엇이든 물어보세요! 🌻"):

        # 사용자 메시지 저장 및 출력
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API로 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": m["role"],
                    "content": m["content"]
                }
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 스트리밍 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 답변 끝에 해바라기 이모지 추가
        response_with_flower = response + " 🌻"

        # 다시 출력
        st.markdown(response_with_flower)

        # 세션에 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_with_flower
            }
        )
