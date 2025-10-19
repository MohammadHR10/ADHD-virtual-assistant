import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

memory = ConversationBufferMemory(return_messages=True)
# Initialize the LLM with Groq
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama-3.1-8b-instant",  # Current supported model (replacement for llama3-8b-8192)
    temperature=0.7,
    max_tokens=512
)

