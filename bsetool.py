import json
import time
from datetime import datetime
from bsedata.bse import BSE
import requests
import re

def get_stockcode(stock_name):
    """
    根据股票名称获取股票代码。

    参数:
    stock_name (str): 股票名称。

    返回:
    str 或 None: 股票代码，如果找不到则返回 None。
    """
    # 定义请求头，模拟浏览器访问
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
    # 定义请求URL
    url = "https://api.bseindia.com/Msource/1D/getQouteSearch.aspx"
    # 定义请求参数
    params = {
        "Type": "EQ",
        "text": stock_name,
        "flag": "site"
    }
    # 发送GET请求获取响应
    response = requests.get(url, headers=headers, params=params)
    # 使用正则表达式解析股票代码
    stock_code = re.findall(f"{stock_name.lower()}/(.+?)/", response.text)
    # 检查是否找到股票代码
    if stock_code:
        return stock_code[0]
    else:
        return None


def get_stock_info_pre(stock_code):
    """
    根据股票代码获取股票的预先信息。

    此函数首先更新股票代码，然后通过给定的股票代码获取相应的股票信息。
    如果找到对应代码的股票信息，则返回该信息；否则返回None。

    参数:
    stock_code (str): 要查询的股票代码。

    返回:
    dict or None: 股票信息的字典，如果未找到则返回None。
    """
    # 初始化BSE对象，用于获取股票信息，并更新股票代码
    b = BSE(update_codes=True)

    # 尝试获取给定股票代码的股票信息
    q = b.getQuote(stock_code)

    # 检查是否成功获取到股票信息
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
    """
    获取股票历史数据

    根据股票名称获取其历史数据。首先通过股票名称获取股票代码，
    如果获取到股票代码，则进一步获取该股票的历史数据；否则返回None。

    参数:
    stock_name (str): 股票名称

    返回:
    stock_history_pre (dict): 股票历史数据，如果未获取到数据则为None
    """
    # 根据股票名称获取股票代码
    stock_code = get_stockcode(stock_name=stock_name)

    # 判断是否成功获取到股票代码
    if stock_code:
        # 如果获取到股票代码，调用函数获取股票历史数据
        stock_history_pre = get_stock_history_pre(stock_code)
        return stock_history_pre
    else:
        # 如果未获取到股票代码，返回None
        return None


def get_stock_history_pre(stock_code):
    # 定义请求头，用于模拟浏览器请求
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
    # 定义请求URL
    url = "https://api.bseindia.com/BseIndiaAPI/api/StockReachGraph/w"
    # 定义请求参数，其中scripcode为股票代码，flag表示数据类型，fromdate和todate表示日期范围，seriesid为系列ID
    params = {
        "scripcode": "506919",
        "flag": "1M",
        "fromdate": "",
        "todate": "",
        "seriesid": ""
    }
    # 发送GET请求并获取响应
    response = requests.get(url, headers=headers, params=params)
    # 将响应内容转换为JSON格式
    response_json = response.json()
    # 初始化时间列表和价格列表
    time_list = []
    price_list = []
    # 获取未清洗的数据
    unclean_data = response.json()["Data"]
    # 遍历未清洗的数据，提取时间并转换格式，提取价格信息
    for data in json.loads(unclean_data):
        time_list.append(convert_date_format(data["dttm"]))
        price_list.append([data["vale1"], data["vale1"], data["vale1"], data["vale1"]])

    # 构建清洗后的数据字典，包括时间类别、周期、股票名称和价格序列
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
    # 返回清洗后的数据
    return clean_data

def test_bsedata():
    b = BSE(update_codes=True)

    # 尝试获取给定股票代码的股票信息
    stock_code = b.getQuote("POBS")
    data = b.getBhavCopyData(stock_code)
    print(data)




def convert_date_format(date_str):
    """
    将给定的日期时间字符串从一种格式转换为另一种格式。

    参数:
    date_str (str): 需要转换格式的原始日期时间字符串。

    返回:
    str: 转换后的日期字符串。

    说明:
    本函数的目的是将指定的日期时间字符串从原始格式转换为目标格式。
    原始格式包括"%a %b %d %Y %H:%M:%S"，目标格式为"%Y/%m/%d"。
    这种转换有助于统一日期格式，以便于显示或数据库存储。
    """

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
    # print(get_stock_history("POBS"))
    test_bsedata()