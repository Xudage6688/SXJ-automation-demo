# -*- coding:utf-8 -*-
# @FileName  :path_config.py
# @Time      :2024/1/27 12:57
# @Author    :Daisy
"""
此模块存放各个包路径
"""
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 根目录

cases_path = os.path.join(path, 'cases')  # 测试用例目录

core_path = os.path.join(path, 'core')  # core目录

data_path = os.path.join(path, 'data')  # 数据目录

data_ini = os.path.join(os.path.abspath(data_path), 'data.ini')

cookie_ini = os.path.join(os.path.abspath(data_path), 'cookie.ini')

pathConfig_path = os.path.join(path, 'path_config')  # 路径目录

utils_path = os.path.join(path, 'public', 'utils')  # utils目录

DEMO_path = os.path.join(path, 'DEMO_Test')  # demo目录

temp_path = os.path.join(path, 'temp')  # 临时目录

reports_path = os.path.join(path, 'temp', 'allure', 'pytest_reports')  # 测试报告目录

unittest_reports_path = os.path.join(temp_path, 'unittest_reports', 'report-')  # unittest测试报告目录

testData_path = os.path.join(path, 'testData')  # 测试数据目录

log_path = os.path.join(temp_path, 'log')  # log目录

test_path = os.path.join(path, 'test')  # test 目录

test_yaml_path = os.path.join(os.path.abspath(test_path), 'test.yaml')

api_path = os.path.join(path, 'API_test')

yaml_path_api = os.path.join(api_path, 'test_cases')  # yaml api目录

yaml_path = os.path.join(os.path.abspath(yaml_path_api), 'demo_api.yaml')
