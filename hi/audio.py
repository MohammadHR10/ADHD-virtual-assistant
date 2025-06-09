import speech_recognition as sr

def record_and_transcribe():
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎤 Listening... (speak clearly)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("✅ Processing speech...")
        return recognizer.recognize_google(audio)
    
    except sr.WaitTimeoutError:
        return "⏱️ No speech detected. Please try again."
    except sr.UnknownValueError:
        return "🤷 Sorry, I couldn't understand that. Please try again."
    except sr.RequestError as e:
        return f"❌ Google Speech error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"
