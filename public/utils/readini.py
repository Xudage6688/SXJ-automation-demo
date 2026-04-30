# -*- coding:utf-8 -*-
# @FileName  :readini.py
# @Time      :2024/1/27 14:16
# @Author    :Daisy
"""
此模块是用来读取ini文件内容的
"""

from data.path_config import *
from configparser import ConfigParser
data_ini =os.path.join(os.path.abspath(data_path), 'data.ini')  #拿到 data.ini文件的路径


# p = configparser.ConfigParser()
#方法1 绝对路径法
# p.read(r'C:\Users\Xu\PycharmProjects\pythonProject2\data\data.ini',encoding='utf-8')
# 方法2 引用路径法
# p.read(data_ini,encoding='utf-8')
# phone_url = p.get('uat','phone_url')
# demo_loginurl = p.get('uat','demo_loginurl')
# demo_homepage = p.get('uat','demo_homepage')
# user = p.get('uat','user')
# password = p.get('uat','password')
# account = p.get('uat','ele_userInput')
# pwd = p.get('uat','ele_userPwd')
# print(phone_url,demo_loginurl,demo_homepage,user,password)

class ReadIni(ConfigParser):
    def __init__(self, filename: object) -> object:
        #继承父类的构造函数 常规写法
        # ConfigParser.__init__(self)
        #继承父类的构造函数 使用super函数
        super(ReadIni,self).__init__()
        #通过self对象调用父类的read方法
        self.read(filename, encoding='utf-8')

    def getini(self,section,option):
        #通过self对象调用父类的get方法 用value变量接收 并且返回value值
        value = self.get(section,option)
        return value


# p = ReadIni(data_ini)
# url = p.getini('uat','phone_url')
# print(url)
