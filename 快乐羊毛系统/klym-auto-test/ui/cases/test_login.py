"""
UI 测试 - 登录模块

对应测试策略：后台登录功能
对应深度测试方案：权限与数据隔离 - 后台权限测试
"""
import pytest
from playwright.sync_api import Page, expect

from ui.pages.login_page import LoginPage
from common.config import Config


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.p0
class TestLoginUI:
    """后台登录 UI 测试"""

    def test_login_page_elements(self, page: Page):
        """登录页元素完整性检查"""
        login_page = LoginPage(page)
        login_page.goto_login()

        # 验证登录页核心元素存在
        expect(login_page.username_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
        expect(login_page.login_button).to_be_visible()

    def test_login_success(self, page: Page):
        """正确账号密码登录成功"""
        login_page = LoginPage(page)
        login_page.login_as_admin()
        login_page.assert_login_success()

    def test_login_wrong_password(self, page: Page):
        """错误密码登录失败，显示错误提示"""
        login_page = LoginPage(page)
        login_page.goto_login()
        login_page.login(Config.ADMIN_USER, "wrong_password_123")
        login_page.assert_login_failed()

    def test_login_empty_submit(self, page: Page):
        """不输入直接点击登录"""
        login_page = LoginPage(page)
        login_page.goto_login()
        login_page.login_button.click()
        # 应有表单校验提示
        assert login_page.is_login_page()

    def test_login_empty_username(self, page: Page):
        """只输入密码，不输入用户名"""
        login_page = LoginPage(page)
        login_page.goto_login()
        login_page.login("", Config.ADMIN_PASS)
        assert login_page.is_login_page()

    def test_login_empty_password(self, page: Page):
        """只输入用户名，不输入密码"""
        login_page = LoginPage(page)
        login_page.goto_login()
        login_page.login(Config.ADMIN_USER, "")
        assert login_page.is_login_page()


@pytest.mark.ui
@pytest.mark.security
@pytest.mark.p1
class TestLoginSecurityUI:
    """登录安全相关 UI 测试"""

    def test_password_masked(self, page: Page):
        """密码输入框应为密文显示"""
        login_page = LoginPage(page)
        login_page.goto_login()
        password_type = login_page.password_input.get_attribute("type")
        assert password_type == "password"

    def test_xss_in_username(self, page: Page):
        """用户名输入 XSS 脚本不应被执行"""
        login_page = LoginPage(page)
        login_page.goto_login()
        login_page.login("<script>alert('xss')</script>", "password")
        # 页面不应弹出 alert
        assert login_page.is_login_page()

    def test_sql_injection_in_username(self, page: Page):
        """用户名输入 SQL 注入不应登录成功"""
        login_page = LoginPage(page)
        login_page.goto_login()
        login_page.login("' OR 1=1 --", "anything")
        assert login_page.is_login_page()
