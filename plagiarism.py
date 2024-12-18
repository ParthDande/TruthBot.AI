import joblib
from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords

# Load the model and vectorizer
model = joblib.load('Models/plagiarism.pkl')
vectorizer  = joblib.load('vectorizers/plagiarism_vectorizer.pkl')

class PlagiarismDetection:
    def __init__(self):
        self.model = joblib.load('Models/plagiarism.pkl')
        self.vectorizer = joblib.load('vectorizers/plagiarism_vectorizer.pkl')
        self.stopwords = set(stopwords.words('english'))

    def ai_plagiarism(self, text):
        self.text = text
        input_text = [self.text]
        
        # Transform input using vectorizer
        transformed_input = self.vectorizer.transform(input_text)
        
        # Get probability predictions
        probabilities = self.model.predict_proba(transformed_input)[0]
        
        # Get the percentage of human-written and AI-generated content
        human_written_prob = probabilities[0] * 100  # Probability of class 0
        ai_generated_prob = probabilities[1] * 100   # Probability of class 1
        
        if ai_generated_prob > human_written_prob:
            prediction = "AI_Generated"
        else:
            prediction = "Human_Written"
        
        return prediction, human_written_prob, ai_generated_prob

