import streamlit as st
from openai import OpenAI

# 페이지 제목
st.title("🌸 탄생화 추천 AI 챗봇")
st.write(
    "생년월일을 입력하면 탄생화와 꽃 사진, 꽃말을 알려드립니다!"
)

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "너는 사용자의 생년월일을 기반으로 탄생화를 알려주는 AI 챗봇이야. "
                    "사용자가 생년월일을 입력하면 탄생화를 알려주고, "
                    "꽃말과 특징을 감성적으로 설명해줘. "
                    "그리고 반드시 아래 형식으로 답변해:\n\n"
                    "꽃 이름: [꽃 이름]\n"
                    "설명: [꽃 설명]\n"
                    "이미지 키워드: [영문 꽃 이름]"
                ),
            }
        ]

    # 이전 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":

            with st.chat_message(message["role"]):

                # assistant 메시지면 이미지 포함 출력
                if message["role"] == "assistant":

                    lines = message["content"].split("\n")

                    flower_name = ""
                    description = ""
                    image_keyword = ""

                    for line in lines:
                        if line.startswith("꽃 이름:"):
                            flower_name = line.replace("꽃 이름:", "").strip()

                        elif line.startswith("설명:"):
                            description = line.replace("설명:", "").strip()

                        elif line.startswith("이미지 키워드:"):
                            image_keyword = line.replace(
                                "이미지 키워드:", ""
                            ).strip()

                    # Unsplash 이미지 URL
                    image_url = (
                        f"https://source.unsplash.com/600x400/?{image_keyword},flower"
                    )

                    st.subheader(f"🌸 {flower_name}")
                    st.image(image_url, use_container_width=True)
                    st.markdown(description)

                else:
                    st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input(
        "생년월일을 입력해주세요! 예: 2004년 3월 15일"
    ):

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

        # 응답 가져오기
        bot_reply = response.choices[0].message.content

        # 세션 저장
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_reply}
        )

        # assistant 메시지 출력
        with st.chat_message("assistant"):

            lines = bot_reply.split("\n")

            flower_name = ""
            description = ""
            image_keyword = ""

            for line in lines:
                if line.startswith("꽃 이름:"):
                    flower_name = line.replace("꽃 이름:", "").strip()

                elif line.startswith("설명:"):
                    description = line.replace("설명:", "").strip()

                elif line.startswith("이미지 키워드:"):
                    image_keyword = line.replace(
                        "이미지 키워드:", ""
                    ).strip()

            # 이미지 URL 생성
            image_url = (
                f"https://source.unsplash.com/600x400/?{image_keyword},flower"
            )

            # 출력
            st.subheader(f"🌸 {flower_name}")
            st.image(image_url, use_container_width=True)
            st.markdown(description)
