import logging
from flask import Flask, request, render_template, jsonify
import time
import random
import requests
import os
from dotenv import load_dotenv
from news_analysis import TextAnalysis
from news_classification import FakeNewsClassifier
from plagiarism import PlagiarismDetection
from TextExtractor import TextExtractor
from flask_sqlalchemy import SQLAlchemy
from PyPDF2 import PdfReader

load_dotenv()

# basic logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = os.getenv("API_URL")
headers = {"Authorization": f"Bearer {os.getenv('HF_AUTH_TOKEN')}"}
sentiment_api = os.getenv("SENTIMENT_API")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DB Models
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
        try:
            input_data = request.get_json()
            input_source = input_data.get("text", "")
            if not input_source:
                return jsonify({"error": "No text provided", "prediction": "inconclusive", "confidence": 0}), 400

            existing_record = FakeNewsRecord.query.filter_by(url=input_source).first()
            if existing_record:
                return jsonify({"prediction": existing_record.label, "confidence": existing_record.confidence})

            text = extractor.extract_text(input_source)
            if not text:
                return jsonify({"error": "Unable to extract text", "prediction": "inconclusive", "confidence": 0}), 400

            processed_text = news_detection.preprocess_custom_input(text)
            prediction, confidence = news_detection.fake_news_classifier(processed_text)
            new_record = FakeNewsRecord(url=input_source, label=prediction, confidence=round(confidence * 100, 2))
            db.session.add(new_record)
            db.session.commit()

            return jsonify({"prediction": prediction, "confidence": round(confidence * 100, 2)})

        except Exception as e:
            logger.exception("Error in /analyze")
            return jsonify({"error": "Something went wrong", "prediction": "inconclusive", "confidence": 0}), 500

@app.route('/sentiment', methods=['GET', 'POST'])
def news_sentiment_analysis():
    if request.method == 'POST':
        try:
            input_source = request.form["text"]
            text = extractor.extract_text(input_source)
            sentiment, confidence = obj.analyze_sentiment(text[:1000])
            time.sleep(random.uniform(1, 2))
            return jsonify({'text': text, 'sentiment': sentiment, 'confidence': round(confidence * 100, 2)})
        except Exception as e:
            logger.exception("Error in /sentiment")
            return jsonify({"error": "Sentiment analysis failed"}), 500

    return render_template('sentiment.html')

@app.route("/summarization", methods=["GET", "POST"])
def summarize():
    if request.method == "POST":
        try:
            input_source = request.form["text"]
            mode = request.form.get("mode", "paragraph")
            length_percent = int(request.form.get("length", 50))

            text = extractor.extract_text(input_source)
            input_length = len(text.split())
            target_length = max(1, int(input_length * (length_percent/100)))

            response = requests.post(API_URL, headers=headers, json={
                "inputs": text,
                "parameters": {"max_length": target_length, "min_length": max(1, int(target_length * 0.8))}
            })
            result = response.json()
            summary = result[0]['summary_text']

            if mode == "bullet":
                summary = summary.replace('. ', '.\n')
                summary = ' ' + summary

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'summary': summary})
            else:
                return render_template("summarization.html", summary=summary)

        except Exception as e:
            logger.exception("Error in /summarization")
            return jsonify({'error': f'Error generating summary: {str(e)}'}), 500

    return render_template("summarization.html", summary="")

@app.route('/plagiarism', methods=['GET', 'POST'])
def news_plagiarism_check():
    if request.method == 'POST':
        try:
            if 'text' in request.form:
                text = request.form['text']
            elif 'file' in request.files:
                file = request.files['file']
                if file.filename.endswith('.pdf'):
                    reader = PdfReader(file)
                    text = "".join(page.extract_text() for page in reader.pages)
                else:
                    text = file.read().decode('utf-8')
            else:
                return jsonify({'error': 'No valid input provided'}), 400

            output, human, ai = news_detection.ai_plagiarism(text)
            return jsonify({"output": output, "human": human, "ai": ai})
        except Exception as e:
            logger.exception("Error in /plagiarism")
            return jsonify({"error": "Plagiarism check failed"}), 500

    return render_template('plagiarism.html')

@app.route("/report", methods=["GET", "POST"])
def comprehensive_report():
    if request.method == "GET":
        return render_template("result.html", report=None)

    if request.method == "POST":
        try:
            input_source = request.form.get("text", "")
            if not input_source:
                return jsonify({"error": "Text is required"}), 400

            text = extractor.extract_text(input_source)
            if not text:
                return jsonify({"error": "Could not extract meaningful text"}), 400

            report_results = {}

            try:
                record = FakeNewsRecord.query.filter_by(url=input_source).first()
                if record:
                    report_results['fake_news'] = {'prediction': record.label, 'confidence': record.confidence}
                else:
                    processed_text = news_detection.preprocess_custom_input(text)
                    prediction, confidence = news_detection.fake_news_classifier(processed_text)
                    db.session.add(FakeNewsRecord(url=input_source, label=prediction, confidence=round(confidence*100,2)))
                    db.session.commit()
                    report_results['fake_news'] = {'prediction': prediction, 'confidence': round(confidence * 100, 2)}
            except Exception as e:
                logger.exception("Fake news check failed")
                report_results['fake_news'] = {'error': 'Fake news check failed'}

            try:
                record = SentimentRecord.query.filter_by(url=input_source).first()
                if record:
                    report_results['sentiment'] = {'prediction': record.sentiment, 'confidence': record.confidence}
                else:
                    sentiment, confidence = obj.analyze_sentiment(text[:1000])
                    db.session.add(SentimentRecord(url=input_source, sentiment=sentiment, confidence=round(confidence * 100, 2)))
                    db.session.commit()
                    report_results['sentiment'] = {'prediction': sentiment, 'confidence': round(confidence * 100, 2)}
            except Exception as e:
                logger.exception("Sentiment check failed")
                report_results['sentiment'] = {'error': 'Sentiment check failed'}

            try:
                record = SummarizationRecord.query.filter_by(url=input_source).first()
                if record:
                    report_results['summarization'] = record.summary
                else:
                    response = requests.post(API_URL, headers=headers, json={"inputs": text, "parameters": {"max_length": 150, "min_length": 80}})
                    summary = response.json()[0]['summary_text']
                    db.session.add(SummarizationRecord(url=input_source, summary=summary))
                    db.session.commit()
                    report_results['summarization'] = summary
            except Exception as e:
                logger.exception("Summarization check failed")
                report_results['summarization'] = 'Summarization failed'

            try:
                record = PlagiarismRecord.query.filter_by(url=input_source).first()
                if record:
                    report_results['plagiarism'] = {'output': record.output, 'human_score': record.human_score, 'ai_score': record.ai_score}
                else:
                    output, human, ai = news_detection.ai_plagiarism(text)
                    db.session.add(PlagiarismRecord(url=input_source, output=output, human_score=human, ai_score=ai))
                    db.session.commit()
                    report_results['plagiarism'] = {'output': output, 'human_score': human, 'ai_score': ai}
            except Exception as e:
                logger.exception("Plagiarism check failed")
                report_results['plagiarism'] = {'error': 'Plagiarism check failed'}

            return render_template("result.html", report=report_results)
        except Exception as e:
            logger.exception("Error in /report")
            return jsonify({"error": "Report generation failed"}), 500

@app.route("/history", methods=["GET"])
def view_history():
    try:
        return render_template("history.html",
                               fake_news_records=FakeNewsRecord.query.all(),
                               sentiment_records=SentimentRecord.query.all(),
                               summarization_records=SummarizationRecord.query.all(),
                               plagiarism_records=PlagiarismRecord.query.all())
    except Exception as e:
        logger.exception("Error loading /history")
        return jsonify({"error": "Failed to load history"}), 500

if __name__ == '__main__':
    news_detection = FakeNewsClassifier()
    obj = TextAnalysis()
    extractor = TextExtractor(max_words=400)
    app.run(host='0.0.0.0', port=5000, debug=True)