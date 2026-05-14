import os

from dotenv import load_dotenv

load_dotenv()


def _is_colab() -> bool:
    try:
        import google.colab  # pyright: ignore[reportMissingImports] # noqa: F401
        return True
    except ImportError:
        return False


def get_api_key() -> str:
    if _is_colab():
        try:
            from google.colab import userdata  # type: ignore
            key = userdata.get("SCOPUS_API_KEY")
            if key:
                return key
        except Exception:
            pass

    key = os.getenv("SCOPUS_API_KEY")
    if not key:
        raise EnvironmentError(
            "SCOPUS_API_KEY not found. Set it as an environment variable, "
            "or set the parameter `api_key`."
        )
    return key
