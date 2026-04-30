"""
通用配置
"""
import logging
import os
import random
import time
from csv import DictReader
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage():
    def __init__(self, driver):
        self.driver = driver
        # self.driver = webdriver.Chrome()  测试用例setup里边去创建
        self.driver.maximize_window()

    def get_url(self, url):
        self.driver.get(url)

    def find_element(self, e_type, e_value):  # 查找单一元素方法
        """
        :param e_type:  xpath/id/link_text/tag
        :param e_value: xpatch value/id value
        :return:
        """
        if e_type == 'xpath':
            return self.driver.find_element(By.XPATH, e_value)
        elif e_type == 'id':
            return self.driver.find_element(By.ID, e_value)
        elif e_type == 'link_text':
            return self.driver.find_element(By.LINK_TEXT, e_value)
        elif e_type == 'partial_link_text':
            return self.driver.find_element(By.PARTIAL_LINK_TEXT, e_value)
        elif e_type == 'tag':
            return self.driver.find_element(By.TAG_NAME, e_value)

    def find_elements(self, e_type, e_value):  # 查找多元素方法
        """
        :param e_type:  xpath/id/link_text/tag
        :param e_value: xpatch value/id value
        :return:
        """
        if e_type == 'xpath':
            return self.driver.find_elements(By.XPATH, e_value)
        elif e_type == 'id':
            return self.driver.find_elements(By.ID, e_value)
        elif e_type == 'link_text':
            return self.driver.find_elements(By.LINK_TEXT, e_value)
        elif e_type == 'partial_link_text':
            return self.driver.find_elements(By.PARTIAL_LINK_TEXT, e_value)
        elif e_type == 'tag':
            return self.driver.find_elements(By.TAG_NAME, e_value)

    def find_element_by_xpath(self, element):  # 直接定义个xpath方法
        """
        :param xpath: xpath方法
        :return:
        """
        return self.find_element(By.XPATH, element)

    def find_element_by_id(self, id):  # 直接定义个ID方法
        """
        :param xpath: ID方法
        :return:
        """
        return self.find_element(By.ID, id)

    def find_element_by_css_selector(self, value):  # 直接定义个CSS_SELECTOR方法
        """
        :param xpath: ID方法
        :return:
        """
        return self.find_element(By.CSS_SELECTOR, value)

    def click_button(self, e_type, e_value, sec=3):  # 点击按钮
        """
        :param e_type: xpath/id/link_text/tag
        :param e_value: 页面元素
        :return:
        """
        self.find_element(e_type, e_value).click()
        time.sleep(sec)

    def click_button_xpath(self, e_value, sec=3):  # xpath方法点击按钮
        """
        :param e_value: 元素
        :param sec: 等待时间
        :return:
        """
        self.find_element('xpath', e_value).click()
        time.sleep(sec)

    def send_keys(self, e_type, e_value, e_keys, sec=1):
        """
        :param e_type: xpath/id/link_text/tag
        :param e_value: 页面元素
        :param e_keys:  需要输入的值
        :return:
        """
        self.find_element(e_type, e_value).send_keys(e_keys)
        time.sleep(sec)

    def send_keys_with_clear(self, e_type, e_value, e_keys):
        """
        :param e_type: xpath/id/link_text/tag
        :param e_value: 页面元素
        :param e_keys:  需要输入的值
        :return:
        """
        element = self.find_element(e_type, e_value)
        element.clear()
        element.send_keys(e_keys)

    def send_keys_with_clear_value(self, e_type, e_value, e_keys):  # 模拟键盘清空值再传
        """
        :param e_type: xpath/id/link_text/tag
        :param e_value: 页面元素
        :param e_keys:  需要输入的值
        :return:
        """
        element = self.find_element(e_type, e_value)
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(e_keys)

    def actionChains_click(self, element, secs=2):
        """
        :param element:
        :param secs: The time you want to stop
        :return:
        """
        element = element
        ActionChains(self.driver).click(element).perform()
        time.sleep(secs)

    def wait(self, sec):  # 封装一个隐式等待
        self.driver.implicitly_wait(sec)

    def quit(self):  # 退出
        self.driver.quit()

    def to_iframe(self, element):  # 封装一个进入iframe框的方法
        self.driver.switch_to.frame(element)

    def uniframe(self):  # 退出iframe
        self.driver.switch_to.default_content()
        time.sleep(1)

    def refresh(self):  # 刷新
        self.driver.refresh()

    def is_element_exist(self, e_type, e_value):  # 判断元素是否存在
        """
        :param e_type: xpath/id/link_text/tag
        :param e_value: 页面元素
        :return:
        """
        try:
            self.find_element(e_type, e_value)
            flag = True
        except NoSuchElementException:
            flag = False
        return flag

    def is_element_exist_css(self, e_value):  # 判断元素是否存在 CSS方法
        """
        :param e_type: xpath/id/link_text/tag
        :param e_value: 页面元素
        :return:
        """
        try:
            self.find_element_by_css_selector(e_value)
            flag = True
        except NoSuchElementException:
            flag = False
        return flag

    def get_element_text_by_xpath(self, xpath):  # xpath获取元素文本
        return self.driver.find_element(By.XPATH).text

    def execute_script(self, js):
        self.driver.execute_script(js)

    def save_png(self, filename):
        self.driver.get_screenshot_as_file(filename)

    def wait_until_present(self, locator, timeout=3):  #
        """等待元素出现
        locator写法例：('xpath',config['report_btn'])  方法+元素
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            print("元素在{}秒内未出现".format(timeout))
            return None

    def random_element(self, e_type, elements):  # 针对下拉框内元素进行随机返回
        """
        :param e_type: xpath/id/link_text/tag
        :param elements: 页面元素组，例如整个下拉框选项包含所有子选项集合
        :return: 随机返回元素组内一个元素
        """
        elements = self.driver.find_elements(e_type, elements)
        random_option = random.choice(elements)
        time.sleep(1)
        return random_option

    def random_name(self):  # 随便来点姓名
        chinese_surnames = ['李', '王', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴', '郑', '孙', '胡', '朱', '高', '林', '何', '许',
                            '郭', '马', '曹', '宋', '唐', '韩', '夏', '秋', '冬', '秦', '赵', '钱', '孙', '李', '周', '吴', '郑', '王',
                            '冯', '陈', '褚', '卫']
        chinese_given_names = ['伟', '静', '丽', '勇', '华', '强', '秀', '芳', '明', '燕', '杰伦', '娜美', '涛', '梅', '超', '宇', '美',
                               '帅', '媖', '婷婷', '晶晶', '慧慧', '磊']
        return random.choice(chinese_surnames) + random.choice(chinese_given_names)

    def random_company_name(self):  # 随便来点公司名
        company_types = ['科技', '网络', '信息', '软件', '传媒', '生物科技', '教育咨询', '金融服务', '智能制造', '新能源']
        prefixes = ['华夏', '中华', '中天', '新', '大', '创', '金', '绿', '蓝海', '智慧', '星辉', '海翼', '银桥', '智远', '蓝网',
                    '绿源', '金泰', '云飞', '明电', '宇宙', '安顺', '世纪', '博通', '环宇', '速达', '雷鸣', '光启', '晶能', '万联', '超界']
        suffixes = ['有限公司', '股份有限公司', '集团', '控股有限公司']
        company_type = random.choice(company_types)
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        return f'{prefix}{company_type}{suffix}'

    def random_click_element_by_js(self, random_option):
        """
        :param  通过js方法随机点击元素
        :return:
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", random_option)
        time.sleep(2)


import logging
import os
from data.path_config import log_path

class CustomLogging:
    def __init__(self, name='custom_logger', log_file=os.path.join(log_path, 'demo_log.txt'), level=logging.INFO):
        # 创建一个logger实例
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 创建一个日志文件处理器

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # 创建一个控制台输出处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # 定义日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器到logger对象
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

import warnings

class FilterWarning(logging.Filter):
    def __init__(self):
        """
        忽略重试警告
        :return:
        """
        # 忽略urllib3 重连错误
        warnings.filterwarnings('ignore')

if __name__ == '__main__':
    # driver = webdriver.Chrome()
    # # p = BasePage(driver)
    # # p.get_url('http://www.baidu.com')
    # # p.wait(10)
    # # p.send_keys('id','kw','kpmg')
    # # p.click_button('id','su')
    # # time.sleep(5)
    #
    # config = read_excel('../conf/config.xlsx', '基础配置')  # 生成器对象需要遍历查看
    # for i in config:
    #     print(i)
    # 使用示例
    custom_log = CustomLogging('demo_logging', 'demo.API_test', logging.DEBUG)
    logger = custom_log.get_logger()

    # 记录不同级别的日志信息
    logger.debug("Debugging message")
    logger.info("Informational message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
