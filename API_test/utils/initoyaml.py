# -*- coding:utf-8 -*-
# @FileName  :initoyaml.py
# @Time      :2024/5/13 17:31
# @Author    :Daisy
# @Brief Introduction    : 把Demo融资租赁服的cookie写到demo_api.yaml里
import configparser
import yaml
from data.path_config import cookie_ini, yaml_path
def ini_to_yaml(ini_path, yaml_path):
    config = configparser.ConfigParser()
    config.read(ini_path)
    cookies = []
    for section in config.sections():
        if section != 'cookies':  # 如果有多个节，确保只处理'cookies'节
            continue
    #
        for option in config.options(section):
            cookie = {
                'name': option,
                'value': config.get(section, option),
            }
            cookies.append(cookie)

    print(cookie)
    # with open(yaml_path, 'w') as f:
    #     yaml.safe_dump({'cookies': cookies}, f, default_flow_style=False)

ini_to_yaml(cookie_ini, yaml_path)
