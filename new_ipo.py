import logging
import re
import time
from datetime import datetime
from lxml import etree, html
import pandas as pd
import requests

def construct_data(ipo_record):
    """
    构建要提交的数据。
    :param ipo_record: 单条 IPO 数据记录
    :return: 构建好的数据字典
    """
    try:
        return {
            "companyName": ipo_record.get("companyName", ""),
            "issueEndDate": ipo_record.get("issueEndDate", ""),
            "issueSize": ipo_record.get("issueSize", ""),
            "issuePrice": ipo_record.get("issuePrice", ""),
            "issueStartDate": ipo_record.get("issueStartDate", ""),
            "series": ipo_record.get("series", ""),
            "sr_no": int(ipo_record.get("sr_no", 0)),
            "status": ipo_record.get("status", ""),
            "symbol": ipo_record.get("symbol", ""),
            "key": "4141880081DCFED05F353030B3ACC78F69FE254"
        }
    except Exception as e:
        logging.error(f"构建数据时发生错误: {e}")
        return {}

def generate_symbol_from_name(company_name):
    # Extract the first part of the company name and convert it to uppercase
    # This assumes the first word or phrase is sufficient for the symbol
    normalized_name = re.sub(r"[^A-Za-z0-9\s]", "", company_name)  # Remove non-alphanumeric characters except space
    parts = normalized_name.split()
    if parts:
        symbol = parts[0].upper()  # Take the first part and convert to uppercase
    else:
        symbol = company_name[:4].upper()  # Fallback if no parts found

    return symbol
def process_data(data):
    for entry in data:
        if "symbol" not in entry or not entry["symbol"]:
            entry["symbol"] = generate_symbol_from_name(entry["companyName"])
    return data

def nseindia_all_ipo():
    """
    即将发行的股票
    :return:
    """
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.nseindia.com/market-data/all-upcoming-issues-ipo',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
    }
    params = {
        'category': 'ipo',
    }
    session = requests.Session()
    session.get(url='https://www.nseindia.com/', headers=headers)
    response = session.get('https://www.nseindia.com/api/all-upcoming-issues', params=params,
                            headers=headers).json()
    return response


def nseindia_ipo():
    """
    现在发行的股票
    :return:
    """
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': '_ga=GA1.1.1473576843.1720061795; nsit=QrD_fubfYRar5sPaL-N_kdd8; _abck=B8FA317C7DA408AE9FE4AE65328B0E6F~0~YAAQUGDQF9ulmpuQAQAAZLNknwwKcj6+utPpTiKTAINpil5nWlAGY9G+8YF2SfnAx9ynMWzUlQpXIRFbocVvBtvMPuqzhYLmU4QhNNQ6SJ68z16STU5HB2hV3ertNULZWTj8Cd+IQgPp2PcOMXUAb5GyTRnQ3ccnDnV4nHipeS5UzoiiqW876XNKvk/ax7H8zoS09p/qYJxx+7gh50J8Xeqn38pRNMVMfo2oYcdwwzUytWt+BVpeB8italQOtdGBgQzDa74VfLiCYhaoh2H3Sv3xnSBubNN/bcZIEOhHN9k/EElL5sT5pbB1Mu9Af9LFT5wpApFKH1vp2+BD+8xlSuGYlhJE4zTGlGQRw1VvICYYmFrMec84Ex/QUnzm+oDRKyScBCtI6iAQuxzV6fb44nXB6QYQhCTA2Od2~-1~-1~-1; defaultLang=en; ak_bmsc=1C7E98DF4F7686C7AC2BC690DD092C9F~000000000000000000000000000000~YAAQUGDQF3SnmpuQAQAAqbpknxgRaiPTFcMtF+AkQJNP3IGGQcoziuXPL7qdBmASMJNOFSHJMg9uOk7tJt/1iFyZk5UY+088hoANVccBXuI4iaU2VbOzDFCwkV3jr5HSapFYC+aPd5pmHPrqfMpRZ87AqWcVOLXkW04mmB7cgIvkbNConmRBp/4Bqf/xvFA1YSpQckpIr+it3/aSVO9s2ZcC5sbzFoJ2sKMhczdTyI6NlYqZ8WvIcPbNyJd+kDekc3xT/RsN8r5MSScaFIO2DBneXpFcd5lf2MwhVY0z+NW0CNv0ZShR5pibYPi4wO/T6MVWYfamECFMeReEfsTTETuPmwwOmd7s0MyE1abKlhbemjeCqfqWiQcmfd4KzRYP81tLM2vRTSLvWZjkqnRxf/q+4pSNipR5EdeI1OojLrmycFMDzY5bcTbi0igDUdH4dvNB+wNDvp7la9Pkng==; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTcyMDY2NTExNSwiZXhwIjoxNzIwNjcyMzE1fQ.-Mvb1RdNQyDBTVQCJ1bh8Qh6TIMXnPyCZAmM1NDWCxc; bm_sz=DDA402FC5793CFD056917784608E140F~YAAQUGDQF+8NppuQAQAAlA6inxj64QUK3NIDs8wpAr9s8O/9vhQpDD8r8kG8qxNHjPblpYPdagm9jQxHZTG/vjUnD8QsAW+i/+sXtHjCgVVFhtHI3+UtpxkWwWNT5+y1st6HZau3a9ayUsy5aOInAkWS03glkUl4EXiWharbtHpTwEp0Udc+a8eAC21mugLiszKq/7qGi73kcS/dYR3xrH35fConSLwOyKGiONrXfHtgco9tTAU4ZB5i/bwbGsK0eF3Oo267OSUApn1/jQoYGoY3fAeQ30PpOpfaggYB7KTDvnCgONrDOfT7z1XmGk+XmHmlow9Bsc/YcFcruD97nGbhNh+0rWpFcW42+girtuCrskTamN4YYlY2AxN9XtmEqM8tRDCoiuZBAdd2Ihxp55YEDfeGCQYAxkWPxI/hwaGc/f1VzJDn23iy0c94cirkGlLSBvagag3kc6ngiqexh13GJv9V/hf+Fr8Z3GtB28rDO04=~3687492~4601140; RT="z=1&dm=nseindia.com&si=3baf6c92-35fa-4b8e-84b6-806fe51a5595&ss=lyglnzcg&sl=0&se=8c&tt=0&bcn=%2F%2F17de4c0f.akstat.io%2F"; _ga_87M7PJ3R97=GS1.1.1720665116.13.1.1720665118.58.0.0; bm_sv=3459EF8D96BA7B7168223745BB30C563~YAAQUGDQF4sPppuQAQAAPheinxiNBZx/YVu67arBubNW3+l81Ofqq7dwJ0tdcoFkU2yyVvkaUaMERs3NculIkh6awEzhu2i8lpiZrxzlsGxGZF+yiccnHx3DZshS1DTuN+bKJVGoLrPvsCk9SfCxxCRnMh3Z//aqvSELNw0YiBLesyokPnPsuFsFgx+cuq4hbSHAKxiXWVYUhkfouQepFK4FIaT8u98HYtaZqmjRNgWSiY7BDccgz75LxryTDfke1eAufg==~1',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.nseindia.com/market-data/all-upcoming-issues-ipo',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
    }
    session = requests.Session()
    session.get(url='https://www.nseindia.com/', headers=headers)
    response = session.get('https://www.nseindia.com/api/ipo-current-issue', headers=headers).json()
    return response


def get_updated_ipo_names(stock_name):
    # 获取新股列表
    nse_upcoming_ipos = nseindia_ipo()
    all_nse_ipos = nseindia_all_ipo()
    stock_name = stock_name

    # 合并所有新股列表
    all_ipos = all_nse_ipos + nse_upcoming_ipos

    # 创建公司名称到symbol的映射
    name_to_symbol = {ipo["companyName"]: ipo["symbol"] for ipo in all_ipos}

    # 更新ipo_watch_list中的公司名称和symbol
    for ipo in stock_name:
        # 查找匹配的公司名称
        matching_name = next((name for name in name_to_symbol if ipo["companyName"] in name), None)
        if matching_name:
            ipo["companyName"] = matching_name
            ipo["symbol"] = name_to_symbol[matching_name]

    return stock_name


def clean_company_names(company_data):
    # 定义要去除的多余文字的正则表达式
    keywords_to_remove = r'\b(IPO|NSE SME|BSE SME|FPO|Ltd|Co|Inc|LLC)\b'
    # try:
    for entry in company_data:
        try:
            original_name = entry['companyName']
            # 去除多余的关键词
            cleaned_name = re.sub(keywords_to_remove, '', original_name, flags=re.I).strip()
            # 修正多余的空格
            cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()
            entry['companyName'] = cleaned_name
        except TypeError:
            continue
    return company_data

def update_status(data):
    """
    status的生成规则
    :param data: 数据字典
    :return:
    """
    try:
        today = datetime.today()
        start_date = datetime.strptime(data["issueStartDate"], "%d-%b-%Y")
        end_date = datetime.strptime(data["issueEndDate"], "%d-%b-%Y")
        if today < start_date:
            data["status"] = "Forthcoming"
        elif start_date <= today <= end_date:
            data["status"] = "Active"
        else:
            data["status"] = "Closed"
        return data
    except ValueError:
        return data

def determine_series(company_name):
    # 判断 series 类型
    if "NSE SME" in company_name:
        return "SME"
    elif "BSE SME" in company_name:
        return "SME"
    elif "IPO" in company_name:
        return "EQ"
    else:
        return None

def safe_xpath_extract(xpath_expr, element, default_value=""):
    try:
        # 尝试提取 XPath 表达式的结果
        return element.xpath(xpath_expr)[0]
    except IndexError:
        # 如果出现 IndexError，则返回默认值
        return default_value

def investorgain_all():
    """
    获取Issuer Company股票信息
    :return:
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        # 'cookie': '_gid=GA1.2.1858214281.1722908614; flashcard=1; __gads=ID=5deb66321aebd28b:T=1722908610:RT=1722913893:S=ALNI_MbEpgNvVLOOi3LMypKpPRzVQ1HjQA; __gpi=UID=00000eb5051100f7:T=1722908610:RT=1722913893:S=ALNI_MYVXd4ENVL3BS1MQhuikdnD_hKFow; __eoi=ID=59e6d93546b22bc3:T=1722908610:RT=1722913893:S=AA-AfjYcBeiZ6tBqWTagOvVfAVEx; _ga_RGRD0KBG0H=GS1.1.1722913518.2.1.1722913928.0.0.0; _ga=GA1.1.979932720.1722908614',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.investorgain.com/report/live-ipo-gmp/331/current/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
    }
    response = requests.get('https://www.investorgain.com/report/live-ipo-gmp/331/current/',
                            headers=headers, verify=False)
    inv_html = etree.HTML(response.text)
    data_ty = inv_html.xpath('//*[@id="mainTable"]/tbody/tr[not(contains(@class, "fullview"))]')
    data_list = []
    for i in data_ty:
        # 获取当前年份
        current_year = datetime.today().year
        company_name = safe_xpath_extract('./td[1]//text()', i)
        issue_price = safe_xpath_extract('./td[2]//text()', i)
        issueSize = safe_xpath_extract('./td[6]//text()', i)
        issue_end_date = f"{safe_xpath_extract('./td[9]//text()', i)}-{current_year}"
        issue_start_date = f"{safe_xpath_extract('./td[8]//text()', i)}-{current_year}"
        series = determine_series(company_name)  # 假设 `determine_series` 是你的函数

        # 创建字典
        dict_s = {
            "companyName": company_name,
            "issuePrice": issue_price,
            "issueSize": issueSize,
            "issueEndDate": issue_end_date,
            "issueStartDate": issue_start_date,
            "series": series
        }
        dict_s = update_status(dict_s)
        data_list.append(dict_s)
    data_list = clean_company_names(data_list)
    return data_list


def split_issue_dates(date_range, year):
    """
    将日期范围字符串拆分为开始日期和结束日期。
    """
    try:
        # 解析日期范围
        start_day, end_day_and_month = date_range.split('-')
        end_day, month = end_day_and_month.split()

        # 创建完整的日期字符串
        start_date_str = f"{start_day} {month} {year}"
        end_date_str = f"{end_day} {month} {year}"

        # 解析日期
        start_date = datetime.strptime(start_date_str, "%d %b %Y")
        end_date = datetime.strptime(end_date_str, "%d %b %Y")

        return start_date.strftime('%d-%b-%Y'), end_date.strftime('%d-%b-%Y')
    except ValueError:
        pass


def ipowatch_upcoming():
    """
    获取Upcoming IPO的股票信息
    :return:
    """
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://ipowatch.in/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    }
    response = requests.get('https://ipowatch.in/upcoming-ipo-calendar-ipo-list/', headers=headers, verify=False)
    cur_html = etree.HTML(response.text)
    data = cur_html.xpath('//div[@data-id="1f27a874"]/div//figure')
    data_list = [['companyName', 'issueStartDate', 'series', 'issueSize', 'issuePrice']]
    for i in data:
        j = i.xpath('.//tbody/tr')
        for j_list in j:
            # 使用列表推导式过滤掉 '\xa0'
            cleaned_data_list = [item for item in j_list.xpath('.//text()') if item != '\xa0']
            data_list.append(cleaned_data_list)
    # 将数据列表转换为 DataFrame
    df = pd.DataFrame(data_list[2:], columns=data_list[0])
    # 将 DataFrame 转换为字典列表
    ipo_dict_list = df.to_dict(orient='records')
    for i in ipo_dict_list:
        # 假设当前年份
        current_year = datetime.today().year
        try:
            # 解析日期范围
            start_date, end_date = split_issue_dates(i["issueStartDate"], current_year)
            i["issueStartDate"] = start_date
            i["issueEndDate"] = end_date
            update_status(i)
        except TypeError:
            i["issueStartDate"] = i["issueStartDate"]
            i["issueEndDate"] = i["issueStartDate"]

    return ipo_dict_list

def tow_name():
    ipo_watch_list = ipowatch_upcoming()
    inv_watch_list = investorgain_all()

    # 获取更新后的 IPO 和 inv 列表
    ipo = get_updated_ipo_names(ipo_watch_list)
    inv = get_updated_ipo_names(inv_watch_list)
    # print(ipo)
    # print(inv)

    # 遍历 inv 列表的公司名称
    inv_company_names = {company["companyName"] for company in inv}

    # 从 ipo 列表中删除公司名称与 inv_company_names 匹配的条目
    ipo = [entry for entry in ipo if entry["companyName"] not in inv_company_names]

    inv = process_data(inv)

    for i in ipo:
        inv.append(i)

    return inv

def get_all_stock_codes():
    data_list_1 = tow_name()
    data_list_2 = nseindia_all_ipo()

    # print(data_list_1)
    # print(data_list_2)
    list_s = []
    # 更新主要数据列表
    for item in data_list_2:
        company_name = item.get('companyName')
        if not item.get('issuePrice') or not item.get('issueSize'):
            for extra_item in data_list_1:
                if company_name in extra_item.get('companyName'):
                    if not item.get('issuePrice'):
                        item['issuePrice'] = extra_item.get('issuePrice')
                    if not item.get('issueSize'):
                        item['issueSize'] = extra_item.get('issueSize')
        list_s.append(item)
    return list_s

def main():
    while True:
        try:
            url = "https://api.dd-pay.top/api/gather/stock/ipo"
            return_data = get_all_stock_codes()
            for i in return_data:
                result = requests.post(url=url, json=construct_data(i))
                print(result.json())
        except:
            pass
        time.sleep(60 * 60 * 3)

if __name__ == "__main__":
    main()