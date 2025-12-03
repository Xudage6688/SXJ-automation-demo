# SXJ_Automation

#### 介绍
SXJ项目python+selenium自动化

#### 软件架构
软件架构说明
python+selenium+pytest

#### pycharm+gitee安装教程

https://blog.csdn.net/qq_38428735/article/details/120604984?ops_request_misc=&request_id=&biz_id=102&utm_term=%E5%A6%82%E4%BD%95%E7%94%A8pycharm+gitee%E6%9D%A5%E5%9B%A2%E9%98%9F%E5%90%88%E4%BD%9C%E5%BC%80%E5%8F%91%E9%A1%B9%E7%9B%AE&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-3-120604984.142^v99^pc_search_result_base7&spm=1018.2226.3001.4187

#### selenium包+谷歌驱动调试教程

https://blog.csdn.net/qq_43125235/article/details/125601564?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522171099127216800215090320%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=171099127216800215090320&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-125601564-null-null.142^v99^pc_search_result_base7&utm_term=pycharm%20selenium&spm=1018.2226.3001.4187

#### 目录说明
采用POM模式
1.  API_test用于接口调试，无需关注
2.  cases 存放测试用例
3.  core 封装selenium和常用操作
4.  data 存放配置文件、元素文件、目录文件
5.  page_object 存放页面对象操作：信审订单、预审、提交、签约、请款、订阅
6.  public 封装了一些小方法：获取cookie、获取短链手机号、读取ini文件、输出报告、生成车架号
7.  temp 存放allure测试报告
8.  test 调试代码用，无需关注
9.  testdata 项目用到的测试数据
10.  xmind xmind输出为csv用例小工具


#### 使用说明
前置条件：selenium包安装，谷歌驱动与自己版本一致。

1.  所有的用户信息都在data.ini配置 uat对应uat环境参数，以此类推。
2.  先执行get cookie获取用户信息
3.  页面操作都在page object里
4.  从预审pre audit到请款request pay
5.  信审
6.  提报、签约、请款、信审后续文审都是使用Chrome调试模式具体方法：
    i. 浏览器右键属性
    ii. 本地谷歌浏览器域名后增加以下代码（注意前面有个空格）：--remote-debugging-port=9222 --user-data-dir="D:\selenium\AutomationProfile\selenium"       文件夹放本地selenium包路径
    iii. 运行代码前手动打开浏览器，登陆app or sxj主页 完成信息预录入。
    iiii. 正常运行代码即可
7. 客户预审和签约 main传参客户手机号


