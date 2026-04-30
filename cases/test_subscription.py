import os
import unittest
from HTMLTestRunnerNew import HTMLTestRunner
from time import strftime
from unittest import TestCase
from data.path_config import reports_path
import allure
import warnings

# 忽略urllib3 重连错误
warnings.filterwarnings('ignore', message='.*connection broken by \'NewConnectionError\'')
from page_object.subscription_app import SubscriptionApp, Options, time, webdriver
from page_object.pre_audit import PreAudit


@allure.feature("APP请阅业务")
class TestSubscriptionApp(TestCase):
    def setUp(self):
        chrome_options = Options()
        # 配置为调试模式
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        time.sleep(1)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.env = 'Uat'
        self.cust_phone = '13800138000'
        self.subscription_app = SubscriptionApp(self.driver, self.env, self.cust_phone)

    def tearDown(self):
        self.driver.quit()

    def test01_order_generate_personal(self):  # 个人订阅单生成
        """
        测试个人订阅单订单生成
        """
        self.subscription_app.order_generate_personal()
        # Add assertions to verify the expected behavior
        assert self.subscription_app.is_element_exist('xpath', '//uni-view[text()="提交成功！请联系客户接收短信，填写信息并做信息授权"]')

    def test02_subscription_preaudit(self):  # 订阅预审
        """
        测试个人订阅单预审及信息填报
        """
        options = webdriver.ChromeOptions()
        options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
        driver = webdriver.Chrome(options=options)
        app = PreAudit(driver, '13800138000', 'Uat')  # 客户手机号+环境
        app.subscription_preaudit()  # 订阅
        time.sleep(2)
        driver.quit()
        assert True
    @unittest.skip('手动跳过')
    def test_order_generate_enterprise(self):  # 企业订阅单生成
        """
        测试企业订阅单订单生成
        """
        self.subscription_app.order_generate_enterprise()
        assert self.subscription_app.is_element_exist('xpath', '//uni-view[text()="提交成功！请联系客户接收短信，填写信息并做信息授权"]')

    def test03_order_submit_personal(self):  # 个人创单预审到待签约
        """
        测试个人创单预审到待签约
        """
        self.subscription_app.order_submit_personal()
        assert True

    def test04_order_submit_enterprise(self):  # 企业创单预审到待签约
        """
        测试企业创单预审到待签约
        """
        self.subscription_app.order_submit_enterprise()
        assert True



if __name__ == '__main__':
    # 第一种运行方式
    # unittest.main()
    # 第二种 通过测试套件
    suite = unittest.TestSuite()
    cases = unittest.defaultTestLoader.discover(os.getcwd(), "test_subscription.py")
    suite.addTests(cases)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # 生成测试报告的路径
    now = strftime('%Y-%m-%d-%H-%M-%S')
    filename = reports_path + '\\' + now + '_report.html'
    f = open(filename, 'wb')
    runner = HTMLTestRunner(stream=f,
                            title='订阅单测试报告',
                            description='po框架用例运行情况如下',
                            tester='Daisy'
                            )
    runner.run(suite)