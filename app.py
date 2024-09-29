from flask import Flask, request, render_template, jsonify
import time
import random
from news_analysis import TextAnalysis
import requests
from xgboost import XGBClassifier
from news_classification import FakeNewsClassifier
from plagiarism import PlagiarismDetection
app = Flask(__name__)
import PyPDF2
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
            print(f"Preprocessing text: {text[:50]}... for domain: {domain}")  # Log input
            text = news_detection.preprocess_custom_input(text, domain)
            print(f"Preprocessed text: {text[:50]}...")  # Log preprocessed text
            
            prediction, confidence = news_detection.fake_news_classifier(text)
            print(f"Raw prediction: {prediction}, confidence: {confidence}")  # Log raw output
            
            return jsonify({
                "prediction": prediction,
                "confidence": round(confidence * 100, 2)
            })
        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            traceback.print_exc()  # Print full traceback to console
            return jsonify({"error": f"Error occurred: {str(e)}"}), 500
    
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
        input_length = len(text)
        min_length = max(1, int(input_length * 0.1))
        min_length = max(1, int(input_length * 0.05))
        result = query({
            "inputs": text,
            "parameters": {
                "max_length": min_length,
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

        output, human, ai = plagiarism.ai_plagiarism(text)
        return jsonify({
            "output": output,
            "human": human,
            "ai": ai
        })

    return render_template('plagiarism.html') # Render the template for GET requests"""

if __name__ == '__main__':
        # Initialize a new model instance
    loaded_model = XGBClassifier()
    news_detection = FakeNewsClassifier()
    plagiarism = PlagiarismDetection()
    # Load the model from the file
    loaded_model.load_model('fake_news_model.json')
    # Run the app
    obj = TextAnalysis()
    app.run(host='0.0.0.0', port=5000, debug=True)
