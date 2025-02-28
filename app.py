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
from flask_sqlalchemy import SQLAlchemy
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class FakeNewsRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    label = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

class SentimentRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    sentiment = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

class SummarizationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    summary = db.Column(db.Text, nullable=False)

class PlagiarismRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    output = db.Column(db.Text, nullable=False)
    human_score = db.Column(db.Float, nullable=False)
    ai_score = db.Column(db.Float, nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()
# Create the database and table
with app.app_context():
    db.create_all()
@app.route("/", methods=["GET"])
def home():
    return render_template('landing_page.html')
@app.route("/home", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "GET":
        return render_template("fakecheck-ai-modern.html")
    
    if request.method == "POST":
        print("POST request received")
        input_data = request.get_json()
        input_source = input_data.get("text", "")
        
        if not input_source:
            return jsonify({
                "error": "No text provided",
                "prediction": "inconclusive",
                "confidence": 0
            }), 400
        
        try:
            # Check if the URL is already in the database
            existing_record = FakeNewsRecord.query.filter_by(url=input_source).first()
            if existing_record:
                print("Existing record found")
                return jsonify({
                    "prediction": existing_record.label,
                    "confidence": existing_record.confidence
                })
            
            # If not, proceed with analysis
            text = extractor.extract_text(input_source)
            if not text:
                return jsonify({
                    "error": "Unable to extract meaningful text",
                    "prediction": "inconclusive",
                    "confidence": 0
                }), 400
            
            processed_text = news_detection.preprocess_custom_input(text)
            prediction, confidence = news_detection.fake_news_classifier(processed_text)
            print(prediction,confidence)
            # Store the result in the database
            new_record = FakeNewsRecord(url=input_source, label=prediction, confidence=round(float(confidence) * 100, 2))
            db.session.add(new_record)
            db.session.commit()
            
            response = {
                "prediction": str(prediction),
                "confidence": round(float(confidence) * 100, 2)
            }
            
            return jsonify(response)
        
        except Exception as e:
            app.logger.error(f"News analysis error: {str(e)}")
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

@app.route("/report", methods=["GET", "POST"])
def comprehensive_report():
    if request.method == "GET":
        return render_template("result.html", report=None)
    
    if request.method == "POST":
        input_source = request.form.get("text", "")
        if not input_source:
            return jsonify({"error": "Text is required"}), 400

        text = extractor.extract_text(input_source)
        if not text:
            return jsonify({"error": "Could not extract meaningful text"}), 400

        report_results = {}

        # Check Fake News Record
        fake_news_record = FakeNewsRecord.query.filter_by(url=input_source).first()
        if fake_news_record:
            report_results['fake_news'] = {
                'prediction': fake_news_record.label,
                'confidence': fake_news_record.confidence
            }
        else:
            processed_text = news_detection.preprocess_custom_input(text)
            prediction, confidence = news_detection.fake_news_classifier(processed_text)
            new_record = FakeNewsRecord(url=input_source, label=prediction, confidence=round(confidence * 100, 2))
            db.session.add(new_record)
            db.session.commit()
            report_results['fake_news'] = {'prediction': prediction, 'confidence': round(confidence * 100, 2)}

        # Check Sentiment Record
        sentiment_record = SentimentRecord.query.filter_by(url=input_source).first()
        if sentiment_record:
            report_results['sentiment'] = {
                'prediction': sentiment_record.sentiment,
                'confidence': sentiment_record.confidence
            }
        else:
            sentiment, confidence = obj.analyze_sentiment(text[:1000])
            new_record = SentimentRecord(url=input_source, sentiment=sentiment, confidence=round(confidence * 100, 2))
            db.session.add(new_record)
            db.session.commit()
            report_results['sentiment'] = {'prediction': sentiment, 'confidence': round(confidence * 100, 2)}

        # Check Summarization Record
        summary_record = SummarizationRecord.query.filter_by(url=input_source).first()
        if summary_record:
            report_results['summarization'] = summary_record.summary
        else:
            response = requests.post(API_URL, headers=headers, json={
                "inputs": text,
                "parameters": {"max_length": 130, "min_length": 50}
            })
            summary = response.json()[0]['summary_text']
            new_record = SummarizationRecord(url=input_source, summary=summary)
            db.session.add(new_record)
            db.session.commit()
            report_results['summarization'] = summary

        # Check Plagiarism Record
        plagiarism_record = PlagiarismRecord.query.filter_by(url=input_source).first()
        if plagiarism_record:
            report_results['plagiarism'] = {
                'output': plagiarism_record.output,
                'human_score': plagiarism_record.human_score,
                'ai_score': plagiarism_record.ai_score
            }
        else:
            output, human, ai = news_detection.ai_plagiarism(text)
            new_record = PlagiarismRecord(url=input_source, output=output, human_score=human, ai_score=ai)
            db.session.add(new_record)
            db.session.commit()
            report_results['plagiarism'] = {'output': output, 'human_score': human, 'ai_score': ai}

        return render_template("result.html", report=report_results)
@app.route("/history", methods=["GET"])
def view_history():
    fake_news_records = FakeNewsRecord.query.all()
    sentiment_records = SentimentRecord.query.all()
    summarization_records = SummarizationRecord.query.all()
    plagiarism_records = PlagiarismRecord.query.all()
    return render_template("history.html", fake_news_records=fake_news_records, sentiment_records=sentiment_records, summarization_records=summarization_records, plagiarism_records=plagiarism_records)

if __name__ == '__main__':
    news_detection = FakeNewsClassifier()
    obj = TextAnalysis()
    extractor = TextExtractor(max_words=400)
    app.run(host='0.0.0.0', port=5000, debug=True)
 