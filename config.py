import os
from dataclasses import dataclass
from dotenv import load_dotenv

MODEL = os.getenv("GEMINI_MODEL" , "gemini-2.5-flash")


@dataclass
class AppConfig:
    api_key: str
    model: str = MODEL

def load_config() -> AppConfig:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY" , "").strip()
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "Missing GEMINI_API_KEY. Copy .env.example to .env and add your Gemini API key."
        )

    return AppConfig(api_key=api_key , model=os.getenv("GEMINI_MODEL" , MODEL))
