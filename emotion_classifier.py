import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from scipy.signal import welch

class EmotionClassifier:
    def __init__(self):
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.emotions = ['Neutral', 'Happy', 'Sad', 'Angry', 'Relaxed']
        self.is_trained = False
        self.sample_rate = 256  # Hz

    def train(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.classifier.fit(X_scaled, y)
        self.is_trained = True

    def classify_emotion(self, eeg_data):
        if not self.is_trained:
            return self.mock_classify_emotion(eeg_data)

        if eeg_data is None:
            return 'No data'

        features = self.extract_features(eeg_data)
        features_scaled = self.scaler.transform(features.reshape(1, -1))

        emotion_index = self.classifier.predict(features_scaled)[0]
        return self.emotions[emotion_index]

    def extract_features(self, eeg_data):
        features = []
        for channel in eeg_data:
            channel_features = self.extract_channel_features(channel)
            features.extend(channel_features)
        
        return np.array(features)

    def extract_channel_features(self, channel_data):
        # Time-domain features
        mean = np.mean(channel_data)
        std = np.std(channel_data)
        max_val = np.max(channel_data)
        min_val = np.min(channel_data)
        ptp = np.ptp(channel_data)

        # Frequency-domain features
        band_powers = self.extract_frequency_band_powers(channel_data)

        return [mean, std, max_val, min_val, ptp] + band_powers

    def extract_frequency_band_powers(self, channel_data):
        freqs, psd = welch(channel_data, fs=self.sample_rate)
        
        # Define frequency bands
        bands = {
            'delta': (0.5, 4),
            'theta': (4, 8),
            'alpha': (8, 13),
            'beta': (13, 30),
            'gamma': (30, 100)
        }
        
        band_powers = []
        for band, (low, high) in bands.items():
            idx = np.logical_and(freqs >= low, freqs <= high)
            band_power = np.sum(psd[idx])
            band_powers.append(band_power)
        
        return band_powers

    def mock_classify_emotion(self, eeg_data):
        # Simple mock classification based on the mean of the EEG data
        mean_activity = np.mean(eeg_data)
        if mean_activity < 20:
            return 'Relaxed'
        elif mean_activity < 40:
            return 'Neutral'
        elif mean_activity < 60:
            return 'Happy'
        elif mean_activity < 80:
            return 'Sad'
        else:
            return 'Angry'
