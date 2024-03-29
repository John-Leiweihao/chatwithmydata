import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
import os
import openai
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.llms import ChatMessage, MessageRole
import twolevelbuckboost
import threelevelbuckboost
import NPCDAB
import ast
openai.api_key = st.secrets["OPENAI_API_KEY"]
api_base = "https://pro.aiskt.com/v1"
openai.base_url = api_base

st.set_page_config(page_title="Chat with the Power electronic robot", page_icon="💎", layout="centered",
                   initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the Power electronic robot🤖, powered by LlamaIndex 🙂")
st.info( "Hello, I am a robot designed specifically for converters!", icon="🤟")
with open('./second.txt', 'r') as file:
    content1 = file.read()
with st.sidebar:
  st.markdown("<h1 style='color: #FF5733;'>Optional Converter</h1>", unsafe_allow_html=True)
  st.markdown('---')
  st.markdown('\n- Two-Level Buck-Boost\n- Three-Level Buck-Boost\n- NPC-Type Three-Level Full-Bridge DAB')
  st.markdown('---')
clear_button=st.sidebar.button('Clear Conversation',key='clear')

if clear_button or "messages" not in st.session_state:  # Initialize the chat messages history
    st.session_state.messages = [{"role": "user", "content": content1},
                                 {"role": "assistant", "content": "OK,I understand."}
                                 ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the buck-boost docs – hang tight! This should take 1-2 minutes."):
        docs = SimpleDirectoryReader("data1").load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-4-0125-preview", temperature=0.1,system_prompt="You are an expert in power supply design in the field of power electronics, and your job is to answer technical questions.Assume that all problems are related to the power supply design.Keep your answers technical and fact-based -- don't hallucinate."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index


index = load_data()
chat_engine = index.as_chat_engine( chat_mode="context")

for message in st.session_state.messages[2:]:  # Display the prior chat messages
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
    # 回答
    if "two-level buck-boost" in prompt.lower():  # 检查输入，不区分大小写
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt, messages_history)
                st.write(response.response)
                st.write("The topology of the two-level buck-boost circuit is shown in the following figure")
                st.image('twolevelbuckboost.png')
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
    elif "three-level buck-boost" in prompt.lower():
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt,messages_history)
                st.write(response.response)
                st.write("The topology of the three-level buck-boost circuit is shown in the following figure")
                st.image('threelevelbuckboost.png')  
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
    elif "npc-type three-level full-bridge dab"in prompt.lower():
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt,messages_history)
                st.write(response.response)
                st.write("The topology of the NPC-type three-level full-bridge DAB is shown in the following figure")
                st.image('NPCDAB.png')  
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
    elif all(param in prompt for param in ["Uin", "Uo", "Prated", "fsw","two-level"]):
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # 如果用户输入不包含"拓扑图"，执行其他回答或操作
                response = chat_engine.chat(prompt,messages_history)
                answer_list = ast.literal_eval(response.response)
                #st.write(response.response)
                Uin, Uo, Prated, fsw = answer_list
                M,L, C1,C2,R,KP,KI=twolevelbuckboost.calculation2(Uin,Uo,Prated,fsw)
                reply="The two-level buck-boost circuit operates in {} mode,the circuit inductance L value is {}H ,the value of capacitor C1 is {}F,The value of capacitor C2 is {}F ,the load resistance R is {}Ω .".format(M,L,C1,C2,R)
                st.write(reply)
                reply1="For this converter, I recommend you to use the single current loop control strategy. Its control block diagram and the controller built by simulink are shown in the figure below.When M=1 the circuit operates in Buck mode, and when M=0 the circuit operates in Boost mode.Where IL is the reference value of inductance current and IL1/IL0 is the measured value of inductance current.The controller used is PI controller, where KP value is {}, KI value is {}, and the output voltage is controlled to the reference voltage by controlling the duty cycle and on-time of switches S1,S2".format(KP,KI)
                st.write(reply1)
                st.image('twolevelbuckboostPI控制框架.png')
                st.image('twolevelbuckboostPI.png')
                message = {"role": "assistant", "content": reply}
                st.session_state.messages.append(message)
    elif all(param in prompt for param in ["Uin", "Uo", "Prated", "fsw","three-level"]):
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt,messages_history)
                answer_list = ast.literal_eval(response.response)
               # st.write(answer_list)
                Uin, Uo, Prated, fsw = answer_list
                M,L, C1, C2,C3,R,KP,KI=threelevelbuckboost.calculation3(Uin,Uo,Prated,fsw)
                reply="The three-level buck-boost circuit operates in {} mode,the circuit inductance L value is {}H ,the value of capacitor C1 is {}F,the value of capacitor C2 is {}F,the value of capacitor C3 is {}F,the load resistance R is {}Ω .".format(M,L,C1,C2,C3,R)
                st.write(reply)
                reply1="For this converter, I recommend you to use the single current loop control strategy. Its control block diagram and the controller built by simulink are shown in the figure below.When M=1 the circuit operates in Buck mode, and when M=0 the circuit operates in Boost mode.Where IL is the reference value of inductance current and IL1/IL0 is the measured value of inductance current.The controller used is PI controller, where KP value is{}, KI value is{}, and the output voltage is controlled to the reference voltage by controlling the duty cycle and on-time of switches S1,S2,S3 and S4.".format(KP,KI)
                st.write(reply1)
                st.image('threelevelbuckboostPI控制框架.png')
                st.image('threelevelbuckboostPI.png')
                message = {"role": "assistant", "content": reply}
                st.session_state.messages.append(message)
    elif all(param in prompt for param in ["Uin", "Uo", "Prated", "fsw","NPC"]):
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt,messages_history)
                answer_list = ast.literal_eval(response.response)
               # st.write(answer_list)
                Uin, Uo, Prated, fsw = answer_list
                n,L, Cin,Cout,R,KP,KI=NPCDAB.calculation4(Uin,Uo,Prated,fsw)
                reply="The turns ratio of the transformer in the NPC-type three-level full-bridge DAB circuit is {}:1.,the circuit inductance L value is {}H ,the value of capacitor Cin is {}F,the value of capacitor Cout is {}F,the load resistance R is {}Ω .".format(n,L,Cin,Cout,R)
                st.write(reply)
                reply1="For this converter, I recommend single voltage closed loop control for the single phase shift control strategy,Its control block diagram and the controller built by simulink are shown in the figure below, where DCout is the reference value of output voltage,V2 is the measured value of the output voltage, and the controller used is the PI controller, KP value is{}, KI value is{}. By controlling the phase difference between the primary unclamped switch tube and the secondary unclamped switch tube, the output voltage is controlled to the reference voltage.".format(KP,KI)
                st.write(reply1)
                st.image('NPCDABPI控制框架.png')
                st.image('NPCDABPI.png')
                message = {"role": "assistant", "content": reply}
                st.session_state.messages.append(message)
    else:
         with st.chat_message("assistant"):
             with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt,messages_history)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)
