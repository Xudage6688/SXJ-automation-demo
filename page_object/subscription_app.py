# -*- coding:utf-8 -*-
# @FileName  :subscription_app.py
# @Time      :2024/3/26 13:44
# @Author    :Daisy
# @Brief Introduction    :  订阅APP进件
# 1.用cmd：C:\Users\Xu\AppData\Local\Google\Chrome\Application\chrome.exe
# --remote-debugging-port=9222 --user-data-dir="D:\selenium\AutomationProfile\selenium"
# 打开浏览器调试模式， 目录后放selenium驱动
# 2.用调试模式启用本地数据实现免登录操作（提前登陆过金融专员APP即可）
import logging
import time
import traceback
import warnings
from pywinauto import Desktop
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, ElementNotSelectableException
from core.basepage import BasePage, CustomLogging
from data.path_config import *
from public.utils.readini import ReadIni
from selenium.webdriver.chrome.options import Options
from data.path_config import testData_path
from page_object.approve_order import ApprovalProcess
from page_object.pre_audit import PreAudit
# 忽略urllib3 重连错误
warnings.filterwarnings('ignore')

chrome_options = Options()
# 配置为调试模式
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
time.sleep(1)
# 设置日志输出到本地文件以及控制台
logger = CustomLogging().get_logger()

# 获取data ini配置
p = ReadIni(data_ini)
# 将配置项存储为字典，以提高查找效率和代码可读性
config = {
    'finance_personal': p.getini('pre', 'finance_personal'),
    'login_input': p.getini('ele', 'login_input'),
    'get_code_button': p.getini('ele', 'get_code_button'),
    'input_code': p.getini('ele', 'input_code'),
    'login_button': p.getini('ele', 'login_button'),
    'report_btn': p.getini('ele', 'report_btn'),
    'operation_btn': p.getini('ele', 'operation_btn'),
    'legal_check': p.getini('ele', 'legal_check'),
    'cus_detail': p.getini('ele', 'cus_detail'),
    'residential_address': p.getini('ele', 'residential_address'),
    'general_complete': p.getini('ele', 'general_complete'),
    'residential_detail': p.getini('ele', 'residential_detail'),
    'residence_status': p.getini('ele', 'residence_status'),
    'general_option1': p.getini('ele', 'general_option1'),
    'marriage_status': p.getini('ele', 'marriage_status'),
    'property_type': p.getini('ele', 'property_type'),
    'driving_materialsBelong': p.getini('ele', 'driving_materialsBelong'),
    'driving_materials': p.getini('ele', 'driving_materials'),
    'employment_situation': p.getini('ele', 'employment_situation'),
    'general_option2': p.getini('ele', 'general_option2'),
    'company_name': p.getini('ele', 'company_name'),
    'company_address': p.getini('ele', 'company_address'),
    'company_detailAddress': p.getini('ele', 'company_detailAddress'),
    'company_phone': p.getini('ele', 'company_phone'),
    'occupation': p.getini('ele', 'occupation'),
    'work_years': p.getini('ele', 'work_years'),
    'income': p.getini('ele', 'income'),
    'company_nature': p.getini('ele', 'company_nature'),
    'company_item': p.getini('ele', 'company_item'),
    'classification_industry': p.getini('ele', 'classification_industry'),
    'connection_timeout': p.getini('ele', 'connection_timeout'),
    'next_step': p.getini('ele', 'next_step'),
    'grantor_next_step': p.getini('ele', 'grantor_next_step'),
    'relationship_applicant': p.getini('ele', 'relationship_applicant'),
    'relationship_applicant2': p.getini('ele', 'relationship_applicant2'),
    'urgencyRelativeName': p.getini('ele', 'urgencyRelativeName'),
    'contact_name': p.getini('ele', 'contact_name'),
    'contact_name2': p.getini('ele', 'contact_name2'),
    'contact_phone': p.getini('ele', 'contact_phone'),
    'contact_phone2': p.getini('ele', 'contact_phone2'),
    'relationship_option': p.getini('ele', 'relationship_option'),
    'car_type': p.getini('ele', 'car_type'),
    'actual_price': p.getini('ele', 'actual_price'),
    'car_series': p.getini('ele', 'car_series'),
    'xc60': p.getini('ele', 'xc60'),
    'car_style': p.getini('ele', 'car_style'),
    'car1': p.getini('ele', 'car1'),
    'car_color': p.getini('ele', 'car_color'),
    'car_next': p.getini('ele', 'car_next'),
    'down_pay': p.getini('ele', 'down_pay'),
    'product_option': p.getini('ele', 'product_option'),
    'product_select': p.getini('ele', 'product_select'),
    'pre_product': p.getini('ele', 'pre_product'),
    'finance_term': p.getini('ele', 'finance_term'),
    'tail_pay': p.getini('ele', 'tail_pay'),
    'cus_rate': p.getini('ele', 'cus_rate'),
    'finance_next': p.getini('ele', 'finance_next'),
    'photo_uploadBtn': p.getini('ele', 'photo_uploadBtn'),
    'submit_btn': p.getini('ele', 'submit_btn'),
    'confirm_submit': p.getini('ele', 'confirm_submit'),
    'final_confirm': p.getini('ele', 'final_confirm'),
    'continue_ele': p.getini('ele', 'continue_ele'),
    'error_message': p.getini('ele', 'error_message'),
    'phone_approval': p.getini('ele', 'phone_approval'),
    'car_apply_city': p.getini('ele', 'car_apply_city'),
    'xian_city': p.getini('ele', 'xian_city'),
    'cust_type': p.getini('ele', 'cust_type'),
    'cust_name': p.getini('ele', 'cust_name'),
    'cust_phone': p.getini('ele', 'cust_phone'),
    'name': p.getini('ele', 'name_apply'),
    'phone': p.getini('ele', 'phone_apply'),
    'sign_next': p.getini('ele', 'sign_next'),
    'personal': p.getini('ele', 'personal'),
    'enterprise': p.getini('ele', 'enterprise'),
    'enterprise_name': p.getini('ele', 'enterprise_name'),
    'married_confirm': p.getini('ele', 'married_confirm'),
    'sign_submit': p.getini('ele', 'sign_submit'),
    'confirm': p.getini('ele', 'confirm'),
    'first_order': p.getini('ele', 'first_order'),
    'save_next_button': p.getini('ele', 'save_next_button'),
    'oder_num_ele': p.getini('ele', 'oder_num_ele')

}
driver_photo = os.path.join(testData_path, '测试驾照.jpg')  # 驾照路径

WAIT_TIME = 1

class SubscriptionApp(BasePage):
    _order_num = None  # 类级别的全局变量（类属性）

    def __init__(self, driver, env, cust_phone):
        self.driver = driver
        super().__init__(self.driver)
        if env == 'Uat':
            self.home_page = p.getini('uat', 'sub_app_generate')
        elif env == 'Pre':
            self.home_page = p.getini('pre', 'sub_app_generate')
        else:
            raise ValueError("Invalid env. Only 'Uat' and 'Pre' are supported.")
        if env == 'Uat':
            self.sub_homepage = p.getini('uat', 'sub_homepage')
        else:
            self.sub_homepage = p.getini('pre', 'sub_homepage')
        self.get_url(self.sub_homepage)
        self.get_url(self.home_page)
        self.env = env
        self.cust_phone = cust_phone

    # 发起个人订阅
    def order_generate_personal(self):  # 个人
        self.click_button_xpath(config['car_apply_city'], WAIT_TIME)
        self.click_button_xpath(config['xian_city'], WAIT_TIME)
        self.click_button_xpath(config['cust_type'], WAIT_TIME)
        self.click_button_xpath(config['personal'], WAIT_TIME)
        self.send_keys('xpath', config['cust_name'], self.random_name(), 2)
        self.send_keys('xpath', config['cust_phone'], self.cust_phone, 2)
        self.click_button_xpath(config['sign_submit'])

    # 发起企业订阅
    def order_generate_enterprise(self):  # 企业
        self.click_button_xpath(config['car_apply_city'], WAIT_TIME)
        self.click_button_xpath(config['xian_city'], WAIT_TIME)
        self.click_button_xpath(config['cust_type'], WAIT_TIME)
        self.click_button_xpath(config['enterprise'], WAIT_TIME)
        self.send_keys('xpath', config['enterprise_name'], self.random_company_name(), 2)
        self.send_keys('xpath', config['name'], self.random_name(), 2)
        self.send_keys('xpath', config['phone'], self.cust_phone, 2)  # 法人手机号
        self.click_button_xpath(config['sign_submit'])

    # 预审做完后APP提报
    def order_submit(self):  # 预审做完后app提报通用页面
        operation_btnLocator = ('xpath', config['operation_btn'])
        self.wait_until_present(operation_btnLocator)
        self.click_button('xpath', config['operation_btn'])  # 去操作
        self.click_button('xpath', config['save_next_button'])  # 保存下一步 客户信息
        self.click_button('xpath', config['save_next_button'])  # 保存下一步 产品信息
        self.click_button('xpath', config['sign_submit'])  # 影像信息 提交
        self.click_button('xpath', config['confirm'], 5)  # 确认

    def order_num_get(self):
        global order_num
        try:  # 点第一个订单小卡片进去获取订单号
            self.click_button_xpath(config['first_order'])
            order_num = self.find_element_by_xpath(config['oder_num_ele']).text
            logging.info(f"订单编号：{order_num}")
        except:
            logging.info(f"订单编号：{order_num}正在提报中，请稍等")

    def upload_file(self, file_path):
        try:
            app = Desktop()
            dialog = app['打开']
            dialog["Edit"].type_keys(file_path)
            time.sleep(2)
            dialog["Button"].click()
        except Exception as e:
            logger.error(f"上传文件失败: {e}")
            return False
        time.sleep(3)  # 确保文件选择完成

    # 个人APP发起订阅流程
    def order_submit_personal(self):  # 个人APP发起订阅流程
        try:
            car_city_selection = ('xpath', config['car_apply_city'])
            self.wait_until_present(car_city_selection)
            # APP创单
            self.order_generate_personal()
            if self.is_element_exist('xpath', config['confirm']):
                logger.info("提交成功,自动开始预审流程")
                self.click_button_xpath(config['confirm'])
                self.order_num_get()
                options = webdriver.ChromeOptions()
                options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
                options.add_argument("--auto-open-devtools-for-tabs")
                driver = webdriver.Chrome(options=options)
                app = PreAudit(driver, self.cust_phone, self.env)  # 客户手机号+环境
                app.subscription_preaudit()  # 客户预审+信息提报
                #  APP提报
                self.get_url(self.sub_homepage)
                self.order_submit()
                if self.is_element_exist('xpath', config['oder_num_ele']):
                    self.order_num_get()
                    logger.info(f"{order_num}已提报成功")
                    return True
                else:
                    logger.error('提报失败',traceback.print_exc())
                    return False
            else:
                logger.error("提交失败", traceback.print_exc())
                return False

        except (NoSuchElementException, TimeoutException, ElementNotSelectableException) as e:
            logging.error(f"加载元素失败：{e}")
            return False
        except Exception as e:
            logging.error(f"发生异常：{e}")
            return False
        finally:
            # 信审流程 不希望走信审流程注释下面两行
            app = ApprovalProcess(self.driver, self.env)
            app.approve_process(order_num)
            logging.info('提报结束')
            self.driver.quit()  # 确保WebDriver关闭

    # 企业APP发起订阅流程
    def order_submit_enterprise(self):  # 企业APP发起订阅流程
        try:
            car_city_selection = ('xpath', config['car_apply_city'])
            self.wait_until_present(car_city_selection)
            # APP创单
            self.order_generate_enterprise()
            if self.is_element_exist('xpath', config['confirm']):
                logger.info("提交成功,自动开始预审流程")
                self.click_button_xpath(config['confirm'])
                self.order_num_get()
                options = webdriver.ChromeOptions()
                options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
                options.add_argument("--auto-open-devtools-for-tabs")
                driver = webdriver.Chrome(options=options)
                # 订阅预审操作
                app = PreAudit(driver, self.cust_phone, self.env)  # 客户手机号+环境
                # 订阅提报操作
                app.subscription_preaudit()  # 客户预审+信息提报
                self.get_url(self.sub_homepage)
                logger.info(f"{order_num}已提报成功")
                # 走APP提报流，目前都是第一步没有修改内容
                self.order_submit()
                if self.is_element_exist('xpath', config['oder_num_ele']):
                    self.order_num_get()
                    print(f"{order_num}已提报成功")
                    return True
                else:
                    print(f"{order_num}提报失败")
                    return False
            else:
                logger.error(f"{order_num}提报失败", traceback.print_exc())
                return False
        except (NoSuchElementException, TimeoutException, ElementNotSelectableException) as e:
            logging.error(f"加载元素失败：{e}")
            return False
        except Exception as e:
            logging.error(f"发生异常：{e}")
            return False
        finally:
            # 信审流程 不希望走信审流程注释下面两行
            app = ApprovalProcess(self.driver, self.env)
            app.approve_process(order_num)
            logging.info(f'{order_num}提报结束')
            self.driver.quit()  # 确保WebDriver关闭


if __name__ == '__main__':
    driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    sub = SubscriptionApp(driver, 'Pre', '13800138000')  # Uat & Pre环境切换+客户手机号
    sub.order_submit_personal()  # APP创单个人单到客户授权到APP提交
    # sub.order_submit_enterprise()  # APP创单企业单到客户授权到APP提交
    # sub.order_submit()  # 单纯提报提交订阅单

    # # 重复提报
    # num_of_repetitions = 10  # 设置要重复执行的次数
    #
    # for _ in range(num_of_repetitions):
    #     driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    #     sub = SubscriptionApp(driver, 'Uat', '13800138000')  # Uat & Pre环境切换+客户手机号
    #     result = sub.order_submit_personal()  # APP创单到客户授权到APP提交
    #     # 可在此处根据result添加判断逻辑或日志记录
    #     if result:
    #         logging.info("执行成功")
    #     else:
    #         logging.warning("执行失败")
    #
    #     # 在每次循环结束后确保关闭WebDriver
    #     sub.driver.quit()
    #
    # # 执行完所有循环后可以添加结束语句
    # logging.info(f"已完成{num_of_repetitions}次提报流程的自动化执行")
