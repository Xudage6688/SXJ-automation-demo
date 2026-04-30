# Demo 自动化测试框架

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green)](https://www.selenium.dev/)
[![pytest](https://img.shields.io/badge/pytest-7.x-orange)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> 某车企金融业务全栈自动化测试框架 - 支持 Web UI 自动化与 API 接口测试

## 项目亮点

- **POM 架构设计** - 采用 Page Object Model 模式，实现页面元素与业务逻辑分离
- **分层架构** - 清晰的测试层、页面层、核心层、工具层分层设计
- **多环境支持** - 支持 UAT/PRE/PROD 环境配置切换
- **双模测试** - 同时支持 UI 自动化测试和 API 接口测试
- **数据驱动** - 测试数据外部化，支持 YAML/INI 配置管理
- **丰富报告** - 集成 Allure 和 HTMLTestRunner 双报告系统

## 技术栈

| 分类 | 技术 |
|------|------|
| 语言 | Python 3.8+ |
| 框架 | Selenium 4.x, pytest 7.x |
| 报告 | Allure, HTMLTestRunner |
| 接口 | requests, PyYAML |
| 工具 | openpyxl, xmind |

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                      Test Cases                             │
│                    测试用例层                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Page Objects                              │
│                  页面对象层                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Core Framework                         │
│                    核心框架层                               │
└─────────────────────────────────────────────────────────────┘
```

详见 [架构设计文档](docs/ARCHITECTURE.md)

## 目录结构

```
demo-automation/
├── cases/              # 测试用例
│   ├── test_subscription.py      # 订阅业务测试
│   ├── test_pre_audit.py         # 预审流程测试
│   ├── test_sign_order.py        # 签约流程测试
│   └── ...
├── core/               # 核心框架
│   └── basepage.py     # BasePage 封装
├── page_object/        # 页面对象
│   ├── pre_audit.py    # 预审页面
│   ├── sign_order.py   # 签约页面
│   └── ...
├── public/utils/       # 工具函数
├── data/               # 测试数据与配置
├── API_test/           # API 测试模块
├── temp/               # 测试报告输出
├── conftest.py         # pytest fixtures
├── pytest.ini          # pytest 配置
└── main.py             # 入口文件
```

## 业务覆盖

### 测试模块

| 模块 | 功能 | 测试场景 |
|------|------|----------|
| 登录 | 用户认证 | 登录验证、权限检查 |
| 预审 | 客户预审 | 资质审核、风险评估 |
| 提报 | 订单提报 | 信息录入、数据校验 |
| 签约 | 合同签署 | 电子签章、合同生成 |
| 请款 | 资金申请 | 放款流程、资金核对 |
| 审批 | 信审流程 | 审批流转、状态跟踪 |
| 订阅 | 订阅业务 | 个人/企业订阅 |

### 测试标记

```python
@pytest.mark.smoke              # 冒烟测试
@pytest.mark.personalOrder      # 个人订单
@pytest.mark.enterpriseOrder    # 企业订单
@pytest.mark.preaudit           # 预审流程
```

## 快速开始

### 环境准备

```bash
# 克隆项目
git clone https://github.com/example/demo-automation.git

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 配置

1. 复制配置模板
```bash
cp .env.example .env
```

2. 修改配置文件
```ini
# data/data.ini
[uat]
username = your_username
password = your_password
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行指定标记
pytest -m smoke

# 生成 Allure 报告
pytest --alluredir ./temp/allure/reports
allure serve ./temp/allure/reports

# 运行 HTML 报告
python main.py
```

## 设计模式

项目运用了多种设计模式：

- **工厂模式**: BasePage 作为抽象工厂
- **单例模式**: WebDriver 实例管理
- **策略模式**: 多环境配置切换
- **装饰器模式**: 日志记录与重试机制

## 最佳实践

1. **显式等待优于隐式等待**: 使用 `WebDriverWait`
2. **配置外部化**: 敏感信息使用环境变量
3. **日志规范**: 使用 logging 模块
4. **类型提示**: 添加类型注解
5. **异常处理**: 明确捕获特定异常

## 文档

- [架构设计](docs/ARCHITECTURE.md)
- [技术栈](docs/TECH_STACK.md)

## License

[MIT License](LICENSE)

## Author

**Xudage6688**

- GitHub: [@Xudage6688](https://github.com/Xudage6688)
