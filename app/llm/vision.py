import base64
import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

MODEL = "gemini-3.6-flash"

PROMPT = """
You are an intelligent OCR engine.

Extract every visible text from this document.

Rules:

- Preserve headings
- Preserve tables
- Preserve lists
- Preserve formatting
- Return ONLY Markdown
- Do NOT summarize
"""


def image_to_markdown(image_path: str) -> str:

    print("=" * 60)
    print("VISION (REST)")
    print("=" * 60)
    print("MODEL :", MODEL)
    print("IMAGE :", image_path)
    print("=" * 60)

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(image_bytes).decode()

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{MODEL}:generateContent"
    )

    response = requests.post(
        url,
        params={
            "key": API_KEY,
        },
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": PROMPT,
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64,
                            },
                        },
                    ],
                }
            ]
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return (
        data["candidates"][0]
        ["content"]["parts"][0]
        ["text"]
    )