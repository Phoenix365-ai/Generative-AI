import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model (chat)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

# Page config
st.set_page_config(page_title="madhu Chatbot", page_icon="🦜", layout="centered")

# --- Custom CSS for aesthetics ---
st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }
    .stChatMessage {
        background-color: #ffffff;
        padding: 10px 16px;
        border-radius: 16px;
        margin-bottom: 8px;
        max-width: 85%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .stChatMessage.user {
        background-color: #dcf8c6;
        margin-left: auto;
    }
    .stChatMessage.assistant {
        background-color: #f1f0f0;
        margin-right: auto;
    }
    .footer {
        font-size: 13px;
        color: #888;
        margin-top: 40px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("## 🦜 madhu Chatbot")
st.markdown("Welcome! Ask me anything. I’m powered by Gemini 💬")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous messages
for role, content in st.session_state.chat_history:
    bubble_class = "user" if role == "user" else "assistant"
    st.markdown(
        f'<div class="stChatMessage {bubble_class}">{content}</div>',
        unsafe_allow_html=True
    )

# Chat input
prompt = st.chat_input("Type your message...")

if prompt:
    # Show user message
    st.session_state.chat_history.append(("user", prompt))
    st.markdown(f'<div class="stChatMessage user">{prompt}</div>', unsafe_allow_html=True)

    # Gemini response
    with st.spinner("Thinking..."):
        try:
            response = chat.send_message(prompt)
            reply = response.text
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

    # Show assistant reply
    st.session_state.chat_history.append(("assistant", reply))
    st.markdown(f'<div class="stChatMessage assistant">{reply}</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown('<div class="footer">Made with 💖 just for u </div>', unsafe_allow_html=True)



