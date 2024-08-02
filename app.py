# from flask import Flask, request, jsonify
# from bs4 import BeautifulSoup
# import json
# import requests as rq
# import time

# app = Flask(__name__)

# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
# }

# def get_price(style_id):
#     url = f'https://www.myntra.com/foundation-and-primer/swiss-beauty/swiss-beauty-long-lasting-makeup-fixer-natural-spray---aloe-vera-with-vitamin-e-50-ml/{style_id}/buy'
#     url_1 = 'https://proxy.scrapeops.io/v1/'
#     params={
#       'api_key': '6eb586dd-4a95-4d4c-8c73-804939bc96f0',
#       'url': url}
#     res = rq.get(url_1, params)
#     # res = rq.get(url, headers=headers)
#     soup = BeautifulSoup(res.content, 'html.parser')
    
#     script_text = next((s.get_text(strip=True) for s in soup.find_all("script") if 'pdpData' in s.text), None)
#     if script_text:
#         try:
#             data = json.loads(script_text[script_text.index('{'):])
#             mrp = data['pdpData']['price']['mrp']
#             price = data['pdpData']['price']['discounted']
#             return mrp, price
#         except (json.JSONDecodeError, KeyError):
#             pass
#     return None, None

# @app.route('/get_prices', methods=['GET'])
# def get_prices():
#     style_ids = request.args.get('style_ids').split(',')
#     data = []
#     for style_id in style_ids:
#         mrp, price = get_price(style_id)
#         data.append({'style_id': style_id, 'mrp': mrp, 'price': price})
#         time.sleep(2)
#     return jsonify(data)

# if __name__ == '__main__':
#     app.run('0.0.0.0', port=5000)






# ==================================================  NEXT CODE =======================================


from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

app = Flask(__name__)

def get_page_source(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_driver_path = "/usr/local/bin/chromedriver"
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)
    
    driver.get(url)
    time.sleep(3)
    page_source = driver.page_source
    driver.quit()
    return page_source

@app.route('/get_page_source', methods=['POST'])
def handle_get_page_source():
    data = request.get_json()
    url = data.get('url')
    source_code = get_page_source(url)
    return jsonify({'source_code': source_code})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

















