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
model = joblib.load('plagiarism.pkl')
vectorizer  = joblib.load('plagiarism_vectorizer.pkl')

# Input text to classify
text = """
Kejriwal was released from Delhi’s Tihar Jail on September 13 after being granted bail by the Supreme Court in connection with a Central Bureau of Investigation (CBI) case related to the alleged excise policy scam. He had spent five months in jail.

Speaking at a rally in Badshahpur, Kejriwal took a swipe at Prime Minister Narendra Modi, alleging that the BJP targeted him because of his political success in Delhi and Punjab.

"PM Modi thought Kejriwal formed a government in Delhi and Punjab. Now, he feared that I would form a government in Haryana," Kejriwal said.
"""
class PlagiarismDetection:
    def __init__(self):
        self.model = joblib.load('plagiarism.pkl')
        self.vectorizer = joblib.load('plagiarism_vectorizer.pkl')
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

obj = PlagiarismDetection()
print(obj.ai_plagiarism(text))
