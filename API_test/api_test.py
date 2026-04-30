# -*- coding:utf-8 -*-
# @FileName  :api_test.py
# @Time      :2024/5/7 10:43
# @Author    :Daisy
# @Brief Introduction    :
import os
import locust
import requests

from data.path_config import data_path
from public.utils.readini import ReadIni


class MyUser(locust.HttpUser):  # 1.创建locust.HttpUser子类
    wait_time = locust.between(1, 2)  # 每个task执行之间的等待时间

    @locust.task
    def get_order_detail(self):
        # 配置文件路径
        cookie_ini = os.path.join(data_path, 'cookie.ini')

        # 读取配置文件
        c = ReadIni(cookie_ini)
        jsession_id = c.getini('cookie 2', 'value')
        acw_tc = c.getini('cookie 4', 'value')

        # 构建请求URL和Headers
        url = 'https://demo-uat.company.com/gateway/dragon/report/queryOrderInfo'
        headers = {
            "Content-Type": "application/json",
            "Cookie": f"JSESSION={jsession_id}; token=null; acw_tc={acw_tc}"
        }

        # 发起HTTP请求
        response = self.client.get(url, headers=headers)
        content = response.json()
        assert content.get('code') == 0
