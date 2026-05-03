from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask('Emotion Detector')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emotionDetector')
def detect_emotion():
    text_to_analyze = request.args.get('textToAnalyze')
    emotion_scores = emotion_detector(text_to_analyze)
    if emotion_scores["dominant_emotion"] is None:
        return "Invalid input! Please try again!"
    anger = emotion_scores['anger']
    disgust = emotion_scores['disgust']
    fear = emotion_scores['fear']
    joy = emotion_scores['joy']
    sadness = emotion_scores['sadness']
    dominant_emotion = emotion_scores['dominant_emotion']
    return (
        f"For the given statement, the system response is 'anger': {anger}, "
        f"'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and 'sadness': {sadness}. "
        f"The dominant emotion is {dominant_emotion}."
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)