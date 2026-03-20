# -*- coding: utf-8 -*-
"""登录页面 Page Object"""
from config import BASE_URL, ADMIN_USER, ADMIN_PASS


class LoginPage:
    def __init__(self, page):
        self.page = page
        # ====== 选择器（根据实际页面修改）======
        self.username_input = 'input[type="text"], input[name="username"], input[placeholder*="用户名"]'
        self.password_input = 'input[type="password"], input[name="password"]'
        self.login_btn = 'button[type="submit"], button:has-text("登录")'
        self.error_msg = '.el-message--error, .ant-message-error, [class*="error"]'

    def goto(self):
        self.page.goto(f"{BASE_URL}/")
        self.page.wait_for_load_state("networkidle")
        return self

    def login(self, username=ADMIN_USER, password=ADMIN_PASS):
        self.page.locator(self.username_input).first.fill(username)
        self.page.locator(self.password_input).first.fill(password)
        self.page.locator(self.login_btn).first.click()
        self.page.wait_for_load_state("networkidle")
        return self

    def is_logged_in(self):
        """判断是否登录成功（URL不再是登录页）"""
        return "/login" not in self.page.url

    def get_error_message(self):
        try:
            return self.page.locator(self.error_msg).first.inner_text(timeout=3000)
        except Exception:
            return None
