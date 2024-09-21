from flask import Blueprint, request, jsonify
from app.scraper import extract_text_from_url

scraping = Blueprint('scraping', __name__)

@scraping.route('/scrape', methods=['POST'])
def scrape_url():
    data = request.get_json()

    if 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    scraped_text = extract_text_from_url(url)

    if scraped_text:
        return jsonify({'scraped_text': scraped_text}), 200
    else:
        return jsonify({'error': 'Failed to scrape the URL'}), 500
