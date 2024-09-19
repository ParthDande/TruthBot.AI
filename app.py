from flask import Flask, request, render_template, jsonify
import time
import random
from news_analysis import TextAnalysis
import requests
# Initialize Flask app
app = Flask(__name__)
# Hugging Face API URL for summarization


@app.route("/")
def home():
    return render_template('fakecheck-ai-modern.html')

@app.route('/sentiment', methods=['GET', 'POST'])
def news_sentiment_analysis():
    if request.method == 'POST':
        text = request.form['user_input']
        sentiment, confidence = obj.analyze_sentiment(text)
        # Simulate processing time
        time.sleep(random.uniform(1, 2))
        
        return jsonify({
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence*100, 2)})
    return render_template('sentiment.html')


@app.route("/summarization", methods=["GET", "POST"])
def index():
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    if request.method == "POST":
        text = request.form["text"]
        max_length = int(request.form["max_length"])
        min_length = 10  # You can adjust the min_length here or take from the form as well.

        # Send the request to Hugging Face API with max_length and min_length parameters
        result = query({
            "inputs": text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length
            }
        })

        # Extract the summary text from the response
        summary = result[0]['summary_text']

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'summary': summary})
        else:
            return render_template("summarization.html", summary=summary)

    return render_template("summarization.html", summary="")

@app.route('/plagiarism')
def news_plagiarism_check():
    return render_template('plagiarism.html')

if __name__ == '__main__':
    # Run the app
    obj = TextAnalysis()
    app.run(host='0.0.0.0', port=5000, debug=True)
