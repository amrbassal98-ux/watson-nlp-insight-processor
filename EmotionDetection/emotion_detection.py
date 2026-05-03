"""
This module provides a function to interact with the Watson NLP Emotion
Predict service. It extracts emotion scores and identifies the dominant emotion.
"""

import json
import requests

def emotion_detector(text_to_analyze):
    """
    Analyzes the provided text using Watson NLP and returns a dictionary
    containing scores for anger, disgust, fear, joy, and sadness, 
    along with the dominant emotion.
    """
    url = (
        'https://sn-watson-emotion.labs.skills.network/v1/'
        'watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    text = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(url, json=text, headers=header, timeout=10)

    # Task 7: Handle status code 400 for blank or invalid entries
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    formatted_response = json.loads(response.text)

    # Task 2 & 3: Navigate JSON and extract scores
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    emotion_list = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
    }

    # Task 3: Identify dominant emotion
    dominant_emotion = max(emotion_list, key=emotion_list.get)

    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
