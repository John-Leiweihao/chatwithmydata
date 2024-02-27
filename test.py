import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
import os
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
import twolevelbuckboost

openai.api_key = st.secrets["OPENAI_API_KEY"]
api_base = "https://pro.aiskt.com/v1"
openai.base_url = api_base

st.set_page_config(page_title="Chat with the Power electronic robot", page_icon="🦙", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the Power electronic robot, powered by LlamaIndex 💬")
st.info(
    "Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)",
    icon="📃")
with open('./second.txt', 'r') as file:
    content1 = file.read()

if "messages" not in st.session_state:  # Initialize the chat messages history
    st.session_state.messages = [{"role": "user", "content": content1},
                                 {"role": "assistant", "content": "OK,I understand."}
                                 ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the buck-boost docs – hang tight! This should take 1-2 minutes."):
        docs = SimpleDirectoryReader("data1").load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-0125-preview", temperature=0.1))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


index = load_data()
chat_engine = index.as_chat_engine( chat_mode="context")

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    messages_history = [
    ChatMessage(role=MessageRole.USER if m["role"] == "user" else MessageRole.ASSISTANT, content=m["content"])
    for m in st.session_state.messages
]
    # 检查用户输入是否包含"拓扑图"
    if "buck-boost" in prompt:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt,messages_history)
                st.write(response.response)
                st.image('buck-boost电路.jfif')  # 假设这是与“拓扑图”相关的图片
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
    elif all(param in prompt for param in ["Uin", "Uo", "Prated", "fsw"]):
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # 如果用户输入不包含"拓扑图"，执行其他回答或操作
                response = chat_engine.chat(prompt,messages_history)
                list=response.response
                #Uin=list[0],Uo=list[1],Prated=list[2],fsw=list[3]
                #M,L1, Cin1, Cout1=twolevelbuckboost.calculation(Uin,Uo,Prated,fsw)
                #reply="这个电路工作在{}模态，其中电路的电感值为{},输入电容值为{},输出电容值为{}.".format(M,L1,Cin1,Cout1)
                st.write(list)
                # 可以在这里添加其他处理逻辑
                message = {"role": "assistant", "content": list}
                st.session_state.messages.append(message)
    else:
         with st.chat_message("assistant"):
             with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt,messages_history)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
