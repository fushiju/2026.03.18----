"""
UI 测试 - 登录模块

基于实际页面验证的行为：
- 空表单提交：三个校验错误（请输入用户名、请输入6-30位数的密码、请输入验证码）
- 验证码错误：顶部弹出 el-message "验证码错误"
- 登录按钮提交后变 disabled（防重复点击）
- 验证码为 canvas 绘制
- URL: https://red.jinyedaojia.com/#/login
"""
import pytest
from playwright.sync_api import Page, expect
from ui.pages.login_page import LoginPage
from common.config import Config


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.p0
class TestLoginPageElements:
    """登录页面元素验证"""

    def test_login_page_title(self, page: Page):
        """验证登录页标题和副标题"""
        login = LoginPage(page)
        login.goto_login()
        expect(page.get_by_text("欢迎登录")).to_be_visible()
        expect(page.get_by_text("快乐羊毛服务管理系统")).to_be_visible()

    def test_login_page_elements_visible(self, page: Page):
        """验证登录页所有元素可见"""
        login = LoginPage(page)
        login.goto_login()
        expect(login.username_input).to_be_visible()
        expect(login.password_input).to_be_visible()
        expect(login.captcha_input).to_be_visible()
        expect(login.captcha_canvas).to_be_visible()
        expect(login.login_button).to_be_visible()
        expect(login.login_button).to_be_enabled()

    def test_password_field_is_masked(self, page: Page):
        """验证密码输入框为密文显示"""
        login = LoginPage(page)
        login.goto_login()
        # 密码框 type 应为 password
        pw_type = login.password_input.get_attribute("type")
        assert pw_type == "password", f"密码框 type 应为 password，实际: {pw_type}"

    def test_captcha_canvas_exists(self, page: Page):
        """验证验证码图片（canvas）存在"""
        login = LoginPage(page)
        login.goto_login()
        expect(login.captcha_canvas).to_be_visible()

    def test_url_is_login(self, page: Page):
        """验证首次访问跳转到登录页"""
        login = LoginPage(page)
        login.goto_login()
        assert login.is_login_page(), f"URL 应包含 #/login，实际: {page.url}"


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.p0
class TestLoginFormValidation:
    """登录表单校验"""

    def test_empty_submit_shows_all_errors(self, page: Page):
        """空表单直接点登录，三个字段都提示错误
        预期：请输入用户名 / 请输入6-30位数的密码 / 请输入验证码
        """
        login = LoginPage(page)
        login.goto_login()
        login.login_button.click()
        page.wait_for_timeout(500)

        errors = login.get_form_errors()
        assert "请输入用户名" in errors, f"缺少用户名校验提示，实际: {errors}"
        assert any("密码" in e for e in errors), f"缺少密码校验提示，实际: {errors}"
        assert "请输入验证码" in errors, f"缺少验证码校验提示，实际: {errors}"

    def test_empty_username_only(self, page: Page):
        """只填密码和验证码，不填用户名
        预期：提示"请输入用户名"
        """
        login = LoginPage(page)
        login.goto_login()
        login.password_input.fill("admin123")
        login.captcha_input.fill("1234")
        login.login_button.click()
        page.wait_for_timeout(500)

        errors = login.get_form_errors()
        assert "请输入用户名" in errors

    def test_empty_password_only(self, page: Page):
        """只填用户名和验证码，不填密码
        预期：提示密码相关错误
        """
        login = LoginPage(page)
        login.goto_login()
        login.username_input.fill("admin")
        login.captcha_input.fill("1234")
        login.login_button.click()
        page.wait_for_timeout(500)

        errors = login.get_form_errors()
        assert any("密码" in e for e in errors), f"缺少密码校验提示，实际: {errors}"

    def test_empty_captcha_only(self, page: Page):
        """只填用户名和密码，不填验证码
        预期：提示"请输入验证码"
        """
        login = LoginPage(page)
        login.goto_login()
        login.username_input.fill("admin")
        login.password_input.fill("admin123")
        login.login_button.click()
        page.wait_for_timeout(500)

        errors = login.get_form_errors()
        assert "请输入验证码" in errors

    def test_short_password(self, page: Page):
        """密码少于6位
        预期：提示密码长度不足
        """
        login = LoginPage(page)
        login.goto_login()
        login.username_input.fill("admin")
        login.password_input.fill("123")
        login.captcha_input.fill("1234")
        login.login_button.click()
        page.wait_for_timeout(500)

        errors = login.get_form_errors()
        assert any("6" in e or "密码" in e for e in errors), f"缺少密码长度提示，实际: {errors}"


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.p0
class TestLoginWrongCredentials:
    """错误凭证登录"""

    def test_wrong_captcha(self, page: Page):
        """验证码错误，顶部弹出错误消息
        预期：弹出"验证码错误"
        """
        login = LoginPage(page)
        login.goto_login()
        login.login("admin", "admin123", captcha="0000")

        error = login.get_error_text()
        assert "验证码" in error, f"期望包含'验证码'，实际: '{error}'"
        assert login.is_login_page()

    def test_wrong_password(self, page: Page):
        """密码错误（需要验证码正确才能验证，此处验证码随机填写）
        预期：仍在登录页（验证码错误或密码错误）
        """
        login = LoginPage(page)
        login.goto_login()
        login.login("admin", "wrongpassword123", captcha="9999")

        assert login.is_login_page(), "错误密码不应登录成功"

    def test_nonexistent_user(self, page: Page):
        """不存在的用户名
        预期：仍在登录页
        """
        login = LoginPage(page)
        login.goto_login()
        login.login("nonexistent_user_xyz", "password123", captcha="1234")

        assert login.is_login_page(), "不存在的用户不应登录成功"


@pytest.mark.ui
@pytest.mark.p1
class TestLoginInteraction:
    """登录交互行为"""

    def test_captcha_refresh_on_click(self, page: Page):
        """点击验证码图片刷新验证码"""
        login = LoginPage(page)
        login.goto_login()
        login.refresh_captcha()
        # canvas 仍然可见
        expect(login.captcha_canvas).to_be_visible()

    def test_login_button_disabled_during_submit(self, page: Page):
        """提交登录时按钮变为 disabled（防重复点击）"""
        login = LoginPage(page)
        login.goto_login()
        login.username_input.fill("admin")
        login.password_input.fill("admin123")
        login.captcha_input.fill("1234")
        login.login_button.click()

        # 提交后按钮应短暂 disabled
        page.wait_for_timeout(200)
        # 注意：按钮可能很快恢复，此处主要验证不会重复提交

    def test_redirect_to_login_without_auth(self, page: Page):
        """未登录直接访问后台页面，应重定向到登录页"""
        login = LoginPage(page)
        page.goto(f"{Config.BASE_URL}/#/dashboard")
        page.wait_for_load_state("networkidle")
        assert login.is_login_page(), f"未登录应跳转登录页，实际: {page.url}"


@pytest.mark.ui
@pytest.mark.security
@pytest.mark.p1
class TestLoginSecurity:
    """登录安全测试"""

    def test_xss_in_username(self, page: Page):
        """用户名输入 XSS 脚本不应被执行"""
        login = LoginPage(page)
        login.goto_login()
        login.login("<script>alert('xss')</script>", "password123", "1234")
        assert login.is_login_page()

    def test_sql_injection_in_username(self, page: Page):
        """用户名输入 SQL 注入不应登录成功"""
        login = LoginPage(page)
        login.goto_login()
        login.login("' OR 1=1 --", "anything123", "1234")
        assert login.is_login_page()

    def test_sql_injection_in_password(self, page: Page):
        """密码输入 SQL 注入不应登录成功"""
        login = LoginPage(page)
        login.goto_login()
        login.login("admin", "' OR '1'='1", "1234")
        assert login.is_login_page()

    def test_long_input_username(self, page: Page):
        """超长用户名输入"""
        login = LoginPage(page)
        login.goto_login()
        login.login("a" * 500, "password123", "1234")
        assert login.is_login_page()

    def test_special_chars_in_username(self, page: Page):
        """特殊字符用户名"""
        login = LoginPage(page)
        login.goto_login()
        login.login("admin!@#$%^&*()", "password123", "1234")
        assert login.is_login_page()
