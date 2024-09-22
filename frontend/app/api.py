import requests
from app.config import SCRAPING_API_URL, QA_API_URL

# Function to send the URL to the Scraping Module
def send_url_to_scraping_module(url):
    try:
        response = requests.post(SCRAPING_API_URL, json={"url": url})
        response_data = response.json()

        if response.status_code == 200:
            return {"status": "success", "scraped_text": response_data.get("scraped_text", "")}
        else:
            return {"status": "error", "error": response_data.get("error", "Unknown error")}
    
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": str(e)}

# Function to send the question to the Q&A Module
def send_question_to_qa_module(question):
    try:
        response = requests.post(QA_API_URL, json={"question": question})
        response_data = response.json()

        if response.status_code == 200:
            return {"status": "success", "answer": response_data.get("answer", "")}
        else:
            return {"status": "error", "error": response_data.get("error", "Unknown error")}
    
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": str(e)}
