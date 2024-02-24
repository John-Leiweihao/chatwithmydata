import streamlit as st
from llama_index.core import GPTVectorStoreIndex, ServiceContext, Document ,SimpleDirectoryReader
import os
import openai
from llama_index.llms.openai import OpenAI
os.environ['OPENAI_API_KEY']=st.secrets["OPENAI_API_KEY"]
openai.api_key =os.environ['OPENAI_API_KEY']
api_base = "https://one.aiskt.com/v1"
openai.base_url=api_base

st.set_page_config(page_title="Chat with the Power electronic robot, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the Power electronic robot, powered by LlamaIndex 💬🦙")
st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")
with open('./first.txt', 'r') as file:
    content1 = file.read()

if "messages" not in st.session_state: # Initialize the chat messages history
    st.session_state.messages = [{"role": "assistant", "content": "Ask me  questions about buck-boost!"}
    ]
    
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the buck-boost docs – hang tight! This should take 1-2 minutes."):
        docs = SimpleDirectoryReader("data1").load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt=content1))
        index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()


index = load_data()
chat_engine = index.as_chat_engine( )

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 检查用户输入是否包含"拓扑图"
    if "拓扑图" in prompt:
        with st.chat_message("assistant"):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            st.image('buck-boost电路.jfif')  # 假设这是与“拓扑图”相关的图片
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
    else:
        with st.chat_message("assistant"):
            # 如果用户输入不包含"拓扑图"，执行其他回答或操作
            response = chat_engine.chat(prompt)
            st.write(response.response)
            # 可以在这里添加其他处理逻辑
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)