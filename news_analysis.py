from transformers import pipeline
import warnings
warnings.filterwarnings("ignore") 
import logging
import time
import random

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
