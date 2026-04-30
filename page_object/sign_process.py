import logging
import time
import traceback

from pywinauto import Desktop
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from core.basepage import BasePage, CustomLogging, FilterWarning
from data.path_config import *
from public.utils.get_preaudit_url import get_UatPreaudit_url, get_PrePreaudit_url
from public.utils.readini import ReadIni


class Config:
    WAIT_TIME = 2
    VIDEO_PATH = os.path.join(testData_path, '测试视频.mp4')
import warnings
# 忽略urllib3 重连错误
# warnings.filterwarnings('ignore')


# 设置日志输出到本地文件以及控制台
logger = CustomLogging().get_logger()

# 打开浏览器手机模式
mobile_emulation = {"deviceName": "Samsung Galaxy S20 Ultra"}
options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")
options.add_experimental_option("mobileEmulation", mobile_emulation)


class SignProcess(BasePage):
    def __init__(self, driver, cus_phone, env):
        self.driver = driver
        self.warning_filter = FilterWarning
        super().__init__(self.driver)
        self.config = Config()  # 引入配置类
        p = ReadIni(data_ini)
        # 通过配置类获取数据，避免硬编码
        self.bank_select = p.getini('ele', 'bank_select')
        self.icbc_selected = p.getini('ele', 'icbc_selected')
        self.bank_num = p.getini('ele', 'bank_num')
        self.abc_selected = p.getini('ele', 'abc_selected')
        self.get_code = p.getini('ele', 'get_code')
        self.input_auth = p.getini('ele', 'input_auth')
        self.sign_submit = p.getini('ele', 'sign_submit')
        self.check_box = p.getini('ele', 'check_box')
        self.face_recon = p.getini('ele', 'face_recon')
        self.upload = p.getini('ele', 'upload')
        self.authorization_read = p.getini('ele', 'authorization_read')
        self.agree_button1 = p.getini('ele', 'agree_button1')
        self.agree_button2 = p.getini('ele', 'agree_button2')
        self.signed = p.getini('ele', 'signed')
        self.review_authbook = p.getini('ele', 'review_authbook')
        self.authorization_unread = p.getini('ele', 'authorization_unread')
        self.read = p.getini('ele', 'read')
        self.select_done = p.getini('ele', 'select_done')
        self.input_signcode = p.getini('ele', 'input_signcode')
        self.ccb_selected = p.getini('ele', 'ccb_selected')
        self.sign_repaycard_nextstep = p.getini('ele', 'sign_repaycard_nextstep')
        self.sign_faceAuth = p.getini('ele', 'sign_faceAuth')
        self.sign_person1 = p.getini('ele', 'sign_person1')
        self.sign_person2 = p.getini('ele', 'sign_person2')
        self.sign_getCode = p.getini('ele', 'sign_getCode')
        self.sign_getCode2 = p.getini('ele', 'sign_getCode2')
        self.sing_getCode_conment = p.getini('ele', 'sing_getCode_conment')
        self.sub_sign_repaycard_nextstep = p.getini('ele', 'sub_sign_repaycard_nextstep')
        self.sign_confirm_mes = p.getini('ele', 'sign_confirm_mes')
        self.confirm = p.getini('ele', 'confirm')

        if env == 'Uat':
            pre_url = get_UatPreaudit_url(cus_phone)
        elif env == 'Pre':
            pre_url = get_PrePreaudit_url(cus_phone)
        else:
            raise ValueError("Invalid env. Only 'Uat' and 'Pre' are supported.")
        self.driver.get(pre_url)
        self.wait(self.config.WAIT_TIME)

    def upload_file(self, file_path):
        app = Desktop()
        dialog = app['打开']
        dialog["Edit"].type_keys(file_path)
        time.sleep(self.config.WAIT_TIME)
        dialog["Button"].click()
        time.sleep(self.config.WAIT_TIME)  # 确保文件选择完成

    def scroll_to_bottom(self):
        js = "document.getElementById('viewerContainer').scrollTo(0,10000)"
        self.execute_script(js)

    def handle_first_contract(self):
        sign_person1_locator = ('xpath', self.sign_person1)
        self.wait_until_present(sign_person1_locator)
        self.click_button('xpath', self.sign_person1)  # 抵押合同处理-个人
        time.sleep(2)
        # 切换iframe
        xpath_iframe = '/html/body/iframe'
        iframe = self.find_element_by_xpath(xpath_iframe)
        # print(iframe)
        self.to_iframe(iframe)
        self.wait(10)
        self.scroll_to_bottom()  # 滚动授权书进度条至底部
        self.wait(5)
        self.uniframe()
        self.wait(5)
        self.click_button('xpath', self.read)

    def handle_second_contract(self):
        # 处理第二份合同的逻辑...
        if self.is_element_exist('xpath', self.sign_person2):
            self.click_button('xpath', self.sign_person2)  # 售后合同处理-个人
            self.wait(5)
            # 切换iframe
            xpath_iframe = '/html/body/iframe'
            iframe = self.find_element_by_xpath(xpath_iframe)
            # print(iframe)
            self.to_iframe(iframe)
            self.wait(10)
            self.scroll_to_bottom()  # 滚动授权书进度条至底部
            self.wait(5)
            self.uniframe()
            self.wait(5)
            self.click_button('xpath', self.read)

        # else:
        #     self.getcode_confirm()

    def getcode_confirm(self):
        self.click_button('xpath', self.sing_getCode_conment)
        self.send_keys('xpath', self.input_auth, '123456', 2)
        submit = self.find_element_by_xpath(self.signed)
        self.actionChains_click(submit)
        time.sleep(5)
        # 订阅提交确认处理逻辑
        if self.is_element_exist('xpath', self.sign_confirm_mes):
            self.click_button_xpath(self.confirm)
            time.sleep(5)
            if self.is_element_exist('xpath', self.review_authbook):
                logger.info("签署完成")
                return True
            else:
                logger.error("授权失败", str(traceback.format_exc()))
                return False
        else:
            if self.is_element_exist('xpath', self.review_authbook):
                logger.info("签署完成")
                return True
            else:
                logger.error("授权失败", str(traceback.format_exc()))
                return False

    # 回租签约流程
    def sign_process(self):
        try:  # 判断是否绑过卡
            if self.is_element_exist('xpath', self.sign_repaycard_nextstep):  # 重复进入签约页面会有下一步按钮
                self.click_button_xpath(self.sign_repaycard_nextstep)
                check_boxLocator = ('xpath', self.check_box)
                self.wait_until_present(check_boxLocator)
                self.click_button('xpath', self.check_box, 1)  # 人脸识别勾选框
                self.click_button('xpath', self.sign_faceAuth)  # 开始人脸识别
                upload_locator = ('xpath', self.upload)
                self.wait_until_present(upload_locator)
                self.send_keys('xpath', self.upload, self.config.VIDEO_PATH, 3)
                sign_person1_locator = ('xpath', self.sign_person1)
                self.wait_until_present(sign_person1_locator)
                # 第一份合同处理
                self.handle_first_contract()
                # 第二份合同处理
                self.handle_second_contract()
                # 获取验证码确认签署
                self.getcode_confirm()
            # 正常第一次签约
            elif self.is_element_exist('xpath', self.bank_select) is True:  # 开户行下拉框存在走新流程
                self.click_button('xpath', self.bank_select)  # 开户行下拉框
                self.click_button('xpath', self.select_done)  # 工商银行完成按钮
                if self.is_element_exist('xpath', self.icbc_selected):  # 如果选择的是工商银行)
                    self.send_keys_with_clear_value('xpath', self.bank_num, '6222023602097492791')  # 工商银行卡写死
                elif self.is_element_exist('xpath', self.abc_selected):  # 如果选择的是农行
                    self.send_keys_with_clear_value('xpath', self.bank_num, '6228496200001864830')  # 农行卡写死
                elif self.is_element_exist('xpath', self.ccb_selected):  # 如果选择的是建行
                    self.send_keys_with_clear_value('xpath', self.bank_num, '6217000730036341879')  # 建行卡写死
                time.sleep(2)
                self.click_button('xpath', self.get_code)  # 获取验证码
                self.send_keys('xpath', self.input_signcode, '111111', 2)
                self.click_button('xpath', self.sign_submit, 3)  # 提交
                time.sleep(2)
                check_boxLocator = ('xpath', self.check_box)
                self.wait_until_present(check_boxLocator)
                self.click_button('xpath', self.check_box, 4)  # 人脸识别勾选框
                self.click_button('xpath', self.sign_faceAuth)  # 开始人脸识别
                upload_locator = ('xpath', self.upload)
                self.wait_until_present(upload_locator)
                self.send_keys('xpath', self.upload, self.config.VIDEO_PATH, 3)
                # 第一份合同处理
                self.handle_first_contract()
                # 第二份合同处理
                self.handle_second_contract()
                # 获取验证码确认签署
                self.getcode_confirm()
            #  判断是否已开始人脸识别
            elif self.is_element_exist('xpath', self.check_box):
                self.click_button('xpath', self.check_box)
                self.click_button('xpath', self.face_recon)
                upload_locator = ('xpath', self.upload)
                self.wait_until_present(upload_locator)
                self.send_keys('xpath', self.upload, self.config.VIDEO_PATH)
                # 第一份合同处理
                self.handle_first_contract()
                # 第二份合同处理
                self.handle_second_contract()
                # 获取验证码确认签署
                self.getcode_confirm()

            else:
                logger.error("签约流程异常", str(traceback.format_exc()))

        except (NoSuchElementException, TimeoutException) as e:
            logger.error("加载元素失败", f"{str(e)}")
            return False

        finally:
            self.driver.quit()  # 确保WebDriver关闭

    # 订阅签约流程
    def subscription_sign_process(self):
        try:  # 判断是否绑过卡
            if self.is_element_exist('xpath', self.sub_sign_repaycard_nextstep):  # 重复进入签约页面会有下一步按钮
                self.click_button_xpath(self.sub_sign_repaycard_nextstep)
                check_boxLocator = ('xpath', self.check_box)
                self.wait_until_present(check_boxLocator)
                self.click_button('xpath', self.check_box, 1)  # 人脸识别勾选框
                self.click_button('xpath', self.sign_faceAuth)  # 开始人脸识别
                upload_locator = ('xpath', self.upload)
                self.wait_until_present(upload_locator)
                self.send_keys('xpath', self.upload, self.config.VIDEO_PATH, 3)
                sign_person1_locator = ('xpath', self.sign_person1)
                self.wait_until_present(sign_person1_locator)
                # 第一份合同处理
                self.handle_first_contract()
                # 第二份合同处理
                self.handle_second_contract()
                # 获取验证码确认签署
                self.getcode_confirm()
            # 正常第一次签约
            elif self.is_element_exist('xpath', self.bank_select) is True:  # 开户行下拉框存在走新流程
                self.click_button('xpath', self.bank_select)  # 开户行下拉框
                self.click_button('xpath', self.select_done)  # 工商银行完成按钮
                if self.is_element_exist('xpath', self.icbc_selected):  # 如果选择的是工商银行)
                    self.send_keys_with_clear_value('xpath', self.bank_num, '6222023602097492791')  # 工商银行卡写死
                elif self.is_element_exist('xpath', self.abc_selected):  # 如果选择的是农行
                    self.send_keys_with_clear_value('xpath', self.bank_num, '6228496200001864830')  # 农行卡写死
                elif self.is_element_exist('xpath', self.ccb_selected):  # 如果选择的是建行
                    self.send_keys_with_clear_value('xpath', self.bank_num, '6217000730036341879')  # 建行卡写死
                time.sleep(2)
                self.click_button('xpath', self.get_code)  # 获取验证码
                self.send_keys('xpath', self.input_signcode, '111111', 2)
                self.click_button('xpath', self.sign_submit, 3)  # 提交
                time.sleep(2)
                check_boxLocator = ('xpath', self.check_box)
                self.wait_until_present(check_boxLocator)
                self.click_button('xpath', self.check_box, 4)  # 人脸识别勾选框
                self.click_button('xpath', self.sign_faceAuth)  # 开始人脸识别
                upload_locator = ('xpath', self.upload)
                self.wait_until_present(upload_locator)
                self.send_keys('xpath', self.upload, self.config.VIDEO_PATH, 3)
                # 第一份合同处理
                self.handle_first_contract()
                # 第二份合同处理
                self.handle_second_contract()
                # 获取验证码确认签署
                self.getcode_confirm()
            #  判断是否已开始人脸识别
            elif self.is_element_exist('xpath', self.check_box):
                self.click_button('xpath', self.check_box)
                self.click_button('xpath', self.face_recon)
                upload_locator = ('xpath', self.upload)
                self.wait_until_present(upload_locator)
                self.send_keys('xpath', self.upload, self.config.VIDEO_PATH)
                # 第一份合同处理
                self.handle_first_contract()
                # 第二份合同处理
                self.handle_second_contract()
                # 获取验证码确认签署
                self.getcode_confirm()

            else:
                logger.error("签约流程异常", str(traceback.format_exc()))

        except (NoSuchElementException, TimeoutException) as e:
            logger.error("加载元素失败", f"{e}")
            return False
        except Exception as e:
            exc_info = traceback.format_exc()
            logger.error(f"发生异常: {str(e)}")
            return False
        finally:
            self.driver.quit()  # 确保WebDriver关闭
            self.warning_filter = FilterWarning


if __name__ == '__main__':
    driver = webdriver.Chrome(options=options)
    sign = SignProcess(driver, '13800138000', 'Pre')  # 客户手机号
    # sign.sign_process()     # 回租客户签约操作
    sign.subscription_sign_process()    # 订阅客户签约操作
