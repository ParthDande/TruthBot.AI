from xgboost import XGBClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import joblib

#  NLTK data path and download necessary resources
nltk.data.path.append('C:/Users/parth/Desktop/fake-news-classification/nltk_data')
nltk.download('stopwords', download_dir='C:/Users/parth/Desktop/fake-news-classification/nltk_data')
nltk.download('punkt', download_dir='C:/Users/parth/Desktop/fake-news-classification/nltk_data')

# stopwords
stop_words = set(stopwords.words('english'))

#  TF-IDF vectorizer
loaded_model = XGBClassifier()
loaded_model.load_model('fake_news_model.json')
tfidf = joblib.load('tfidf_vectorizer.pkl')

class FakeNewsClassifier:
    def __init__(self):
        self.model = loaded_model
        self.tfidf = tfidf

    def preprocess_custom_input(self, text, domain):
        tokens = word_tokenize(text.lower())  
        filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]  # Remove stopwords and non-alphanumeric tokens
        filtered_tokens.append(domain)  
        cleaned_text = ' '.join(filtered_tokens)
        vectorized_text = self.tfidf.transform([cleaned_text])
        return vectorized_text

    def fake_news_classifier(self, text):
        # Get prediction and probabilities
        probabilities = self.model.predict_proba(text)
        predicted_class = probabilities[0].argmax()  #  index of max probability
        confidence_score = probabilities[0][predicted_class]  # Confidence for the predicted class
        
        mapping = {1: "Real", 0: "Fake"}
        prediction = mapping[predicted_class]
        return prediction, confidence_score

# Testing the model
obj = FakeNewsClassifier()
text_to_classify ="Angelina Jolie is going to be the next president of the United States"
domain = "www.cnn.com"
vectorized_text = obj.preprocess_custom_input(text_to_classify, domain)
prediction, confidence = obj.fake_news_classifier(vectorized_text)
