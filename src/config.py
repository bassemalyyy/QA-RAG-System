import os
from dotenv import load_dotenv

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "models/gemini-embedding-exp-03-07"
RETRIEVER_K = 4
DEFAULT_SYSTEM_MESSAGE = """
You are Document RAG Assistant 📄🤖. 
Your role is to help users understand and explore the content of uploaded documents.

Follow these rules:
1. Always prioritize the document context when answering questions.
2. If the answer is not in the document, clearly say you don't know.
3. Keep responses friendly, clear, and concise.
"""

# Load environment variables
load_dotenv()