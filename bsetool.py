import json
import re
import time
from datetime import datetime

import requests
from bsedata.bse import BSE


def get_stockcode(stock_name):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.bseindia.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.bseindia.com/",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    url = "https://api.bseindia.com/Msource/1D/getQouteSearch.aspx"
    params = {
        "Type": "EQ",
        "text": stock_name,
        "flag": "site"
    }
    response = requests.get(url, headers=headers, params=params)
    stock_code = re.findall(f"{stock_name.lower()}/(.+?)/", response.text)
    if stock_code:
        return stock_code[0]
    else:
        return None


def get_stock_info_pre(stock_code):
    b = BSE(update_codes=True)
    q = b.getQuote(stock_code)
    if q:
        return q
    else:
        return None


def get_stock_current_info(stock_name):
    stock_code = get_stockcode(stock_name=stock_name)
    if stock_code:
        stock_info_pre = get_stock_info_pre(stock_code)
        stock_info = {
            "close_prices": [
                [
                    int(time.time() * 1000),
                    stock_info_pre["currentValue"]
                ]
            ],
            "companyName": stock_info_pre["companyName"],
            "current_price": stock_info_pre["currentValue"],
            "percent_change": stock_info_pre["pChange"],
            "prasent": 0,
            "stock": stock_info_pre["securityID"]
        }
        return stock_info
    else:
        return None


def get_stock_history(stock_name):
    stock_code = get_stockcode(stock_name=stock_name)
    if stock_code:
        stock_history_pre = get_stock_history_pre(stock_code)
        return stock_history_pre
    else:
        return None


def get_stock_history_pre(stock_code):
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.bseindia.com",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.bseindia.com/",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    url = "https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w"
    params = {
        "scripcode": "506919",
        "flag": "1M",
        "fromdate": "",
        "todate": "",
        "seriesid": ""
    }
    response = requests.get(url, headers=headers, params=params)
    response_json = response.json()
    time_list = []
    price_list = []
    unclean_data = response.json()["Data"]
    for data in json.loads(unclean_data):
        time_list.append(convert_date_format(data["dttm"]))
        price_list.append([data["vale1"], data["vale1"], data["vale1"], data["vale1"]])

    clean_data = {
        "categories": time_list,
        "period": "1mo",
        "series": [
            {
                "data": price_list,
                "name": "Kline"
            }
        ],
        "stock": response_json["Scripname"]
    }
    return clean_data


def convert_date_format(date_str):
    # 定义原始日期时间字符串的格式
    original_format = "%a %b %d %Y %H:%M:%S"
    # 定义目标日期字符串的格式
    target_format = "%Y/%m/%d"

    # 解析原始日期时间字符串为datetime对象
    dt_object = datetime.strptime(date_str, original_format)

    # 将datetime对象格式化为目标格式的字符串
    formatted_date_str = dt_object.strftime(target_format)

    return formatted_date_str


if __name__ == '__main__':
    print(get_stock_history("POBS"))
