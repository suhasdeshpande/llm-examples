import openai
import streamlit as st
import http.client
import pinecone
pinecone.init(api_key="d37c4793-4a04-4eac-86af-d6a9f0e280f5", environment="asia-southeast1-gcp-free")

index_name = 'knowledge-base'

index = pinecone.Index(index_name)


conn = http.client.HTTPSConnection("api.courier.com")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    courier_api_key = st.text_input("Courier API Key", key="courier_api_key", type="password")


payload = ""



st.title("🐦 BirdWatch")
st.caption("ゞ Turning logs into conversations")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What you want to know?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if not courier_api_key:
        st.info("Please add your Courier API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    prompt = st.session_state.messages[-1]
    input = prompt.get('content')

    response_from_open_ai = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=input,
        encoding_format="float"
    )

    embedding = response_from_open_ai.get('data')[0].get('embedding')

    query_response = index.query(
        top_k=2,
        include_metadata=True,
        vector=embedding,
    )

    print('query_response', query_response)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(query_response)
