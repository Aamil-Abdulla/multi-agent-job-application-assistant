import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_MODEL_FAST = "llama-3.1-8b-instant"

TAVILY_API_KEY = os.getenv("TAVILY_KEY")

langsmith_key = os.getenv("LANGSMITH_KEY")
if langsmith_key:
    os.environ["LANGSMITH_API_KEY"] = langsmith_key
    os.environ["LANGSMITH_TRACING_V2"] = "true"

langchain_project = os.getenv("LANGCHAIN_PROJECT")
if langchain_project:
    os.environ["LANGCHAIN_PROJECT"] = langchain_project