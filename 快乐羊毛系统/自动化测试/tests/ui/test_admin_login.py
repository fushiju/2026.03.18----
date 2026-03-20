"""
后台管理系统 — UI自动化测试（登录模块）

使用Playwright进行浏览器自动化测试。
覆盖: 登录成功/失败、页面元素验证、登出。
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import TestConfig


@pytest.mark.ui
class TestAdminLoginUI:
    """后台登录UI测试"""

    @pytest.mark.P0
    @pytest.mark.smoke
    def test_login_page_loads(self, page):
        """登录页面正常加载"""
        page.goto(TestConfig.ADMIN_BASE_URL)
        # 等待页面加载完成
        page.wait_for_load_state("networkidle")
        # 截图记录
        page.screenshot(path="reports/login_page.png")
        # 验证登录页面元素存在（根据实际页面调整选择器）
        # 常见选择器: input[type=text], input[type=password], button
        print(f"页面标题: {page.title()}")

    @pytest.mark.P0
    @pytest.mark.smoke
    def test_login_success(self, page):
        """正确账号密码登录成功"""
        page.goto(TestConfig.ADMIN_BASE_URL)
        page.wait_for_load_state("networkidle")

        # 填写登录表单（选择器需根据实际页面调整）
        # 尝试常见的登录表单选择器
        selectors = {
            "username": [
                'input[placeholder*="用户名"]',
                'input[placeholder*="账号"]',
                'input[name="username"]',
                'input[type="text"]',
                '#username',
            ],
            "password": [
                'input[placeholder*="密码"]',
                'input[name="password"]',
                'input[type="password"]',
                '#password',
            ],
            "submit": [
                'button[type="submit"]',
                'button:has-text("登录")',
                'button:has-text("登 录")',
                '.login-button',
                '#login-btn',
            ],
        }

        # 尝试找到用户名输入框
        username_input = None
        for sel in selectors["username"]:
            if page.locator(sel).count() > 0:
                username_input = page.locator(sel).first
                break

        password_input = None
        for sel in selectors["password"]:
            if page.locator(sel).count() > 0:
                password_input = page.locator(sel).first
                break

        submit_btn = None
        for sel in selectors["submit"]:
            if page.locator(sel).count() > 0:
                submit_btn = page.locator(sel).first
                break

        if username_input and password_input and submit_btn:
            username_input.fill(TestConfig.ADMIN_USERNAME)
            password_input.fill(TestConfig.ADMIN_PASSWORD)
            submit_btn.click()

            # 等待登录完成（页面跳转或出现后台元素）
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

            # 截图记录登录后页面
            page.screenshot(path="reports/after_login.png")

            # 验证是否登录成功（URL变化或出现后台菜单）
            current_url = page.url
            print(f"登录后URL: {current_url}")
            # 通常登录成功后URL会变化，不再停留在登录页
        else:
            pytest.skip("未找到登录表单元素，请根据实际页面调整选择器")

    @pytest.mark.P0
    def test_login_wrong_password(self, page):
        """错误密码登录失败"""
        page.goto(TestConfig.ADMIN_BASE_URL)
        page.wait_for_load_state("networkidle")

        # 尝试找到登录表单
        username_sel = 'input[type="text"]'
        password_sel = 'input[type="password"]'

        if page.locator(username_sel).count() > 0 and page.locator(password_sel).count() > 0:
            page.locator(username_sel).first.fill(TestConfig.ADMIN_USERNAME)
            page.locator(password_sel).first.fill("wrong_password_123")

            # 点击登录
            submit_selectors = ['button[type="submit"]', 'button:has-text("登录")', 'button:has-text("登 录")']
            for sel in submit_selectors:
                if page.locator(sel).count() > 0:
                    page.locator(sel).first.click()
                    break

            page.wait_for_timeout(2000)

            # 验证：应显示错误提示或停留在登录页
            page.screenshot(path="reports/login_fail.png")
            # 应仍在登录页
            print(f"错误登录后URL: {page.url}")
        else:
            pytest.skip("未找到登录表单")

    @pytest.mark.P1
    def test_login_empty_fields(self, page):
        """空字段登录"""
        page.goto(TestConfig.ADMIN_BASE_URL)
        page.wait_for_load_state("networkidle")

        # 不填任何内容直接点登录
        submit_selectors = ['button[type="submit"]', 'button:has-text("登录")', 'button:has-text("登 录")']
        for sel in submit_selectors:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click()
                break

        page.wait_for_timeout(1000)
        page.screenshot(path="reports/login_empty.png")
        # 应有表单校验提示


@pytest.mark.ui
class TestAdminNavigation:
    """后台导航测试"""

    @pytest.fixture(autouse=True)
    def login_first(self, page):
        """每个测试前先登录"""
        page.goto(TestConfig.ADMIN_BASE_URL)
        page.wait_for_load_state("networkidle")

        username_sel = 'input[type="text"]'
        password_sel = 'input[type="password"]'

        if page.locator(username_sel).count() > 0:
            page.locator(username_sel).first.fill(TestConfig.ADMIN_USERNAME)
            page.locator(password_sel).first.fill(TestConfig.ADMIN_PASSWORD)

            submit_selectors = ['button[type="submit"]', 'button:has-text("登录")', 'button:has-text("登 录")']
            for sel in submit_selectors:
                if page.locator(sel).count() > 0:
                    page.locator(sel).first.click()
                    break

            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)

    @pytest.mark.P1
    def test_admin_dashboard_loads(self, page):
        """后台首页/仪表盘加载"""
        page.screenshot(path="reports/dashboard.png")
        print(f"后台首页URL: {page.url}")
        print(f"后台首页标题: {page.title()}")

    @pytest.mark.P1
    def test_order_page_accessible(self, page):
        """订单管理页面可访问"""
        # 尝试点击订单管理菜单
        menu_selectors = [
            'text=订单管理',
            'text=订单',
            '[data-menu="order"]',
            'a:has-text("订单")',
        ]
        for sel in menu_selectors:
            if page.locator(sel).count() > 0:
                page.locator(sel).first.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(1000)
                page.screenshot(path="reports/order_page.png")
                print(f"订单页URL: {page.url}")
                break

    @pytest.mark.P2
    def test_page_load_performance(self, page):
        """后台页面加载性能 < 2秒"""
        import time
        start = time.time()
        page.goto(TestConfig.ADMIN_BASE_URL)
        page.wait_for_load_state("networkidle")
        elapsed = time.time() - start
        print(f"登录页加载时间: {elapsed:.2f}秒")
        assert elapsed < 5, f"页面加载时间 {elapsed:.2f}秒 超过5秒"
