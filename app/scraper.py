from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extract_text_from_url(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-dev-shm-usage")  
        options.add_argument("--disable-gpu")  
        options.add_argument("--remote-debugging-port=9222")  


        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        driver.quit()

        return body_text

    except Exception as e:
        print(f"Error while scraping: {e}")
        return None
    

def clean_and_chunk_text(scraped_text, chunk_size=500):
    cleaned_text = scraped_text.replace('\n', ' ').strip()  
    cleaned_text = ' '.join(cleaned_text.split())  

    text_length = len(cleaned_text)
    chunks = [cleaned_text[i:i + chunk_size] for i in range(0, text_length, chunk_size)]
    
    return chunks



