import time
from bsedata.bse import BSE
import re
import json
from datetime import datetime, timedelta
import requests
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
    response = requests.get(url, headers=headers, params=params,timeout=5)
    # 使用正则表达式解析股票代码
    stock_code = re.findall(f"{stock_name.lower()}/(.+?)/", response.text)
    # 检查是否找到股票代码
    if stock_code:
        return stock_code[0]
    else:
        return None

def get_india_dates():
    # 获取当前日期
    current_date = datetime.now()

    # 格式化当前日期为字符串
    current_date_str = current_date.strftime("%d-%m-%Y")

    # 计算30天前的日期
    thirty_days_ago = current_date - timedelta(days=30)

    # 格式化30天前的日期为字符串
    thirty_days_ago_str = thirty_days_ago.strftime("%d-%m-%Y")

    # 返回两个日期字符串
    return thirty_days_ago_str, current_date_str

def nes_market(stock_name):
    """
    获取行情
    :param stock_name: SYMBOL
    :return:
    """
    url = 'https://www.nseindia.com/api/historical/cm/equity'
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": f"https://www.nseindia.com/get-quotes/equity?symbol={stock_name}",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0",
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        data_now = get_india_dates()
        rise_time = data_now[0]
        terminal_time = data_now[1]
        params = {
            "symbol": stock_name,
            "series": '["SM","ST"]',
            "from": rise_time,
            "to": terminal_time
        }
        session = requests.Session()
        session.get(url='https://www.nseindia.com/', headers=headers, verify=False, timeout=5)
        response = session.get(url, headers=headers, params=params, timeout=5)
        unclean_data = response.json()["data"]
        clean_date_date = []
        clean_chart_data = []
        for data in unclean_data:
            clean_date_date.append(datetime.strptime(data["CH_TIMESTAMP"], "%Y-%m-%d").strftime("%Y/%m/%d"))
            clean_chart_data.append([str(data["CH_OPENING_PRICE"]), str(data["CH_CLOSING_PRICE"]), str(data["CH_TRADE_LOW_PRICE"]), str(data["CH_TRADE_HIGH_PRICE"])])
        return_data = {
            "categories": clean_date_date,
            "period": "1mo",
            "series": [
                {
                    "data": clean_chart_data,
                    "name": "Kline"
                }
            ],
            "stock": stock_name
        }
        return return_data
    except:
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
    if stock_code != None:
        # 如果获取到股票代码，调用函数获取股票历史数据
        stock_history_pre = get_bse_stock_hitory(stock_name=stock_name,stock_code=stock_code)
        return stock_history_pre
    else:
        return nes_market(stock_name=stock_name)

# def convert_date_format(date_str):
#     """
#     将给定的日期时间字符串从一种格式转换为另一种格式。
#
#     参数:
#     date_str (str): 需要转换格式的原始日期时间字符串。
#
#     返回:
#     str: 转换后的日期字符串。
#
#     说明:
#     本函数的目的是将指定的日期时间字符串从原始格式转换为目标格式。
#     原始格式包括"%a %b %d %Y %H:%M:%S"，目标格式为"%Y/%m/%d"。
#     这种转换有助于统一日期格式，以便于显示或数据库存储。
#     """
#
#     # 定义原始日期时间字符串的格式
#     original_format = "%a %b %d %Y %H:%M:%S"
#     # 定义目标日期字符串的格式
#     target_format = "%Y/%m/%d"
#
#     # 解析原始日期时间字符串为datetime对象
#     dt_object = datetime.strptime(date_str, original_format)
#
#     # 将datetime对象格式化为目标格式的字符串
#     formatted_date_str = dt_object.strftime(target_format)
#
#     return formatted_date_str



def gen_time():
    now = datetime.now()

    # 减去一个月（这里简单减去30天，不考虑月份长度或回滚）
    # 注意：这种方法可能不适用于所有情况，特别是当月份天数不同时
    one_month_ago = now - timedelta(days=30)

    # 格式化日期为日-月-年
    formatted_date = one_month_ago.strftime('%d-%m-%Y')
    return formatted_date


def get_bse_stock_hitory(stock_name, stock_code):
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Origin": "https://charting.bseindia.com",
        "Pragma": "no-cache",
        "Referer": "https://charting.bseindia.com/index.html?SYMBOL=506919",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://charting.bseindia.com/charting/RestDataProvider.svc/getDat"
    params = {
        "exch": "N",
        "scode": "506919",
        "type": "b",
        "mode": "bseL",
        "fromdate": f"{gen_time()}-01:01:00-AM"
    }
    response = requests.post(url, headers=headers, params=params)
    unclean_data = json.loads(response.json()["getDatResult"])["DataInputValues"][0]
    clean_date_date = []
    unclean_date_data = unclean_data["DateData"][0]["Date"].split(",")
    for date in unclean_date_data:
        clean_date_date.append(clean_date(date))
    clean_chart_data = []
    for i in range(len(unclean_data["OpenData"][0]["Open"].split(","))):
        clean_chart_data.append([unclean_data["OpenData"][0]["Open"].split(",")[i], unclean_data["CloseData"][0]["Close"].split(",")[i], unclean_data["LowData"][0]["Low"].split(",")[i], unclean_data["HighData"][0]["High"].split(",")[i]])
    return_data = {
            "categories": clean_date_date,
            "period": "1mo",
            "series": [
                {
                    "data": clean_chart_data,
                    "name": "Kline"
                }
            ],
            "stock": stock_name
    }
    return return_data


def clean_date(date_unclean):
    date_str = date_unclean.split()[0].replace('\/', '/')

    # 将字符串转换为datetime对象
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')

    # 将datetime对象格式化为年/月/日格式
    formatted_date_str = date_obj.strftime('%Y/%m/%d')

    return formatted_date_str


if __name__ == '__main__':
    # print(get_stock_history("POBS"))
    print(get_stockcode(stock_name="BRACEPORT"))
    pass