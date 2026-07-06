"""Centralized configuration loaded from environment variables."""

import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    """Application settings validated with Pydantic."""

    flask_host: str = Field(default_factory=lambda: os.getenv("FLASK_HOST", "0.0.0.0"))
    flask_port: int = Field(default_factory=lambda: int(os.getenv("FLASK_PORT", "5000")))
    flask_env: str = Field(default_factory=lambda: os.getenv("FLASK_ENV", "production"))

    watson_api_url: str = Field(
        default_factory=lambda: os.getenv(
            "WATSON_API_URL",
            "https://sn-watson-emotion.labs.skills.network/v1/"
            "watson.runtime.nlp.v1/NlpService/EmotionPredict",
        )
    )
    watson_model_id: str = Field(
        default_factory=lambda: os.getenv(
            "WATSON_MODEL_ID", "emotion_aggregated-workflow_lang_en_stock"
        )
    )
    watson_api_timeout: int = Field(
        default_factory=lambda: int(os.getenv("WATSON_API_TIMEOUT", "10"))
    )


settings = Settings()
