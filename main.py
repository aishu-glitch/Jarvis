from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import streamlit as st
import os
import json
import datetime
from chat_box import render_chat_ui  


# ✅ Create chats folder
if not os.path.exists("chats"):
    os.makedirs("chats")


def save_message(session_id, role, message):
    timestamp = datetime.datetime.now().isoformat()
    chat_file = f"chats/{session_id}.json"

    if os.path.exists(chat_file):
        with open(chat_file, "r") as f:
            data = json.load(f)
    else:
        data = {"title": "untitled chat", "timestamp": session_id, "messages": []}

    data["messages"].append({
        "role": role,
        "message": message,
        "timestamp": timestamp
    })

    with open(chat_file, "w") as f:
        json.dump(data, f, indent=2)


def start_new_chat():
    if "current_chat" in st.session_state and st.session_state["current_chat"]:
        old_id = st.session_state["current_chat"]
        old_chat_file = f"chats/{old_id}.json"

        if os.path.exists(old_chat_file):
            with open(old_chat_file, "r") as f:
                old_data = json.load(f)

            full_chat_text = "\n".join([m["message"] for m in old_data["messages"]])

            if full_chat_text.strip():
                summary_prompt = f"summarize this conversation:\n{full_chat_text}\n"
                summary = Ollama(model="llama2")(summary_prompt).strip()

                title_prompt = f"generate a simple 3-5 word title:\n{summary}\n"
                title = Ollama(model="llama2")(title_prompt).strip()

                old_data["title"] = title

                with open(old_chat_file, "w") as f:
                    json.dump(old_data, f, indent=2)

    # ✅ New chat ID
    session_id = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"chats/{session_id}.json", "w") as f:
        json.dump({"title": "untitled chat", "timestamp": session_id, "messages": []}, f, indent=2)

    st.session_state["current_chat"] = session_id


# ✅ Prompt rules
prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""You are Jarvis — a helpful AI assistant.

Rules:
- Reply like ChatGPT — clear, polite, natural.
- No RP actions like *smiles* *chuckles* *adjust glasses*
- No robotic tone.

Conversation:
{history}

User: {input}
Jarvis:"""
)

# ✅ LangChain memory + model
chat_memory = ConversationBufferMemory(return_messages=True)
llm = Ollama(model="llama2")

chain = ConversationChain(
    llm=llm,
    memory=chat_memory,
    prompt=prompt,
    verbose=False
)

# ✅ chat session storage
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# ✅ create new chat on first run
if "current_chat" not in st.session_state:
    start_new_chat()

# ✅ UI input
user_input, send = render_chat_ui()

# ✅ Handle sending
if send and user_input.strip():
    # save to UI conversation
    st.session_state["messages"].append({"role": "user", "content": user_input})
    save_message(st.session_state["current_chat"], "user", user_input)

    # Get AI reply
    response = chain.run(user_input).strip()

    st.session_state["messages"].append({"role": "assistant", "content": response})
    save_message(st.session_state["current_chat"], "assistant", response)
    

    st.rerun()
