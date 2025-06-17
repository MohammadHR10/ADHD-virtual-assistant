import streamlit as st
import requests
import time
import os
import random
import speech_recognition as sr
from datetime import datetime

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

# Get the response from the adhd assistant and show it 
def get_response(prompt):
    # message_placeholder = st.empty()
    # full_response = ""
    # Send request to backend
    payload = {
        "user_id": st.session_state.user_id,
        "message": prompt
    }

    try:
        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_URL, json=payload)
            if response.status_code == 200:
                reply = response.json().get("response", "No response")
                if reply.startswith('"') and reply.endswith('"'):
                    reply = reply[1:-1]
        
                # Simulate stream of response with milliseconds delay
                # for chunk in reply.split():
                #     full_response += chunk + " "
                #     time.sleep(0.05)
                #     # Add a blinking cursor to simulate typing
                #     st.markdown(full_response + "▌")
                st.markdown(reply)
                
            else:
                st.error(f"❌ Backend error: {response.status_code} - {response.text}")
        if response.status_code == 200:
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        else: 
            st.session_state.chat_history.append({"role": "assistant", "content": "Something went wrong! Try to rerun."})
        
    except Exception as e:
        st.error(f"🚨 Request failed: {e}")
    st.rerun()    
       
        
# Show if there is no chat history
if not st.session_state.chat_history:
    st.title("🧠 ADHD Routine Assistant")
    st.markdown("### 💬 Chat with your ADHD Assistant")
    

# Input mode selection - only show audio option if not in cloud
if IS_CLOUD:
    mode = "Type"
    st.info("ℹ️ Audio features are only available in the local version")
else:
    mode = st.radio("Input Mode", ["Type", "Speak"], horizontal=True)
    
    
# --- Chat History ---
for history in st.session_state.chat_history:
    with st.chat_message(history["role"]):
        st.markdown(history["content"])

if mode == "Type":
    if prompt := st.chat_input("What's in your mind?"):
        # Add prompt to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            get_response(prompt)
            
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
            st.session_state.chat_history.append({"role": "user", "content": user_message})
            
            with st.chat_message("user"):
                st.markdown(user_message)
            
            with st.chat_message("assistant"):
                get_response(user_message)
                
        except sr.WaitTimeoutError:
            st.error("No speech detected. Please try again.")
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand that. Please try again.")
        except sr.RequestError as e:
            st.error(f"Sorry, there was an error with the speech recognition service: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
                 

# Show environment info in sidebar
new_chat = st.sidebar.button("New chat", key="new_chat_btn", help="Start a new chat")
st.sidebar.markdown("### ℹ️ Environment Info")
st.sidebar.markdown(f"**Mode:** {'Cloud' if IS_CLOUD else 'Local'}")
st.sidebar.markdown(f"**Backend URL:** {BACKEND_URL}")

if new_chat:
    st.session_state.chat_history = []
    st.rerun()

if not IS_CLOUD:
    st.sidebar.markdown("""
    ### 🎙️ Audio Features Available
    - Voice input
    - Speech recognition
    - Real-time audio 
        processing
    """)