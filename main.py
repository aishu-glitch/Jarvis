from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import streamlit as st

st.title("Jarvis 🤖")

prompt = PromptTemplate(
    input_variables=["history","input"],
    template="""
You are **Jarvis**, an intelligent, polite, confident AI assistant.
You NEVER call yourself Nova. Always respond as Jarvis.

Conversation so far:
{history}

User: {input}
Jarvis:
"""
)

# Input box
input_txt = st.text_input("Please enter your queries here...")

# Memory to store full chat history
chat_memory = ConversationBufferMemory(return_messages=False)
llm = Ollama(model="llama2")

# Conversation chain
chain = ConversationChain(
    llm=llm,
    memory=chat_memory,
    prompt=prompt,
    verbose=False
)

# Session state to display chat like ChatGPT
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Generate reply
if input_txt:
    response = chain.run(input_txt)  # ✅ no index extraction
    st.session_state["messages"].append({"role":"assistant","content":response})

# Display only Jarvis replies (not user input)
for msg in st.session_state["messages"]:
    st.write(msg["content"])
