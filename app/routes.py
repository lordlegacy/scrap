from flask import Blueprint, request, jsonify
from app.scraper import extract_text_from_url, clean_and_chunk_text
from app.database import process_and_store_chunks, retrieve_similar_chunk

scraping = Blueprint('scraping', __name__)

@scraping.route('/scrape', methods=['POST'])
def scrape_url():
    data = request.get_json()

    if 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400

    url = data['url']
    scraped_text = extract_text_from_url(url)
    
    if scraped_text:
        chunks = clean_and_chunk_text(scraped_text)
        process_and_store_chunks(chunks, url)
        return jsonify({'message': f'Successfully processed {len(chunks)} chunks from {url}'}), 200
    else:
        return jsonify({'error': 'Failed to scrape the URL'}), 500

@scraping.route('/similar', methods=['POST'])
def find_similar_text():
    data = request.get_json()

    if 'query' not in data:
        return jsonify({'error': 'No query text provided'}), 400

    query_text = data['query']
    similar_chunk = retrieve_similar_chunk(query_text)

    if similar_chunk:
        return jsonify({
            'similar_text': similar_chunk,
            'message': 'Successfully retrieved similar text chunk'
        }), 200
    else:
        return jsonify({'error': 'No similar text found'}), 404