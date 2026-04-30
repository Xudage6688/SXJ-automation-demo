import csv
import os

import xmindparser

xmindparser.config = {
    'showTopicId':False, #是否展示主题ID
    'hideEmptyValue': True #是否隐藏空值
}

class rowInCSV:
    def __init__(self):
        self.vsxj=""
        self.title=""
        self.level="Medium: P2"
        self.impactVersion=""
        self.repairVersion=""
        self.module=""
        self.tag=""
        self.stepId=""
        self.step=""
        self.excepted_result=""

filePath = 'D:\项目\Demo\需求\订阅-扣收定金.xmind'





def read_node(node_lists,rowslist,module,step):
    if len(node_lists)>=0:
      for node in node_lists['topics']:
          if not list(node.keys()).__contains__('topics'):
             row = rowInCSV()
             setattr(row,'module',module)
             setattr(row, 'step', "".join(step))
             setattr(row, 'excepted_result', node['title'])
             setattr(row, 'title', "【"+module+"】"+step[0].replace(',','')+"-"+step[-1].replace(',','')+"-"+node['title'])
             rowslist.append(row)
          else:
              if len(step)==0:
                  step.append(node['title'])
              else:
                  step.append("," + node['title'])
              read_node(node,rowslist,module,step)
              step.pop()
      return rowslist

def is_csv_empty(file_path):
    with open(file_path, 'r', newline='',encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            return False  # 如果能读取到数据，文件不为空，返回False
    return True  # 如果未读取到数据，文件为空，返回True
              
def addline(filePath,row):
    with open(filePath, 'a+', newline="",encoding='utf-8') as csvfile:
        fieldnames = ['需求', '标题', '优先级', '影响版本', '修复的版本', '模块', '标签', '步骤ID', '步骤', '期望结果']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
        reader = csv.reader(csvfile, delimiter=',')
        if is_csv_empty(filePath):
            writer.writeheader();
        writer.writerow({'需求': row.vsxj, '标题': row.title, '优先级': row.level, '影响版本': row.impactVersion,
                         '修复的版本': row.repairVersion, '模块': row.module, '标签': row.tag, '步骤ID': row.stepId,
                         '步骤': row.step, '期望结果': row.excepted_result})

def delFile(filePath):
    if os.path.exists(filePath):
        os.remove(filePath)




if __name__ == '__main__':
    content = xmindparser.xmind_to_dict(filePath)
    node_lists = content[0]['topic']['topics']
    case_list = []
    for node_list in node_lists:
        module = node_list['title']  # 模块名称
        rowslist = []
        step=[]
        case_list.append(read_node(node_list,rowslist,module,step))
    delFile("D:\项目\Demo\插入应还款数据.csv")
    delFile("D:\项目\Demo\系统自动发盘.csv")
    delFile("D:\项目\Demo\手动重新扣款.csv")
    delFile("D:\项目\Demo\场景.csv")
    for rowlist in case_list:
        for row in rowlist:
            if row.module == "插入应还款数据":
                setattr(row, 'vsxj', 'REQ-6965')
                addline("D:\项目\Demo\插入应还款数据.csv", row)
            elif row.module == "系统自动发盘":
                setattr(row, 'vsxj', 'REQ-6476')
                addline("D:\项目\Demo\系统自动发盘.csv", row)
            elif row.module == "手动重新扣款":
                setattr(row, 'vsxj', 'REQ-6477')
                addline("D:\项目\Demo\手动重新扣款.csv", row)
            else:
                setattr(row, 'vsxj', 'REQ-7021')
                addline("D:\项目\Demo\场景.csv", row)