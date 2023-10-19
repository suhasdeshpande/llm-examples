import openai
import streamlit as st
import http.client

conn = http.client.HTTPSConnection("api.courier.com")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    courier_api_key = st.text_input("Courier API Key", key="courier_api_key", type="password")


payload = ""

headers = {
    'Content-Type': "application/json",
    'User-Agent': "insomnia/8.3.0",
    'Authorization': "Bearer " + courier_api_key
    }

conn.request("POST", "/debug", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


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

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
