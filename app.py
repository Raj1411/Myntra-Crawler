from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests as rq
import logging

app = Flask(__name__)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua-platform': 'Windows',
    'connection': 'keep-alive',
    'Referer': 'http://www.wikipedia.org/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}

def get_soup(style_id):
    url = f'https://www.myntra.com/{style_id}/buy'
    
    try:
        res = rq.get(url, headers=headers,params={'api-key':'6eb586dd-4a95-4d4c-8c73-804939bc96f0',
                                                 'url': 'https://quotes.toscrape.com/'})
        res.raise_for_status()  # Check for HTTP request errors
        
        soup = BeautifulSoup(res.text, 'html.parser')
        return str(soup)  # Convert soup to a string
        
    except rq.RequestException as e:
        logging.error(f"Error fetching data for style_id {style_id}: {e}")
        return 'OOS'

@app.route('/get_soup', methods=['GET'])
def get_soup_view():
    style_ids = request.args.get('style_ids')
    if not style_ids:
        return jsonify({'error': 'style_ids parameter is required'}), 400
    
    style_ids = style_ids.split(',')
    data = []
    for style_id in style_ids:
        soup = get_soup(style_id)
        data.append({'style_id': style_id, 'soup': soup})
    
    return jsonify(data)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run('0.0.0.0', port=5000)
