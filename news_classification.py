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
nltk.data.path.append('nltk_data/')

# stopwords
stop_words = set(stopwords.words('english'))
models = ["XGBClassifier_Model.pkl", "LGBMClassifier_Model.pkl", "logistic_regression_model.pkl", "Random_forest_Model.pkl","Support_Vector_Machine_Model.pkl"]
#  TF-IDF vectorizer
fake_news_model = joblib.load("Models/XGBClassifier_Model.pkl")
tfidf = joblib.load('vectorizers/tfidf_vectorizer.pkl')
model = joblib.load('Models/plagiarism.pkl')
vectorizer  = joblib.load('vectorizers/plagiarism_vectorizer.pkl')

class FakeNewsClassifier:
    def __init__(self):
        self.models = models
        self.fake_news_vectorizer = tfidf
        self.plagiarism_model = model
        self.plagiarism_vectorizer = vectorizer

   
    def preprocess_custom_input(self,full_text):
        # Step 1: Preprocess the text
        tokens = word_tokenize(full_text.lower())  # Convert to lowercase and tokenize
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Remove stopwords and non-alphanumeric tokens
        cleaned_text = ' '.join(filtered_tokens)
        # Step 2: Vectorize the cleaned text (using the same TF-IDF vectorizer)
        vectorized_text = self.fake_news_vectorizer.transform([cleaned_text]).toarray()

        return vectorized_text


    def fake_news_classifier(self, text,text_type='general'):
        prediction = []
        all_confidence_score = []
        for model in self.models:
            model = joblib.load(f"Models/{model}")
            self.fake_news_model = model
            # Get prediction and probabilities
            if hasattr(self.fake_news_model, "predict_proba"):
                probabilities = self.fake_news_model.predict_proba(text)
                predicted_class = probabilities[0].argmax()
                confidence_score = probabilities[0][predicted_class]  # Confidence for the predicted class
                all_confidence_score.append(confidence_score)
            else:
                predicted_class = self.fake_news_model.predict(text)[0]
            prediction.append(predicted_class)
            
        # Get the majority vote from the predictions
        predicted_class = max(set(prediction), key=prediction.count)
        confidence_score = sum(all_confidence_score) / len(all_confidence_score) if all_confidence_score else 0
        mapping = {1: "Real", 0: "Fake"}
        prediction = mapping[predicted_class]
        return prediction, confidence_score
    

    def ai_plagiarism(self, text):
        self.text = text
        input_text = [self.text]
        
        # Transform input using vectorizer
        transformed_input = self.plagiarism_vectorizer.transform(input_text)
        
        # Get probability predictions
        probabilities = self.plagiarism_model.predict_proba(transformed_input)[0]
        
        # Get the percentage of human-written and AI-generated content
        human_written_prob = probabilities[0] * 100  # Probability of class 0
        ai_generated_prob = probabilities[1] * 100   # Probability of class 1
        
        if ai_generated_prob > human_written_prob:
            prediction = "AI_Generated"
        else:
            prediction = "Human_Written"
        
        return prediction, human_written_prob, ai_generated_prob
    