from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)
import warnings
import os 
from dotenv import load_dotenv
warnings.filterwarnings("ignore") 
# Hugging Face API URL for summarization
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {os.getenv('HF_AUTH_TOKEN')}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/summarization", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        input_length = len(text)
        print(input_length)
        min_length = max(1, int(input_length * 0.3))
        max_length = max(1, int(input_length * 0.6))
        result = query({
            "inputs": text,
            "parameters": {
                "max_length": min_length,
                "min_length": min_length
            }
        })
        print(min_length)
        print(max_length)

        # Extract the summary text from the response
        summary = result[0]['summary_text']

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'summary': summary})
        else:
            return render_template("summarization.html", summary=summary)

    return render_template("summarization.html", summary="")

if __name__ == "__main__":
    app.run(debug=True)
