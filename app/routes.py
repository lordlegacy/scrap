from flask import Blueprint, request, jsonify
from app.scraper import extract_text_from_url, clean_and_chunk_text


scraping = Blueprint('scraping', __name__)

@scraping.route('/scrape', methods=['POST'])
def scrape_url():
    data = request.get_json()

    if 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    scraped_text = extract_text_from_url(url)
    chunks = clean_and_chunk_text(scraped_text)


    if scraped_text:
        return chunks, 200
    else:
        return jsonify({'error': 'Failed to scrape the URL'}), 500
