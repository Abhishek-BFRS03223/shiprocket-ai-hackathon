import os

# Try to load environment variables, but don't fail if python-dotenv is not available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass

class Config:
    """Configuration class for AI Agent"""
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
    LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
    LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "shiprocket-ai-hackathon")
    
    # Vector Database Configuration
    FAISS_INDEX_PATH = "ai_agent/vector_store"
    
    # Memory Configuration
    MEMORY_ENABLED = True
    MAX_MEMORY_TOKENS = 4000
    
    # Agent Configuration
    AGENT_MAX_ITERATIONS = 10
    AGENT_VERBOSE = True 