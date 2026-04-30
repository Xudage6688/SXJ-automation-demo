import time

from webdriver_helper import get_webdriver
from selenium.webdriver.common.by import By

driver = get_webdriver()

driver.get("https://demo-uat.company.com/ant-web/home")
driver.maximize_window()
# driver.get_screenshot_as_file("DEMO.png")

cookies = [{'domain': 'demo-uat.company.com', 'expiry': 1706241625, 'httpOnly': False, 'name': 'token', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'null'},
           {'domain': 'demo-uat.company.com', 'expiry': 1706155279, 'httpOnly': False, 'name': 'RANDOM_CODE', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '21c67a87-d89f-4d21-89ee-6655dab80613'},
           {'domain': 'demo-uat.company.com', 'expiry': 1706241625, 'httpOnly': False, 'name': 'JSESSION', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': 'q7Vm+Eq9lhIPwdUxFuDhvkUiBbnzXh7Z4RcGpwopk9I='},
           {'domain': 'demo-uat.company.com', 'expiry': 1706157017, 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '2f624a1a17061552171408933e34441fbd9442a2610373b961396ec67f1fb9'}]
driver.delete_all_cookies()
for cookie in cookies:
    if 'expiry' in cookie:  # 有的cookie里面有这个参数，有的没有。有的话，需要做处理。
        del cookie['expiry']   # 这个expiry参数值得类型会影响到登录识别，所以需要删掉或者更改值为整形
    driver.add_cookie(cookie)
driver.refresh()


time.sleep(10)
driver.quit()
"""
account = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div/div[2]/form/div[1]/div/div/div/input')
print(account)

print(account.tag_name) #元素标签
print(account.rect) #冤死大小 位置

account.send_keys("测试用户") #输入内容
print("账号",account.get_attribute("value"))  #获取账号元素
account.screenshot("zhanghao.png") #为账号元素截图

password = driver.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div/div[2]/form/div[2]/div/div/div/input')
password.send_keys("${TEST_PASSWORD}")  # 从环境变量或配置文件读取

print("密码",password.get_attribute('value'))
"""













