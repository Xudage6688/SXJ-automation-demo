# -*- coding:utf-8 -*-
# @FileName  :get_phone_code.py
# @Time      :2024/1/27 11:59
# @Author    :Daisy
import logging
import os
import requests
from data.path_config import data_path
from public.utils.readini import ReadIni

cookie_ini = os.path.join(os.path.abspath(data_path), 'cookie.ini')
data_ini = os.path.join(os.path.abspath(data_path), 'data.ini')
c = ReadIni(cookie_ini)
p = ReadIni(data_ini)
# 拿到cookie.ini里的键值对
jsession_id = c.getini('cookie 2', 'value')
acw_tc = c.getini('cookie 4', 'value')
url = p.getini('uat', 'phone_url')
headers = {
    "Content-Type": "application/json",
    "Cookie": "JSESSION=" + jsession_id + "; token=null; acw_tc=" + acw_tc + ""

}


def getCode(phone):
    response = requests.get(url + phone, headers=headers)

    # 发起HTTP请求
    try:
        response = requests.get(url + phone, headers=headers)
        response.raise_for_status()  # 若响应状态码不是200，即抛出HTTPError异常
        content = response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"登录过期，请先运行get_cookie程序: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"登录过期，请先运行get_cookie程序: {err}")
        return None

    text = str(content)
    text = text.split('}')
    start_index = text[0].find("您的短信验证码是") + len("您的短信验证码是")

    # 提取验证码
    substring = text[0][start_index:start_index + 6]
    # return substring
    # 检查是否找到code
    if substring:
        return substring
    else:
        logging.warning("No Phone Code found in the response content.")
        return None


if __name__ == '__main__':
    phone = ['13900139000','13311116666']
    numbers = getCode('13900139000')
    print(numbers)
