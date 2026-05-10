import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[4] / ".env")


def get_api_key() -> str:
    key = os.getenv("SCOPUS_API_KEY")
    if not key:
        raise EnvironmentError(
            "SCOPUS_API_KEY not found. Set it as an environment variable or in a .env file at the project root."
        )
    return key
