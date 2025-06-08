import streamlit as st
import requests
import time
import os

# Try to import audio features, but don't fail if not available
try:
    from audio import record_and_transcribe
    AUDIO_AVAILABLE = True
except (ImportError, OSError):
    AUDIO_AVAILABLE = False
    st.warning("🎙️ Audio features are not available in this environment. Please use text input instead.")

BACKEND_BASE = os.getenv("BACKEND_URL", "http://localhost:5001")
BACKEND_URL = f"{BACKEND_BASE}/chat"


# Session State
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 ADHD Routine Assistant")
st.markdown("Choose how you want to interact:")

# Only show audio option if available
input_options = ["Type"]
if AUDIO_AVAILABLE:
    input_options.append("Speak")

mode = st.radio("Input Mode", input_options, horizontal=True)

user_message = ""
if mode == "Type":
    user_message = st.text_input("📝 Enter your message:")
elif mode == "Speak" and AUDIO_AVAILABLE:
    if st.button("🎤 Record Now"):
        try:
            user_message = record_and_transcribe()
            st.success(f"You said: {user_message}")
        except Exception as e:
            st.error(f"🎙️ Speech error: {e}")

if user_message:
    st.spinner("🤖 Thinking...")
    payload = {
        "user_id": st.session_state.user_id,
        "message": user_message
    }

    try:
        st.text(f"DEBUG: Sending to {BACKEND_URL}")
        response = requests.post(BACKEND_URL, json=payload)
        
        if response.status_code == 200:
            reply = response.json().get("response", "No response")
            st.session_state.chat_history.append(("You", user_message))
            st.session_state.chat_history.append(("AI", reply))
            st.success(reply)
        else:
            st.error(f"❌ Backend error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"🚨 Request failed: {e}")

st.header("🗂️ Chat History")
for sender, msg in st.session_state.chat_history[::-1]:
    st.markdown(f"*{sender}:* {msg}")