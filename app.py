from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import json
import requests as rq
import logging

application = Flask(__name__)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

# logging.basicConfig(level=logging.DEBUG)

def get_price(style_id):
    url = f'https://www.myntra.com/foundation-and-primer/swiss-beauty/swiss-beauty-long-lasting-makeup-fixer-natural-spray---aloe-vera-with-vitamin-e-50-ml/{style_id}/buy'
    try:
        res = rq.get(url, headers=headers)
        res.raise_for_status()
    except rq.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return 'OOS', 'OOS'
    
    # Log the response content
    # logging.debug(f"Response content for {style_id}: {res.text[:500]}")  # Log the first 500 characters
    
    soup = BeautifulSoup(res.text, 'html.parser')
    script_text = next((s.get_text(strip=True) for s in soup.find_all("script") if 'pdpData' in s.text), None)
    
    if script_text:
        try:
            data = json.loads(script_text[script_text.index('{'):])
            logging.debug(f"Extracted JSON data for {style_id}: {data}")
            mrp = data['pdpData']['price']['mrp']
            price = data['pdpData']['price']['discounted']
            return mrp, price
        except (json.JSONDecodeError, KeyError) as e:
            # logging.error(f"JSON decoding or key error: {e}")
            return 'OOS', 'OOS'
    
    # logging.error("pdpData not found in script tags")
    return 'OOS', 'OOS'

@application.route('/get_prices', methods=['GET'])
def get_prices():
    style_ids = request.args.get('style_ids').split(',')
    data = []
    for style_id in style_ids:
        mrp, price = get_price(style_id)
        data.append({'style_id': style_id, 'mrp': mrp, 'price': price})
    return jsonify(data)

if __name__ == '__main__':
    application.run('0.0.0.0', port=5000)
