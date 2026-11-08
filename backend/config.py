"""환경변수 로드 (.env)"""
import os
from dotenv import load_dotenv

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
HIRA_API_KEY = os.getenv("HIRA_API_KEY", "")
EGEN_API_KEY = os.getenv("EGEN_API_KEY", "")

# RAG
CHROMA_DIR = os.getenv("CHROMA_DIR", "backend/rag/chroma_db")
