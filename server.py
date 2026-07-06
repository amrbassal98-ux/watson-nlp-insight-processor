"""Flask server for the Emotion Detection application."""

import logging
from flask import Flask, request, render_template
from pydantic import BaseModel, ValidationError
from EmotionDetection.emotion_detection import emotion_detector
from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask("Emotion Detector")


class TextRequest(BaseModel):
    """Input validation for the text to analyze."""

    text_to_analyze: str


@app.route("/")
def index():
    """Renders the main application page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def detect_emotion():
    """Processes text for emotion detection and returns formatted results."""
    text_to_analyze = request.args.get("textToAnalyze")

    try:
        validated = TextRequest(text_to_analyze=text_to_analyze or "")
    except ValidationError as exc:
        logger.warning("Invalid input: %s", exc)
        return "Invalid text! Please try again!.", 400

    if not text_to_analyze:
        return "Invalid text! Please try again!.", 400

    try:
        emotion_scores = emotion_detector(text_to_analyze)
    except Exception:
        logger.exception("Emotion detection failed")
        return "Error processing text. Please try again later.", 500

    if emotion_scores["dominant_emotion"] is None:
        return "Invalid text! Please try again!.", 400

    anger = emotion_scores["anger"]
    disgust = emotion_scores["disgust"]
    fear = emotion_scores["fear"]
    joy = emotion_scores["joy"]
    sadness = emotion_scores["sadness"]
    dominant_emotion = emotion_scores["dominant_emotion"]

    return (
        f"For the given statement, the system response is 'anger': {anger}, "
        f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and "
        f"'sadness': {sadness}. The dominant emotion is {dominant_emotion}."
    )


if __name__ == "__main__":
    logger.info(
        "Starting server on %s:%s (env=%s)",
        settings.flask_host,
        settings.flask_port,
        settings.flask_env,
    )
    app.run(
        host=settings.flask_host,
        port=settings.flask_port,
        debug=settings.flask_env == "development",
    )
