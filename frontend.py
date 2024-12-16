# 必要なPythonライブラリをインポート
import uuid, boto3
import streamlit as st
from os.path import basename
from urllib.parse import unquote
from oci.config import from_file
from oci.generative_ai_agent_runtime.models import ChatDetails, CreateSessionDetails
from oci.generative_ai_agent_runtime.generative_ai_agent_runtime_client import GenerativeAiAgentRuntimeClient

service_endpoint = "https://agent-runtime.generativeai.us-chicago-1.oci.oraclecloud.com"
agent_endpoint_id = "ocid1.genaiagentendpoint.oc1.us-chicago-1.XXXXXXX" # エージェントエンドポイントIDを入れる

# Agentクライアントを作成
if "client" not in st.session_state:
    config = from_file()
    st.session_state.client = GenerativeAiAgentRuntimeClient(
        config=config,
        service_endpoint=service_endpoint
    )
client = st.session_state.client

# セッションIDを作成
if "session_id" not in st.session_state:
    st.session_state.session_id = client.create_session(
        create_session_details=CreateSessionDetails(
            display_name=str(uuid.uuid4()),
        ),
        agent_endpoint_id=agent_endpoint_id
    ).data.id
session_id = st.session_state.session_id

# メッセージ格納用のリストを作成
if "messages" not in st.session_state:
    st.session_state.messages = []
messages = st.session_state.messages

# タイトルを表示
st.title("おっす、おらOCI生成AIエージェント！")

# 過去のメッセージを表示
for message in messages:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

# チャット入力欄を定義
if prompt := st.chat_input("何でもは知らないわよ。知ってることだけ"):

    # ユーザーの入力をメッセージに追加
    messages.append({"role": "human", "text": prompt})

    # ユーザーの入力を画面に表示
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bedrockエージェントの呼び出し設定
    response = client.chat(
        agent_endpoint_id=agent_endpoint_id,
        chat_details=ChatDetails(
            user_message=prompt,
            session_id=session_id,
            should_stream=False
        )
    )

    # エージェントの回答を画面に表示
    with st.chat_message("assistant"):
        answer = response.data.message.content.text
        st.write(answer)

        # 取得したチャンクの引用元をすべてリストアップ
        filenames = [
            basename(unquote(citation.source_location.url))
            for citation in response.data.traces[0].citations
        ]

        # 重複排除して表示
        if filenames:
            st.markdown("【参考にした資料】")
            for filename in sorted(set(filenames)):
                st.markdown(f"- {filename}")

        # 会話履歴を追加
        messages.append({"role": "assistant", "text": answer})