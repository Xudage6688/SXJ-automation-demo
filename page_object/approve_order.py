import logging
import sys
import time
from selenium import webdriver
from core.basepage import BasePage, CustomLogging
from data.path_config import *
from public.utils.readini import ReadIni
from selenium.webdriver.chrome.options import Options
import warnings
# 忽略urllib3 重连错误
warnings.filterwarnings('ignore')

# 配置日志
loger = CustomLogging().get_logger()

chrome_options = Options()
# 配置为调试模式
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
time.sleep(1)
# 获取data ini配置
p = ReadIni(data_ini)
user = p.getini('uat', 'user')
pwd = p.getini('uat', 'password')
url = p.getini('uat', 'demo_loginurl')
ele_user = p.getini('uat', 'user')
ele_pwd = p.getini('uat', 'password')
approve_center = p.getini('ele', 'approve_center')
login_error = p.getini('ele', 'login_error')
transfer_manage = p.getini('ele', 'transfer_manage')
audit_transfer = p.getini('ele', 'audit_transfer')
order_input = p.getini('ele', 'order_input')
query_button = p.getini('ele', 'query_button')
no_data_ele = p.getini('ele', 'no_data_ele')
transfer_checkbox = p.getini('ele', 'transfer_checkbox')
transfer_button = p.getini('ele', 'transfer_button')
transfer_staff = p.getini('ele', 'transfer_staff')
transfer_confirm = p.getini('ele', 'transfer_confirm')
task_manage = p.getini('ele', 'task_manage')
phone_approve_task = p.getini('ele', 'phone_approve_task')
audit_approve_task = p.getini('ele', 'audit_approve_task')
audit_transfer_tag = p.getini('ele', 'audit_transfer_tag')
phone_approve_tag = p.getini('ele', 'phone_approve_tag')
audit_approve_tag = p.getini('ele', 'audit_approve_tag')
handle_button = p.getini('ele', 'handle_button')
approval_opinion_select = p.getini('ele', 'approval_opinion_select')
approve_pass = p.getini('ele', 'approve_pass')
second_opinion = p.getini('ele', 'second_opinion')
full_agree = p.getini('ele', 'full_agree')
approval_remark = p.getini('ele', 'approval_remark')
no_addition = p.getini('ele', 'no_addition')
submit_button = p.getini('ele', 'submit_button')
iframe_task_detail = p.getini('ele', 'iframe_task_detail')
iframe_phone_task = p.getini('ele', 'iframe_phone_task')
comfirm_button = p.getini('ele', 'comfirm_button')
handler = p.getini('ele', 'handler')
add_material = p.getini('ele', 'add_material')
material_input = p.getini('ele', 'material_input')


class ApprovalProcess(BasePage):
    def __init__(self, driver, env):
        self.driver = driver
        super().__init__(self.driver)
        if env == 'Uat':
            home_page = p.getini('uat', 'demo_homepage')
            self.iframe_transfer = p.getini('uat', 'iframe_transfer')
            self.iframe_phone_approve = p.getini('uat', 'iframe_phone_approve')
            self.iframe_audit_approve = p.getini('uat', 'iframe_audit_approve')
            self.transfer_staff = p.getini('ele', 'transfer_staff')
            self.add_material = '是'    # 是否加收材料

        elif env == 'Pre':
            home_page = p.getini('pre', 'demo_homepage')
            self.iframe_transfer = p.getini('pre', 'iframe_transfer')
            self.iframe_phone_approve = p.getini('pre', 'iframe_phone_approve')
            self.iframe_audit_approve = p.getini('pre', 'iframe_audit_approve')
            self.transfer_staff = p.getini('ele', 'transfer_staff')
            self.add_material = '是'    # 是否加收材料

        else:
            raise ValueError("Invalid env. Only 'Uat' and 'Pre' are supported.")

        self.env = env  # 存储env变量
        self.home_page = home_page  # 存储主页URL
        self.get_url(home_page)  # 打开demo主页
        time.sleep(3)
        if self.is_element_exist('xpath', login_error):  # 针对未登录场景处理
            self.send_keys('xpath', ele_user, user, 3)  # 浏览器已记录用户账号密码的可注释该两步操作，直接手动输入验证码
            self.send_keys('xpath', ele_pwd, pwd, 3)
            # 手动输入验证码
            approve_center_locator = ('xpath', approve_center)
            self.wait_until_present(approve_center_locator, 10)
            loger.info("demo主页登录完成，请重新运行程序")

        else:
            approve_center_locator = ('xpath', approve_center)
            self.wait_until_present(approve_center_locator)
            # 打开这几个审核页
            self.click_button_xpath(approve_center, 1)  # 审批中心
            self.click_button_xpath(transfer_manage, 1)  # 转件管理
            self.click_button_xpath(audit_transfer, 1)  # 信审转件
            self.click_button_xpath(task_manage, 1)  # 任务管理
            self.click_button_xpath(phone_approve_task, 1)  # 电审
            self.click_button_xpath(audit_approve_task, 1)  # 信审
            self.click_button_xpath(audit_transfer_tag, 1)  # 转件页签

    def into_iframe(self, iframe):
        iframe_ele = self.find_element_by_xpath(iframe)
        self.to_iframe(iframe_ele)
        time.sleep(3)

    def close_driver(self):
        # 提供一个方法用于在使用完类实例后关闭driver
        self.driver.quit()

    def pre_audit_process(self, order_num):
        # 信审流程
        self.click_button_xpath(audit_approve_tag)  # 信审任务
        self.into_iframe(self.iframe_audit_approve)
        self.send_keys_with_clear('xpath', order_input, order_num)  # 输入订单编号
        self.click_button_xpath(query_button)  # 查询

    def pre_phone_process(self, order_num):
        # 执行电审流程的操作
        self.click_button_xpath(phone_approve_tag)  # 电审任务
        self.into_iframe(self.iframe_phone_approve)
        self.send_keys_with_clear('xpath', order_input, order_num)  # 输入订单编号
        self.click_button_xpath(query_button)  # 查询

    def perform_audit_process(self):
        # 执行信审流程的操作
        self.click_button_xpath(handle_button)  # 我要办理
        self.uniframe()  # 退出信审查询iframe框
        # 审批页iframe框待处理
        self.into_iframe(iframe_task_detail)
        approval_opinion_select_locator = ('xpath', approval_opinion_select)
        self.wait_until_present(approval_opinion_select_locator)
        self.click_button_xpath(approval_opinion_select, 1)  # 审批意见
        self.click_button_xpath(approve_pass, 1)  # 通过选项
        self.click_button_xpath(second_opinion, 1)  # 二级意见
        self.click_button_xpath(full_agree, 1)  # 完全同意
        self.send_keys('xpath', approval_remark, '同意')  # 审批备注
        if self.add_material == '是':   # 走加收材料路线
            self.click_button_xpath(add_material, 1)
            self.send_keys('xpath', material_input, '居住证')
            self.click_button_xpath(submit_button, 1)  # 提交
            time.sleep(2)
        elif self.add_material == '否':
            self.click_button_xpath(no_addition, 1)  # 不加收材料
            self.click_button_xpath(submit_button, 1)  # 提交
            time.sleep(2)
        else:
            self.click_button_xpath(submit_button, 1)  # 提交
            time.sleep(2)
        if self.is_element_exist('xpath', comfirm_button):  # 订阅不需要关注人确认
            self.click_button_xpath(comfirm_button, 5)  # 确定
            time.sleep(2)
            self.uniframe()
            audit_transfer_tag_locator = ('xpath', audit_transfer_tag)
            self.wait_until_present(audit_transfer_tag_locator, 5)
            self.click_button_xpath(audit_transfer_tag, 1)  # 转件页签
        else:
            self.uniframe()
            audit_transfer_tag_locator = ('xpath', audit_transfer_tag)
            self.wait_until_present(audit_transfer_tag_locator, 5)
            self.click_button_xpath(audit_transfer_tag, 1)  # 转件页签

    def perform_phone_process(self):
        # 电审操作
        self.click_button_xpath(handle_button)  # 我要办理
        self.uniframe()  # 退出电审查询iframe框
        self.into_iframe(iframe_phone_task)  # 进入我要办理iframe框
        approval_opinion_select_locator = ('xpath', approval_opinion_select)
        self.wait_until_present(approval_opinion_select_locator)
        self.click_button_xpath(approval_opinion_select, 1)  # 审批意见
        self.click_button_xpath(approve_pass, 1)  # 通过选项
        self.click_button_xpath(second_opinion, 1)  # 二级意见
        self.click_button_xpath(full_agree, 1)  # 完全同意
        self.send_keys('xpath', approval_remark, '同意')  # 审批备注
        if self.is_element_exist('xpath', no_addition):  # 订阅加收材料处理
            self.click_button_xpath(no_addition, 1)  # 不加收材料
            self.click_button_xpath(submit_button, 1)  # 提交
            time.sleep(3)
        else:
            self.click_button_xpath(submit_button, 1)  # 提交
            time.sleep(3)
        if self.is_element_exist('xpath', comfirm_button):  # 订阅不需要关注人确认
            self.click_button_xpath(comfirm_button, 5)  # 确定
            time.sleep(3)
            self.uniframe()
            audit_transfer_tag_locator = ('xpath', audit_transfer_tag)
            self.wait_until_present(audit_transfer_tag_locator, 5)
            self.click_button_xpath(audit_transfer_tag, 1)  # 转件页签
        else:
            self.uniframe()
            audit_transfer_tag_locator = ('xpath', audit_transfer_tag)
            self.wait_until_present(audit_transfer_tag_locator, 5)
            self.click_button_xpath(audit_transfer_tag, 1)  # 转件页签

    def transfer_order(self):
        # 转件操作
        self.click_button_xpath(transfer_checkbox, 1)  # 信审转件checkbox
        self.click_button_xpath(transfer_button, 1)  # 转件按钮
        self.click_button_xpath(self.transfer_staff, 1)  # 转件处理人：测试审批人
        self.click_button_xpath(transfer_confirm, 1)  # 转件确定
        self.uniframe()

    # 信审主流程
    def approve_process(self, order_num, max_loops=4):
        try:
            # 循环转件处理 若设置了最大循环次数且已达到上限，则停止循环
            loop_count = 0
            while True:
                # 若设置了最大循环次数且已达到上限，则停止循环
                if max_loops is not None and loop_count >= max_loops:
                    break

                for _ in range(3):
                    # 信审iframe框处理
                    self.into_iframe(self.iframe_transfer)
                    self.send_keys_with_clear('xpath', order_input, order_num)
                    # 信审转件操作
                    self.click_button_xpath(query_button)
                    if not self.is_element_exist('xpath', no_data_ele):
                        # 如果找到了订单信息，则跳出循环进行转件给审核员测试用户可在data.ini文件中修改 transfer_staff
                        if self.is_element_exist('xpath', handler):  # 当前处理人是测试审批人时候，进行审核操作,不是则转件
                            self.uniframe()
                            self.pre_audit_process(order_num)
                            if self.is_element_exist('xpath', no_data_ele):  # 查无数据即开始电审流程
                                self.uniframe()
                                # 电审流程
                                self.pre_phone_process(order_num)
                                self.perform_phone_process()
                            else:
                                self.perform_audit_process()
                            # 继续下一轮转件
                            break
                        else:
                            self.transfer_order()
                            self.pre_audit_process(order_num)
                            if self.is_element_exist('xpath', no_data_ele):  # 查无数据即开始电审流程
                                self.uniframe()
                                # 电审流程
                                self.pre_phone_process(order_num)
                                self.perform_phone_process()
                            else:
                                self.perform_audit_process()
                            # 继续下一轮转件
                            break
                    else:  # 没找到结束进程
                        loger.info(f"{order_num}信审完成,结束任务...")
                        return False
                # 每次完成一轮查找和审批流程后，计数器增加
                loop_count += 1
                logging.info(f"{order_num}已完成第{loop_count}轮转件及审批流程")

        except Exception as e:
            loger.error(f"Exception error occurred: {e}")
        finally:
            self.close_driver()  # 确保WebDriver关闭

if __name__ == '__main__':
    order_nums = ['5399514952']
    driver = webdriver.Chrome(options=chrome_options)  # 用调试模式打开driver对象
    app = ApprovalProcess(driver, 'Pre')
    app.approve_process('2411246116 ')  # 信审单号