from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = soup.find('title').get_text() if soup.find('title') else 'No title found'
    meta_author = soup.find('meta', attrs={'name': 'author'})
    author = meta_author['content'] if meta_author else 'No author found'
    
    return jsonify({
        'title': title,
        'author': author
    })

if __name__ == '__main__':
    app.run()
