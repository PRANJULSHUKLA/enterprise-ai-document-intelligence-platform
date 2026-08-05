from app.constants.models import GeminiModels
from app.llm.gemini import client


class GeminiChat:

    @staticmethod
    def generate(prompt: str):

        response = client.models.generate_content(
            model=GeminiModels.VISION,
            contents=prompt,
        )

        return response.text