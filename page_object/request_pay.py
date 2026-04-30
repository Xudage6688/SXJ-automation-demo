# -*- coding:utf-8 -*-
# @FileName  :request_pay.py
# @Time      :2024/3/18 14:43
# @Author    :Daisy
# @Brief Introduction    :  请款流程
import logging
import time
from pywinauto import Desktop
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from core.basepage import BasePage, CustomLogging
from data.path_config import *
from public.utils.readini import ReadIni
from selenium.webdriver.chrome.options import Options
import warnings

# 忽略urllib3 重连错误
warnings.filterwarnings('ignore')
# 设置日志输出到本地文件以及控制台
logger = CustomLogging().get_logger()

chrome_options = Options()
# 配置为调试模式
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
time.sleep(1)

# 获取data ini配置
p = ReadIni(data_ini)
operation_btn = p.getini('ele', 'operation_btn')
cus_phone = p.getini('uat', 'cus_phone')  # uat的客户手机号
sign_submit = p.getini('ele', 'sign_submit')
other_info = p.getini('ele', 'other_info')
tax_input = p.getini('ele', 'tax_input')
date_select = p.getini('ele', 'date_select')
confirm_uniview = p.getini('ele', 'confirm_uniview')
picker_address = p.getini('ele', 'picker_address')
done_button = p.getini('ele', 'done_button')
grantor_next_step = p.getini('ele', 'grantor_next_step')
photo_uploadBtn = p.getini('ele', 'photo_uploadBtn')
reqPay_suc = p.getini('ele', 'reqPay_suc')
oder_num_ele = p.getini('ele', 'oder_num_ele')
reqPay_button = p.getini('ele', 'reqPay_button')
card_title = p.getini('ele', 'card_title')
operation_card = p.getini('ele', 'operation_card')

PHOTO_PATH = os.path.join(testData_path, '陈朋涛.jpg')


class RequestPayout(BasePage):
    def __init__(self, driver, env):
        self.driver = driver
        super().__init__(self.driver)
        if env == 'Uat':
            home_page = p.getini('uat', 'demo_app_home')
        elif env == 'Pre':
            home_page = p.getini('pre', 'demo_app_home')
        else:
            raise ValueError("Invalid env. Only 'Uat' and 'Pre' are supported.")

        self.env = env  # 存储env变量
        self.home_page = home_page  # 存储主页URL
        self.get_url(self.home_page)  # 打开请款APP页

    def upload_file(self, file_path):
        app = Desktop()
        dialog = app['打开']
        dialog["Edit"].type_keys(file_path)
        dialog["Button"].click()
        time.sleep(2)  # 确保文件选择完成

    # 获取订单编号
    def order_num_get(self):
        try:
            order_num = self.find_element_by_xpath(oder_num_ele).text
            logger.info(f"订单编号：{order_num}开始请款")

        except Exception as e:
            logger.info(f"订单编号获取失败,错误信息{e}")
            return False
        return order_num

    def request_payout(self):
        try:
            # rePay_locator = self.find_element_by_xpath(reqPay_button)
            # self.wait_until_present(rePay_locator)
            self.click_button_xpath(reqPay_button)
            self.click_button_xpath(card_title)  # 小卡片点击
            order_num = self.order_num_get()
            self.click_button('xpath', operation_card)  # 去操作
            if self.is_element_exist('xpath', other_info):
                self.click_button_xpath(other_info)  # 其他信息
                self.send_keys('xpath', tax_input, '2000')  # 发票金额
                self.click_button_xpath(date_select)  # 开票日期选择
                self.click_button_xpath(confirm_uniview)  # 确定
                self.click_button_xpath(picker_address)  # 上牌地区
                self.click_button_xpath(done_button)  # 完成
                self.click_button_xpath(grantor_next_step)  # 其他信息下一步
                photo_ele = self.find_element_by_xpath(photo_uploadBtn)
                self.actionChains_click(photo_ele)
                # 本地上传文件操作
                self.upload_file(PHOTO_PATH)
                self.click_button_xpath(grantor_next_step)  # 影像信息下一步
                self.wait(5)
                self.click_button_xpath(grantor_next_step)  # 选传信息下一步
                self.wait(5)
                self.click_button_xpath(grantor_next_step)  # 备注信息下一步
                self.click_button_xpath(sign_submit)  # 提交
                if self.find_elements('xpath', reqPay_suc):
                    logger.info(f"{order_num}请款已提交至文审")
                    return False
                else:
                    logger.info(f"当前订单{order_num}已在其他发渠道发起文审")
                    return True
            else:
                self.click_button_xpath(sign_submit)  # 提交
                if self.find_elements('xpath', reqPay_suc):
                    logger.info(f"{order_num}请款已提交至文审")
                    return True
                else:
                    logger.info(f"当前订单{order_num}已在其他发渠道发起文审")
                    return False


        except (NoSuchElementException, TimeoutException) as e:
            logger.error(f"Exception error occurred: {e}")
            return False
        except Exception as e:
            logger.info(f"订单请款提交不成功，请检查{e}")
            return False
        finally:
            self.driver.quit()  # 确保WebDriver关闭


if __name__ == '__main__':
    driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    reqpay = RequestPayout(driver, 'Pre')
    reqpay.request_payout()

    # num_of_repetitions = 1  # 设置要重复执行的次数
    # for _ in range(num_of_repetitions):
    #     driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    #     reqpay = RequestPayout(driver, 'Uat')
    #     reqpay.request_payout()
    #     # 在每次循环结束后确保关闭WebDriver
    #     reqpay.driver.quit()
    #     # 执行完所有循环后可以添加结束语句
    # print(f"已完成{num_of_repetitions}次请款流程的自动化执行")
