import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("GEMINI DEBUG")
print("=" * 60)
print("API KEY LOADED :", api_key is not None)
print("API KEY PREFIX :", api_key[:8] if api_key else None)
print("MODEL          :", os.getenv("MODEL_NAME"))
print("=" * 60)

client = genai.Client(
    api_key=api_key,
)

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "models/gemini-3.6-flash",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "models/gemini-embedding-001",
)