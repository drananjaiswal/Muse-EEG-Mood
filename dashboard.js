document.addEventListener('DOMContentLoaded', () => {
    fetchEmotionHistory();
    // Refresh data every minute
    setInterval(fetchEmotionHistory, 60000);
});

function fetchEmotionHistory() {
    fetch('/get_emotion_history')
        .then(response => response.json())
        .then(data => {
            updateEmotionHistoryChart(data);
            updateEmotionSummary(data);
        })
        .catch(error => console.error('Error:', error));
}

function updateEmotionHistoryChart(data) {
    const emotions = ['Neutral', 'Happy', 'Sad', 'Angry', 'Relaxed'];
    const traces = emotions.map(emotion => ({
        x: [],
        y: [],
        type: 'scatter',
        mode: 'lines',
        name: emotion
    }));

    data.forEach(entry => {
        const timestamp = new Date(entry.timestamp);
        emotions.forEach((emotion, index) => {
            traces[index].x.push(timestamp);
            traces[index].y.push(entry.emotion === emotion ? 1 : 0);
        });
    });

    const layout = {
        title: 'Emotion History (Last 24 Hours)',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Emotion', range: [-0.1, 1.1] },
        showlegend: true
    };

    Plotly.newPlot('emotion-history-chart', traces, layout);
}

function updateEmotionSummary(data) {
    const emotionCounts = {};
    data.forEach(entry => {
        emotionCounts[entry.emotion] = (emotionCounts[entry.emotion] || 0) + 1;
    });

    const emotionEmojis = {
        'Happy': '😊',
        'Angry': '😠',
        'Neutral': '😐',
        'Sad': '😢',
        'Relaxed': '😌'
    };

    const summaryHtml = `
        <p>Time range: ${new Date(data[data.length - 1].timestamp).toLocaleString()} - ${new Date(data[0].timestamp).toLocaleString()}</p>
        ${Object.entries(emotionCounts)
            .map(([emotion, count]) => `<p>${emotionEmojis[emotion]} ${emotion}: ${count}</p>`)
            .join('')}
    `;

    document.getElementById('emotion-counts').innerHTML = summaryHtml;
}
