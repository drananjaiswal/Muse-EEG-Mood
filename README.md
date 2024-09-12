# Muse EEG Emotion Classifier

This project is a Flask-based application for capturing and classifying emotions using EEG data from Muse devices, utilizing the muse_tools library.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Installation

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/your-username/muse-eeg-emotion-classifier.git
   cd muse-eeg-emotion-classifier
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask application:
   ```
   python main.py
   ```

2. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

1. On the main page, click the "Connect Muse" button to establish a connection with your Muse device.
2. Once connected, you will see real-time EEG data visualization and emotion classification.
3. Use the "View Emotion History Dashboard" link to see long-term emotion tracking data.

## File Structure

- `main.py`: The main Flask application
- `emotion_classifier.py`: Contains the EmotionClassifier class for emotion classification
- `muse_connection.py`: Handles the connection and data collection from the Muse device
- `templates/`: Contains HTML templates for the web interface
- `static/`: Contains CSS and JavaScript files for the frontend

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
