import os

from dotenv import load_dotenv

load_dotenv()

KEYWORD_WEIGHT = 0.40
SEMANTIC_WEIGHT = 0.60

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1"
)

OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "deepseek/deepseek-chat-v3-0324"
)