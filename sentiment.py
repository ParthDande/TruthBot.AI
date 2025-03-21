from flask import Flask, request, render_template, jsonify
from transformers import pipeline
import logging
import time
import random

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class TextAnalysis:
    def __init__(self):
        logger.info("🔄 Loading sentiment pipeline...")
        self.sentiment_pipeline = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        logger.info("✅ Sentiment pipeline loaded successfully.")

    def analyze_sentiment(self, text):
        logger.info(f"🔍 Analyzing text: {text[:60]}...")  # Short preview
        result = self.sentiment_pipeline(text)
        sentiment = result[0]['label']
        score = result[0]['score']
        return sentiment, score

# Initialize model object
logger.info("🚀 Initializing TextAnalysis object...")
obj = TextAnalysis()
logger.info("✅ TextAnalysis object initialized.")

@app.route('/sentiment', methods=['GET', 'POST'])
def news_sentiment_analysis():
    if request.method == 'POST':
        try:
            logger.info("📩 POST request received at /sentiment")

            data = request.get_json()
            raw_text = data.get('text', '').strip()
            logger.info(f"✏️ Received input text: {raw_text[:100]}...")

            sentiment, confidence = obj.analyze_sentiment(raw_text[:1000])
            time.sleep(random.uniform(1, 2))

            logger.info(f"✅ Sentiment: {sentiment}, Confidence: {confidence}")
            return jsonify({
                'sentiment': sentiment,
                'confidence': round(confidence * 100, 2)
            })

        except Exception as e:
            logger.exception("❌ Error in /sentiment route")
            return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

    logger.info("📥 GET request - rendering template")
    return render_template('sentiment.html')


if __name__ == '__main__':
    logger.info("🌐 Starting Flask app...")
    app.run(debug=True, port=5001)
