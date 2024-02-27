import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
import openai
# 配置和初始化
openai.api_key = st.secrets["OPENAI_API_KEY"]
api_base = "https://pro.aiskt.com/v1"
openai.base_url = api_base

st.set_page_config(page_title="Chat with the Power electronic robot", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the Power electronic robot, powered by LlamaIndex 💬")
st.info("Check out the full tutorial to build this app in our [blog post](https://blog.streamlit.io/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/)", icon="📃")

# 初始化聊天历史
if "memory" not in st.session_state:
    st.session_state.memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the buck-boost docs – hang tight! This should take 1-2 minutes."):
        docs = SimpleDirectoryReader("data2").load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-0125-preview", temperature=0.1))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()
chat_engine = index.as_chat_engine(chat_mode="context", verbose=True) 

# 显示聊天历史
for message in st.session_state.memory.messages:  # 使用memory替代session_state.messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 用户输入
if prompt := st.chat_input("Your question"):
    # 更新聊天历史
    st.session_state.memory.add_message(role="user", content=prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 直接使用memory对象
            response = chat_engine.chat(prompt, st.session_state.memory.messages)
            st.write(response.response)
            if "buck-boost" in prompt:
                st.image('buck-boost电路.jfif')  # 显示图片
            # 更新聊天历史
            st.session_state.memory.add_message(role="assistant", content=response.response)
