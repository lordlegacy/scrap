from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def extract_text_from_url(url):
    try:
        # Set up Chrome options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run Chrome in headless mode
        options.add_argument("--no-sandbox")  # Required for Docker
        options.add_argument("--disable-dev-shm-usage")  # Overcome resource limitations in Docker
        options.add_argument("--disable-gpu")  # Disable GPU rendering
        options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging

        # Set up the WebDriver
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
