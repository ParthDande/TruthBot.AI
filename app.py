from flask import Flask, request, render_template, jsonify
import time
import random
from news_analysis import TextAnalysis
import requests
from news_classification import FakeNewsClassifier
from plagiarism import PlagiarismDetection
app = Flask(__name__)
import PyPDF2
from newspaper import Article

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}
@app.route("/", methods=["GET"])
def home():
    return render_template('index.html')
import traceback

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        text = data.get("text")
        domain = data.get("domain")
        
        if not text or not domain:
            return jsonify({"error": "Missing text or domain"}), 400
        
        try:
            text = news_detection.preprocess_custom_input(text, domain)
            prediction, confidence = news_detection.fake_news_classifier(text)
            
            return jsonify({
                "prediction": prediction,
                "confidence": round(confidence * 100, 2)
            })
        except Exception as e:
            app.logger.error(f"Error in analysis: {str(e)}", exc_info=True)
            return jsonify({"error": f"Error occurred: {str(e)}"}), 500
    
    return render_template('fakecheck-ai-modern.html')


@app.route('/sentiment', methods=['GET', 'POST'])
def news_sentiment_analysis():
    if request.method == 'POST':
        text = request.form['text']
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
    headers = {
        "Authorization": "Bearer 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",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36'
    }
    if request.method == "POST":
        # Check if input is from URL or direct text
        if request.form.get("url"):
            # URL input processing
            try:
                url = request.form["url"]
                # Create Article object
                article = Article(url, browser_user_agent=headers['User-Agent'])
                article.download()
                article.parse()
                text = article.text
            except Exception as e:
                return jsonify({'error': f'Error fetching article: {str(e)}'}), 400
        else:
            # Text input processing
            text = request.form["text"]

        # Validate input length
        input_length = len(text)
        min_length = max(1, int(input_length * 0.05))
        
        # Call Hugging Face API for summarization
        try:
            response = requests.post(API_URL, headers=headers, json={
                "inputs": text,
                "parameters": {
                    "max_length": min_length,
                    "min_length": min_length
                }
            })
            result = response.json()
            summary = result[0]['summary_text']

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'summary': summary})
            else:
                return render_template("summarization.html", summary=summary)
        
        except Exception as e:
            return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

    return render_template("summarization.html", summary="")
@app.route('/plagiarism', methods=['GET', 'POST'])
def news_plagiarism_check():
    if request.method == 'POST':
        if 'text' in request.form:
            text = request.form['text']
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.pdf'):
                from PyPDF2 import PdfReader  # Import PDF reader
                reader = PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()  # Convert PDF to text
            else:
                text = file.read().decode('utf-8')
        else:
            return jsonify({"error": "No text or file provided"}), 400

        output, human, ai = news_detection.ai_plagiarism(text)
        return jsonify({
            "output": output,
            "human": human,
            "ai": ai
        })

    return render_template('plagiarism.html') # Render the template for GET requests
def get_report_data(text):
    """Generate report data based on the given text."""
    report_results = {
        'sentiment': {},
        'fake_news': {},
        'summarization': '',
        'plagiarism': {},
        'virality': {
            'potential_views': random.randint(1000, 100000),
            'trending_score': random.uniform(0.1, 0.9),
            'engagement_prediction': random.choice(['Low', 'Medium', 'High'])
        }
    }

    # Sentiment Analysis
    sentiment, sentiment_confidence = obj.analyze_sentiment(text)
    report_results['sentiment'] = {
        'sentiment': sentiment,
        'confidence': round(sentiment_confidence * 100, 2)
    }

    # Fake News Detection
    processed_text = news_detection.preprocess_custom_input(text, 'general')
    prediction, confidence = news_detection.fake_news_classifier(processed_text)
    report_results['fake_news'] = {
        'prediction': prediction,
        'confidence': round(confidence * 100, 2)
    }

    # Summarization
    summary_response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": text, "parameters": {"max_length": 50, "min_length": 10}}
    )
    summary_result = summary_response.json()
    report_results['summarization'] = summary_result[0]['summary_text']

    # Plagiarism Check
    output, human, ai = news_detection.ai_plagiarism(text)
    report_results['plagiarism'] = {
        'output': output,
        'human_score': human,
        'ai_score': ai
    }

    return report_results

@app.route('/report', methods=['GET', 'POST'])
def comprehensive_report():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            return jsonify({"error": "Text is required"}), 400

        try:
            report_results = get_report_data(text)
            return render_template("report.html", report=report_results)
        except Exception as e:
            app.logger.error(f"Error in comprehensive report generation: {str(e)}", exc_info=True)
            return jsonify({"error": f"Error occurred: {str(e)}"}), 500

    return render_template("report.html", report=None)


if __name__ == '__main__':
    news_detection = FakeNewsClassifier()
    obj = TextAnalysis()
    app.run(host='0.0.0.0', port=5000, debug=True)

