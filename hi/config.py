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
    model_name="llama3-70b-8192",  # You can also use "llama2-70b-4096" or other Llama models
    temperature=0.7,
    max_tokens=512
)

