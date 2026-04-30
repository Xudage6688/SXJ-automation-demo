# -*- coding:utf-8 -*-
# @FileName  :test_pre_audit.py
# @Time      :2024/3/30 14:09
# @Author    :Daisy
# @Brief Introduction    : 测试回租预审和订阅预审
import allure
import pytest
from page_object.pre_audit import *


@allure.feature("预审操作")
class TestPreAudit:

    def setup(self ):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
        # options.add_argument("--auto-open-devtools-for-tabs")
        self.driver = webdriver.Chrome(options=options)  # 用调试模式打开driver对象
        self.cust_phone = '13800138000'
        self.env = 'Uat'
        self.preaudit = PreAudit(self.driver,self.cust_phone, self.env)

    @allure.story("回租预审")
    @pytest.mark.preaudit
    def test_order_preauit(self):
        self.preaudit.personal_audit()
        assert True
    @allure.story("订阅预审")
    @pytest.mark.subscription_preaudit
    def test_order_sub_reauit(self):
        self.preaudit.subscription_preaudit()
        assert True

    def test_mainmoduel(self):
        print("test_mainmoduel模式下的测试报告")
        assert True
    def teardown(self):
        self.driver.quit()


if __name__ == '__main__':
    pytest.main(
        ['-vs', '--alluredir=../temp/allure/reports',
         '--clean-alluredir', './test_pre_audit.py::TestPreAudit::test_mainmoduel'])
    # 中间生成allure报告路径
    os.system("allure serve ../temp/allure/reports")  # 添加allure服务，生成报告路径
