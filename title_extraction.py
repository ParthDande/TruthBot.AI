import requests
from bs4 import BeautifulSoup

# Function to scrape title and article text from a URL
def scrape_content(url):
    # Send a GET request to fetch the content of the page
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the title of the page
    title = soup.title.string if soup.title else "No title found"
    
    # Remove script and style tags, as they don't contain readable content
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    
    # Extract and clean all the text from the page
    text = soup.get_text(separator=' ')
    
    # Strip and clean the text (optional: could add further processing)
    cleaned_text = ' '.join(text.split())
    
    return title, cleaned_text

# Example usage
url = 'https://www.ndtv.com/opinion/opinion-should-we-be-worried-about-unemployable-human-bots-6591294'  # Replace with the URL of the article you want to scrape
title, article = scrape_content(url)

# Save the title and article to a text file
with open('scraped_content.txt', 'w', encoding='utf-8') as f:
    f.write(f"Title: {title}\n\n")
    f.write(f"Article: {article}\n")

print("Title and article have been saved to 'scraped_content.txt'.")
