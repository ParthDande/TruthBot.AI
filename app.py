from flask import Flask, request, render_template, jsonify 
app = Flask(__name__)
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import time
import random
from news_analysis import TextAnalysis
from transformers import pipeline
nltk.download('vader_lexicon')
@app.route("/") 
def home(): 

    return render_template('fakecheck-ai-modern.html')
#if we run this file directly then the __name__ variable will be __main__ 

@app.route('/sentiment', methods=['GET', 'POST'])
def news_sentiment_analysis():
    if request.method == 'POST':
        text = request.form['user_input']
        sentiment, confidence = obj.analyze_sentiment(text)
        time.sleep(random.uniform(1, 2))  # Simulate processing time
        return jsonify({
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence, 2)})
    
    return render_template('sentiment.html')

@app.route('/summarization', methods=['GET', 'POST'])
def news_summarization():
        if request.method == "POST":
                summarizer = pipeline("summarization")
                text = request.form["text"]
                max_length = int(request.form["max_length"])
                summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'summary': summary})
                else:
                        return render_template("summarization.html", summary=summary)
        return render_template("summarization.html", summary="")

@app.route('/plagiarism')
def news_plagiarism_check():
    return render_template('plagiarism.html')

if __name__ == '__main__':
    obj = TextAnalysis()
    app.run(host='0.0.0.0', port=5000,debug=True)