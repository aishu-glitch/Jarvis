import streamlit as st

def render_chat_ui():
    # Custom CSS to mimic ChatGPT input bar behavior
    st.markdown(
        """
        <style>
        /* Chat container scrolls behind input box */
        .main {
            padding-bottom: 130px !important;
        }

        /* Fixed bottom chat input box */
        .chat-input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 15px;
            background-color: #0d0d0d; /* Dark theme like ChatGPT */
            border-top: 1px solid #333;
            z-index: 1000;
        }

        /* Textarea style like ChatGPT */
        textarea {
            border-radius: 14px !important;
            border: 1px solid #3d3d3d !important;
            background-color: #1e1e1e !important;
            color: white !important;
            resize: none !important;
            padding: 12px !important;
            font-size: 16px !important;
            min-height: 50px !important;
            max-height: 200px !important; /* expand up to this */
            overflow-y: auto !important;
        }

        /* Send button style */
        .send-btn {
            background-color: #ffffff10;
            color: white;
            border-radius: 8px;
            padding: 8px 18px;
            border: 1px solid #444;
            cursor: pointer;
        }

        .send-btn:hover {
            background-color: #ffffff20;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h2 style='text-align:center;color:white;'>Jarvis 🤖</h2>", unsafe_allow_html=True)

    # Chat messages
    for chat in st.session_state.get("messages", []):
        role, content = chat["role"], chat["content"]
        if role == "user":
            st.markdown(f"<div style='text-align:right;background:#1e1e1e;padding:10px;border-radius:10px;margin:6px;'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left;background:#222;padding:10px;border-radius:10px;margin:6px;'>{content}</div>", unsafe_allow_html=True)

    # Input box
    with st.container():
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        user_input = st.text_area("", placeholder="Message Jarvis...", label_visibility="collapsed")
        
        send = st.button("Send", key="send", help="Send message", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    return user_input, send
