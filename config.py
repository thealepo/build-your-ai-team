import os

from dotenv import load_dotenv


def load_config() -> tuple[str, str]:
    """Return the API key and model from the local environment."""
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "Missing GEMINI_API_KEY. Copy .env.example to .env "
            "and add your Gemini API key."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    return api_key, model
