# -*- coding:utf-8 -*-
# @FileName  :api_demom.py
# @Time      :2024/5/7 12:42
# @Author    :Daisy
# @Brief Introduction    :

import os
import requests

from data.path_config import data_path
from public.utils.readini import ReadIni


def get_order_detail():
    # 配置文件路径
    cookie_ini = os.path.join(data_path, 'cookie.ini')

    # 读取配置文件
    c = ReadIni(cookie_ini)
    jsession_id = c.getini('cookie 2', 'value')
    acw_tc = c.getini('cookie 4', 'value')

    # 构建请求URL和Headers
    url = 'https://demo-uat.company.com/gateway/dragon/authApply/getPreOrderHisList'
    headers = {
        "Content-Type": "application/json",
        "Cookie": f"JSESSION={jsession_id}; token=null; acw_tc={acw_tc};XXL_JOB_LOGIN_IDENTITY=${XXL_JOB_LOGIN_IDENTITY}"  # 从环境变量或配置文件读取
    }
    body = {
        "preApproveNo": "",
        "orderNo": "",
        "custName": "",
        "custCertificateNo": "",
        "createTime": "",
        "status": "",
        "agentCode": "",
        "createId": "",
        "leaseMode": "",
        "partnerCode": "",
        "retailPlatformBizNo": "",
        "preAuthCreateTimeStart": "",
        "preAuthCreateTimeEnd": "",
        "current": 1,
        "size": 10,
        "isMaster": 1
}


    # 发起HTTP请求
    response = requests.post(url, headers=headers, json=body)
    content = response.json()
    print(content)
    # assert content.get('code') == 0


if __name__ == '__main__':
    result = get_order_detail()
