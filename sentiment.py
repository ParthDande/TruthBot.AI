from flask import Flask, request, render_template
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import random

nltk.download('vader_lexicon', quiet=True)

app = Flask(__name__)
class TextAnalysis:
    @staticmethod
    def analyze_sentiment(text):
        sia = SentimentIntensityAnalyzer()
        sentiment_scores = sia.polarity_scores(text)
            
        compound_score = sentiment_scores['compound']
            
        if compound_score >= 0.05:
                return "Positive", abs(compound_score) * 100
        elif compound_score <= -0.05:
                return "Negative", abs(compound_score) * 100
        else:
                return "Neutral", (1 - abs(compound_score)) * 100


@app.route('/sentiment', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        obj = TextAnalysis()
        text = request.form['user_input']
        sentiment, confidence = obj.analyze_sentiment(text)
        time.sleep(random.uniform(1, 2))  # Simulate processing time
        return {
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence, 2)
        }
    return render_template('sentiment.html')

if __name__ == '__main__':
    app.run(debug=True)
