from flask import Flask, render_template, jsonify
from muse_connection import MuseConnection
from emotion_classifier import EmotionClassifier
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import logging
import random

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

muse_connection = MuseConnection()
emotion_classifier = EmotionClassifier()

# Simulated database to store emotion data (last 24 hours, assuming 1 entry per minute)
MAX_HISTORY_LENGTH = 1440  # 24 hours * 60 minutes
emotion_history = deque(maxlen=MAX_HISTORY_LENGTH)

# Populate emotion_history with mock data
def populate_mock_emotion_data():
    emotions = ['Neutral', 'Happy', 'Sad', 'Angry', 'Relaxed']
    now = datetime.now()
    for i in range(MAX_HISTORY_LENGTH):
        timestamp = now - timedelta(minutes=i)
        emotion = random.choice(emotions)
        emotion_history.appendleft({
            'timestamp': timestamp.isoformat(),
            'emotion': emotion
        })
    logging.debug(f"Populated emotion history with {len(emotion_history)} mock entries")

populate_mock_emotion_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/get_emotion')
def get_emotion():
    muse_connection.collect_data()
    eeg_data = muse_connection.get_latest_eeg_data()
    channel_names = muse_connection.get_channel_names()
    
    if eeg_data is not None:
        emotion = emotion_classifier.classify_emotion(eeg_data)
        features = emotion_classifier.extract_features(eeg_data)
        band_powers = [emotion_classifier.extract_frequency_band_powers(channel) for channel in eeg_data]
        
        # Store emotion data with timestamp
        emotion_history.appendleft({
            'timestamp': datetime.now().isoformat(),
            'emotion': emotion
        })
        
        logging.debug(f"Added emotion to history: {emotion}")
        logging.debug(f"Current emotion history length: {len(emotion_history)}")
        
        return jsonify({
            'emotion': emotion,
            'eeg_data': eeg_data.tolist(),
            'channel_names': channel_names,
            'features': features.tolist(),
            'band_powers': band_powers if isinstance(band_powers[0], list) else [bp.tolist() for bp in band_powers]
        })
    else:
        return jsonify({
            'emotion': 'No data',
            'eeg_data': None,
            'channel_names': channel_names,
            'features': None,
            'band_powers': None
        })

@app.route('/get_emotion_history')
def get_emotion_history():
    logging.debug("get_emotion_history route called")
    # Return the last 24 hours of emotion data
    recent_history = list(emotion_history)
    logging.debug(f"Returning {len(recent_history)} entries from emotion history")
    return jsonify(recent_history)

@app.route('/connect_muse')
def connect_muse():
    if muse_connection.connect():
        return jsonify({'status': 'success', 'message': 'Connected to mock Muse device'})
    else:
        return jsonify({'status': 'error', 'message': 'Failed to connect to mock Muse device'})

@app.route('/disconnect_muse')
def disconnect_muse():
    muse_connection.disconnect()
    return jsonify({'status': 'success', 'message': 'Disconnected from mock Muse device'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
