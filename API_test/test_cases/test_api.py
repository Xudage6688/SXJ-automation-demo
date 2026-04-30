# -*- coding:utf-8 -*-
# @FileName  :test_api.py
# @Time      :2024/5/7 16:22
# @Author    :Daisy
# @Brief Introduction    :
import os

import pytest
import requests

from API_test.utils.yaml_util import YamlUtils
from data.path_config import yaml_path_api
class TestDemoApi:
    @pytest.mark.parametrize('args', YamlUtils(yaml_path_api+'/demo_api.yaml').read_yaml())
    # @pytest.mark.parametrize('args', YamlUtils('test_api.yaml').read_yaml())
    def test_send_request(self, args):
        url = args['request']['url']
        method = args['request']['method'].lower()
        headers = args['request']['headers']
        params = args['request']['params']
        if method == 'get':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'post':
            response = requests.post(url, headers=headers, params=params, json=params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        print(response.text)

if __name__ == '__main__':
    pytest.main(['-s', 'test_api.py'])