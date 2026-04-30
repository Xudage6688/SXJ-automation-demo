# # -*- coding:utf-8 -*-
# # @FileName  :test_draft_home.py
# # @Time      :2024/1/27 18:46
# # @Author    :Daisy
# import os
#
# import allure
# import pytest
# from selenium import  webdriver
# from page_object.draft_demologin import draftHome
# @allure.feature("测试Demo融资租赁查询中心")
# class TestDraftHome:
#     def setup_class(self):
#         self.driver = webdriver.Chrome()
#         self.dh = draftHome(self.driver)
#
#     @allure.story("依次点击查询中心子tab页面")
#     @pytest.mark.parametrize('data',[" 订单列表 "," 预审结果查询 "," 签约结果查询 "])
#     def test_queryCenter(self,data):
#         self.dh.pre_auditTab(data)
#         allure.attach(self.driver.get_screenshot_as_png(),data+"截图")
#
#     # @pytest.mark.parametrize('data', [" 订单信息查询 ", " 对公合同信息查询 ", " 佣金查询 "])
#     # def test_saleCenter(self,data):
#     #     self.dh.sale_center(data)
#
#     def teardonw_class(self):
#         self.dh.quit()
#
# if __name__ == '__main__':
#     pytest.main(['-vs','--alluredir=../temp/allure/reports','--clean-alluredir','./test_draft_home.py'])    # 中间生成allure报告路径
#     os.system("allure serve ../temp/allure/reports")  # 添加allure服务，生成报告路径
