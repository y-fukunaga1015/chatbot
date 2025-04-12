import streamlit as st
from openai import OpenAI

# OpenAIクライアント初期化
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

USER_NAME = "user"
ASSISTANT_NAME = "assistant"
model = "gpt-4o-mini"

st.title("StreamlitのChatサンプル（OpenAI API版）")

def response_chatgpt(user_msg: str, chat_history: list = []):
    system_msg = "あなたはアシスタントです。"
    messages = [
        {"role": "system", "content": system_msg}
    ]

    # チャット履歴を追加
    if chat_history:
        for chat in chat_history:
            messages.append({"role": chat["name"], "content": chat["msg"]})

    # ユーザーメッセージを追加
    messages.append({"role": USER_NAME, "content": user_msg})

    # OpenAI API でレスポンス生成
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response

# チャットログをセッションに保持
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# 入力受付
user_msg = st.chat_input("メッセージを入力")
if user_msg:
    # 過去のチャットを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])

    # ユーザーの発言を表示
    with st.chat_message(USER_NAME):
        st.write(user_msg)

    # アシスタントの応答を取得・表示
    response = response_chatgpt(user_msg, chat_history=st.session_state.chat_log)
    assistant_msg = response.choices[0].message.content
    with st.chat_message(ASSISTANT_NAME):
        st.write(assistant_msg)

    # セッションにログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})

    # デバッグ用にチャットログを表示
    print("■ チャットログ:")
    for chat in st.session_state.chat_log:
        print(f"  {chat['name']}: {chat['msg']}")
