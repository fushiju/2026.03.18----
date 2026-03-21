# 快乐羊毛管理后台 UI 自动化测试设计文档

**日期**: 2026-03-21
**状态**: 已确认
**范围**: 管理后台 PC Web 端，从登录模块开始

---

## 1. 背景与目标

快乐羊毛综合优惠生活服务平台的管理后台（`https://red.jinyedaojia.com/`）需要 UI 自动化测试，覆盖登录、订单、分佣、品牌管理等核心模块。

**说明**：`自动化测试/admin-web/` 下存在早期代码框架（login_page.py、conftest.py、helpers.py、case_mapping.py 等），但该框架未完成且结构不完整。本方案在 `UI自动化/` 下全新搭建，采用更清晰的分层结构。旧代码中的 `case_mapping.py`（@case 装饰器用于 Excel 追溯）设计可复用，将集成到新框架中。

**目标**：
- 基于现有 Excel 测试用例，实现数据驱动的自动化测试
- 从登录模块（10条用例）开始，逐步扩展到全部后台模块
- 框架可复用，新增模块只需添加 Page Object + 测试文件

## 2. 技术栈

| 组件 | 技术选型 | 版本 |
|------|---------|------|
| 浏览器自动化 | Playwright | >= 1.40.0 |
| 测试框架 | pytest | >= 7.4.0 |
| Playwright 集成 | pytest-playwright | >= 0.4.0 |
| HTML 报告 | pytest-html | >= 4.0.0 |
| Allure 报告 | allure-pytest | >= 2.13.0 |
| 验证码识别 | ddddocr | >= 1.4.0 |
| Excel 数据读取 | openpyxl | >= 3.1.0 |
| Python 环境 | Python | 3.14 |

## 3. 项目结构

```
UI自动化/
├── conftest.py                   # pytest fixtures（浏览器实例、登录状态、失败截图）
├── requirements.txt              # 依赖清单
├── pytest.ini                    # pytest 运行配置
│
├── config/
│   └── settings.py               # 环境配置（URL、账号、超时时间）
│
├── pages/                        # Page Object Model
│   ├── base_page.py              # 页面基类（通用等待、点击、输入、截图）
│   └── login_page.py             # 登录页封装
│
├── utils/
│   ├── captcha_solver.py         # ddddocr 验证码识别 + 重试逻辑
│   ├── excel_reader.py           # 读取 Excel 用例数据
│   └── screenshot.py             # 截图工具
│
├── tests/
│   └── test_login.py             # 登录模块测试（数据驱动，10条用例）
│
├── screenshots/                  # 失败截图存放目录
├── reports/                      # HTML/Allure 测试报告
└── 测试用例/                      # 已有 Excel 用例（只读，不修改）
```

## 4. 核心设计

### 4.1 Page Object Model

每个页面封装为一个类，测试代码只调用页面方法，不直接操作定位器。

**BasePage** 提供：
- 通用等待、点击、输入、获取文本
- 截图方法

**LoginPage** 提供：
- `goto()` — 打开登录页
- `fill_username(value)` — 输入用户名
- `fill_password(value)` — 输入密码
- `fill_captcha(value)` — 输入验证码
- `click_login()` — 点击登录按钮
- `get_captcha_image()` — 获取验证码图片二进制数据
- `click_captcha_image()` — 点击刷新验证码
- `get_error_message()` — 获取错误提示文本
- `login_with_captcha(username, password)` — 完整登录流程（含 OCR 识别 + 重试）

### 4.2 验证码处理策略

登录页有 4 位图形验证码（小写字母 + 数字）。

**推荐方案：测试环境后端关闭验证码校验**（如支持万能验证码 "1234" 或配置开关跳过校验）。这是最稳定的方案，消除 OCR 不确定性。

**降级方案：ddddocr OCR 识别**（当后端无法配置时使用）：

```
截取验证码图片 → ddddocr 识别 → 输入识别结果 → 提交登录
    ↓ 如果登录失败且提示"验证码错误"
点击刷新验证码 → 重新识别 → 重新提交（最多重试 3 次）
    ↓ 如果 3 次均失败
标记测试为 pytest.skip("验证码识别连续失败")，不计为 FAIL
```

**风险说明**：ddddocr 对混合小写字母+数字的验证码识别率约 60-80%，3 次重试后仍有 5-10% 失败概率。强烈建议优先使用测试环境绕过方案。

### 4.3 数据驱动

直接读取 `测试用例/登录.xlsx`，解析每行为一条测试数据，通过 `pytest.mark.parametrize` 参数化执行。

Excel 列映射（`登录.xlsx` Sheet "测试用例"）：

| 列序号 | 表头 | 用途 |
|--------|------|------|
| A | 所属模块 | 测试分组标记 |
| B | 用例标题 | 测试用例 ID/名称 |
| C | 前置条件 | 测试前提（如 URL 可访问） |
| D | 测试步骤 | 自动化操作序列 |
| E | 预期结果 | 断言依据 |
| F | 测试数据/备注 | 补充信息 |

第 1 行为表头，第 2 行起为数据行。

### 4.4 测试用例覆盖

| # | 用例标题 | 测试函数 | 断言 |
|---|---------|---------|------|
| 1 | 正确账号密码登录 | `test_login_success` | URL 含 `/dashboard/index`，页面显示 "admin" |
| 2 | 验证码刷新功能 | `test_captcha_refresh` | 点击后验证码图片 src 变化 |
| 3 | 空用户名登录 | `test_empty_username` | 提示 "请输入用户名" |
| 4 | 空密码登录 | `test_empty_password` | 提示 "请输入密码" |
| 5 | 空验证码登录 | `test_empty_captcha` | 提示输入验证码 |
| 6 | 验证码格式校验 | `test_captcha_format` | 提示仅限小写字母或数字 |
| 7 | 错误密码登录 | `test_wrong_password` | 提示 "用户名或密码错误" |
| 8 | 错误验证码登录 | `test_wrong_captcha` | 提示 "验证码错误"，验证码自动刷新 |
| 9 | 不存在的用户名 | `test_nonexistent_user` | 提示 "用户名或密码错误" |
| 10 | 验证用户名错误 | `test_wrong_username` | 提示用户名错误 |

### 4.5 Fixtures 设计

**登录测试用 fixtures**（每条用例独立页面，测试登录本身的各种场景）：

```python
@pytest.fixture(scope="session")
def browser():
    """会话级浏览器实例，所有测试共享"""

@pytest.fixture
def page(browser):
    """每个测试用例独立的页面上下文（function scope），登录测试需要每次全新页面"""

@pytest.fixture
def login_page(page):
    """LoginPage 对象，已导航到登录页"""

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    """测试失败时自动截图到 screenshots/ 目录"""
```

**后续模块用 fixtures**（共享已登录会话，避免重复登录）：

```python
@pytest.fixture(scope="session")
def logged_in_page(browser):
    """会话级已登录页面，供后续模块测试复用"""
```

### 4.6 配置管理

```python
# config/settings.py — 优先从环境变量读取，回退到默认值
import os

BASE_URL = os.getenv("KLYM_BASE_URL", "https://red.jinyedaojia.com/")
ADMIN_USERNAME = os.getenv("KLYM_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("KLYM_PASSWORD", "admin123")
CAPTCHA_BYPASS = os.getenv("KLYM_CAPTCHA_BYPASS", "")  # 设置万能验证码值，空则走 OCR
TIMEOUT = 10000          # 全局超时 10 秒
HEADLESS = True          # CI 用 True，调试用 False
SCREENSHOT_DIR = "screenshots/"
```

项目根目录提供 `.env.example` 示例文件，实际 `.env` 文件通过 `.gitignore` 排除。

## 5. 运行与报告

```bash
# 安装依赖
pip install -r requirements.txt
playwright install chromium

# 运行登录测试
pytest tests/test_login.py -v --html=reports/login_report.html

# 有头模式调试
pytest tests/test_login.py -v --headed

# 生成 Allure 报告
pytest tests/test_login.py --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 6. 扩展路径

登录完成后按优先级扩展：

| 阶段 | 模块 | 新增文件 |
|------|------|---------|
| 当前 | 登录 | `login_page.py` + `test_login.py` |
| 第2期 | 首页/仪表盘 | `dashboard_page.py` + `test_dashboard.py` |
| 第3期 | 订单系统 | `order_page.py` + `test_order.py` |
| 第4期 | 品牌管理 | `brand_page.py` + `test_brand.py` |
| 第5期 | 分佣系统 | `commission_page.py` + `test_commission.py` |
| 第6期 | 权限/推广/营销等 | 对应 page + test 文件 |

每个模块遵循相同模式：新增 Page Object + 测试文件，框架完全复用。

## 7. 交付物清单

| 文件 | 说明 |
|------|------|
| `requirements.txt` | Python 依赖清单 |
| `pytest.ini` | pytest 运行配置 |
| `.gitignore` | 排除 screenshots/、reports/、__pycache__/、.env |
| `.env.example` | 环境变量示例 |
| `config/settings.py` | 环境配置 |
| `pages/base_page.py` | 页面基类 |
| `pages/login_page.py` | 登录页 Page Object |
| `utils/captcha_solver.py` | 验证码识别 |
| `utils/excel_reader.py` | Excel 用例数据读取 |
| `conftest.py` | pytest fixtures |
| `tests/test_login.py` | 登录测试用例（10条） |
