import numpy as np
import time
import logging

class MuseConnection:
    def __init__(self):
        self.latest_eeg_data = None
        self.channel_names = ['TP9', 'AF7', 'AF8', 'TP10']
        self.sample_rate = 256  # Hz
        self.buffer_size = 256  # 1 second of data
        self.is_connected = False

    def connect(self):
        try:
            # Simulate connection delay
            time.sleep(1)
            self.is_connected = True
            logging.info("Connected to mock Muse device")
            return True
        except Exception as e:
            logging.error(f"Error connecting to mock Muse: {str(e)}")
            return False

    def collect_data(self):
        if not self.is_connected:
            if not self.connect():
                return

        try:
            # Generate mock EEG data
            mock_eeg_data = np.random.randn(len(self.channel_names), self.buffer_size)
            self.latest_eeg_data = mock_eeg_data
        except Exception as e:
            logging.error(f"Error collecting mock Muse data: {str(e)}")

    def get_latest_eeg_data(self):
        return self.latest_eeg_data

    def get_channel_names(self):
        return self.channel_names

    def disconnect(self):
        self.is_connected = False
        logging.info("Disconnected from mock Muse device")
