# -*- coding:utf-8 -*-
# @FileName  :test_app_personal.py
# @Time      :2024/1/27 23:42
# @Author    :Daisy
import os

import allure
import pytest
from test_pre_audit import TestPreAudit
from page_object.submit_order import *
import warnings
# 忽略urllib3 重连错误
warnings.filterwarnings('ignore')

@allure.feature("APP提报信审操作")
class TestSubmitOrder:
    def setup_class(self):
        chrome_options = Options()
        # 配置为调试模式
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        time.sleep(1)
        self.driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
        self.sub = SubmitOrder(self.driver, 'Uat')  # Uat & Pre环境切换

    @allure.story("创单+预审+提报+审核")
    @pytest.mark.parametrize('cust_phone', ['13800138000'])
    @pytest.mark.smoke
    def test_appSubmit(self, cust_phone):
        self.sub.personal_order_process(cust_phone)  # 创单+预审+提报+审核

    @pytest.mark.parametrize('cust_phone', ['13800138000'])
    @pytest.mark.personalOrder
    def test_order_generate_personal(self, cust_phone):  # 创建个人预审单+预审
        self.sub.order_generate_personal(cust_phone)
        pre_audit = TestPreAudit()

    def test_submit_alone(self):  # 个人单独提报功能
        self.sub.order_submit_personal()

    @pytest.mark.parametrize('cust_phone', ['13800138000'])
    def test_order_generate_personal(self, cust_phone):  # 创建个人预审单
        self.sub.order_generate_personal(cust_phone)

    def teardown_class(self):
        self.driver.quit()


if __name__ == '__main__':
    pytest.main(
        ['-vs', '--alluredir=../temp/allure/reports', '--clean-alluredir',
         './test_app_personal.py::OrderGenerateSubmit'])  # 中间生成allure报告路径
    # os.system("allure serve ../temp/allure/reports")  # 添加allure服务，生成报告路径
