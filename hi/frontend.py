import streamlit as st
import cv2
from PIL import Image
import numpy as np
from speech_emotion import speech_emotion
from tools1 import talk_with_user
import time
import threading
import queue
import pandas as pd

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = "user_" + str(int(time.time()))
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False

def process_video():
    """Process video feed and detect emotions"""
    cap = cv2.VideoCapture(0)
    while st.session_state.is_listening:
        ret, frame = cap.read()
        if not ret:
            continue
            
        try:
            # Convert to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get emotion from frame
            emotion = speech_emotion.get_emotion_summary(st.session_state.user_id)
            
            # Add emotion to history
            st.session_state.emotion_history.append({
                'emotion': emotion['dominant_emotion'],
                'confidence': emotion['confidence'],
                'timestamp': time.time()
            })
            
            # Display frame
            st.image(frame_rgb, caption=f"Current Emotion: {emotion['dominant_emotion']} ({emotion['confidence']:.0%})")
            
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            continue
            
        time.sleep(0.1)
    
    cap.release()

def main():
    st.title("ADHD Assistant with Emotion Recognition")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        if st.button("Start/Stop Emotion Recognition"):
            st.session_state.is_listening = not st.session_state.is_listening
            if st.session_state.is_listening:
                speech_emotion.start_listening(st.session_state.user_id)
            else:
                speech_emotion.stop_listening()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Video Feed")
        if st.session_state.is_listening:
            process_video()
        else:
            st.info("Click 'Start/Stop Emotion Recognition' to begin")
    
    with col2:
        st.header("Chat")
        # Chat input
        user_input = st.text_input("Type your message:")
        if user_input:
            # Process user input
            response = talk_with_user(f"User ID: {st.session_state.user_id}. User input: {user_input}")
            
            # Add to chat history
            st.session_state.chat_history.append({
                'user': user_input,
                'assistant': response,
                'timestamp': time.time()
            })
        
        # Display chat history
        for chat in st.session_state.chat_history:
            st.write(f"👤 You: {chat['user']}")
            st.write(f"🤖 Assistant: {chat['assistant']}")
            st.write("---")
    
    # Emotion history
    st.header("Emotion History")
    if st.session_state.emotion_history:
        emotion_df = pd.DataFrame(st.session_state.emotion_history)
        st.line_chart(emotion_df['confidence'])

if __name__ == "__main__":
    main()
