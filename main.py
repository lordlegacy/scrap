from scraping_app.scraper import extract_text_from_url
import sys

if __name__ == "__main__":
    #if len(sys.argv) != 2:
    #    print("Usage: python main.py <URL>")
   #     sys.exit(1)
    #url = sys.argv[1]
    
    text = extract_text_from_url(url)
    
    if text:
        print("Scraped Text:")
        print(text)
    else:
        print("Failed to scrape the URL.")
