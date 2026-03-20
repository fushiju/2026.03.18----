"""
LoginPage - 快乐羊毛后台登录页

实际页面结构（通过 a11y snapshot 确认）：
- 标题：欢迎登录 / 快乐羊毛服务管理系统
- textbox "用户名" — placeholder 为"用户名"
- textbox "密码" — placeholder 为"密码"
- textbox "验证码" — placeholder 为"验证码"
- Canvas — 验证码图片（canvas 绘制，非 img 标签）
- button "登 录" — 按钮文字中间有空格
- URL: https://red.jinyedaojia.com/#/login
"""
from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage
from common.config import Config
from common.logger import logger


class LoginPage(BasePage):
    """快乐羊毛后台登录页"""

    def __init__(self, page: Page):
        super().__init__(page)
        # 定位器 — 基于实际页面 a11y tree
        self.username_input = page.get_by_role("textbox", name="用户名")
        self.password_input = page.get_by_role("textbox", name="密码")
        self.captcha_input = page.get_by_role("textbox", name="验证码")
        self.captcha_canvas = page.locator("canvas")
        self.login_button = page.get_by_role("button", name="登 录")
        # 错误提示（Element UI 消息组件）
        self.error_message = page.locator(".el-message--error")
        self.form_error = page.locator(".el-form-item__error")

    def goto_login(self):
        """打开登录页"""
        self.goto("/")
        self.page.wait_for_load_state("networkidle")
        logger.info("打开登录页")

    def login(self, username: str, password: str, captcha: str = ""):
        """执行登录操作"""
        logger.info(f"登录: {username}")
        self.username_input.fill(username)
        self.password_input.fill(password)
        if captcha:
            self.captcha_input.fill(captcha)
        self.login_button.click()
        self.page.wait_for_timeout(1000)

    def login_as_admin(self):
        """使用管理员账号登录

        验证码处理方案（按优先级）：
        1. 开发关闭测试环境验证码（推荐）
        2. 开发提供万能验证码
        3. 接入 OCR 识别
        """
        self.goto_login()
        self.login(Config.ADMIN_USER, Config.ADMIN_PASS, captcha="1234")

    def refresh_captcha(self):
        """点击验证码 canvas 刷新"""
        self.captcha_canvas.click()
        self.page.wait_for_timeout(500)
        logger.info("刷新验证码")

    def get_error_text(self) -> str:
        """获取登录错误提示（顶部弹出消息）"""
        try:
            self.error_message.first.wait_for(state="visible", timeout=3000)
            return self.error_message.first.text_content() or ""
        except Exception:
            return ""

    def get_form_errors(self) -> list:
        """获取所有表单校验错误"""
        errors = []
        for i in range(self.form_error.count()):
            text = self.form_error.nth(i).text_content()
            if text:
                errors.append(text.strip())
        return errors

    def is_login_page(self) -> bool:
        """判断当前是否在登录页"""
        return "#/login" in self.page.url

    def assert_login_success(self):
        """断言登录成功（URL 不再是 #/login）"""
        self.page.wait_for_timeout(2000)
        assert not self.is_login_page(), f"仍在登录页: {self.page.url}"
        logger.info("登录成功")

    def assert_login_failed(self, expected_msg: str = None):
        """断言登录失败"""
        assert self.is_login_page(), f"不在登录页: {self.page.url}，可能意外登录成功"
        if expected_msg:
            error = self.get_error_text()
            form_errors = self.get_form_errors()
            all_errors = error + " ".join(form_errors)
            assert expected_msg in all_errors, (
                f"期望包含 '{expected_msg}'，实际: '{all_errors}'"
            )
        logger.info("登录失败（符合预期）")

    def assert_has_form_error(self):
        """断言有表单校验错误（红字提示）"""
        self.page.wait_for_timeout(500)
        errors = self.get_form_errors()
        assert len(errors) > 0, "未出现表单校验错误"
        logger.info(f"表单校验错误: {errors}")
