from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import json
import requests as rq

app = Flask(__name__)

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def get_price(style_id):
    url = f'https://www.myntra.com/foundation-and-primer/swiss-beauty/swiss-beauty-long-lasting-makeup-fixer-natural-spray---aloe-vera-with-vitamin-e-50-ml/{style_id}/buy'
    
    try:
        res = rq.get(url, headers=headers)
        res.raise_for_status()  # Check for HTTP request errors
        
        soup = BeautifulSoup(res.text, 'html.parser')
        script_text = next((s.get_text(strip=True) for s in soup.find_all("script") if 'pdpData' in s.text), None)
        
        if script_text:
            try:
                data = json.loads(script_text[script_text.index('{'):])
                mrp = data['pdpData']['price']['mrp']
                return data
            except (json.JSONDecodeError, KeyError):
                pass
        return 'OOS'
        
    except rq.RequestException:
        return 'OOS'

@app.route('/get_prices', methods=['GET'])
def get_prices():
    style_ids = request.args.get('style_ids')
    if not style_ids:
        return jsonify({'error': 'style_ids parameter is required'}), 400
    
    style_ids = style_ids.split(',')
    data = []
    for style_id in style_ids:
        mrp = get_price(style_id)
        data.append({'style_id': style_id, 'mrp': mrp})
    
    return jsonify(data)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
