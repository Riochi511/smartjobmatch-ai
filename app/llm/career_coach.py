from app.llm.providers import OpenRouterProvider
from app.llm.prompts import SYSTEM_PROMPT

from app.config import OPENROUTER_MODEL

from app.exceptions.custom_exceptions import (
    AIServiceException
)


class CareerCoach:

    @staticmethod
    def generate(context):

        try:

            client = OpenRouterProvider.get_client()

            response = client.chat.completions.create(

                model=OPENROUTER_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": str(context)
                    }
                ],

                temperature=0.7,
                max_tokens=700
            )

            return response.choices[0].message.content

        except Exception as e:

            raise AIServiceException(
                f"Career Coach failed: {str(e)}"
            )