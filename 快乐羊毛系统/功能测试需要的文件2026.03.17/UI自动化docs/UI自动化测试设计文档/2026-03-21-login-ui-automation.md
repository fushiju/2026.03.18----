# 登录模块 UI 自动化测试 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `UI自动化/` 目录下搭建 Playwright + Python + pytest 自动化框架，实现管理后台登录模块 10 条测试用例的自动化执行。

**Architecture:** Page Object Model 分层架构。BasePage 封装通用操作，LoginPage 封装登录页元素和方法，conftest.py 管理浏览器生命周期和失败截图，utils/ 提供验证码识别和 Excel 读取工具。

**Tech Stack:** Python 3.14, Playwright, pytest, ddddocr, openpyxl

**Spec:** `docs/superpowers/specs/2026-03-21-admin-web-ui-automation-design.md`

---

## 文件结构总览

```
UI自动化/
├── requirements.txt           # 新建 - 依赖清单
├── pytest.ini                 # 新建 - pytest 配置
├── .gitignore                 # 新建 - 忽略规则
├── .env.example               # 新建 - 环境变量示例
├── conftest.py                # 新建 - fixtures
├── config/
│   ├── __init__.py            # 新建
│   └── settings.py            # 新建 - 配置
├── pages/
│   ├── __init__.py            # 新建
│   ├── base_page.py           # 新建 - 页面基类
│   └── login_page.py          # 新建 - 登录页 PO
├── utils/
│   ├── __init__.py            # 新建
│   ├── captcha_solver.py      # 新建 - 验证码识别
│   └── excel_reader.py        # 新建 - Excel 读取
├── tests/
│   ├── __init__.py            # 新建
│   └── test_login.py          # 新建 - 登录测试
├── screenshots/               # 新建目录
├── reports/                   # 新建目录
└── 测试用例/                   # 已存在，只读
    └── 登录.xlsx
```

---

### Task 1: 项目初始化 — 配置文件

**Files:**
- Create: `UI自动化/requirements.txt`
- Create: `UI自动化/pytest.ini`
- Create: `UI自动化/.gitignore`
- Create: `UI自动化/.env.example`

- [ ] **Step 1: 创建 requirements.txt**

```text
playwright>=1.40.0
pytest>=7.4.0
pytest-playwright>=0.4.0
pytest-html>=4.0.0
allure-pytest>=2.13.0
ddddocr>=1.4.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
```

- [ ] **Step 2: 创建 pytest.ini**

```ini
[pytest]
testpaths = tests
markers =
    login: 登录模块测试
    smoke: 冒烟测试
addopts = -v --tb=short
```

- [ ] **Step 3: 创建 .gitignore**

```
screenshots/
reports/
__pycache__/
*.pyc
.env
.pytest_cache/
```

- [ ] **Step 4: 创建 .env.example**

```
KLYM_BASE_URL=https://red.jinyedaojia.com/
KLYM_USERNAME=admin
KLYM_PASSWORD=admin123
KLYM_CAPTCHA_BYPASS=
```

- [ ] **Step 5: 创建空目录的占位文件**

创建 `screenshots/.gitkeep` 和 `reports/.gitkeep`。

- [ ] **Step 6: 安装依赖**

运行: `pip install -r requirements.txt && playwright install chromium`

- [ ] **Step 7: 提交**

```bash
git add UI自动化/requirements.txt UI自动化/pytest.ini UI自动化/.gitignore UI自动化/.env.example UI自动化/screenshots/.gitkeep UI自动化/reports/.gitkeep
git commit -m "feat: 初始化UI自动化项目配置文件"
```

---

### Task 2: 配置模块 — config/settings.py

**Files:**
- Create: `UI自动化/config/__init__.py`
- Create: `UI自动化/config/settings.py`

- [ ] **Step 1: 创建 config/__init__.py**

空文件。

- [ ] **Step 2: 创建 config/settings.py**

```python
"""项目全局配置 — 优先从环境变量读取，回退到默认值"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 环境配置
BASE_URL = os.getenv("KLYM_BASE_URL", "https://red.jinyedaojia.com/")
ADMIN_USERNAME = os.getenv("KLYM_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("KLYM_PASSWORD", "admin123")

# 验证码：设置万能值则跳过 OCR，为空则走 ddddocr 识别
CAPTCHA_BYPASS = os.getenv("KLYM_CAPTCHA_BYPASS", "")

# 超时与浏览器
TIMEOUT = 10000  # 毫秒
HEADLESS = os.getenv("KLYM_HEADLESS", "true").lower() == "true"

# 路径
SCREENSHOT_DIR = BASE_DIR / "screenshots"
REPORT_DIR = BASE_DIR / "reports"
TESTCASE_DIR = BASE_DIR / "测试用例"
```

- [ ] **Step 3: 提交**

```bash
git add UI自动化/config/
git commit -m "feat: 添加配置模块 config/settings.py"
```

---

### Task 3: 工具层 — Excel 读取器

**Files:**
- Create: `UI自动化/utils/__init__.py`
- Create: `UI自动化/utils/excel_reader.py`
- Create: `UI自动化/tests/__init__.py`
- Create: `UI自动化/tests/test_excel_reader.py`

- [ ] **Step 1: 写失败测试**

```python
# tests/test_excel_reader.py
from utils.excel_reader import read_login_cases


def test_read_login_cases_returns_list():
    """读取登录.xlsx 应返回非空列表"""
    cases = read_login_cases()
    assert isinstance(cases, list)
    assert len(cases) > 0


def test_read_login_cases_has_required_fields():
    """每条用例应包含必要字段"""
    cases = read_login_cases()
    first = cases[0]
    assert "用例标题" in first
    assert "测试步骤" in first
    assert "预期结果" in first
```

- [ ] **Step 2: 运行测试确认失败**

运行: `cd UI自动化 && pytest tests/test_excel_reader.py -v`
预期: FAIL — ModuleNotFoundError

- [ ] **Step 3: 实现 excel_reader.py**

```python
# utils/excel_reader.py
"""读取 Excel 测试用例数据"""
from pathlib import Path
import openpyxl
from config.settings import TESTCASE_DIR


def read_test_cases(file_name: str, sheet_name: str = None) -> list[dict]:
    """读取指定 Excel 文件，返回字典列表。第1行为表头，第2行起为数据。"""
    file_path = TESTCASE_DIR / file_name
    wb = openpyxl.load_workbook(file_path, read_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active

    rows = list(ws.iter_rows(values_only=True))
    wb.close()

    if len(rows) < 2:
        return []

    headers = [str(h).strip() if h else f"col_{i}" for i, h in enumerate(rows[0])]
    result = []
    for row in rows[1:]:
        values = [str(v).strip() if v else "" for v in row]
        if any(values):
            result.append(dict(zip(headers, values)))
    return result


def read_login_cases() -> list[dict]:
    """读取登录测试用例"""
    return read_test_cases("登录.xlsx", "测试用例")
```

- [ ] **Step 4: 运行测试确认通过**

运行: `cd UI自动化 && pytest tests/test_excel_reader.py -v`
预期: 2 passed

- [ ] **Step 5: 提交**

```bash
git add UI自动化/utils/ UI自动化/tests/
git commit -m "feat: 添加 Excel 测试用例读取工具"
```

---

### Task 4: 工具层 — 验证码识别

**Files:**
- Create: `UI自动化/utils/captcha_solver.py`

- [ ] **Step 1: 实现 captcha_solver.py**

```python
# utils/captcha_solver.py
"""验证码识别 — 优先使用万能验证码绕过，降级使用 ddddocr OCR"""
from config.settings import CAPTCHA_BYPASS


def solve_captcha(image_bytes: bytes) -> str:
    """识别验证码图片，返回识别结果字符串"""
    # 优先使用万能验证码
    if CAPTCHA_BYPASS:
        return CAPTCHA_BYPASS

    # 降级：ddddocr OCR 识别
    import ddddocr
    ocr = ddddocr.DdddOcr(show_ad=False)
    result = ocr.classification(image_bytes)
    # 只保留小写字母和数字，截取前4位
    cleaned = "".join(c for c in result.lower() if c.isalnum())
    return cleaned[:4]
```

- [ ] **Step 2: 提交**

```bash
git add UI自动化/utils/captcha_solver.py
git commit -m "feat: 添加验证码识别工具（支持万能验证码绕过）"
```

---

### Task 5: 页面对象 — BasePage

**Files:**
- Create: `UI自动化/pages/__init__.py`
- Create: `UI自动化/pages/base_page.py`

- [ ] **Step 1: 实现 base_page.py**

```python
# pages/base_page.py
"""页面基类 — 封装 Playwright 通用操作"""
from playwright.sync_api import Page
from config.settings import TIMEOUT, SCREENSHOT_DIR


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(TIMEOUT)

    def goto(self, path: str = ""):
        """导航到指定路径"""
        from config.settings import BASE_URL
        url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        self.page.goto(url)

    def fill(self, selector: str, value: str):
        """清空并填入值"""
        self.page.fill(selector, value)

    def click(self, selector: str):
        """点击元素"""
        self.page.click(selector)

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """检查元素是否可见"""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def screenshot(self, name: str):
        """截图保存"""
        path = SCREENSHOT_DIR / f"{name}.png"
        self.page.screenshot(path=str(path))
        return path

    @property
    def current_url(self) -> str:
        return self.page.url
```

- [ ] **Step 2: 提交**

```bash
git add UI自动化/pages/
git commit -m "feat: 添加 BasePage 页面基类"
```

---

### Task 6: 页面对象 — LoginPage

**Files:**
- Create: `UI自动化/pages/login_page.py`

- [ ] **Step 1: 实现 login_page.py**

注意：选择器需要在实际页面上确认。以下基于 `https://red.jinyedaojia.com/#/login` 页面结构预设，实施时需根据实际 DOM 调整。

```python
# pages/login_page.py
"""登录页 Page Object"""
import time
from pages.base_page import BasePage
from utils.captcha_solver import solve_captcha


class LoginPage(BasePage):
    """管理后台登录页面"""

    # --- 选择器（实施时根据实际页面 DOM 调整） ---
    SEL_USERNAME = 'input[placeholder*="用户名"], input[placeholder*="账号"], input[name="username"]'
    SEL_PASSWORD = 'input[placeholder*="密码"], input[type="password"]'
    SEL_CAPTCHA_INPUT = 'input[placeholder*="验证码"]'
    SEL_CAPTCHA_IMAGE = '.login-code img, .code-img img, img[alt*="验证码"]'
    SEL_LOGIN_BTN = 'button:has-text("登录"), button[type="submit"]'
    SEL_ERROR_MSG = '.el-message, .el-form-item__error, .el-notification'

    def goto_login(self):
        """打开登录页"""
        self.goto("#/login")
        self.page.wait_for_load_state("networkidle")

    def fill_username(self, value: str):
        self.fill(self.SEL_USERNAME, value)

    def fill_password(self, value: str):
        self.fill(self.SEL_PASSWORD, value)

    def fill_captcha(self, value: str):
        self.fill(self.SEL_CAPTCHA_INPUT, value)

    def click_login(self):
        self.click(self.SEL_LOGIN_BTN)

    def get_captcha_image_bytes(self) -> bytes:
        """获取验证码图片的二进制数据"""
        img = self.page.query_selector(self.SEL_CAPTCHA_IMAGE)
        if img:
            return img.screenshot()
        return b""

    def get_captcha_image_src(self) -> str:
        """获取验证码图片 src 属性"""
        img = self.page.query_selector(self.SEL_CAPTCHA_IMAGE)
        return img.get_attribute("src") if img else ""

    def click_captcha_image(self):
        """点击验证码图片刷新"""
        self.click(self.SEL_CAPTCHA_IMAGE)
        time.sleep(0.5)  # 等待新验证码加载

    def get_error_message(self, timeout: int = 3000) -> str:
        """获取页面错误提示信息"""
        try:
            self.page.wait_for_selector(self.SEL_ERROR_MSG, timeout=timeout)
            elements = self.page.query_selector_all(self.SEL_ERROR_MSG)
            texts = [el.text_content() or "" for el in elements]
            return " ".join(texts).strip()
        except Exception:
            return ""

    def login_with_captcha(self, username: str, password: str, max_retries: int = 3) -> bool:
        """完整登录流程：填写表单 + OCR 验证码 + 重试"""
        self.fill_username(username)
        self.fill_password(password)

        for attempt in range(max_retries):
            # 识别验证码
            img_bytes = self.get_captcha_image_bytes()
            captcha_text = solve_captcha(img_bytes)
            self.fill_captcha(captcha_text)
            self.click_login()

            # 等待结果
            self.page.wait_for_timeout(1500)

            # 检查是否登录成功（URL 变化）
            if "dashboard" in self.current_url or "login" not in self.current_url:
                return True

            # 检查是否验证码错误（需要重试）
            error = self.get_error_message()
            if "验证码" in error:
                self.click_captcha_image()
                continue
            else:
                # 非验证码错误（用户名/密码错误等），不重试
                return False

        return False
```

- [ ] **Step 2: 提交**

```bash
git add UI自动化/pages/login_page.py
git commit -m "feat: 添加 LoginPage 页面对象（含验证码处理）"
```

---

### Task 7: Fixtures — conftest.py

**Files:**
- Create: `UI自动化/conftest.py`

- [ ] **Step 1: 实现 conftest.py**

```python
# conftest.py
"""pytest fixtures — 浏览器管理、页面上下文、失败截图"""
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from config.settings import HEADLESS, SCREENSHOT_DIR
from pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser():
    """会话级浏览器实例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    """每个测试用例独立的浏览器上下文和页面"""
    context = browser.new_context()
    pg = context.new_page()
    yield pg
    pg.close()
    context.close()


@pytest.fixture
def login_page(page) -> LoginPage:
    """LoginPage 对象，已导航到登录页"""
    lp = LoginPage(page)
    lp.goto_login()
    return lp


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    """测试失败时自动截图"""
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        name = request.node.name.replace("[", "_").replace("]", "")
        page.screenshot(path=str(SCREENSHOT_DIR / f"FAIL_{name}.png"))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """将测试结果存储到 request.node 上，供 screenshot_on_failure 使用"""
    import pluggy
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
```

- [ ] **Step 2: 提交**

```bash
git add UI自动化/conftest.py
git commit -m "feat: 添加 conftest.py（浏览器管理 + 失败截图）"
```

---

### Task 8: 登录测试用例 — test_login.py

**Files:**
- Create: `UI自动化/tests/test_login.py`

- [ ] **Step 1: 实现 test_login.py（10 条用例）**

```python
# tests/test_login.py
"""管理后台登录模块 UI 自动化测试 — 对应 测试用例/登录.xlsx 10 条用例"""
import pytest
from pages.login_page import LoginPage
from config.settings import ADMIN_USERNAME, ADMIN_PASSWORD


class TestLoginSuccess:
    """正向登录测试"""

    @pytest.mark.smoke
    @pytest.mark.login
    def test_01_correct_login(self, login_page: LoginPage):
        """用例1: 正确账号密码登录 → 跳转到 dashboard，显示用户名"""
        success = login_page.login_with_captcha(ADMIN_USERNAME, ADMIN_PASSWORD)
        assert success, "登录未成功跳转"
        assert "dashboard" in login_page.current_url, f"URL 未跳转到 dashboard: {login_page.current_url}"
        # 检查页面显示用户名
        assert login_page.page.is_visible(f'text="{ADMIN_USERNAME}"', timeout=5000) or \
               login_page.page.is_visible(f'text="admin"', timeout=2000), \
               "页面未显示当前登录用户名"


class TestCaptcha:
    """验证码相关测试"""

    @pytest.mark.login
    def test_02_captcha_refresh(self, login_page: LoginPage):
        """用例2: 验证码刷新功能 → 点击后图片 src 变化"""
        src_before = login_page.get_captcha_image_src()
        login_page.click_captcha_image()
        login_page.page.wait_for_timeout(1000)
        src_after = login_page.get_captcha_image_src()
        assert src_before != src_after, "验证码图片未刷新"

    @pytest.mark.login
    def test_06_captcha_format_validation(self, login_page: LoginPage):
        """用例6: 验证码格式校验 — 输入含大写字母的验证码"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password(ADMIN_PASSWORD)
        login_page.fill_captcha("AbC1")
        login_page.click_login()
        login_page.page.wait_for_timeout(1000)
        error = login_page.get_error_message()
        assert "验证码" in error or "小写" in error, f"未提示验证码格式错误: {error}"

    @pytest.mark.login
    def test_08_wrong_captcha(self, login_page: LoginPage):
        """用例8: 错误验证码登录 → 提示验证码错误，验证码自动刷新"""
        src_before = login_page.get_captcha_image_src()
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password(ADMIN_PASSWORD)
        login_page.fill_captcha("zzzz")  # 故意填错
        login_page.click_login()
        login_page.page.wait_for_timeout(1500)
        error = login_page.get_error_message()
        assert "验证码" in error, f"未提示验证码错误: {error}"
        # 验证码应自动刷新
        src_after = login_page.get_captcha_image_src()
        assert src_before != src_after, "验证码未自动刷新"


class TestEmptyFields:
    """空字段校验"""

    @pytest.mark.login
    def test_03_empty_username(self, login_page: LoginPage):
        """用例3: 空用户名登录 → 提示请输入用户名"""
        login_page.fill_username("")
        login_page.fill_password(ADMIN_PASSWORD)
        login_page.fill_captcha("test")
        login_page.click_login()
        login_page.page.wait_for_timeout(1000)
        error = login_page.get_error_message()
        assert "用户名" in error, f"未提示输入用户名: {error}"

    @pytest.mark.login
    def test_04_empty_password(self, login_page: LoginPage):
        """用例4: 空密码登录 → 提示请输入密码"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password("")
        login_page.fill_captcha("test")
        login_page.click_login()
        login_page.page.wait_for_timeout(1000)
        error = login_page.get_error_message()
        assert "密码" in error, f"未提示输入密码: {error}"

    @pytest.mark.login
    def test_05_empty_captcha(self, login_page: LoginPage):
        """用例5: 空验证码登录 → 提示输入验证码"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password(ADMIN_PASSWORD)
        login_page.fill_captcha("")
        login_page.click_login()
        login_page.page.wait_for_timeout(1000)
        error = login_page.get_error_message()
        assert "验证码" in error, f"未提示输入验证码: {error}"


class TestWrongCredentials:
    """错误凭据测试"""

    @pytest.mark.login
    def test_07_wrong_password(self, login_page: LoginPage):
        """用例7: 错误密码登录 → 提示用户名或密码错误"""
        login_page.fill_username(ADMIN_USERNAME)
        login_page.fill_password("wrongpassword")
        # 需要正确验证码才能测试密码错误
        login_page.login_with_captcha(ADMIN_USERNAME, "wrongpassword")
        error = login_page.get_error_message()
        assert "用户名" in error or "密码" in error or "错误" in error, \
            f"未提示用户名或密码错误: {error}"

    @pytest.mark.login
    def test_09_nonexistent_user(self, login_page: LoginPage):
        """用例9: 不存在的用户名登录 → 提示用户名或密码错误"""
        login_page.login_with_captcha("nonexistentuser", "anypassword")
        error = login_page.get_error_message()
        assert "用户名" in error or "密码" in error or "错误" in error, \
            f"未提示用户名或密码错误: {error}"

    @pytest.mark.login
    def test_10_wrong_username(self, login_page: LoginPage):
        """用例10: 验证用户名错误 → 提示用户名错误"""
        login_page.login_with_captcha("fushuju", ADMIN_PASSWORD)
        error = login_page.get_error_message()
        assert "用户名" in error or "错误" in error, \
            f"未提示用户名错误: {error}"
```

- [ ] **Step 2: 运行测试（有头模式调试）**

运行: `cd UI自动化 && pytest tests/test_login.py -v --headed`

首次运行预期部分失败 — 需要根据实际页面 DOM 调整 LoginPage 中的选择器。

- [ ] **Step 3: 根据实际页面 DOM 调整选择器**

打开 `https://red.jinyedaojia.com/#/login`，用浏览器 DevTools 检查元素，更新 `pages/login_page.py` 中的 `SEL_*` 选择器常量。

- [ ] **Step 4: 再次运行，确认全部通过**

运行: `cd UI自动化 && pytest tests/test_login.py -v --headed`
预期: 10 passed

- [ ] **Step 5: 生成 HTML 报告**

运行: `cd UI自动化 && pytest tests/test_login.py -v --html=reports/login_report.html --self-contained-html`

- [ ] **Step 6: 提交**

```bash
git add UI自动化/tests/test_login.py
git commit -m "feat: 实现登录模块10条UI自动化测试用例"
```

---

### Task 9: 验收 — 完整运行与报告

- [ ] **Step 1: headless 模式完整运行**

运行: `cd UI自动化 && pytest tests/test_login.py -v --html=reports/login_report.html --self-contained-html`

- [ ] **Step 2: 检查报告**

用浏览器打开 `UI自动化/reports/login_report.html`，确认：
- 10 条用例全部列出
- 通过/失败状态正确
- 失败用例有截图附件

- [ ] **Step 3: 最终提交**

```bash
git add -A UI自动化/
git commit -m "feat: 登录模块UI自动化测试完成（10条用例）"
```
