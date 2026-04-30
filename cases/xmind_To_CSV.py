#需要安装xmindparser

import os
from public.utils.readini import ReadIni
from data.path_config import data_path
import xmindparser
from XMind.xmind import read_node,delFile,addline


xmindparser.config = {
    'showTopicId':False, #是否展示主题ID
    'hideEmptyValue': True #是否隐藏空值
}

if __name__ == '__main__':
    cookie_ini = os.path.join(os.path.abspath(data_path), 'xmind.ini')
    c = ReadIni(cookie_ini)
    XmindPath = c.getini('xmind', 'xmind_Path')
    CSVPath = c.getini('xmind', 'CSV_Path')
    REQ = c.getini('xmind', 'vsxj')
    content = xmindparser.xmind_to_dict(XmindPath)
    node_lists = content[0]['topic']['topics']
    case_list = []
    for node_list in node_lists:
        module = node_list['title']  # 模块名称
        rowslist = []
        step = []
        case_list.append(read_node(node_list, rowslist, module, step))

    delFile(CSVPath)
    for rowlist in case_list:
        for row in rowlist:
            setattr(row, 'vsxj', REQ)
            addline("D:\项目\Demo\插入应还款数据.csv", row)

