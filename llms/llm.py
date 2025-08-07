from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST")

model = ChatOllama(
    model="qwen2.5vl:7b",
    base_url=OLLAMA_HOST,
    keep_alive="1h",
)
