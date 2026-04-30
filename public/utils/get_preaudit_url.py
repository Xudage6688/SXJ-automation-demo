# -*- coding:utf-8 -*-
# @FileName  :get_preaudit_url.py
# @Time      :2024/2/2 16:33
# @Author    :Daisy
# @Brief Introduction:获取手机号预审链接
import os
import re
import requests
import logging

from data.path_config import data_path
from public.utils.readini import ReadIni

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_UatPreaudit_url(phone):
    # 配置文件路径
    cookie_ini = os.path.join(data_path, 'cookie.ini')
    data_ini = os.path.join(data_path, 'data.ini')

    # 读取配置文件
    p = ReadIni(data_ini)
    c = ReadIni(cookie_ini)
    jsession_id = c.getini('cookie 2', 'value')
    acw_tc = c.getini('cookie 4', 'value')

    # 构建请求URL和Headers
    url = p.getini('uat', 'phone_url')
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"JSESSION={jsession_id}; token=null; acw_tc={acw_tc}"
    }

    # 发起HTTP请求
    try:
        response = requests.get(url+phone, headers=headers)
        response.raise_for_status()  # 若响应状态码不是200，即抛出HTTPError异常
        content = response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"登录过期，请先运行get_cookie程序: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"登录过期，请先运行get_cookie程序: {err}")
        return None

    # 解析响应内容
    text = str(content)
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    # print(links)
    # 检查是否找到URL
    if links:
        return links[0]
    else:
        logging.warning("No URL found in the response content.")
        return None

def get_PrePreaudit_url(phone):
    # 配置文件路径
    pre_cookie_ini = os.path.join(data_path, 'pre_cookie.ini')
    data_ini = os.path.join(data_path, 'data.ini')

    # 读取配置文件
    p = ReadIni(data_ini)
    c = ReadIni(pre_cookie_ini)
    jsession_id = c.getini('cookie 2', 'value')
    acw_tc = c.getini('cookie 4', 'value')

    # 构建请求URL和Headers
    url = p.getini('pre', 'phone_url')
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"JSESSION={jsession_id}; token=null; acw_tc={acw_tc}"
    }

    # 发起HTTP请求
    try:
        response = requests.get(url+phone, headers=headers)
        response.raise_for_status()  # 若响应状态码不是200，即抛出HTTPError异常
        content = response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"登录过期，请先运行get_cookie程序: {http_err}")
        return None
    except requests.exceptions.RequestException as err:
        logging.error(f"登录过期，请先运行get_cookie程序: {err}")
        return None

    # 解析响应内容
    text = str(content)
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)

    # 检查是否找到URL
    if links:
        return links[0]
    else:
        logging.warning("No URL found in the response content.")
        return None


if __name__ == '__main__':
    get_UatPreaudit_url('13800138000')  # 客户手机号
    url = get_UatPreaudit_url('13800138000')  # 客户手机号
    print(url)
    # get_PrePreaudit_url('18129999999')  # 客户手机号

