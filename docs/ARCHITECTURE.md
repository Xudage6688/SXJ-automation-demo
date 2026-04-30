# 架构设计文档

## 项目概述

Demo 自动化测试框架是一个面向金融业务的全栈自动化测试解决方案，支持 Web UI 自动化测试和 API 接口测试。

## 设计原则

### 1. Page Object Model (POM) 模式

采用 POM 设计模式，将页面元素定位与业务逻辑分离，提高代码可维护性和复用性。

```
┌─────────────────────────────────────────────────────────────┐
│                      Test Cases (cases/)                    │
│                    测试用例层 - 业务验证逻辑                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Page Objects (page_object/)               │
│                  页面对象层 - 封装页面操作                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Core (core/)                           │
│                    核心框架层 - 基础封装                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Selenium WebDriver                       │
│                      底层驱动                                │
└─────────────────────────────────────────────────────────────┘
```

### 2. 分层架构

| 层级 | 目录 | 职责 |
|------|------|------|
| 测试层 | `cases/` | 测试用例定义、数据驱动、断言验证 |
| 页面层 | `page_object/` | 页面元素定位、操作封装、业务流程 |
| 核心层 | `core/` | WebDriver 封装、通用方法、日志管理 |
| 工具层 | `public/utils/` | 配置读取、Cookie 管理、报告生成 |
| 数据层 | `data/` | 配置文件、测试数据、元素定义 |
| API层 | `API_test/` | 接口测试、YAML 用例、配置管理 |

### 3. 模块职责

#### 核心模块 (core/)

- `basepage.py`: 封装 Selenium WebDriver 常用操作
  - 元素定位统一封装
  - 显式/隐式等待
  - iframe 切换
  - 截图功能
  - 日志记录

#### 页面对象模块 (page_object/)

| 文件 | 业务模块 | 主要功能 |
|------|----------|----------|
| `draft_demologin.py` | 登录模块 | 用户登录、权限验证 |
| `pre_audit.py` | 预审模块 | 客户预审、资质审核 |
| `submit_order.py` | 提报模块 | 订单提报、信息录入 |
| `sign_order.py` | 签约模块 | 合同签署、电子签章 |
| `request_pay.py` | 请款模块 | 资金申请、放款流程 |
| `approve_order.py` | 审批模块 | 信审流程、审批操作 |
| `subscription_app.py` | 订阅模块 | 个人/企业订阅业务 |

#### 工具模块 (public/utils/)

- `get_cookie.py`: Cookie 获取与管理
- `readini.py`: INI 配置文件读取
- `reports_out.py`: HTML 测试报告生成
- `get_phone_code.py`: 验证码获取
- `Vin_Genarate.py`: 车架号生成工具

### 4. 数据驱动

测试数据与代码分离，支持多环境配置：

```
data/
├── data.ini          # UAT 环境配置
├── pre_cookie.ini    # PRE 环境配置
├── elements.py       # 元素定位配置
└── path_config.py    # 路径配置
```

### 5. 测试框架集成

```
pytest
├── fixtures (conftest.py)    # 测试夹具
├── markers (pytest.ini)      # 用例分类标记
├── allure reports            # 测试报告
└── HTML reports              # HTML 报告
```

## 设计模式应用

### 工厂模式
- `BasePage` 作为抽象工厂
- 各 Page Object 继承并实现具体操作

### 单例模式
- WebDriver 实例管理
- 配置文件读取器

### 策略模式
- 多环境配置切换
- 不同浏览器的 Driver 策略

### 装饰器模式
- 日志记录装饰器
- 重试机制装饰器

## 扩展性设计

### 1. 多环境支持
通过配置文件切换 UAT/PRE/PROD 环境

### 2. 并行执行
支持 pytest-xdist 并行测试

### 3. 报告集成
- Allure 报告
- HTMLTestRunner 报告
- 日志文件

### 4. CI/CD 集成
支持 Jenkins、GitLab CI 等持续集成平台

## 目录结构

```
demo-automation/
├── cases/              # 测试用例
├── core/               # 核心框架
├── page_object/        # 页面对象
├── public/             # 公共工具
│   └── utils/          # 工具函数
├── data/               # 测试数据
├── API_test/           # API 测试
│   ├── api_keys/       # API 密钥配置
│   ├── conf/           # API 配置
│   ├── test_cases/     # API 测试用例
│   └── utils/          # API 工具
├── temp/               # 临时文件（报告等）
├── testData/           # 测试数据文件
├── conftest.py         # pytest 配置
├── pytest.ini          # pytest 设置
└── main.py             # 入口文件
```

## 最佳实践建议

1. **显式等待优于隐式等待**: 使用 `WebDriverWait` 替代 `time.sleep()`
2. **配置外部化**: 敏感信息使用环境变量
3. **日志规范**: 使用 logging 模块替代 print
4. **类型提示**: 添加类型注解提高代码可读性
5. **异常处理**: 明确捕获特定异常，避免裸 except