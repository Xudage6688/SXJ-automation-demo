# -*- coding:utf-8 -*-
# @FileName  :cookie_to_yaml.py
# @Time      :2024/5/14 9:26
# @Author    :Daisy
# @Brief Introduction    :

import os

import yaml
from ruamel.yaml import YAML
import ruamel.yaml
from data.path_config import test_yaml_path
from API_test.utils.yaml_util import YamlUtils


def format_cookie(cookies):
    jsession_value = None
    acw_tc_value = None

    # 假设cookies是一个字典列表，每个条目包含键名和值
    # 遍历字典列表
    for cookie in cookies:
        if cookie['name'] == 'JSESSION':
            jsession_value = cookie['value']
        elif cookie['name'] == 'acw_tc':
            acw_tc_value = cookie['value']
    # 输出结果
    cookie_formatted = f"JSESSION={jsession_value}; acw_tc={acw_tc_value}"
    return cookie_formatted

    # 创建一个YAML的OrderedDict来保持顺序
    # yaml = YAML(typ='safe', pure=True)  # 初始化变量来存储找到的值
    # # 使用ruamel.yaml的safe_dump方法写入YAML文件
    # with open(test_yaml_path, 'w') as f:
    #     yaml.dump(cookie_new, f)


# 假设你已经有了cookies数据
cookies = [{'domain': 'demo-uat.company.com', 'expiry': 1715736837, 'httpOnly': False, 'name': 'token',
            'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'null'},
           {'domain': 'demo-uat.company.com', 'expiry': 1715736837, 'httpOnly': False,
            'name': 'JSESSION', 'path': '/', 'sameSite': 'Lax', 'secure': False,
            'value': 'owODctAwlZtgO0n4pCUONdp3iFvHHWggl5FcFM9z1JM='},
           {'domain': 'demo-uat.company.com', 'expiry': 1715650494, 'httpOnly': False,
            'name': 'RANDOM_CODE', 'path': '/', 'sameSite': 'Lax', 'secure': False,
            'value': '4b6319f2-a784-41e3-9a48-a7061a92a0ae'},
           {'domain': 'demo-uat.company.com', 'expiry': 1715652233, 'httpOnly': True, 'name': 'acw_tc',
            'path': '/', 'sameSite': 'Lax', 'secure': False,
            'value': '2f624a1617156504342131570e5f9d3d29c362c3df36782be234d314680af5'}]

# 调用函数写入YAML文件
# cookie_new = format_cookie(cookies)
# ------------------------------------------------------------------------------------


read_yaml = YamlUtils(test_yaml_path)
yaml_content = read_yaml.read_yaml()
#
#
# def replace_cookie_in_data(data, new_cookie):
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if key == 'headers' and 'Cookie' in value:
#                 data[key]['Cookie'] = new_cookie
#             else:
#                 replace_cookie_in_data(value, new_cookie)
#     elif isinstance(data, list):
#         for item in data:
#             replace_cookie_in_data(item, new_cookie)
#
# # cookie_new = "JSESSION=<TOKEN_PLACEHOLDER>; acw_tc=<TOKEN_PLACEHOLDER>"
# cookie_new = "JSESSION=123; acw_tc=888"
#
# # 替换所有出现的Cookie值
# for item in yaml_content:
#     replace_cookie_in_data(item, cookie_new)
#
# with open(test_yaml_path, 'w', encoding="utf-8") as f:
#     yaml.default_flow_style = False # 使用块样式而不是流动样式
#     yaml.dump(yaml_content, f)

#-----------------------------------------------------------------------

def replace_cookie(data, new_cookie, path=None):
    def recursive_replace(d, new_cookie):
        if isinstance(d, dict):
            for key, value in d.items():
                if key == 'headers' and 'Cookie' in value:
                    d[key]['Cookie'] = new_cookie
                else:
                    recursive_replace(value, new_cookie)
        elif isinstance(d, list):
            for item in d:
                recursive_replace(item, new_cookie)

    recursive_replace(data, new_cookie)

    if path is not None:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.default_flow_style = False
            yaml.dump(data, f)

# 示例使用
cookie_new = "JSESSION=sdfgbdfgsdfg; acw_tc=34634563"
replace_cookie(yaml_content, cookie_new, test_yaml_path)