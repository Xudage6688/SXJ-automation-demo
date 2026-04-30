# -*- coding:utf-8 -*-
# @FileName  :sign_order.py
# @Time      :2024/3/8 14:02
# @Author    :Daisy
# @Brief Introduction    :Demo融资租赁签约流程
# 1.用cmd：C:\Users\Xu\AppData\Local\Google\Chrome\Application\chrome.exe
# --remote-debugging-port=9222 --user-data-dir="D:\selenium\AutomationProfile\selenium"
# 打开浏览器调试模式， 目录后放selenium驱动
# 2.用调试模式启用本地数据实现免登录操作（提前登陆过金融专员APP即可）
import logging
import re
import time
import traceback

from selenium.common import NoSuchElementException, TimeoutException, ElementNotSelectableException
from public.utils.Vin_Genarate import get_vin
from selenium import webdriver
from core.basepage import BasePage, CustomLogging
from data.path_config import *
from public.utils.readini import ReadIni
from selenium.webdriver.chrome.options import Options
from page_object.sign_process import SignProcess, options
import warnings
# 忽略urllib3 重连错误
warnings.filterwarnings('ignore')
# 设置日志输出到本地文件以及控制台
logger = CustomLogging().get_logger()



# 配置为调试模式
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
time.sleep(1)

# 获取data ini配置
p = ReadIni(data_ini)
operation_btn = p.getini('ele', 'operation_btn')
cus_phone = p.getini('uat', 'cus_phone')  # uat的客户手机号
sms_checkBox = p.getini('ele', 'sms_checkBox')
sign_cus_phone = p.getini('ele', 'sign_cus_phone')
comment_confirm = p.getini('ele', 'comment_confirm')
cus_detail = p.getini('ele', 'cus_detail')
sign_next = p.getini('ele', 'sign_next')
vin_input = p.getini('ele', 'vin_input')
finance_next = p.getini('ele', 'finance_next')
sign_finance_next = p.getini('ele', 'sign_finance_next')
sign_submit = p.getini('ele', 'sign_submit')
submit_suc = p.getini('ele', 'submit_suc')
invoice_entity = p.getini('ele', 'invoice_entity')
invoice_entity_option = p.getini('ele', 'invoice_entity_option')
payee = p.getini('ele', 'payee')
resend_sms = p.getini('ele', 'resend_sms')
agent_info = p.getini('ele', 'agent_info')
ent_repayCard = p.getini('ele', 'ent_repayCard')
ent_legal_option = p.getini('ele', 'ent_legal_option')


class SignOder(BasePage):
    def __init__(self, driver, env):
        self.driver = driver
        super().__init__(self.driver)
        if env == 'Uat':
            home_page = p.getini('uat', 'sign_url')
        elif env == 'Pre':
            home_page = p.getini('pre', 'sign_url')
        else:
            raise ValueError("Invalid env. Only 'Uat' and 'Pre' are supported.")

        self.env = env  # 存储env变量
        self.home_page = home_page  # 存储主页URL
        self.get_url(home_page)  # 打开签约APP页

    def sign_after(self):
        global extracted_phone
        self.is_element_exist('xpath', submit_suc)
        logger.info('签约已提交，开始客户签约操作')
        self.get_url(self.home_page)
        operation_btnLocator = ('xpath', operation_btn)
        self.wait_until_present(operation_btnLocator)
        self.click_button('xpath', operation_btn)  # 获取刚提交的客户手机号
        self.click_button('xpath', sms_checkBox)
        sign_cus_phone_ele = self.find_element_by_xpath(sign_cus_phone)  # 根据页面元素找到客户手机号操作
        text = sign_cus_phone_ele.text
        # 正则提取纯数字
        phone_number = re.search(r'(\d{11})', text)
        if phone_number:
            extracted_phone = phone_number.group(0)
            logger.info("客户手机号码是：", str(extracted_phone))
        else:
            logger.error("未找到手机号码", str(traceback.format_exc()))


    def start_cus_sign(self):   # 走客户签约流程
        new_driver = webdriver.Chrome(options=options)
        SignProcess(new_driver, str(extracted_phone), self.env).sign_process()  # 客户手机号签约流程操作
        logger.info(f"{str(extracted_phone)}签约已完成")

    def order_sign(self):  # 签约操作  自动输入车架号

        global extracted_phone
        try:
            operation_btnLocator = ('xpath', operation_btn)
            self.wait_until_present(operation_btnLocator)
            self.click_button('xpath', operation_btn)
            if self.is_element_exist('xpath', sms_checkBox):  # 重发短信操作是否存在，在走重发流程
                self.click_button('xpath', sms_checkBox)
                sign_cus_phone_ele = self.find_element_by_xpath(sign_cus_phone)  # 根据页面元素找到客户手机号操作
                text = sign_cus_phone_ele.text
                # 根据页面元素取得手机号操作
                phone_number = re.search(r'(\d{11})', text)
                if phone_number:
                    extracted_phone = phone_number.group(0)
                    logger.info("客户的手机号码是：", str(extracted_phone))
                else:
                    logger.info("未找到手机号码")
                self.click_button('xpath', comment_confirm)  # 确认重发短信
                logger.info(f"{str(extracted_phone)}短信已重发，自动开始客户签约流程")
                self.driver.quit()  # 退出当前driver开始签约流程
                new_driver = webdriver.Chrome(options=options)
                SignProcess(new_driver, str(extracted_phone), self.env).sign_process()  # 客户手机号签约流程操作
            else:  # 没有重发短信操作，则走正常流程
                self.click_button('xpath', cus_detail, 4)  # 客户信息
                # 企业单处理
                if self.is_element_exist('xpath', ent_repayCard):  # 还款归属人为空
                    self.click_button_xpath(ent_repayCard)
                    self.click_button_xpath(ent_legal_option)   # 法人
                    self.click_button('xpath', sign_next)  # 下一步
                    self.send_keys('xpath', vin_input, get_vin())  # 车架号
                    time.sleep(2)
                    self.click_button('xpath', finance_next)
                    self.click_button('xpath', sign_finance_next)  # 融资信息下一步
                    # 开票单位处理
                    if self.is_element_exist('xpath', payee):  # 判断是否有收款方
                        # 经销商信息处理
                        agent_name = self.find_element_by_xpath(agent_info)
                        # 使用JavaScript获取元素的值
                        value = self.driver.execute_script("return arguments[0].value;", agent_name)
                        self.send_keys('xpath', invoice_entity, value, 2)
                        time.sleep(2)
                        self.click_button_xpath(invoice_entity_option)
                        self.click_button('xpath', finance_next)  # 其他信息下一步
                        self.click_button('xpath', finance_next)  # 备注信息下一步
                        self.click_button('xpath', sign_submit)  # 提交
                    else:
                        self.click_button('xpath', finance_next)  # 其他信息下一步
                        self.click_button('xpath', finance_next)  # 备注信息下一步
                        self.click_button('xpath', sign_submit)  # 提交
                        try:
                            self.sign_after()  # 提交后提取客户手机号操作

                            self.driver.quit()  # 退出当前driver开始签约流程

                            self.start_cus_sign()  # 客户签约流程
                        except Exception as e:
                            exc_info = traceback.format_exc()
                            logger.error(f"发生异常: {str(e)}\n堆栈跟踪信息: {exc_info}")
                            return False
                else:   # 个人单
                    self.click_button('xpath', sign_next)  # 下一步
                    self.send_keys('xpath', vin_input, get_vin())  # 车架号
                    time.sleep(2)
                    self.click_button('xpath', finance_next)
                    self.click_button('xpath', sign_finance_next)  # 融资信息下一步
                    # 开票单位处理
                    if self.is_element_exist('xpath', payee):  # 判断是否有收款方
                        # 经销商信息处理
                        agent_name = self.find_element_by_xpath(agent_info)
                        # 使用JavaScript获取元素的值
                        value = self.driver.execute_script("return arguments[0].value;", agent_name)
                        self.send_keys('xpath', invoice_entity, value, 2)
                        time.sleep(2)
                        self.click_button_xpath(invoice_entity_option)
                        self.click_button('xpath', finance_next)  # 其他信息下一步
                        self.click_button('xpath', finance_next)  # 备注信息下一步
                        self.click_button('xpath', sign_submit)  # 提交

                        self.sign_after()  # 提交后提取客户手机号操作

                        self.driver.quit()  # 退出当前driver开始签约流程

                        self.start_cus_sign()   # 客户签约流程
                        return True

                    else:
                        self.click_button('xpath', finance_next)  # 其他信息下一步
                        self.click_button('xpath', finance_next)  # 备注信息下一步
                        self.click_button('xpath', sign_submit)  # 提交
                        try:
                            self.sign_after()  # 提交后提取客户手机号操作

                            self.driver.quit()  # 退出当前driver开始签约流程

                            self.start_cus_sign()  # 客户签约流程

                        except Exception as e:
                            exc_info = traceback.format_exc()
                            logger.error(f"发生异常: {str(e)}")
                            return False
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException) as e:
            logger.error(f"Exception error occurred: {str(e)}")
            return False

        finally:
            self.driver.quit()  # 确保WebDriver关闭


if __name__ == '__main__':
    driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    sign = SignOder(driver, 'Pre')  # Uat & Pre环境切换
    result = sign.order_sign()
    #
    # num_of_repetitions = 2  # 设置要重复执行的次数
    #
    # for _ in range(num_of_repetitions):
    #     driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    #     sign = SignOder(driver, 'Pre')  # Uat & Pre环境切换
    #     result = sign.order_sign()
    #
    #     # 在每次循环结束后确保关闭WebDriver
    #     sign.driver.quit()
    # # 执行完所有循环后可以添加结束语句
    # print(f"已完成{num_of_repetitions}次签约流程的自动化执行")
