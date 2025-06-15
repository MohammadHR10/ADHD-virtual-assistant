import streamlit as st
import requests
import time
import os
import speech_recognition as sr
import platform

# Initialize speech recognition
recognizer = sr.Recognizer()

# Get backend URL from environment variable or use default
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5001/chat")

# Check if running in cloud environment
IS_CLOUD = os.getenv("RENDER", "false").lower() == "true"

# Session State
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{int(time.time())}"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("🧠 ADHD Routine Assistant")
st.markdown("### 💬 Chat with your ADHD Assistant")

# Input mode selection - only show audio option if not in cloud
if IS_CLOUD:
    mode = "Type"
    st.info("ℹ️ Audio features are only available in the local version")
else:
    mode = st.radio("Input Mode", ["Type", "Speak"], horizontal=True)

user_message = ""
if mode == "Type":
    user_message = st.text_input("📝 Enter your message:")
elif mode == "Speak":
    if st.button("🎤 Record Now"):
        try:
            with sr.Microphone() as source:
                st.info("🎤 Listening... (Speak now)")
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=1)
                # Record audio
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                st.info("✅ Processing speech...")
                
            # Use Google's speech recognition
            user_message = recognizer.recognize_google(audio)
            st.success(f"You said: {user_message}")
        except sr.WaitTimeoutError:
            st.error("No speech detected. Please try again.")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand that. Please try again.")
        except sr.RequestError as e:
            st.error(f"Sorry, there was an error with the speech recognition service: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if user_message:
    st.spinner("🤖 Thinking...")
    payload = {
        "user_id": st.session_state.user_id,
        "message": user_message
    }

    try:
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

# Display chat history
st.header("🗂️ Chat History")
for sender, msg in st.session_state.chat_history[::-1]:
    st.markdown(f"*{sender}:* {msg}")

# Show environment info in sidebar
st.sidebar.markdown("### ℹ️ Environment Info")
st.sidebar.markdown(f"**Mode:** {'Cloud' if IS_CLOUD else 'Local'}")
st.sidebar.markdown(f"**Backend URL:** {BACKEND_URL}")

if not IS_CLOUD:
    st.sidebar.markdown("""
    ### 🎙️ Audio Features Available
    - Voice input
    - Speech recognition
    - Real-time audio processing
    """)