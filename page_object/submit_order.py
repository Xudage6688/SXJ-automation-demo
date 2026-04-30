# -*- coding:utf-8 -*-
# @FileName  :submit_order.py
# @Time      :2024/3/4 17:46
# @Author    :Daisy
# @Brief Introduction    :Demo融资租赁提报
# 1.用cmd：C:\Users\Xu\AppData\Local\Google\Chrome\Application\chrome.exe
# --remote-debugging-port=9222 --user-data-dir="D:\selenium\AutomationProfile\selenium"
# 打开浏览器调试模式， 目录后放selenium驱动
# 2.用调试模式启用本地数据实现免登录操作（提前登陆过金融专员APP即可）
import random
import time
from pywinauto import Desktop
from selenium import webdriver
from core.basepage import BasePage, CustomLogging
from data.path_config import *
from public.utils.readini import ReadIni
from selenium.webdriver.chrome.options import Options
from data.path_config import testData_path
from page_object.approve_order import ApprovalProcess
from page_object.pre_audit import PreAudit
import warnings
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
    'card_title': p.getini('ele', 'card_title'),
    'operation_card': p.getini('ele', 'operation_card'),
    'personal_apply': p.getini('ele', 'personal_apply'),
    'sales_select': p.getini('ele', 'sales_select'),
    'name_apply': p.getini('ele', 'name_apply'),
    'ent_submit': p.getini('ele', 'ent_submit'),
    'phone_apply': p.getini('ele', 'phone_apply'),
    'pre_submit': p.getini('ele', 'pre_submit'),
    'confirm': p.getini('ele', 'confirm'),
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
    'term_elements': p.getini('ele', 'term_elements'),
    'term_group': p.getini('ele', 'term_group'),
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
    'register_address': p.getini('ele', 'register_address'),
    'register_address_detail': p.getini('ele', 'register_address_detail'),
    'address_compare': p.getini('ele', 'address_compare'),
    'yes_option': p.getini('ele', 'yes_option'),
    'company_nature_ent': p.getini('ele', 'company_nature_ent'),
    'llc_option': p.getini('ele', 'llc_option'),
    'date_establishment': p.getini('ele', 'date_establishment'),
    'confirm_uniview': p.getini('ele', 'confirm_uniview'),
    'company_phone_ent': p.getini('ele', 'company_phone_ent'),
    'shareholding_ratio': p.getini('ele', 'shareholding_ratio'),
    'relation_applier': p.getini('ele', 'relation_applier'),
    'legal_option': p.getini('ele', 'legal_option'),
    'legal_residential_address': p.getini('ele', 'legal_residential_address'),
    'unit_name': p.getini('ele', 'unit_name'),
    'unit_phone': p.getini('ele', 'unit_phone'),
    'unit_address': p.getini('ele', 'unit_address'),
    'unit_address_detail': p.getini('ele', 'unit_address_detail'),
    'unit_type': p.getini('ele', 'unit_type'),
    'foreign_option': p.getini('ele', 'foreign_option'),
    'legal_occupation': p.getini('ele', 'legal_occupation'),
    'legal_address_detail': p.getini('ele', 'legal_address_detail'),
    'occupation_option': p.getini('ele', 'occupation_option'),
    'legal_salary': p.getini('ele', 'legal_salary'),
    'salary_option': p.getini('ele', 'salary_option'),
    'ent_contact_name': p.getini('ele', 'ent_contact_name'),
    'ent_contact_phone': p.getini('ele', 'ent_contact_phone'),
    'ent_contact2': p.getini('ele', 'ent_contact2'),
    'ent_contact2_name': p.getini('ele', 'ent_contact2_name'),
    'ent_contact2_phone': p.getini('ele', 'ent_contact2_phone'),
    'ent_photo': p.getini('ele', 'ent_photo'),
    'enter_apply': p.getini('ele', 'enter_apply'),
    'legal_name': p.getini('ele', 'legal_name'),
    'legal_phone': p.getini('ele', 'legal_phone'),
    'company_name_apply': p.getini('ele', 'company_name_apply'),
    'ent_contact1': p.getini('ele', 'ent_contact1'),
    'ent_driver_photo': p.getini('ele', 'ent_driver_photo'),
    'ent_continue_ele': p.getini('ele', 'ent_continue_ele'),
    'sales_option_sichuan': p.getini('ele', 'sales_option_sichuan'),
    'sales_option_chongqing': p.getini('ele', 'sales_option_chongqing'),
    'oder_num_ele': p.getini('ele', 'oder_num_ele')

}
driver_photo = os.path.join(testData_path, '测试驾照.jpg')  # 驾照路径
license_photo = os.path.join(testData_path, '营业执照2.jpg')  # 驾照路径
log_file_path = os.path.join('log_path', 'demo.log')


class SubmitOrder(BasePage):
    _order_num = None  # 类级别的全局变量（类属性）

    def __init__(self, driver, env):
        self.driver = driver
        super().__init__(self.driver)
        if env == 'Uat':
            self.home_page = p.getini('uat', 'demo_app_home')
        elif env == 'Pre':
            self.home_page = p.getini('pre', 'demo_app_home')

        else:
            raise ValueError("Invalid env. Only 'Uat' and 'Pre' are supported.")
        self.get_url(self.home_page)
        self.env = env

    # 获取订单编号
    def order_num_get(self):
        global order_num
        try:
            order_num = self.find_element_by_xpath(config['oder_num_ele']).text
            logger.info(f"订单编号：{order_num} 开始提报")

        except:
            logger.info(f"订单编号获取失败")
            return False

    # 上传文件操作
    def upload_file(self, file_path):
        try:
            app = Desktop()
            dialog = app['打开']
            dialog["Edit"].type_keys(file_path)
            time.sleep(2)
            dialog["Button"].click()
        except Exception as e:
            print(f"上传文件失败: {e}")
            return False
        time.sleep(3)  # 确保文件选择完成

    # 个人申请输入
    def applyer_info_input(self):
        self.click_button('xpath', config['residential_address'])  # 居住地址
        self.click_button('xpath', config['general_complete'])  # 通用完成选项1
        self.send_keys_with_clear('xpath', config['residential_detail'], '测试详细地址')  # 居住详细地址
        self.click_button('xpath', config['residence_status'], 1)  # 居住状况
        self.click_button('xpath', config['general_option1'], 1)  # 通用选项
        self.click_button('xpath', config['marriage_status'], 1)  # 婚姻状况
        self.click_button('xpath', config['general_option1'], 1)  # 通用选项
        self.click_button('xpath', config['property_type'], 1)  # 房产类型
        self.click_button('xpath', config['general_option1'], 1)  # 通用选项
        self.click_button('xpath', config['driving_materialsBelong'], 1)  # 驾照归属
        self.click_button('xpath', config['general_option1'], 1)  # 通用选项
        self.click_button('xpath', config['driving_materials'], 1)  # 驾照
        self.click_button('xpath', config['general_option1'], 1)  # 通用选项
        self.click_button('xpath', config['employment_situation'], 1)  # 就业状况
        self.click_button('xpath', config['general_option2'], 1)  # 通用选项2
        self.send_keys_with_clear_value('xpath', config['company_name'], '测试单位')  # 单位名称
        time.sleep(2)
        self.click_button('xpath', config['company_item'], 1)
        self.click_button('xpath', config['company_address'], 1)  # 单位地址
        self.click_button('xpath', config['general_complete'], 1)  # 通用完成选项1
        self.send_keys_with_clear('xpath', config['company_detailAddress'], '测试单位详细地址')  # 单位详细地址
        self.send_keys_with_clear('xpath', config['company_phone'], '6802105')  # 单位电话
        self.click_button('xpath', config['occupation'], 1)  # 职业
        self.click_button('xpath', config['general_option2'], 1)  # 通用选项2
        self.send_keys('xpath', config['work_years'], '5', 2)  # 工作年限
        self.click_button('xpath', config['income'], 1)  # 收入
        self.click_button('xpath', config['general_option2'], 1)  # 通用选项2
        self.click_button('xpath', config['company_nature'])  # 单位性质
        self.click_button('xpath', config['general_option1'], 1)  # 通用选项
        self.click_button('xpath', config['classification_industry'], 1)  # 行业分类
        self.click_button('xpath', config['general_option1'], 1)  # 通用选项
        self.wait(5)

    # 联系人输入
    def contact_info_input(self):
        self.click_button('xpath', config['relationship_applicant'])  # 与申请人关系
        self.click_button('xpath', config['relationship_option'])  # 父母
        self.send_keys('xpath', config['contact_name'], '父母1')
        self.send_keys('xpath', config['contact_phone'], '13311112222')
        self.click_button('xpath', config['relationship_applicant2'])  # 与申请人关系
        self.click_button('xpath', config['relationship_option'])  # 父母
        self.send_keys('xpath', config['contact_name2'], '父母2')
        self.send_keys('xpath', config['contact_phone2'], '13311113333')
        time.sleep(2)

    # 车辆信息录入
    def car_info_input(self):
        car_type_locator = ('xpath', config['car_type'])
        self.wait_until_present(car_type_locator)
        self.click_button('xpath', config['car_type'])  # 车辆类型
        self.click_button('xpath', config['general_option1'])  # 新车
        self.click_button('xpath', config['car_series'])  # 车系
        self.click_button('xpath', config['xc60'])  # xc60
        self.click_button('xpath', config['car_style'])  # 车型
        self.click_button('xpath', config['car1'])  # 第一款车
        self.send_keys_with_clear_value('xpath', config['actual_price'], random.randint(300000, 400000))
        self.send_keys_with_clear_value('xpath', config['car_color'], '黑')
        time.sleep(2)

    # 产品信息录入
    def product_info_input(self):
        self.click_button('xpath', config['product_option'])  # 产品信息
        if self.env == 'Uat':
            self.click_button('xpath', config['product_select'], 5)  # 自营产品无尾付
        else:
            self.click_button('xpath', config['pre_product'], 5)  # 自营产品无尾付
        self.click_button('xpath', config['finance_term'])  # 融资期限
        self.random_element('xpath', config['term_group']).click()  # 随机期数
        # self.click_button('xpath', config['general_option1'])  # 第一个期数
        # self.click_button('xpath',cus_rate)#客户利率
        # self.click_button('xpath',general_option1)#第一个利率
        self.send_keys('xpath', config['down_pay'], random.randint(100000, 200000), 1)  # 首付金额
        time.sleep(3)

    # 创建个人预审单
    def order_generate_personal(self, cus_phone):  # 创建个人预审单
        personal_apply_btnLocator = ('xpath', config['personal_apply'])
        self.wait_until_present(personal_apply_btnLocator)
        self.click_button_xpath(config['personal_apply'])
        self.click_button_xpath(config['sales_select'])  # 经销商
        self.click_button_xpath(config['sales_option_sichuan'])
        self.send_keys('xpath', config['name_apply'], self.random_name())
        self.send_keys('xpath', config['phone_apply'], cus_phone)
        self.click_button_xpath(config['pre_submit'])
        self.click_button_xpath(config['confirm'])

    # 提交操作
    def submit_handler(self):  # 不想提报提交可注释该方法
        self.click_button('xpath', config['submit_btn'])  # 提交
        self.click_button('xpath', config['confirm_submit'])  # 确认提交
        self.click_button('xpath', config['final_confirm'], 5)  # 确认
        time.sleep(3)
        logger.info(f'{order_num} 提报完成')

    # 个人APP提报去操作
    def order_submit_personal(self):  # 个人提报流程
        self.get_url(self.home_page)
        report_btnLocator = ('xpath', config['report_btn'])
        self.wait_until_present(report_btnLocator)
        self.click_button('xpath', config['report_btn'])  # 提报按钮
        self.click_button('xpath', config['card_title'])  # 小卡片点击
        self.order_num_get()
        self.click_button('xpath', config['operation_card'])  # 去操作
        self.click_button('xpath', config['cus_detail'])  # 客户信息
        if self.is_element_exist('xpath', config['connection_timeout']):
            self.refresh()
        elif self.is_element_exist('xpath', config['legal_check']):  # 企业单处理
            logger.info("企业单请先做法人征信授权")
            return False
        else:
            self.applyer_info_input()  # 申请人信息填写
            self.click_button('xpath', config['next_step'], 4)  # 下一步
            self.click_button('xpath', config['next_step'], 4)  # 联系人下一步触发报错
            if self.is_element_exist('xpath', config['error_message']):  # 判断是否有联系人报错
                self.contact_info_input()  # 联系人信息填写
                self.click_button('xpath', config['next_step'], 4)  # 联系人下一步
                garantor_btnLocator = ('xpath', config['grantor_next_step'])
                self.wait_until_present(garantor_btnLocator)
                self.click_button('xpath', config['grantor_next_step'])  # 担保人下一步
            else:  # 无填写联系就下一步到担保人
                garantor_btnLocator = ('xpath', config['grantor_next_step'])
                self.wait_until_present(garantor_btnLocator)
                self.click_button('xpath', config['grantor_next_step'])  # 担保人下一步
            # 车辆信息填写
            self.car_info_input()
            self.click_button('xpath', config['car_next'])  # 车辆信息下一步
            # 产品信息填写
            self.product_info_input()
            self.click_button('xpath', config['finance_next'])  # 融资信息下一步
            # 影像信息信息处理
            if self.is_element_exist('xpath', config['continue_ele']):  # 针对已有影像信息，直接跳过流程
                self.enterprise_submit_handle()
                logger.info(f'{order_num} 提报填写结束')
            else:
                photo_ele = self.find_element_by_xpath(config['photo_uploadBtn'])  # 没有就上传
                self.actionChains_click(photo_ele)
                # 本地上传文件操作
                self.upload_file(driver_photo)
                self.enterprise_submit_handle()
                logger.info(f'{order_num} 提报填写结束')

    # 从创单到预审到提报提交到信审
    def personal_order_process(self, cus_phone):
        try:
            self.order_generate_personal(cus_phone)
            options = webdriver.ChromeOptions()
            options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
            # options.add_argument("--auto-open-devtools-for-tabs")
            driver = webdriver.Chrome(options=options)
            app = PreAudit(driver, cus_phone, self.env)  # 客户手机号+环境
            app.personal_audit()
            self.order_submit_personal()
            # # 提交流程
            self.submit_handler()
            # # 信审流程
            app = ApprovalProcess(self.driver, self.env)
            app.approve_process(order_num)
        except Exception as e:
            logger.error(f"发生异常：{e}")

        finally:
            self.driver.quit()

    # ----------------------------------企业单分割----------------------------------------

    # 企业创单
    def order_generate_enterprise(self, cus_phone):
        enterprise_apply_btnLocator = ('xpath', config['enter_apply'])
        self.wait_until_present(enterprise_apply_btnLocator)
        self.click_button_xpath(config['enter_apply'])
        self.click_button_xpath(config['sales_select'])  # 经销商
        self.click_button_xpath(config['sales_option_chongqing'])
        self.send_keys('xpath', config['legal_name'], self.random_name())
        self.send_keys('xpath', config['legal_phone'], cus_phone)
        self.send_keys('xpath', config['company_name_apply'], self.random_company_name())
        self.click_button_xpath(config['pre_submit'])
        self.click_button_xpath(config['confirm'])

    # 企业信息填写
    def enterprise_info_input(self):
        self.click_button('xpath', config['register_address'], 1)  # 注册地
        self.click_button('xpath', config['general_complete'], 1)  # 通用完成按钮
        self.send_keys('xpath', config['register_address_detail'], '企业详细地址')  # 企业注册详细地址
        if self.is_element_exist('xpath', config['address_compare']):
            self.click_button_xpath(config['address_compare'], 1)  # 经营地址与营业执照是否一致
            self.click_button_xpath(config['yes_option'], 1)  # 是
            self.click_button_xpath(config['company_nature_ent'], 1)  # 企业性质
            self.click_button_xpath(config['llc_option'], 1)  # 有限责任
            self.click_button_xpath(config['date_establishment'], 1)  # 成立日期
            self.click_button_xpath(config['confirm_uniview'], 1)  # 确定
            self.send_keys('xpath', config['company_phone_ent'], '6802888')  # 企业电话
        else:
            self.click_button_xpath(config['company_nature_ent'], 1)  # 企业性质
            self.click_button_xpath(config['llc_option'], 1)  # 有限责任
            self.click_button_xpath(config['date_establishment'], 1)  # 成立日期
            self.click_button_xpath(config['confirm_uniview'], 1)  # 确定
            self.send_keys('xpath', config['company_phone_ent'], '6802888')  # 企业电话

    # 企业担保人
    def enterprise_guarantor_info_input(self):
        self.click_button_xpath(config['relation_applier'], 1)  # 与申请人关系
        self.click_button_xpath(config['legal_option'], 1)  # 法人
        self.click_button_xpath(config['legal_residential_address'], 1)  # 现居住地址
        self.click_button('xpath', config['general_complete'], 1)  # 通用完成按钮
        self.send_keys('xpath', config['legal_address_detail'], '法人现居住地址', 3)  # 法人现居住地址
        self.send_keys('xpath', config['unit_name'], '上海Demo公司', 3)  # 单位名称
        time.sleep(2)
        self.click_button('xpath', config['company_item'], 1)
        self.send_keys('xpath', config['unit_phone'], '6802888')  # 单位电话
        self.click_button_xpath(config['unit_address'], 1)  # 单位地址
        self.click_button('xpath', config['general_complete'], 1)  # 通用完成按钮
        self.send_keys('xpath', config['unit_address_detail'], '单位详细地址')
        self.click_button('xpath', config['unit_type'], 1)  # 单位性质
        self.click_button('xpath', config['foreign_option'], 1)  # 外企
        self.click_button('xpath', config['legal_occupation'], 1)  # 职业
        self.click_button('xpath', config['occupation_option'], 1)  # 职业选项1
        self.click_button('xpath', config['legal_salary'], 1)  # 年薪
        self.click_button('xpath', config['salary_option'], 1)  # 年薪选项1

    # 企业联系人
    def enterprise_contact_info_input(self):
        self.click_button('xpath', config['ent_contact1'])  # 与申请人关系
        self.click_button('xpath', config['relationship_option'])  # 父母
        self.send_keys('xpath', config['ent_contact_name'], '父母1')
        self.send_keys('xpath', config['ent_contact_phone'], '13311112222')
        self.click_button('xpath', config['ent_contact2'])  # 与申请人关系
        self.click_button('xpath', config['relationship_option'])  # 父母
        self.send_keys('xpath', config['ent_contact2_name'], '父母2')
        self.send_keys('xpath', config['ent_contact2_phone'], '13311113333')
        time.sleep(2)

    # 企业营业执照处理
    def enterprise_bl_photo(self):
        # 影像信息-企业营业执照
        photo_ele = self.find_element_by_xpath(config['ent_photo'])  #
        self.actionChains_click(photo_ele)
        # 本地上传文件操作
        self.upload_file(license_photo)

    # 企业驾照处理
    def enterprise_dl_photo(self):
        # 影像信息-驾照
        photo_ele = self.find_element_by_xpath(config['ent_driver_photo'])  #
        self.actionChains_click(photo_ele)
        # 本地上传文件操作
        self.upload_file(driver_photo)

    # 提报提交处理
    def enterprise_submit_handle(self):
        self.click_button('xpath', config['next_step'])  # 影像信息下一步
        self.click_button('xpath', config['next_step'])  # 选传下一步
        self.click_button('xpath', config['finance_next'])  # 备注信息下一步

    # 企业提交操作
    def enterprise_submit_handler(self):  # 不想提报提交可注释该方法
        self.click_button('xpath', config['ent_submit'])  # 提交
        self.click_button('xpath', config['confirm_submit'])  # 确认提交
        self.click_button('xpath', config['final_confirm'], 5)  # 确认
        logger.info(f'{order_num} 提报完成')

    # 企业提报
    def order_submit_enterprise(self):  # 企业提报流程
        self.get_url(self.home_page)
        report_btnLocator = ('xpath', config['report_btn'])
        self.wait_until_present(report_btnLocator)
        self.click_button('xpath', config['report_btn'])  # 提报按钮
        self.click_button('xpath', config['card_title'])  # 小卡片点击
        self.order_num_get()    # 获取当前订单号
        self.click_button('xpath', config['operation_card'])  # 去操作
        self.click_button('xpath', config['cus_detail'])  # 客户信息
        self.enterprise_info_input()
        self.click_button_xpath(config['grantor_next_step'], 3)  # 企业信息下一步
        self.send_keys('xpath', config['shareholding_ratio'], '88')  # 法人持股比例
        self.click_button_xpath(config['grantor_next_step'], 3)  # 法人信息下一步
        self.enterprise_guarantor_info_input()
        self.click_button_xpath(config['grantor_next_step'], 3)  # 担保人下一步
        self.enterprise_contact_info_input()
        self.click_button_xpath(config['grantor_next_step'], 3)  # 联系人下一步
        self.car_info_input()
        self.click_button_xpath(config['grantor_next_step'], 3)  # 车辆信息下一步
        self.product_info_input()
        self.click_button_xpath(config['grantor_next_step'], 3)  # 融资信息下一步
        # 影像信息信息处理
        self.enterprise_bl_photo()
        self.enterprise_dl_photo()
        # 提报提交
        self.enterprise_submit_handle()

    # 企业创单到提报
    def enterprise_order_process(self, cus_phone):
        try:
            self.order_generate_enterprise(cus_phone)
            time.sleep(1)
            options = webdriver.ChromeOptions()
            options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
            # options.add_argument("--auto-open-devtools-for-tabs")
            driver = webdriver.Chrome(options=options)
            app = PreAudit(driver, cus_phone, self.env)  # 客户手机号+环境
            app.personal_audit()
            self.order_submit_enterprise()
            # 不想提交注释下面流程
            self.enterprise_submit_handler()
            # 信审流程
            app = ApprovalProcess(self.driver, self.env)
            app.approve_process(order_num)

        except Exception as e:
            logger.error(f"发生异常：{e}")

        finally:
            logger.info(f'{order_num} 提报结束')
            self.driver.quit()


if __name__ == '__main__':
    # driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    # sub = SubmitOrder(driver, 'Uat')  # Uat & Pre环境切换
    # sub.order_submit_personal()  # 个人单纯提报
    # sub.order_submit_enterprise()  # 企业单纯提报
    # sub.personal_order_process('13800138000')  # 个人创单+预审+提报+审核
    # sub.enterprise_order_process('13800138000')  # 企业创单+预审+提报+审核

    # #
    # # 重复提报
    num_of_repetitions = 1  # 设置要重复执行的次数

    for _ in range(num_of_repetitions):
        driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
        sub = SubmitOrder(driver, 'Pre')  # Uat & Pre环境切换
        # result = sub.personal_order_process('13800138000')   # 创单+预审+提报+审核
        result = sub.enterprise_order_process('13800138000')   # 创单+预审+提报+审核
        # 可在此处根据result添加判断逻辑或日志记录
        if result:
            logger.info("创单执行成功")
        else:
            logger.warning("信审流程执行失败")

        # 在每次循环结束后确保关闭WebDriver
        sub.driver.quit()

    # 执行完所有循环后可以添加结束语句
    logger.info(f"已完成{num_of_repetitions}次提报流程的自动化执行")
