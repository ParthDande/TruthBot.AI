from flask import Flask, render_template, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Initialize the summarization pipeline
summarizer = pipeline("summarization")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        max_length = int(request.form["max_length"])
        summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)[0]['summary_text']
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'summary': summary})
        else:
            return render_template("summarization.html", summary=summary)
    return render_template("summarization.html", summary="")

if __name__ == "__main__":
    app.run(debug=True)