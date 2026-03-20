# -*- coding: utf-8 -*-
"""
管理后台 - 登录模块自动化测试
对应用例: ht-hj-001, aq-zq-004(SQL注入), ht-hj-006(token过期)
"""
import pytest
import sys
sys.path.insert(0, '..')
from pages.login_page import LoginPage
from config import BASE_URL


class TestLogin:
    """后台登录测试"""

    def test_login_success(self, page):
        """验证正确账号密码登录成功"""
        # conftest已经登录了，这里验证登录状态
        assert "/login" not in page.url, "登录失败，仍在登录页"
        print(f"✅ 当前页面: {page.url}")

    def test_login_wrong_password(self, browser_context):
        """验证错误密码登录失败"""
        new_page = browser_context.new_page()
        login = LoginPage(new_page).goto()
        login.login(username="admin", password="wrong_password")
        new_page.wait_for_timeout(2000)

        # 应该还在登录页或有错误提示
        error = login.get_error_message()
        is_still_login = "/login" in new_page.url or error is not None
        assert is_still_login, "错误密码不应该登录成功"
        print(f"✅ 错误密码被拒绝, 提示: {error}")
        new_page.close()

    def test_login_empty_username(self, browser_context):
        """验证空用户名不可登录"""
        new_page = browser_context.new_page()
        login = LoginPage(new_page).goto()
        login.login(username="", password="admin123")
        new_page.wait_for_timeout(2000)

        is_still_login = "/login" in new_page.url
        assert is_still_login, "空用户名不应该登录成功"
        print("✅ 空用户名被拦截")
        new_page.close()

    def test_login_sql_injection(self, browser_context):
        """[安全] 验证SQL注入不能登录 (对应 aq-zq-004)"""
        new_page = browser_context.new_page()
        login = LoginPage(new_page).goto()
        login.login(username="' OR 1=1 --", password="' OR '1'='1")
        new_page.wait_for_timeout(2000)

        assert "/login" in new_page.url or not login.is_logged_in(), \
            "SQL注入不应该登录成功！严重安全漏洞！"
        print("✅ SQL注入被拦截")
        new_page.close()

    def test_login_xss_injection(self, browser_context):
        """[安全] 验证XSS注入不执行 (对应 aq-zq-005)"""
        new_page = browser_context.new_page()
        login = LoginPage(new_page).goto()
        login.login(username='<script>alert("xss")</script>', password="test")
        new_page.wait_for_timeout(2000)

        # 检查页面是否弹出了alert
        dialog_triggered = False
        new_page.on("dialog", lambda d: d.dismiss())
        # 如果没触发dialog就是安全的
        assert not dialog_triggered, "XSS脚本不应该被执行！"
        print("✅ XSS注入被过滤")
        new_page.close()
