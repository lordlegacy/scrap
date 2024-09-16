from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extract_text_from_url(url):
    try:
        # Set up the WebDriver (this downloads the correct version of ChromeDriver)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Visit the given URL
        driver.get(url)
        
        # Extract all the visible text from the body of the page
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        
        # Close the browser
        driver.quit()
        
        return body_text

    except Exception as e:
        print(f"Error while scraping: {e}")
        return None
