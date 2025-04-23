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
import warnings
warnings.filterwarnings("ignore") 
# stopwords
stop_words = set(stopwords.words('english'))
#  TF-IDF vectorizer

class FakeNewsClassifier:
    def __init__(self):
        self.model_paths = [
            "Models/XGBClassifier_Model.pkl",
            "Models/LGBMClassifier_Model.pkl",
            "Models/logistic_regression_model.pkl",
            "Models/Random_Forest_Model.pkl",
            "Models/Support_Vector_Machine_Model.pkl"
        ]
        self.loaded_models = [joblib.load(path) for path in self.model_paths]
        self.fake_news_vectorizer = joblib.load('vectorizers/tfidf_vectorizer.pkl')
        self.plagiarism_model = joblib.load('Models/plagiarism.pkl')
        self.plagiarism_vectorizer = joblib.load('vectorizers/plagiarism_vectorizer.pkl')

    def preprocess_custom_input(self, full_text):
        tokens = word_tokenize(full_text.lower())
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
        cleaned_text = ' '.join(filtered_tokens)
        vectorized_text = self.fake_news_vectorizer.transform([cleaned_text]).toarray()
        return vectorized_text

    def fake_news_classifier(self, text, text_type='general'):
        prediction = []
        all_confidence_score = []

        for model in self.loaded_models:
            if hasattr(model, "predict_proba"):
                probabilities = model.predict_proba(text)
                predicted_class = probabilities[0].argmax()
                confidence_score = probabilities[0][predicted_class]
                all_confidence_score.append(confidence_score)
            else:
                predicted_class = model.predict(text)[0]
            prediction.append(predicted_class)

        final_prediction = max(set(prediction), key=prediction.count)
        avg_confidence = sum(all_confidence_score) / len(all_confidence_score) if all_confidence_score else 0
        label = {1: "Real", 0: "Fake"}[final_prediction]
        return label, avg_confidence

    def ai_plagiarism(self, text):
        transformed_input = self.plagiarism_vectorizer.transform([text])
        probabilities = self.plagiarism_model.predict_proba(transformed_input)[0]
        human_written_prob = probabilities[0] * 100
        ai_generated_prob = probabilities[1] * 100
        prediction = "AI_Generated" if ai_generated_prob > human_written_prob else "Human_Written"
        return prediction, human_written_prob, ai_generated_prob

    