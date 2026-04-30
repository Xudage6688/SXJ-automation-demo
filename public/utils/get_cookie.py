# -*- coding:utf-8 -*-
# @FileName  :get_cookie.py
# @Time      :2024/1/27 12:03
# 获取当前登陆用户cookie，为后期实现免密登陆主页，两套环境两套cookie
# @Author    :Daisy


# -------------------------------------------------------
import os
import time
import logging

import yaml
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
from webdriver_helper import get_webdriver
from selenium.webdriver.common.by import By

from API_test.utils.yaml_util import YamlUtils
from public.utils.readini import *
from data.path_config import *
from core.basepage import CustomLogging
# 配置日志
loger = CustomLogging().get_logger()

cookie_ini = os.path.join(os.path.abspath(data_path), 'cookie.ini')
data_ini = os.path.join(os.path.abspath(data_path), 'data.ini')
pre_cookie_ini = os.path.join(os.path.abspath(data_path), 'pre_cookie.ini')
# 写入配置文件的函数
def write_config(config, path):
    try:
        with open(path, "w") as configfile:
            config.write(configfile)
            if path == cookie_ini:
                loger.info(f'UAT环境Cookie写入配置文件成功')
            else:
                loger.info(f'PRE环境Cookie写入配置文件成功')

    except Exception as e:
        loger.error(f'写入配置文件失败: {e}')


global_cookie = None


# 登录UAT环境并获取cookie的函数
def getUatCookie():
    global global_cookie
    p = ReadIni(cookie_ini)
    u = ReadIni(data_ini)
    user = u.getini('uat', 'user')  # dataini # 进行参数配置
    pwd = u.getini('uat', 'password')
    url = u.getini('uat', 'demo_loginurl')
    ele_user = u.getini('uat', 'ele_userInput')
    ele_pwd = u.getini('uat', 'ele_userPwd')
    driver = get_webdriver()
    try:
        driver.get(url)
        driver.maximize_window()

        driver.find_element(By.XPATH, ele_user).send_keys(user)
        driver.find_element(By.XPATH, ele_pwd).send_keys(pwd)

        # 手动输入验证码
        time.sleep(10)

        cookies = driver.get_cookies()
        # 格式化cookie
        global_cookie = format_cookie(cookies)
        # 写入格式化cookie到yaml文件
        replace_cookie()

        # for i, item in enumerate(cookies):
        #     section = f"cookie {i + 1}"
        #     p[section] = item
    except (NoSuchElementException, NoSuchWindowException) as e:
        logging.error(f"UI元素未找到或窗口不存在: {e}")
        driver.quit()
        return

    # write_config(p, cookie_ini)     # 写到cookie_ini文件里
    driver.quit()


# 登录PRE环境并获取cookie的函数:pre的cookie在pre_cookie.ini文件里

def getPreCookie():
    p = ReadIni(pre_cookie_ini)
    u = ReadIni(data_ini)
    user = u.getini('pre', 'user')
    pwd = u.getini('pre', 'password')
    url = u.getini('pre', 'demo_loginurl')
    ele_user = u.getini('pre', 'ele_userInput')
    ele_pwd = u.getini('pre', 'ele_userPwd')
    driver = get_webdriver()
    try:
        driver.get(url)
        driver.maximize_window()

        driver.find_element(By.XPATH, ele_user).send_keys(user)
        driver.find_element(By.XPATH, ele_pwd).send_keys(pwd)

        # 手动输入验证码
        time.sleep(8)

        cookies = driver.get_cookies()
        print(cookies)
        for i, item in enumerate(cookies):
            section = f"cookie {i + 1}"
            p[section] = item
    except (NoSuchElementException, NoSuchWindowException) as e:
        logging.error(f"UI元素未找到或窗口不存在: {e}")
        driver.quit()
        return

    write_config(p, pre_cookie_ini)
    driver.quit()


def format_cookie(cookies):
    """
    格式化输出jsession_value和acw_tc_value
    """
    jsession_value = None
    acw_tc_value = None
    # 遍历字典列表
    for cookie in cookies:
        if cookie['name'] == 'JSESSION':
            jsession_value = cookie['value']
        elif cookie['name'] == 'acw_tc':
            acw_tc_value = cookie['value']
    # 输出结果
    cookie_formatted = f"JSESSION={jsession_value}; acw_tc={acw_tc_value}"
    return cookie_formatted


read_yaml = YamlUtils(yaml_path)
yaml_content = read_yaml.read_yaml()
path = yaml_path

def replace_cookie():
    """
    递归遍历嵌套字典列表，替换yaml文件里的所有Cookie值
    """

    def recursive_replace(d, global_cookie):
        if isinstance(d, dict):
            for key, value in d.items():
                if key == 'headers' and 'Cookie' in value:
                    d[key]['Cookie'] = global_cookie
                else:
                    recursive_replace(value, global_cookie)
        elif isinstance(d, list):
            for item in d:
                recursive_replace(item, global_cookie)

    recursive_replace(yaml_content, global_cookie)

    if path is not None:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.default_flow_style = False
            yaml.dump(yaml_content, f, allow_unicode=True, encoding='utf-8')
    print('Yaml文件Cookie替换成功')


if __name__ == '__main__':
    getUatCookie()  # 获取UAT环境的cookie
    # getPreCookie()  # 获取PRE环境的cookie
