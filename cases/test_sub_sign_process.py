# -*- coding:utf-8 -*-
# @FileName  :test_sub_sign_process.py
# @Time      :2024/4/9 11:40
# @Author    :Daisy
# @Brief Introduction    :订阅业务客户签约
import allure
import pytest
from page_object.sign_process import *
import warnings
# 忽略urllib3 重连错误
warnings.filterwarnings('ignore', message='.*connection broken by \'NewConnectionError\'')
@allure.feature("订阅业务客户签约")
class TestPreAudit:
    def setup_class(self ):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
        options.add_argument("--auto-open-devtools-for-tabs")
        self.driver = webdriver.Chrome(options=options)  # 用调试模式打开driver对象
        self.cust_phone = '13800138000'
        self.env = 'Uat'
        self.sign = SignProcess(self.driver,self.cust_phone, self.env)

    @allure.story("回租客户签约")
    def test_order_preauit(self):
        self.sign.sign_process()
        allure.attach(self.driver.get_screenshot_as_png(),  "回租签约结果截图")

    @allure.story("订阅客户签约")
    def test_order_preauit(self):
        self.sign.subscription_sign_process()
        allure.attach(self.driver.get_screenshot_as_png(),  "订阅签约结果截图")


    def teardown_class(self):
        self.driver.quit()


if __name__ == '__main__':
    pytest.main(
        ['-vs', '--alluredir=../temp/allure/reports', '--clean-alluredir', './test_sub_sign_process.py'])
    # 中间生成allure报告路径
    os.system("allure serve ../temp/allure/reports")  # 添加allure服务，生成报告路径