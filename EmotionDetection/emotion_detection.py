"""Watson NLP Emotion Predict integration."""

import json
import logging

import requests

from config import settings

logger = logging.getLogger(__name__)


def emotion_detector(text_to_analyze: str) -> dict:
    """Analyze text for emotion using Watson NLP.

    Returns a dict with scores for anger, disgust, fear, joy, sadness,
    and the dominant emotion.  Returns all-None values when the input is
    blank or otherwise invalid.
    """
    url = settings.watson_api_url
    header = {"grpc-metadata-mm-model-id": settings.watson_model_id}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            url,
            json=payload,
            headers=header,
            timeout=settings.watson_api_timeout,
        )
    except requests.exceptions.Timeout:
        logger.error("Watson API request timed out")
        raise
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to Watson API")
        raise

    if response.status_code == 400:
        logger.info("Watson API returned 400 for input: %s", text_to_analyze[:50])
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    if response.status_code == 401:
        logger.error("Watson API authentication failed (401)")
        raise RuntimeError("Watson API authentication failed")

    if response.status_code == 403:
        logger.error("Watson API access denied (403)")
        raise RuntimeError("Watson API access denied")

    if response.status_code == 429:
        logger.error("Watson API rate limit exceeded (429)")
        raise RuntimeError("Watson API rate limit exceeded")

    if response.status_code >= 500:
        logger.error("Watson API server error: %s", response.status_code)
        raise RuntimeError(f"Watson API server error: {response.status_code}")

    if response.status_code != 200:
        logger.error("Watson API returned unexpected status: %s", response.status_code)
        raise RuntimeError(f"Watson API error: {response.status_code}")

    try:
        formatted_response = json.loads(response.text)
        emotions = formatted_response["emotionPredictions"][0]["emotion"]
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        logger.error("Failed to parse Watson API response: %s", exc)
        raise RuntimeError("Invalid response from Watson API") from exc

    anger_score = emotions["anger"]
    disgust_score = emotions["disgust"]
    fear_score = emotions["fear"]
    joy_score = emotions["joy"]
    sadness_score = emotions["sadness"]

    emotion_list = {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
    }

    dominant_emotion = max(emotion_list, key=emotion_list.get)

    return {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score,
        "dominant_emotion": dominant_emotion,
    }
