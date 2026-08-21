import base64
import os
import time

import requests
from dotenv import load_dotenv


load_dotenv(override=True)


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


def image_to_markdown(
    image_path: str,
    max_retries: int = 3,
) -> str:

    print("=" * 60)
    print("VISION (REST)")
    print("=" * 60)
    print("MODEL :", MODEL)
    print("IMAGE :", image_path)
    print("=" * 60)

    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    image_base64 = base64.b64encode(
        image_bytes
    ).decode()

    url = (
        "https://generativelanguage.googleapis.com/"
        f"v1beta/models/{MODEL}:generateContent"
    )

    payload = {
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
                ]
            }
        ]
    }

    for attempt in range(1, max_retries + 1):

        try:

            print(
                f"Vision request attempt "
                f"{attempt}/{max_retries}"
            )

            response = requests.post(
                url,
                params={
                    "key": API_KEY,
                },
                json=payload,
                timeout=120,
            )

            # Retry temporary server/rate-limit errors.
            if response.status_code in {
                429,
                500,
                502,
                503,
                504,
            }:

                print(
                    f"Gemini returned "
                    f"{response.status_code}."
                )

                if attempt < max_retries:

                    wait_time = 5 * attempt

                    print(
                        f"Retrying in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            response.raise_for_status()

            data = response.json()

            candidates = data.get(
                "candidates",
                []
            )

            if not candidates:
                raise RuntimeError(
                    "Gemini returned no candidates."
                )

            content = candidates[0].get(
                "content",
                {}
            )

            parts = content.get(
                "parts",
                []
            )

            if not parts:
                raise RuntimeError(
                    "Gemini returned no content parts."
                )

            text = parts[0].get("text")

            if not text:
                raise RuntimeError(
                    "Gemini returned empty OCR output."
                )

            return text

        except requests.exceptions.Timeout as e:

            print(
                f"Vision request timed out "
                f"on attempt {attempt}."
            )

            if attempt >= max_retries:
                raise RuntimeError(
                    "Gemini Vision request timed out "
                    "after multiple attempts."
                ) from e

            wait_time = 5 * attempt

            print(
                f"Retrying in "
                f"{wait_time} seconds..."
            )

            time.sleep(wait_time)

        except requests.exceptions.RequestException as e:

            print(
                f"Vision request failed "
                f"on attempt {attempt}: {e}"
            )

            if attempt >= max_retries:
                raise

            wait_time = 5 * attempt

            print(
                f"Retrying in "
                f"{wait_time} seconds..."
            )

            time.sleep(wait_time)

    raise RuntimeError(
        "Gemini Vision failed after "
        "multiple attempts."
    )