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
from TextExtractor import TextExtractor
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}
@app.route("/", methods=["GET"])
def home():
    return render_template('landing_page.html')
@app.route("/home", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    # Render the HTML page for input and output
    if request.method == "GET":
        return render_template("fakecheck-ai-modern.html")
    
    # Handle the analysis when POST request is made
    if request.method == "POST":
        input_source = request.form.get("text", "")
        
        # Validate input
        if not input_source:
            return jsonify({
                "error": "No text provided",
                "prediction": "inconclusive",
                "confidence": 0
            }), 400
        
        try:
            # Extract and preprocess text
            text = extractor.extract_text(input_source)
            if not text:
                return jsonify({
                    "error": "Unable to extract meaningful text",
                    "prediction": "inconclusive",
                    "confidence": 0
                }), 400
            
            # Preprocess the text
            processed_text = news_detection.preprocess_custom_input(text)
            
            # Classify the text
            prediction, confidence = news_detection.fake_news_classifier(processed_text)
            
            # Prepare response
            response = {
                "prediction": str(prediction),  # Ensure string conversion
                "confidence": round(float(confidence) * 100, 2)  # Ensure float conversion
            }
            
            return jsonify(response)
        
        except Exception as e:
            # Log the full error for debugging
            app.logger.error(f"News analysis error: {str(e)}")
            
            # Return a user-friendly error response
            return jsonify({
                "error": "An unexpected error occurred during analysis",
                "prediction": "inconclusive",
                "confidence": 0
            }), 500
@app.route('/sentiment', methods=['GET', 'POST'])
def news_sentiment_analysis():
    if request.method == 'POST':
        input_source = request.form["text"]
        text = extractor.extract_text(input_source)
        sentiment, confidence = obj.analyze_sentiment(text[:1000])#this only takes first  1000 characters
        time.sleep(random.uniform(1, 2))
        
        return jsonify({
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence*100, 2)})
    return render_template('sentiment.html')



@app.route("/summarization", methods=["GET", "POST"])
def summarize():
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {
        "Authorization": "Bearer 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",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36'
    }
    if request.method == "POST":
        input_source = request.form["text"]
        # Get mode and length from form
        mode = request.form.get("mode", "paragraph")
        length_percent = int(request.form.get("length", 50))
        
        text = extractor.extract_text(input_source)
        
        # Calculate lengths based on percentage
        input_length = len(text.split())
        target_length = max(1, int(input_length * (length_percent/100)))
        
        # Call Hugging Face API for summarization
        try:
            response = requests.post(API_URL, headers=headers, json={
                "inputs": text,
                "parameters": {
                    "max_length": target_length,
                    "min_length": max(1, int(target_length * 0.8))
                }
            })
            result = response.json()
            summary = result[0]['summary_text']

            # Format based on mode
            if mode == "bullet":
                summary = summary.replace('. ', '.\n')
                summary = ' ' + summary

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

        output, human, ai = news_detection.ai_plagiarism(text)
        return jsonify({
            "output": output,
            "human": human,
            "ai": ai
        })

    return render_template('plagiarism.html') # Render the template for GET requests
def truncate_text(text, max_tokens=500):
    tokens = text.split()
    if len(tokens) > max_tokens:
        return ' '.join(tokens[:max_tokens])
    return text

def get_report_data(text):
    report_results = {}

    # Fake News Detection
    processed_text = news_detection.preprocess_custom_input(text)
    prediction, confidence = news_detection.fake_news_classifier(processed_text)
    report_results['fake_news'] = {
        'prediction': prediction,
        'confidence': round(confidence * 100, 2)
    }

    # Summarization
    summary_response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": text, "parameters": {"max_length": 130, "min_length": 50}}
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

    sentiment, confidence = obj.analyze_sentiment(text[:1000])
    report_results['sentiment'] = {
        'prediction': sentiment,
        'confidence': round(confidence * 100, 2)}
    return report_results

@app.route('/report', methods=['GET', 'POST'])
def comprehensive_report():
    if request.method == "POST":
        input_source = request.form["text"]
        app.logger.info(f"Received input source: {input_source}")
        
        text = extractor.extract_text(input_source)
        app.logger.info(f"Extracted text: {text}")
        
        if not text:
            return jsonify({"error": "Text is required"}), 400

        try:
            # Truncate the text to a maximum of 500 tokens
            truncated_text = truncate_text(text)
            app.logger.info(f"Truncated text: {truncated_text}")

            report_results = get_report_data(truncated_text)
            return render_template("result.html", report=report_results)
        except Exception as e:
            app.logger.error(f"Error in comprehensive report generation: {str(e)}", exc_info=True)
            return jsonify({"error": f"Error occurred: {str(e)}"}), 500

    return render_template("result.html", report=None)


if __name__ == '__main__':
    news_detection = FakeNewsClassifier()
    obj = TextAnalysis()
    extractor = TextExtractor(max_words=400)
    app.run(host='0.0.0.0', port=5000, debug=True)
 