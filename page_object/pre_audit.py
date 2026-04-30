# -*- coding:utf-8 -*-
# @FileName  :pre_audit.py
# @Time      :2024/2/3 10:47
# @Author    :Daisy
# @Brief Introduction    : 客户预审流程
# -------------------------------------------------------------------
import random
import time
import traceback
import pyautogui
from pywinauto import Desktop
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from core.basepage import BasePage
from public.utils.get_preaudit_url import get_UatPreaudit_url, get_PrePreaudit_url
from public.utils.readini import ReadIni
from data.path_config import *
from core.basepage import CustomLogging
# 配置日志
loger = CustomLogging().get_logger()

# 获取data ini配置
p = ReadIni(data_ini)
idcard_left = p.getini('ele', 'idcard_left')
idcard_right = p.getini('ele', 'idcard_right')
album = p.getini('ele', 'album')
region = p.getini('ele', 'region')
USCI_code = p.getini('ele', 'USCI_code')
region_confirm = p.getini('ele', 'region_confirm')
married = p.getini('ele', 'married')
married_confirm = p.getini('ele', 'married_confirm')
unmarried = p.getini('ele', 'unmarried')
education = p.getini('ele', 'education')
education_confirm = p.getini('ele', 'education_confirm')
next = p.getini('ele', 'next')
check_box = p.getini('ele', 'check_box')
face_recon = p.getini('ele', 'face_recon')
upload = p.getini('ele', 'upload')
authorization_unread = p.getini('ele', 'authorization_unread')
ent_authorization_unread = p.getini('ele', 'ent_authorization_unread')
authorization_read = p.getini('ele', 'authorization_read')
iframe = p.getini('ele', 'iframe')
authorization = p.getini('ele', 'authorization')
read = p.getini('ele', 'read')
sign_next = p.getini('ele', 'sign_next')
agree_button1 = p.getini('ele', 'agree_button1')
agree_button2 = p.getini('ele', 'agree_button2')
ent_agree_button1 = p.getini('ele', 'ent_agree_button1')
ent_agree_button2 = p.getini('ele', 'ent_agree_button2')
get_code = p.getini('ele', 'get_code')
input_auth = p.getini('ele', 'input_auth')
signed = p.getini('ele', 'signed')
sub_cusResidential_address = p.getini('ele', 'sub_cusResidential_address')
address_detail_selection = p.getini('ele', 'address_detail_selection')
business_address = p.getini('ele', 'business_address')
business_address_detail = p.getini('ele', 'business_address_detail')
review_authbook = p.getini('ele', 'review_authbook')
sub_education = p.getini('ele', 'sub_education')
residence_status = p.getini('ele', 'residence_status')
company_name = p.getini('ele', 'company_name')
company_item = p.getini('ele', 'company_item')
sub_car = p.getini('ele', 'sub_car')
complete_order = p.getini('ele', 'complete_order')
company_address = p.getini('ele', 'company_address')
company_detailAddress = p.getini('ele', 'company_detailAddress')
company_nature = p.getini('ele', 'company_nature')
sub_contact = p.getini('ele', 'sub_contact')
sub_contact_name = p.getini('ele', 'sub_contact_name')
sub_contact_phone = p.getini('ele', 'sub_contact_phone')
save_next_button = p.getini('ele', 'save_next_button')
sub_car_series = p.getini('ele', 'sub_car_series')
xc60 = p.getini('ele', 'xc60')
sub_car_style = p.getini('ele', 'sub_car_style')
car1 = p.getini('ele', 'car1')
sub_product = p.getini('ele', 'sub_product')
sub_product_select = p.getini('ele', 'sub_product_select')
sub_term = p.getini('ele', 'sub_term')
car_dealer = p.getini('ele', 'car_dealer')
photo_uploadBtn = p.getini('ele', 'photo_uploadBtn')
business_contact_address = p.getini('ele', 'business_contact_address')
sign_submit = p.getini('ele', 'sign_submit')
confirm = p.getini('ele', 'confirm')
business_married = p.getini('ele', 'business_married')
sub_success = p.getini('ele', 'sub_success')
business_mailing_address = p.getini('ele', 'business_mailing_address')
sub_general_done = p.getini('ele', 'sub_general_done')
sub_agree_button1 = p.getini('ele', 'sub_agree_button1')
sub_agree_button2 = p.getini('ele', 'sub_agree_button2')
actual_user = p.getini('ele', 'actual_user')
actual_phone = p.getini('ele', 'actual_phone')
ent_photo = p.getini('ele', 'ent_photo')
ent_driver_photo = p.getini('ele', 'ent_driver_photo')
sub_term_selection = p.getini('ele', 'sub_term_selection')
exist_enterprise = p.getini('ele', 'exist_enterprise')
term_elements = p.getini('ele', 'term_elements')
business_address_detail1 = p.getini('ele', 'business_address_detail1')
open_ad_check = p.getini('ele', 'open_ad_check')
open_ad_back = p.getini('ele', 'open_ad_back')
# 设定一些通用参数
WAIT_TIME = 5  # 通用等待时间
driver_photo = os.path.join(testData_path, '测试驾照.jpg')  # 驾照路径
front_faces =[
    os.path.join(testData_path, '王飞.jpg'),
    os.path.join(testData_path, '新疆身份证正面.png'),
    os.path.join(testData_path, '刘香港.png'),
    os.path.join(testData_path, '吴孙培.png'),
    os.path.join(testData_path, '何孔涛.png'),
    os.path.join(testData_path, '李涵真.png'),
    os.path.join(testData_path, '曹雄雅.png'),
    os.path.join(testData_path, '杨春吉.jpg'),
    os.path.join(testData_path, '游志勇.jpg'),
    os.path.join(testData_path, '郑伟儒.jpg'),
    os.path.join(testData_path, '马艳平.jpg'),
    os.path.join(testData_path, '徐乐.jpg'),
    os.path.join(testData_path, '张平.jpg'),
    os.path.join(testData_path, '周芸.jpg')]    # 随机一个身份证


# front_faces = [
#     os.path.join(testData_path, '李涵真.png')
# ]  # 指定人脸图片
FILE_PATH_2 = os.path.join(testData_path, '背面2.jpg')  # 反面
VIDEO_PATH = os.path.join(testData_path, '测试视频.mp4')  # 人脸识别视频


class PreAudit(BasePage):
    def __init__(self, driver, PHONE_NUMBER, url_type='Uat'):
        self.driver = driver
        self.PHONE_NUMBER=PHONE_NUMBER
        super().__init__(self.driver)
        if url_type == 'Uat':
            pre_url = get_UatPreaudit_url(PHONE_NUMBER)
        elif url_type == 'Pre':
            pre_url = get_PrePreaudit_url(PHONE_NUMBER)
        else:
            raise ValueError("Invalid url_type. Only 'Uat' and 'Pre' are supported.")
        self.driver.get(pre_url)
        self.env = url_type
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

    # 预审个人信息录入
    def pre_personal_ifo_input(self):
        self.click_button('xpath', region, 1)
        self.click_button('xpath', region_confirm, 1)
        self.click_button('xpath', married, 1)
        self.click_button('xpath', married_confirm, 1)
        self.click_button('xpath', education, 1)
        self.click_button('xpath', education_confirm, 1)
        self.click_button('xpath', next, WAIT_TIME)

    # 人脸识别
    def face_id_input(self):
        self.click_button('xpath', check_box)
        self.click_button('xpath', face_recon)
        upload_location = ('xpath',upload)
        self.wait_until_present(upload_location, 5)
        self.send_keys('xpath', upload, VIDEO_PATH, 3)
        time.sleep(5)

    # iframe切换
    def iframe_handel(self):
        # iframe 切换和滚动操作
        xpath_iframe = '/html/body/iframe'
        iframe = self.find_element_by_xpath(xpath_iframe)
        self.to_iframe(iframe)
        js = "document.getElementById('viewerContainer').scrollTo(0,10000)"
        self.execute_script(js)
        time.sleep(1)
        self.uniframe()

    # 勾选框验证码处理
    def checkbox_phonecode_handle(self):  # 两个勾选框手机验证码处理
        self.click_button('xpath', agree_button1, 1)
        self.click_button('xpath', agree_button2, 1)
        self.click_button('xpath', get_code)
        self.send_keys('xpath', input_auth, '123456', 3)

    # 身份证正反面上传
    def upload_id_photo(self):
        self.click_button('xpath', idcard_left)
        element = self.find_element_by_xpath(album)
        self.actionChains_click(element)
        self.upload_file(random.choice(front_faces))    # 随机选一个身份证
        self.click_button('xpath', idcard_right)
        element2 = self.find_element_by_xpath(album)
        self.actionChains_click(element2)
        self.upload_file(FILE_PATH_2)

    # 回租业务预审流程
    def personal_audit(self):  # 提报个人&企业预审
        try:
            #  判断是否已做完信息填写
            if self.is_element_exist('xpath', check_box):
                self.face_id_input()

            #  判断是否上传过身份证
            elif not self.is_element_exist('xpath', idcard_left):
                #  信息填写，针对法人授权处理，增加企业统一验证码录入
                if self.is_element_exist('xpath', USCI_code):
                    self.send_keys_with_clear('xpath', USCI_code, '911101088432004739')
                    self.pre_personal_ifo_input()
                    self.face_id_input()
                else:
                    self.pre_personal_ifo_input()
                    #  开始人脸识别
                    self.face_id_input()
            else:
                # 点击按钮和文件上传操作
                self.upload_id_photo()
                #  信息填写，针对法人授权处理，增加企业统一验证码录入
                if self.is_element_exist('xpath', USCI_code):
                    self.send_keys_with_clear('xpath', USCI_code, '911101088432004739')
                    self.pre_personal_ifo_input()
                    self.face_id_input()
                else:
                    self.pre_personal_ifo_input()
                    #  开始人脸识别
                    self.face_id_input()

            # 已读授权书处理
            if self.is_element_exist('xpath', authorization_read):
                self.checkbox_phonecode_handle()
                submit = self.find_element_by_xpath(signed)
                self.actionChains_click(submit)
                time.sleep(4)
                if self.is_element_exist('xpath', review_authbook):
                    loger.info(f"{self.PHONE_NUMBER}预审授权完成")
                else:
                    loger.info(f"{self.PHONE_NUMBER}授权失败")
            # 未读 个人授权书处理
            else:
                authorization_unread_locator = ('xpath', authorization_unread)
                self.wait_until_present(authorization_unread_locator, WAIT_TIME)
                self.click_button('xpath', authorization_unread, 4)
                time.sleep(3)
                # iframe 切换和滚动操作
                self.iframe_handel()
                self.wait(3)
                self.click_button_xpath(read)
                # 未读 企业授权书处理
                if self.is_element_exist('xpath', authorization_unread):
                    # authorization_unread_locator = ('xpath', ent_authorization_unread)
                    authorization_unread_locator = ('xpath', authorization_unread)
                    self.wait_until_present(authorization_unread_locator, WAIT_TIME)
                    self.click_button('xpath', authorization_unread, 4)
                    time.sleep(3)
                    self.iframe_handel()
                    self.wait(3)
                    self.click_button('xpath', read)
                    self.wait(3)
                    self.click_button('xpath', ent_agree_button1, 1)
                    self.click_button('xpath', ent_agree_button2, 1)
                    self.click_button('xpath', get_code)
                    self.send_keys('xpath', input_auth, '123456', 3)
                    submit = self.find_element_by_xpath(signed)
                    self.actionChains_click(submit)
                    time.sleep(4)
                    if self.is_element_exist('xpath', review_authbook):
                        loger.info(f"{self.PHONE_NUMBER}授权完成")
                        return True
                    else:
                        loger.info(f"{self.PHONE_NUMBER}授权失败")
                        return False
                else:
                    self.checkbox_phonecode_handle()
                    submit = self.find_element_by_xpath(signed)
                    self.actionChains_click(submit)
                    time.sleep(4)
                    if self.is_element_exist('xpath', review_authbook):
                        loger.info(f"{self.PHONE_NUMBER}授权完成")
                        return True
                    else:
                        loger.info(f"{self.PHONE_NUMBER}授权失败")
                        return False

        except (NoSuchElementException, TimeoutException) as e:
            loger.error(f"元素未找到：{e}")
            print(f"加载元素失败：{e}")
            return False
        except Exception as e:
            loger.error(f"发生异常：{e}")
            traceback.print_exc()  # 输出异常信息
            return False
        finally:
            self.driver.quit()  # 确保WebDriver关闭  #

# -----------------------订阅分割--------------------------------------------

    # 订阅私户去完善信息填报
    def subscription_input_personal(self):
        # 客户信息
        address_detail_selection_locator = ('xpath', address_detail_selection)
        self.wait_until_present(address_detail_selection_locator, WAIT_TIME)
        self.click_button_xpath(address_detail_selection, 1)  # 居住详细地址下拉框
        self.click_button_xpath(sub_general_done, 1)  # 完成按钮
        self.send_keys('xpath', sub_cusResidential_address, '南山大道888号')  # 居住详细地址输入框
        self.click_button_xpath(married, 1)  # 婚姻状况
        self.click_button_xpath(married_confirm, 1)  # 完成按钮
        self.click_button_xpath(sub_education, 1)  # 学历
        self.click_button_xpath(sub_general_done, 1)
        self.click_button_xpath(residence_status, 1)  # 居住状况
        self.click_button_xpath(sub_general_done, 1)
        self.send_keys('xpath', company_name, '测试单位')  # 单位名称
        time.sleep(2)
        self.click_button('xpath', company_item, 1)
        self.click_button('xpath', company_address, 1)  # 单位详细地址选项
        self.click_button_xpath(sub_general_done, 1)  # 完成按钮
        self.send_keys('xpath', company_detailAddress, '南山大道888号')  # 单位详细地址输入
        self.click_button_xpath(company_nature, 1)  # 单位性质
        self.click_button_xpath(married_confirm, 1)  # 完成按钮
        self.click_button_xpath(sub_contact, 1)  # 与申请人关系
        self.click_button_xpath(sub_general_done, 1)  # 完成按钮
        self.send_keys('xpath', sub_contact_name, '父母')
        self.send_keys('xpath', sub_contact_phone, '13540987495')
        self.click_button_xpath(save_next_button, 1)  # 保存并下一步
        # 产品信息
        self.click_button_xpath(sub_car_series, 1)  # 车系UAT 选EM 30 PRE选XC60
        if self.env == 'Uat':
            self.click_button_xpath(sub_car, 1)  # EM 30
            self.click_button_xpath(sub_car_style, 1)  # 车型
        else:
            xc60_locator = ('xpath', xc60)
            self.wait_until_present(xc60_locator, WAIT_TIME)
            self.click_button_xpath(xc60, 1)  # XC 60
            self.click_button_xpath(sub_car_style, 1)  # 车型
        car1_locator = ('xpath', car1)
        self.wait_until_present(car1_locator, WAIT_TIME)
        self.click_button_xpath(car1, 1)  # 第一个在售车
        self.click_button_xpath(sub_product, 1)  # 产品
        self.click_button_xpath(sub_product_select, 1)  # 订阅产品验证02
        self.click_button_xpath(sub_term_selection, 1)  # 期数选择
        random_term = self.random_element('xpath', term_elements)  # 随机选择期数
        self.random_click_element_by_js(random_term)
        time.sleep(2)
        # 点击随机选项
        random_term.click()
        self.click_button_xpath(married_confirm, 1)  # 完成按钮
        self.click_button_xpath(car_dealer, 1)  # 交车门店
        self.click_button_xpath(married_confirm, 1)  # 完成按钮
        self.click_button_xpath(save_next_button, 1)  # 保存并下一步
        # 影像信息
        photo_ele = self.find_element_by_xpath(photo_uploadBtn)  # 没有就上传
        self.actionChains_click(photo_ele)
        # 本地上传文件操作
        self.upload_file(driver_photo)
        # 提交
        self.click_button_xpath(sign_submit, 2)
        self.click_button_xpath(confirm, 3)

    # 订阅公户预审信息完善
    def subscription_input_enterprise(self):
        # 企业信息
        address_detail_selection_locator = ('xpath', address_detail_selection)
        self.wait_until_present(address_detail_selection_locator, WAIT_TIME)
        self.click_button_xpath(business_address, 1)  # 居住详细地址下拉框
        self.click_button_xpath(sub_general_done, 1)  # 完成按钮
        self.send_keys('xpath', business_address_detail, '南山大道888号')  # 居住详细地址输入框
        self.click_button_xpath(business_contact_address)  # 通讯地址
        self.click_button_xpath(sub_general_done, 1)  # 完成按钮
        self.send_keys('xpath', business_mailing_address, '南山大道888号')  # 通讯地址输入框
        self.click_button_xpath(business_married, 1)  # 婚姻状况
        self.click_button_xpath(married_confirm, 1)  # 完成按钮

    # 订阅公户提报
    def subscription_submit_enterprise(self):
        # 提报客户信息
        self.send_keys('xpath', actual_user, '测试用户')  # 实际用车人
        self.send_keys('xpath', actual_phone, '13800138000')  # 实际用车人电话
        self.click_button_xpath(save_next_button, 1)  # 保存并下一步
        # 产品信息
        self.click_button_xpath(sub_car_series, 1)  # 车系UAT 选EM 30 PRE选XC60
        xc60_locator = ('xpath', xc60)
        self.wait_until_present(xc60_locator, WAIT_TIME)
        if self.env == 'Uat':
            self.click_button_xpath(sub_car, 1)  # EM 30
            self.click_button_xpath(sub_car_style, 1)  # 车型
        else:
            xc60_locator = ('xpath', xc60)
            self.wait_until_present(xc60_locator, WAIT_TIME)
            self.click_button_xpath(xc60, 1)  # XC 60
            self.click_button_xpath(sub_car_style, 1)  # 车型
        car1_locator=('xpath', car1)
        self.wait_until_present(car1_locator, WAIT_TIME)
        self.click_button_xpath(car1, 1)  # 第一个在售车
        self.click_button_xpath(sub_product, 1)  # 产品
        self.click_button_xpath(sub_product_select, 1)  # 订阅产品验证02
        self.click_button_xpath(sub_term_selection, 1)  # 期数选择
        random_term = self.random_element('xpath', term_elements)  # 随机选择期数
        self.random_click_element_by_js(random_term)
        time.sleep(2)
        # 点击随机选项
        random_term.click()
        self.click_button_xpath(married_confirm, 1)  # 完成按钮
        self.click_button_xpath(car_dealer, 1)  # 交车门店
        self.click_button_xpath(married_confirm, 1)  # 完成按钮
        self.click_button_xpath(save_next_button, 1)  # 保存并下一步
        # 影像信息-企业营业执照
        photo_ele = self.find_element_by_xpath(ent_photo)  #
        self.actionChains_click(photo_ele)
        # 本地上传文件操作
        self.upload_file(driver_photo)
        # 影像信息-驾照
        photo_ele = self.find_element_by_xpath(ent_driver_photo)  #
        self.actionChains_click(photo_ele)
        # 本地上传文件操作
        self.upload_file(driver_photo)
        # 提交
        self.click_button_xpath(sign_submit, 2)
        self.click_button_xpath(confirm, 3)

    # 订阅业务预审流程
    def subscription_preaudit(self):  # 订阅个人&企业预审+提报
        try:
            # 开屏广告处理
            self.click_button_xpath(open_ad_check)
            self.click_button_xpath(open_ad_back)
            if self.is_element_exist('xpath', idcard_left):  # 上传身份证路线
                # 点击按钮和文件上传操作
                self.upload_id_photo()
                #  信息填写，针对法人授权处理，增加企业统一验证码录入 走法人订阅流程
                if self.is_element_exist('xpath', USCI_code):
                    self.send_keys_with_clear('xpath', USCI_code, '911101088432004739')
                    self.subscription_input_enterprise()
                    # 下一步
                    self.click_button_xpath(sign_next)
                    # 开始人脸识别
                    self.face_id_input()
                    # 未读 企业信息授权书处理
                    if self.is_element_exist('xpath', authorization_unread):
                        authorization_unread_locator = ('xpath', authorization_unread)
                        self.wait_until_present(authorization_unread_locator, WAIT_TIME)
                        self.click_button('xpath', authorization_unread, 4)
                        time.sleep(3)
                        self.iframe_handel()
                        self.wait(3)
                        self.click_button('xpath', read)
                        self.wait(3)
                        # 企业法人授权书处理
                        self.is_element_exist('xpath', authorization_unread)
                        authorization_unread_locator = ('xpath', authorization_unread)
                        self.wait_until_present(authorization_unread_locator, WAIT_TIME)
                        self.click_button('xpath', authorization_unread, 4)
                        time.sleep(3)
                        self.iframe_handel()
                        self.wait(3)
                        self.click_button('xpath', read)
                        self.click_button('xpath', sub_agree_button1, 1)
                        self.click_button('xpath', sub_agree_button2, 1)
                        self.click_button('xpath', get_code)
                        self.send_keys('xpath', input_auth, '123456', 3)
                        submit = self.find_element_by_xpath(signed)
                        self.actionChains_click(submit)
                        # 订阅提报后续流程
                        self.click_button_xpath(complete_order)  # 去完善
                        # 企业提报后续流程
                        self.subscription_submit_enterprise()
                        if self.is_element_exist('xpath', sub_success):
                            loger.info("订阅提报提交完成")
                            return True
                        else:
                            loger.info("订阅提报提交失败")
                            return False
                    else:  # 单个授权书场景处理
                        self.click_button('xpath', read)
                        self.click_button('xpath', sub_agree_button1, 1)
                        self.click_button('xpath', sub_agree_button2, 1)
                        self.click_button('xpath', get_code)
                        self.send_keys('xpath', input_auth, '123456', 3)
                        submit = self.find_element_by_xpath(signed)
                        self.actionChains_click(submit)
                        # 订阅提报后续流程
                        self.click_button_xpath(complete_order)  # 去完善
                        # 企业提报后续流程
                        self.subscription_submit_enterprise()
                        if self.is_element_exist('xpath', sub_success):
                            loger.info("订阅提报提交完成")
                            return True
                        else:
                            loger.info("订阅提报提交失败")
                            return False
                # 走个人订阅流程
                else:
                    # 下一步
                    self.click_button_xpath(sign_next)
                    # 开始人脸识别
                    self.face_id_input()
            elif self.is_element_exist('xpath', check_box):  # 人脸识别流程
                # 开始人脸识别
                self.face_id_input()

            else:  # 判断企业还是个人
                if self.is_element_exist('xpath', exist_enterprise):  # 企业名称元素
                    # 企业订阅提报后续流程
                    self.subscription_submit_enterprise()
                else:
                    # 个人订阅提报后续流程
                    self.subscription_input_personal()
                if self.is_element_exist('xpath', sub_success):
                    loger.info("订阅提报提交完成")
                    return True
                else:
                    loger.info("订阅提报提交失败")
                    return False

            # 已读授权书处理
            if self.is_element_exist('xpath', authorization_read):
                self.checkbox_phonecode_handle()
                submit = self.find_element_by_xpath(signed)
                self.actionChains_click(submit)
                # 订阅提报后续流程
                self.click_button_xpath(complete_order)  # 去完善
                self.subscription_input_personal()
                if self.is_element_exist('xpath', sub_success):
                    loger.info("订阅提报提交完成")
                    return True
                else:
                    loger.info("订阅提报提交失败")
                    return False
            # 未读 个人授权书处理
            else:
                authorization_unread_locator = ('xpath', authorization_unread)
                self.wait_until_present(authorization_unread_locator, WAIT_TIME)
                self.click_button('xpath', authorization_unread, 4)
                time.sleep(3)
                # iframe 切换和滚动操作
                self.iframe_handel()
                self.wait(3)
                self.click_button_xpath(read)
                # 未读 企业授权书处理
                if self.is_element_exist('xpath', authorization_unread):
                    # authorization_unread_locator = ('xpath', ent_authorization_unread)
                    authorization_unread_locator = ('xpath', authorization_unread)
                    self.wait_until_present(authorization_unread_locator, WAIT_TIME)
                    self.click_button('xpath', authorization_unread, 4)
                    time.sleep(3)
                    self.iframe_handel()
                    self.wait(3)
                    self.click_button('xpath', read)
                    self.wait(3)
                    self.click_button('xpath', ent_agree_button1, 1)
                    self.click_button('xpath', ent_agree_button2, 1)
                    self.click_button('xpath', get_code)
                    self.send_keys('xpath', input_auth, '123456', 3)
                    submit = self.find_element_by_xpath(signed)
                    self.actionChains_click(submit)
                    # 订阅提报后续流程
                    self.click_button_xpath(complete_order)  # 去完善
                    self.subscription_input_personal()
                    if self.is_element_exist('xpath', sub_success):
                        loger.info("订阅提报提交完成")
                        return True
                    else:
                        loger.info("订阅提报提交失败")
                        return False
                else:
                    self.checkbox_phonecode_handle()
                    submit = self.find_element_by_xpath(signed)
                    self.actionChains_click(submit)
                    # 订阅提报后续流程
                    self.click_button_xpath(complete_order)  # 去完善
                    self.subscription_input_personal()
                    if self.is_element_exist('xpath', sub_success):
                        loger.info("订阅提报提交完成")
                        return True
                    else:
                        loger.info("订阅提报提交失败")
                        return False

        except (NoSuchElementException, TimeoutException) as e:
            loger.error(f"元素未找到：{e}")
            print(f"加载元素失败：{e}")
            return False
        except Exception as e:
            loger.error(f"发生异常：{e}")
            traceback.print_exc()  # 输出异常信息
            return False
        finally:
            self.driver.quit()  # 确保WebDriver关闭

if __name__ == '__main__':
    phone = ['13800138000', '13900139000', '18227038250']
    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", {"deviceName": "Samsung Galaxy S20 Ultra"})
    # options.add_argument("--auto-open-devtools-for-tabs")
    driver = webdriver.Chrome(options=options)
    app = PreAudit(driver, '13800138000', 'Uat')  # 客户手机号+环境
    app.personal_audit()  # 回租
    # app.subscription_preaudit()    # 订阅
