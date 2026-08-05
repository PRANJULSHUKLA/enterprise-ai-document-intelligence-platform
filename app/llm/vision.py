from PIL import Image

from app.llm.gemini import client, MODEL_NAME


PROMPT = """
You are an intelligent OCR engine.

Extract every visible text from this document page.

Rules:

- Preserve headings
- Preserve tables
- Preserve lists
- Preserve formatting
- Return ONLY Markdown
- Do NOT summarize
"""


def image_to_markdown(image_path: str):

    image = Image.open(image_path)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            PROMPT,
            image,
        ],
    )

    return response.text