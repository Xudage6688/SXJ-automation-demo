# -*- coding:utf-8 -*-
# @FileName  :userData_test.py
# @Time      :2024/3/4 18:59    路径后需要有selenium驱动
# @Author    :Daisy    cmd：C:\Users\Xu\AppData\Local\Google\Chrome\Application\chrome.exe
# @Brief Introduction    : 启用本地用户数据的浏览器  --remote-debugging-port=9222 --user-data-dir="D:\selenium\AutomationProfile\selenium"
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = Options()
#配置为调试模式
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
time.sleep(1)
#用调试模式打开driver对象
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://demo-uat.company.com/sale-app/view/Layout/home')
driver.find_element(By.XPATH,'//uni-view[text()="提报"]/..').click() #提报元素
time.sleep(5)
driver.find_element(By.XPATH,'//uni-view[@class="btn bg"][1]').click()  #第一个去操作
time.sleep(5)
driver.find_element(By.XPATH,'//uni-view[@class="icon iconfont icon-youjiantou_huaban icon-font"][1]').click() #第一个客户信息
time.sleep(5)
driver.find_element(By.XPATH,'//span[text()="居住地址"]/..').click() #居住地址
time.sleep(2)
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[1]/div[2]').click() #完成
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="form-currentResidenceAddress"]/uni-view/uni-view[1]/uni-view/uni-view/uni-view[2]/uni-view/uni-textarea/div/textarea').send_keys('测试录') #居住详细地址
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="form-residentialType"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #居住状况
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[1]').click() #自置
driver.find_element(By.XPATH,'//*[@id="form-marriage"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #婚姻状况
time.sleep(2)
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[1]').click() #未婚
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="form-propertyType"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #房产类型
time.sleep(2)
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[1]').click() #本地房产
time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="form-driveFilesBelong"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #驾照材料归属
time.sleep(2)
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[1]').click() #申请人
driver.find_element(By.XPATH,'//*[@id="form-driverFiles"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #驾驶类材料
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[1]').click() #驾照
driver.find_element(By.XPATH,'//*[@id="form-employment"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #就业状况
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[2]').click() #专业技术人员
driver.find_element(By.XPATH,'//*[@id="form-companyName"]/uni-view/uni-view[1]/uni-view/uni-view/uni-view/uni-view[1]/uni-view/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys('承租人单位') #单位名称
driver.find_element(By.XPATH,'//*[@id="form-companyProvince"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #单位地址
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[1]/div[2]').click() #完成
driver.find_element(By.XPATH,'//*[@id="form-companyAddress"]/uni-view/uni-view[1]/uni-view/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys('承租人单位详细地址') #单位详细地址
driver.find_element(By.XPATH,'//*[@id="form-companyPhone"]/uni-view/uni-view[1]/uni-view/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys('6802105') #单位电话
driver.find_element(By.XPATH,'//*[@id="form-custProfession"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #职业
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[2]').click() #专业技术人员
driver.find_element(By.XPATH,'//*[@id="form-workYears"]/uni-view/uni-view[1]/uni-view/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys('5') #工作年限
driver.find_element(By.XPATH,'//*[@id="active0"]/uni-form/span/uni-view[25]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #税后收入
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[3]').click() #收入档次
driver.find_element(By.XPATH,'//*[@id="form-companyNature"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #单位性质
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[1]').click() #外企
driver.find_element(By.XPATH,'//*[@id="form-industry"]/uni-view/uni-view[1]/uni-view/uni-view/uni-picker/div[2]/uni-view').click() #行业分类
driver.find_element(By.XPATH,'/html/body/uni-app/div/div[2]/div[2]/div[9]').click() #软件



