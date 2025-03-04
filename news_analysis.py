import time
import random
from huggingface_hub import InferenceClient
import warnings
warnings.filterwarnings("ignore") 
import os 
from dotenv import load_dotenv
class TextAnalysis:
    def __init__(self):
            self.client = InferenceClient(
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            token=os.getenv("SENTIMENT_API")
        )

    def analyze_sentiment(self, text):
        result = self.client.text_classification(text)

        # Extract sentiment and score with the highest score
        sentiment = result[0]['label']
        score = result[0]['score']
        return sentiment,score

