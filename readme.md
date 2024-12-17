# TruthBot.ai

TruthBot.ai is a news analysis platform that verifies credibility, detects fake news, analyzes sentiment, summarizes content, and checks for plagiarism. It features a simple interface and powerful backend.

---

## Features

### 1. **Fake News Detection**
- 🛡️ Detects fake news with domain-specific preprocessing.
- 📊 Provides confidence scores.

### 2. **Sentiment Analysis**
- 😊 Analyzes sentiment (Positive, Negative, Neutral).
- 📈 Displays confidence levels.

### 3. **Text Summarization**
- ✂️ Summarizes news using Hugging Face BART-Large-CNN.
- 🔧 Adjusts summary length automatically.

### 4. **Plagiarism Detection**
- 🔍 Detects AI-generated or human-authored plagiarism.
- 📜 Provides human and AI scores.

### 5. **Reports**
- 📑 Combines:
  - 😊 Sentiment analysis.
  - 🛡️ Fake news detection.
  - ✂️ Summarization.
  - 🔍 Plagiarism detection.
  - 📈 Virality metrics.

### 6. **Text Extraction**
- 🧹 Extracts text from:
  - 🌐 URLs
  - 📄 PDFs
  - 📝 Plain text

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TruthBot.ai.git
   ```

2. Navigate to the project directory:
   ```bash
   cd TruthBot.ai
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your Hugging Face API key:
   - Replace `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` with your key.

---

## Usage

1. Run the app:
   ```bash
   python app.py
   ```

2. Open your browser at:
   ```
   http://127.0.0.1:5000
   ```

3. Use endpoints:
   - 🏠 `/`: Home page.
   - 🛡️ `/analyze`: Fake news detection.
   - 😊 `/sentiment`: Sentiment analysis.
   - ✂️ `/summarization`: Summarization.
   - 🔍 `/plagiarism`: Plagiarism check.
   - 📑 `/report`: Full reports.

---

## API Reference

### Fake News Detection (`/analyze`)
- **Method:** `POST`
- **Parameters:**
  - 📝 `text`: News content.
  - 🌐 `domain`: News domain.
- **Response:**
  - 🛡️ `prediction`: Result.
  - 📊 `confidence`: Score.

### Sentiment Analysis (`/sentiment`)
- **Method:** `POST`
- **Parameters:**
  - 📝 `text`: Input text or URL.
- **Response:**
  - 😊 `sentiment`: Result.
  - 📈 `confidence`: Score.

### Summarization (`/summarization`)
- **Method:** `POST`
- **Parameters:**
  - 📝 `text`: Input text or URL.
- **Response:**
  - ✂️ `summary`: Generated summary.

### Plagiarism Detection (`/plagiarism`)
- **Method:** `POST`
- **Parameters:**
  - 📝 `text`: Input text or URL.
- **Response:**
  - 🔍 `output`: Plagiarism check results.
  - 🧾 `human_score`: Human content score.
  - 🤖 `ai_score`: AI content score.

### Comprehensive Report (`/report`)
- **Method:** `POST`
- **Parameters:**
  - 📝 `text`: Input text or URL.
- **Response:**
  - 📑 Full analysis report.

---

## Project Structure

- 📂 `app.py`: Main app file.
- 📁 `templates/`: HTML templates.
- 📁 `static/`: Static assets.
- 🛠️ `news_analysis.py`: Sentiment analysis.
- 🛡️ `news_classification.py`: Fake news detection.
- 🔍 `plagiarism.py`: Plagiarism detection.
- 📜 `TextExtractor.py`: Text extraction utility.

---

## Contributing

Contributions welcome! Submit pull requests or open issues for suggestions or bug reports.

---

## License

MIT License. See LICENSE file for details.

---

## Acknowledgments

- 🌐 [Flask](https://flask.palletsprojects.com/) for the web framework.
- 🤗 [Hugging Face](https://huggingface.co/) for the model.
- 📄 [PyPDF2](https://pypi.org/project/PyPDF2/) for PDFs.
- 📰 [Newspaper3k](https://newspaper.readthedocs.io/) for article parsing.

