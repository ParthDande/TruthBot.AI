from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Hugging Face API URL for summarization
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route("/summarization", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        input_length = len(text)
        min_length = max(1, int(input_length * 0.1))
        min_length = max(1, int(input_length * 0.05))
        result = query({
            "inputs": text,
            "parameters": {
                "max_length": min_length,
                "min_length": min_length
            }
        })

        # Extract the summary text from the response
        summary = result[0]['summary_text']

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'summary': summary})
        else:
            return render_template("summarization.html", summary=summary)

    return render_template("summarization.html", summary="")

if __name__ == "__main__":
    app.run(debug=True)
