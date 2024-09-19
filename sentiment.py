from huggingface_hub import InferenceClient


from flask import Flask, request, render_template
import time
import random
app = Flask(__name__)
class TextAnalysis:
    @staticmethod
    def analyze_sentiment(text):
        
        client = InferenceClient(
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
            token="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"
        )

        # Perform sentiment analysis
        result = client.text_classification(text)

        # Extract sentiment and score with the highest score
        sentiment = result[0]['label']
        score = result[0]['score']
        return sentiment,score


@app.route('/sentiment', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        obj = TextAnalysis()
        text = request.form['user_input']
        sentiment, confidence = obj.analyze_sentiment(text)
        time.sleep(random.uniform(1, 2))  # Simulate processing time
        return {
            'text': text,
            'sentiment': sentiment,
            'confidence': round(confidence * 100, 2)  # Convert to percentage and round to 2 decimal places
        }
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=5001)
