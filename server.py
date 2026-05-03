"""
This module implements a Flask server for an Emotion Detection application.
It provides routes for rendering the index page and processing text to
extract emotional scores and the dominant emotion using the EmotionDetection package.
"""

from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask('Emotion Detector')

@app.route('/')
def index():
    """
    Renders the main application page (index.html).
    """
    return render_template('index.html')

@app.route('/emotionDetector')
def detect_emotion():
    """
    Retrieves text from request arguments, processes it for emotion detection,
    and returns a formatted string containing the results or an error message.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    emotion_scores = emotion_detector(text_to_analyze)

    # Validate if the dominant_emotion is present
    if emotion_scores["dominant_emotion"] is None:
        return "Invalid text! Please try again!."

    # Extracting individual scores for the final response
    anger = emotion_scores['anger']
    disgust = emotion_scores['disgust']
    fear = emotion_scores['fear']
    joy = emotion_scores['joy']
    sadness = emotion_scores['sadness']
    dominant_emotion = emotion_scores['dominant_emotion']

    # Returning the formatted response as required by Task 6
    return (
        f"For the given statement, the system response is 'anger': {anger}, "
        f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and "
        f"'sadness': {sadness}. The dominant emotion is {dominant_emotion}."
    )

if __name__ == '__main__':
    # Deploying the application on localhost:5000
    app.run(host='0.0.0.0', port=5000)
