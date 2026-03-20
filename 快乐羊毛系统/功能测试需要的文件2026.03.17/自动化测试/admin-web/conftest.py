# -*- coding: utf-8 -*-
"""
pytest fixtures —— 所有测试共享的浏览器初始化和登录逻辑
"""
import pytest
import os
from playwright.sync_api import sync_playwright
from config import BASE_URL, ADMIN_USER, ADMIN_PASS, HEADLESS, SLOW_MO, SCREENSHOT_DIR, DEFAULT_TIMEOUT


@pytest.fixture(scope="session")
def browser_context():
    """整个测试session共用一个浏览器，避免每个文件都重新打开"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
        )
        context.set_default_timeout(DEFAULT_TIMEOUT)
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def logged_in_page(browser_context):
    """登录一次，整个session复用"""
    page = browser_context.new_page()
    page.goto(f"{BASE_URL}/")
    page.wait_for_load_state("networkidle")

    # ========== 登录逻辑（根据实际页面调整选择器） ==========
    # 以下是常见后台登录页面的通用写法，你需要根据实际页面修改选择器
    try:
        # 尝试查找用户名输入框（常见选择器）
        username_input = page.locator(
            'input[type="text"], input[name="username"], input[placeholder*="用户名"], '
            'input[placeholder*="账号"], #username'
        ).first
        password_input = page.locator(
            'input[type="password"], input[name="password"], input[placeholder*="密码"], #password'
        ).first
        login_btn = page.locator(
            'button[type="submit"], button:has-text("登录"), button:has-text("Login"), '
            '.login-btn, #login-btn'
        ).first

        username_input.fill(ADMIN_USER)
        password_input.fill(ADMIN_PASS)
        login_btn.click()

        # 等待登录成功（跳转到首页/仪表盘）
        page.wait_for_load_state("networkidle")
        # 等一下确保页面稳定
        page.wait_for_timeout(2000)
        print(f"✅ 登录成功: {page.url}")

    except Exception as e:
        # 截图保存登录失败的页面，方便排查
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        page.screenshot(path=f"{SCREENSHOT_DIR}/login_failed.png")
        print(f"❌ 登录失败，截图已保存。当前URL: {page.url}")
        print(f"   错误: {e}")
        print(f"   请检查 config.py 中的账号密码，并根据实际页面修改 conftest.py 中的选择器")

    yield page
    page.close()


@pytest.fixture
def page(logged_in_page):
    """每个测试方法共用已登录的page"""
    return logged_in_page


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page):
    """测试失败时自动截图"""
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        name = request.node.name.replace("/", "_").replace("::", "_")
        page.screenshot(path=f"{SCREENSHOT_DIR}/FAIL_{name}.png")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """让fixture能拿到测试结果"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
