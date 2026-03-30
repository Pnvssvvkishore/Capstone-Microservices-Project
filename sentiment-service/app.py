from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from textblob import TextBlob

app = Flask(__name__)
metrics = PrometheusMetrics(app)

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"message": "No text provided"}), 400
        
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    if polarity > 0.1:
        sentiment = 'POSITIVE'
    elif polarity < -0.1:
        sentiment = 'NEGATIVE'
    else:
        sentiment = 'NEUTRAL'
        
    return jsonify({
        "text": text,
        "polarity": polarity,
        "sentiment": sentiment
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
