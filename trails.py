import os
from dotenv import load_dotenv
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
tavily_key = os.getenv("TAVILY_KEY")
langsmith_key = os.getenv("LANGSMITH_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_KEY")
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
groq_model = "llama-3.3-70b-versatile"
groq_model_8k = "llama-3.3-8b-instant"
