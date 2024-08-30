import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/stocks', methods=['GET'])
def get_all_stocks():
    headers = {
        "accept": "application/json",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://cn.tradingview.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://cn.tradingview.com/",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    # cookies = {
    #     "_sp_ses.cf1a": "*",
    #     "cookiePrivacyPreferenceBannerProduction": "notApplicable",
    #     "_sp_id.cf1a": "2e2692ba-fe94-481e-a1eb-f02c2d4cf52e.1724989036.1.1724989037.1724989036.7f5c19a7-73ca-4cba-90b1-7fbbe6021b75",
    #     "cookiesSettings": "{\"analytics\":true,\"advertising\":true}",
    #     "_ga": "GA1.1.1551904631.1724989037",
    #     "_ga_YVVRYGL0E0": "GS1.1.1724989036.1.0.1724989036.60.0.0"
    # }
    url = "https://scanner.tradingview.com/india/scan"
    data = {
        "columns": [
            "name",
            "description",
            "logoid",
            "update_mode",
            "type",
            "typespecs",
            "close",
            "pricescale",
            "minmov",
            "fractional",
            "minmove2",
            "currency",
            "change",
            "volume",
            "relative_volume_10d_calc",
            "market_cap_basic",
            "fundamental_currency_code",
            "price_earnings_ttm",
            "earnings_per_share_diluted_ttm",
            "earnings_per_share_diluted_yoy_growth_ttm",
            "dividends_yield_current",
            "sector.tr",
            "market",
            "sector",
            "recommendation_mark"
        ],
        "ignore_unknown_fields": False,
        "options": {
            "lang": "zh"
        },
        "range": [
            0,
            100000
        ],
        "sort": {
            "sortBy": "name",
            "sortOrder": "asc",
            "nullsFirst": False
        },
        "preset": "all_stocks"
    }
    stocks_list = []
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, headers=headers, data=data)
    for stock in response.json()["data"]:
        stocks_list.append(stock["d"][0])
    return jsonify(stocks_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5608, debug=True)
