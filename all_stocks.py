import json
import time

import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


@app.route('/stocks', methods=['GET'])
def get_all_stocks():
    """
    获取所有股票信息

    通过发送POST请求到TradingView的API，获取印度市场的所有股票信息，并以JSON格式返回。
    """
    # 设置请求头，模拟浏览器行为和指定接受的语言
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

    # 定义API请求的URL
    url = "https://scanner.tradingview.com/india/scan"

    # 定义请求的数据，包括所需的股票信息字段和排序方式
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

    # 初始化股票列表
    stocks_list = []

    # 将请求数据转换为JSON格式
    data = json.dumps(data, separators=(',', ':'))

    # 发送POST请求并获取响应
    response = requests.post(url, headers=headers, data=data)

    # 解析响应数据，提取所需字段，并构建自定义的股票数据字典
    for stock in response.json()["data"]:
        append_data = {

            "close_prices": [
                [
                    int(time.time() * 1000),
                    stock["d"][6]
                ]
            ],
            "companyName": "MAKERS LABORATORIES LTD.-$",
            "current_price": stock["d"][6],
            "percent_change": stock["d"][12],
            "prasent": 0,
            "stock": stock["d"][1]

        }

        # 将构建的股票数据字典添加到股票列表中
        stocks_list.append(append_data)

    # 以JSON格式返回股票列表
    return jsonify(stocks_list)


if __name__ == '__main__':
    # all_stocks = get_all_stocks()
    # print(all_stocks)
    app.run(host='0.0.0.0', port=5608, debug=True)
