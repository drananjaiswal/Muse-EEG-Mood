let eegChart, bandPowersChart;
const channelNames = ['TP9', 'AF7', 'AF8', 'TP10'];
const bandNames = ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'];
let isConnected = false;

const emotionEmojis = {
    'Happy': '😊',
    'Angry': '😠',
    'Neutral': '😐',
    'Sad': '😢',
    'Relaxed': '😌'
};

function initCharts() {
    const eegData = channelNames.map(channel => ({
        y: [],
        type: 'line',
        name: channel
    }));

    const eegLayout = {
        title: 'Real-time EEG Data',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Amplitude' },
        showlegend: true
    };

    Plotly.newPlot('eeg-chart', eegData, eegLayout);
    eegChart = document.getElementById('eeg-chart');

    const bandPowersData = channelNames.map(channel => ({
        x: bandNames,
        y: [],
        type: 'bar',
        name: channel
    }));

    const bandPowersLayout = {
        title: 'Frequency Band Powers',
        xaxis: { title: 'Frequency Bands' },
        yaxis: { title: 'Power' },
        barmode: 'group',
        showlegend: true
    };

    Plotly.newPlot('band-powers-chart', bandPowersData, bandPowersLayout);
    bandPowersChart = document.getElementById('band-powers-chart');
}

function updateEmotion() {
    if (!isConnected) {
        document.getElementById('emotion-text').textContent = 'Disconnected';
        document.getElementById('emotion-emoji').textContent = '';
        return;
    }

    fetch('/get_emotion')
        .then(response => response.json())
        .then(data => {
            if (data.emotion === 'No data') {
                document.getElementById('emotion-text').textContent = 'No data received';
                document.getElementById('emotion-emoji').textContent = '';
            } else {
                document.getElementById('emotion-text').textContent = data.emotion;
                document.getElementById('emotion-emoji').textContent = emotionEmojis[data.emotion] || '';
                updateEEGChart(data.eeg_data);
                updateFeatures(data.features);
                updateBandPowers(data.band_powers);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('emotion-text').textContent = 'Error occurred';
            document.getElementById('emotion-emoji').textContent = '';
        });
}

function updateEEGChart(eegData) {
    if (eegData) {
        const update = {
            y: eegData
        };

        Plotly.extendTraces(eegChart, update, [0, 1, 2, 3]);

        if (eegChart.data[0].y.length > 100) {
            Plotly.relayout(eegChart, {
                xaxis: {
                    range: [eegChart.data[0].y.length - 100, eegChart.data[0].y.length]
                }
            });
        }
    }
}

function updateFeatures(features) {
    if (features) {
        document.getElementById('features').textContent = JSON.stringify(features, null, 2);
    }
}

function updateBandPowers(bandPowers) {
    if (bandPowers) {
        const update = {
            y: bandPowers
        };

        Plotly.restyle(bandPowersChart, update);
    }
}

function connectMuse() {
    fetch('/connect_muse')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                isConnected = true;
                document.getElementById('connection-status').textContent = 'Status: Connected';
                document.getElementById('connect-muse').disabled = true;
                document.getElementById('disconnect-muse').disabled = false;
            } else {
                alert('Failed to connect to Muse device. Please make sure it is turned on and in range.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while trying to connect to the Muse device.');
        });
}

function disconnectMuse() {
    fetch('/disconnect_muse')
        .then(response => response.json())
        .then(data => {
            isConnected = false;
            document.getElementById('connection-status').textContent = 'Status: Disconnected';
            document.getElementById('connect-muse').disabled = false;
            document.getElementById('disconnect-muse').disabled = true;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while trying to disconnect from the Muse device.');
        });
}

document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    setInterval(updateEmotion, 1000);

    document.getElementById('connect-muse').addEventListener('click', connectMuse);
    document.getElementById('disconnect-muse').addEventListener('click', disconnectMuse);
});
