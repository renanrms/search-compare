import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[4] / ".env")


def _is_colab() -> bool:
    try:
        import google.colab  # noqa: F401
        return True
    except ImportError:
        return False


def get_api_key() -> str:
    if _is_colab():
        try:
            from google.colab import userdata
            key = userdata.get("SCOPUS_API_KEY")
            if key:
                return key
        except Exception:
            pass

    key = os.getenv("SCOPUS_API_KEY")
    if not key:
        raise EnvironmentError(
            "SCOPUS_API_KEY not found. Set it as an environment variable, in a .env file, "
            "or as a Colab secret named SCOPUS_API_KEY."
        )
    return key
