from openai import OpenAI
import streamlit as st
import random

st.set_page_config("ChatMinds", page_icon="🔥")
st.title("ChatMinds🔥")

devlopers = ["*Nasir*", "*Aatif*", "*Vishal*", "*Ahsan*"]
random.shuffle(devlopers)
dev_text = ", ".join(devlopers)
st.markdown(f"Developed by {dev_text}")


with st.sidebar:
    st.sidebar.title("Configure")
    model = st.selectbox("Model", ("gpt-3.5-turbo", "gpt-4"))
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1)


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            temperature=temperature,
        ):
            full_response += response.choices[0].delta.content or ""
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
