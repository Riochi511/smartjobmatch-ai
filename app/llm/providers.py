from openai import OpenAI

from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL
)

from app.exceptions.custom_exceptions import (
    AIServiceException
)


class OpenRouterProvider:

    @staticmethod
    def get_client():

        if not OPENROUTER_API_KEY:

            raise AIServiceException(
                "OpenRouter API key is missing."
            )

        return OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL
        )