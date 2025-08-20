from openai import OpenAI
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Sam's alternate Chatbot")
st.caption("🚀 Work with a shy chat.")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Alright, what’s the problem? How can I help you? Let’s fix it. Let’s get it done."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    
    # Your fixed system prompt
    system_prompt = {
        "role": "system",
        "content": "Your name is Sam, but act like Donald Trump. Respond in his speaking style: confident, direct, dominant tone, with catchphrases and emphasis."
    }
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # Build the full messages list for the API (system prompt + history)
    api_messages = [system_prompt] + st.session_state.messages
    
    # Get model response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=api_messages
    )
    
    msg = response.choices[0].message.content
    
    # Save only user/assistant messages (no system)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
