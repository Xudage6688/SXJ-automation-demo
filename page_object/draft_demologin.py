# -*- coding:utf-8 -*-
# @FileName  :draft_demologin.py
# @Time      :2024/1/27 18:23
# @Author    :Daisy
"""
封装Demo融资租赁主页

"""
import time

from selenium.webdriver.common.by import By
from public.utils.get_cookie import getUatCookie
from core.basepage import BasePage

from public.utils.readini import *
from data.elements import Element as e
from data.path_config import *
p = ReadIni(data_ini)
user = p.getini('uat','user')
pwd = p.getini('uat','password')
cookie = {'domain': 'demo-uat.company.com', 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '2f624a2a17063629113358470e142f96b56b11a75867d1e021f8126a64ba8c'}
p = ReadIni(data_ini)
url = p.getini('uat', 'demo_loginurl')
class draftHome(BasePage):

    def __init__(self,driver):
        self.driver = driver
        super().__init__(self.driver)
        self.driver.get(url)    #打开Demo融资租赁主页
        driver.find_element(By.XPATH, e.ele_userInput).send_keys(user)
        driver.find_element(By.XPATH, e.ele_userPwd).send_keys(pwd)
        time.sleep(8)
        driver.find_element(By.XPATH,e.home_Query_Center).click()
        time.sleep(5)
    def pre_auditTab(self,tab):
        xpath_tab = '//span[text()="'+tab+'"]'
        self.click_button('xpath',xpath_tab)

    def sale_center(self,tab):
        xpath_tab = '//span[text()="'+tab+'"]'
        self.click_button('xpath','//div[text()=" 销售中心 "]')
        self.click_button('xpath',xpath_tab)

