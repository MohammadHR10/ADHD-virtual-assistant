import os
#from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from config import llm, memory 
from tools1 import TOOLS
from audio import SpeechRecognition

# Load memory
#memory = ConversationBufferMemory(return_messages=True)

# Initialize Whisper model
speech_rec = SpeechRecognition()

# Initialize LangChain agent with your custom tools
agent = initialize_agent(
    tools=TOOLS,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

def main():
    print("🧠 ADHD AI Assistant (Type or Speak)")
    print("Say 'exit' anytime to quit.")

    user_id = "default_user"

    while True:
        try:
            mode = input("\nChoose input method — [T]ype / [S]peak: ").strip().lower()

            if mode in ['exit', 'quit', 'bye']:
                print("\n🧠 AI: Take care! You're doing great. 👋")
                break

            if mode == 's':
                print("🎤 Listening...")
                user_input = speech_rec.record_and_transcribe().strip()
                print(f"🗣️ You said: {user_input}")
            elif mode == 't':
                user_input = input("You: ").strip()
            else:
                print("❌ Invalid input. Choose 'T' or 'S'.")
                continue

            if not user_input:
                continue

            # Use agent.invoke instead of deprecated agent.run
            response = agent.invoke({"input": user_input})
            
            # Extract the response content - this is the key fix
            ai_response = response.get("output", "I'm not sure how to respond to that.")
            
            # Save to memory (optional if agent already tracks this)
            memory.save_context({"input": user_input}, {"output": ai_response})

            print(f"\n🧠 AI: {ai_response}")

        except KeyboardInterrupt:
            print("\n\n🧠 AI: Interrupted. Take a deep breath. 🌿")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print(f"Error type: {type(e)}")
            # Add more debugging information
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()