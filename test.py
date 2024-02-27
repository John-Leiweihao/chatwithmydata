import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document ,SimpleDirectoryReader
import os
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer

openai.api_key =st.secrets["OPENAI_API_KEY"]
api_base = "https://pro.aiskt.com/v1"
openai.base_url=api_base
memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

st.set_page_config(page_title="Chat with the Power electronic robot", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the Power electronic robot, powered by LlamaIndex 💬")
st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
with open('./second.txt', 'r') as file:
    content1 = file.read()

if "messages" not in st.session_state: # Initialize the chat messages history
    st.session_state.messages = [{"role": "user", "content": content1},{"role": "assistant", "content": "OK,I understand."}
    ]
    
@st.cache_resource(show_spinner=False)
def load_data():
        docs = SimpleDirectoryReader("data2").load_data()
        index = VectorStoreIndex.from_documents(docs)
        return index

index = load_data()
llm=OpenAI(model="gpt-4-0125-preview", temperature=0.5)
chat_engine = index.as_chat_engine(chat_mode="context",llm=llm,memory=memory) 

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

def update_chat_memory(user_input, bot_response=None):
    # 将用户输入添加到聊天记忆中
    memory.add_message({"role": "user", "content": user_input})
    if bot_response:
        # 如果有机器人响应，也添加到聊天记忆中
        memory.add_message({"role": "assistant", "content": bot_response})

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    update_chat_memory(prompt)  # 更新聊天记忆以包含最新的用户输入

    if "buck-boost" in prompt:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt, memory=memory)  # 确保传入当前的聊天记忆
                st.write(response.response)
                st.image('buck-boost电路.jfif')
                update_chat_memory(prompt, response.response)  # 更新聊天记忆以包含机器人的响应
    else:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt, memory=memory)  # 确保传入当前的聊天记忆
                st.write(response.response)
                update_chat_memory(prompt, response.response)  # 同上
