import PyPDF2
from newspaper import Article
import requests
import io

class TextExtractor:
    def __init__(self, max_words=400):
        """
        Initialize TextExtractor with a maximum word count.
        
        :param max_words: Maximum number of words to extract (default: 400)
        """
        self.max_words = max_words
    
    def extract_text(self, input_source):
        """
        Extract text from various sources.
        
        :param input_source: Can be a file path, file object, URL, or raw text
        :return: Extracted text limited to max_words
        """
        # Determine input type and extract text accordingly
        if isinstance(input_source, str):
            # Check if input is a URL
            if input_source.startswith(('http://', 'https://')):
                return self._extract_from_url(input_source)
            
            # Check if input is a file path ending with .pdf
            elif input_source.lower().endswith('.pdf'):
                return self._extract_from_pdf(input_source)
            
            # Assume it's raw text
            else:
                return self._truncate_text(input_source)
        
        # Check if input is a file-like object
        elif hasattr(input_source, 'read'):
            # Check if it's a PDF
            if input_source.name.lower().endswith('.pdf'):
                return self._extract_from_pdf_file(input_source)
            
            # Assume it's a text file
            else:
                return self._truncate_text(input_source.read().decode('utf-8'))
        
        else:
            raise ValueError("Unsupported input type. Provide a URL, file path, file object, or text string.")
    
    def _extract_from_url(self, url):
        """
        Extract text from a news article URL.
        
        :param url: URL of the article
        :return: Extracted and truncated text
        """
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36'
        }
        try:
            article = Article(url, browser_user_agent=headers['User-Agent'])
            article.download()
            article.parse()
            complete_text = article.text+" "+article.title
            return self._truncate_text(complete_text)
        except Exception as e:
            raise ValueError(f"Error extracting text from URL: {str(e)}")

    
    def _extract_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file path.
        
        :param pdf_path: Path to the PDF 
        """
        try:
            with open(pdf_path, 'rb') as file:
                return self._extract_from_pdf_file(file)
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
    
    def _extract_from_pdf_file(self, pdf_file):
        """
        Extract text from a PDF file object.
        
        :param pdf_file: File object of the PDF
        :return: Extracted and truncated text
        """
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + " "
            
            return self._truncate_text(text)
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    def _truncate_text(self, text):
        """
        Truncate text to specified maximum word count.
        
        :param text: Input text
        :return: Truncated text
        """
        # Remove extra whitespaces and split into words
        words = text.strip().split()
        
        # Truncate to max_words
        truncated_words = words[:self.max_words]
        
        return ' '.join(truncated_words)

# Example usage
if __name__ == "__main__":
    # Create an instance of TextExtractor
    extractor = TextExtractor(max_words=400)
    
    # Example: Extract from a URL
    # url_text = extractor.extract_text("https://example.com/news-article")
    
    # Example: Extract from a PDF file
    # pdf_text = extractor.extract_text("/path/to/document.pdf")
    
    # Example: Extract from raw text
    # text = extractor.extract_text("Your long text goes here...")
    pass