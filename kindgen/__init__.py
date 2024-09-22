import os
import logging

import cohere
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

API_KEY = os.getenv("COHERE_API_KEY")

if not API_KEY:
    raise ValueError(
        "API Key for Cohere not found. Set COHERE_API_KEY in .env or in environment."
    )

try:
    cohere_client = cohere.Client(api_key=API_KEY)
except Exception as e:
    raise ConnectionError(f"Failed to initialize Cohere client: {str(e)}")

__all__ = ["cohere_client"]
