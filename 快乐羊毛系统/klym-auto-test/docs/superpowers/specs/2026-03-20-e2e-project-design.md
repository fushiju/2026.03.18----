# 快乐羊毛 E2E 自动化测试项目设计文档

> **项目名称**：klym-auto-test
> **文档版本**：V1.0
> **编写日期**：2026-03-20
> **技术栈**：Python + pytest + requests + Playwright
> **项目路径**：`D:\测试2026.03.09\快乐羊毛系统\klym-auto-test\`

---

## 一、项目概述

基于快乐羊毛平台的详细需求文档（V3.0）、测试策略文档（V1.0）和完整测试用例，搭建接口自动化 + UI 自动化测试项目。

### 1.1 设计目标

- 接口测试和 UI 测试分层独立，按功能模块组织用例
- 适配"边开发边提测"的节奏，模块可独立开发和执行
- 用例文件与测试策略文档章节（4.1-4.11）一一对应
- 支持灵活的标记组合执行（P0/P1/P2、冒烟、模块）

### 1.2 被测系统

| 端 | 地址 | 账号 |
|----|------|------|
| 管理后台 | https://red.jinyedaojia.com/ | admin / admin123 |
| 今夜到家后台（旧） | https://develop1.jinyedaojia.com/ | admin / admin#$% |

### 1.3 技术选型

| 组件 | 选择 | 理由 |
|------|------|------|
| 测试框架 | pytest | 灵活、插件丰富、参数化方便 |
| 接口请求 | requests | 轻量、直观 |
| UI 自动化 | playwright (Python) | 自动等待、支持录制、API 拦截 |
| 报告 | pytest-html + allure（可选） | 清晰的测试结果展示 |
| 日志 | loguru | 简单好用 |
| 数据驱动 | pytest.mark.parametrize + JSON | 测试数据和逻辑分离 |

---

## 二、项目结构

```
klym-auto-test/
├── api/                          # 接口自动化
│   ├── client.py                 # HTTP 客户端封装（登录态管理、请求/响应日志）
│   ├── cases/                    # 按功能模块分文件
│   │   ├── test_login.py              # 登录鉴权接口
│   │   ├── test_commission.py         # 分佣系统（P0）
│   │   ├── test_dining_system.py      # 餐饮折扣-系统直连（P0）
│   │   ├── test_dining_manual.py      # 餐饮折扣-人工辅助（P0）
│   │   ├── test_order_state.py        # 订单状态机（P0）
│   │   ├── test_payment.py            # 支付流程（P0）
│   │   ├── test_virtual_goods.py      # 虚拟商品（P0）
│   │   ├── test_product_sync.py       # 选品仓库（P1）
│   │   ├── test_withdraw.py           # 提现结算（P1）
│   │   ├── test_excel_import.py       # Excel佣金导入（P1）
│   │   ├── test_permission.py         # 权限与越权（P1）
│   │   └── test_security.py           # 安全测试（注入/篡改）
│   └── conftest.py               # API 测试 fixtures
├── ui/                           # UI 自动化
│   ├── pages/                    # Page Object Model
│   │   ├── base_page.py               # 基础页面（通用操作封装）
│   │   ├── login_page.py             # 登录页
│   │   ├── dashboard_page.py         # 数据概况页
│   │   ├── commission_page.py        # 分佣配置页
│   │   ├── order_page.py             # 订单管理页
│   │   ├── product_sync_page.py      # 选品仓库页
│   │   ├── merchant_page.py          # 商家/加盟管理页
│   │   ├── finance_page.py           # 财务管理页
│   │   └── system_page.py            # 系统设置页
│   ├── cases/                    # UI 测试用例
│   │   ├── test_login.py
│   │   ├── test_commission.py
│   │   ├── test_order.py
│   │   ├── test_product_sync.py
│   │   └── ...
│   └── conftest.py               # UI 测试 fixtures（浏览器启动等）
├── common/                       # 共享工具
│   ├── config.py                 # 环境配置（URL、账号密码）
│   ├── logger.py                 # 日志工具
│   ├── db.py                     # 数据库连接（可选）
│   └── data/                     # 测试数据
│       ├── commission_data.json       # 分佣测试数据
│       ├── dining_data.json           # 餐饮折扣测试数据
│       └── test_files/                # 测试文件（图片、Excel等）
├── reports/                      # 测试报告输出
├── screenshots/                  # 失败截图
├── conftest.py                   # 全局 fixtures
├── pytest.ini                    # pytest 配置
├── requirements.txt              # 依赖
└── README.md                     # 使用说明
```

---

## 三、核心模块设计

### 3.1 API Client 封装

由于没有 API 文档，采用渐进式抓包补充策略。

```python
class KLYMClient:
    def __init__(self, base_url, username, password):
        self.session = requests.Session()
        self.base_url = base_url
        self.login(username, password)

    def request(self, method, path, **kwargs):
        # 统一请求：自动带 token、记录日志、断言状态码
        ...

    def login(self, username, password):
        # 登录获取 token/cookie
        ...
```

功能要点：
- 登录后自动维护 cookie/token
- 所有请求自动记录日志（方便调试和抓包补充接口）
- 支持多角色切换（admin、商家主账号、门店子账号）

### 3.2 Page Object Model

```python
class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, menu, submenu=None): ...
    def wait_loading(self): ...
    def get_table_data(self): ...
    def screenshot_on_fail(self): ...
```

各业务页面继承 BasePage，封装该页面特有操作。

### 3.3 测试数据驱动

分佣计算等场景使用参数化，测试数据来自 JSON 文件，与深度测试方案中的用例编号对应：

```python
@pytest.mark.parametrize("case", load_data("commission_data.json"))
def test_commission_basic(api_client, case):
    ...
```

### 3.4 pytest 标记体系

```ini
markers =
    p0: P0 阻塞上线用例
    p1: P1 重要用例
    p2: P2 一般用例
    api: 接口测试
    ui: UI 测试
    smoke: 冒烟测试
    commission: 分佣系统
    dining: 餐饮折扣
    order: 订单管理
    payment: 支付流程
    security: 安全测试
```

执行示例：
- `pytest -m "p0 and api"` — P0 接口用例
- `pytest -m smoke` — 冒烟测试
- `pytest -m commission` — 分佣模块全量
- `pytest api/` — 全部接口测试
- `pytest ui/` — 全部 UI 测试

### 3.5 Fixtures 设计

```python
# 全局 fixtures - 各角色登录态
@pytest.fixture(scope="session")
def admin_client():        # 后台管理员

@pytest.fixture(scope="session")
def merchant_client():     # 商家品牌主账号

@pytest.fixture(scope="session")
def store_client():        # 门店子账号

@pytest.fixture(scope="session")
def browser():             # Playwright 浏览器实例

@pytest.fixture
def admin_page(browser):   # 已登录的后台页面
```

---

## 四、功能模块与用例文件对应关系

| 测试策略章节 | 优先级 | API 用例文件 | UI 用例文件 |
|------------|--------|------------|-----------|
| 4.1 分佣系统 | P0 | test_commission.py | test_commission.py |
| 4.2 餐饮折扣-系统直连 | P0 | test_dining_system.py | test_dining_system.py |
| 4.2 餐饮折扣-人工辅助 | P0 | test_dining_manual.py | test_dining_manual.py |
| 4.3 订单状态机 | P0 | test_order_state.py | test_order.py |
| 4.4 选品仓库 | P1 | test_product_sync.py | test_product_sync.py |
| 4.5 外卖模块 | P2 | (待提测) | (待提测) |
| 4.6 电影票务 | P2 | (待提测) | (待提测) |
| 4.7 会员充值 | P2 | (待提测) | (待提测) |
| 4.8 个人中心 | P2 | (待提测) | (待提测) |
| 4.9 商家端 | P1 | test_permission.py | (待提测) |
| 4.10 后台管理 | P1 | test_excel_import.py | (待提测) |
| 安全测试 | P1 | test_security.py | — |
| 提现结算 | P1 | test_withdraw.py | (待提测) |

---

## 五、适配"提一点测一点"的策略

1. 每个功能模块独立文件，开发提测一个模块就补一个文件
2. 接口用例先写（抓包获取接口），UI 用例后补
3. 用 `@pytest.mark.skip(reason="待提测")` 标记未提测模块
4. 新增模块只需：
   - 抓接口加到 `api/cases/`
   - 加 Page Object 到 `ui/pages/`
   - 写用例到对应 cases 目录

---

*文档结束*
