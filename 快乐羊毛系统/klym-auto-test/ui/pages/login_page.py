"""
LoginPage - 后台登录页
"""
from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage
from common.config import Config
from common.logger import logger


class LoginPage(BasePage):
    """快乐羊毛后台登录页"""

    def __init__(self, page: Page):
        super().__init__(page)
        # 定位器 - 根据实际页面结构调整
        self.username_input = page.get_by_placeholder("请输入用户名")
        self.password_input = page.get_by_placeholder("请输入密码")
        self.login_button = page.get_by_role("button", name="登录")
        self.error_message = page.locator(".el-message--error, .login-error, .ant-message-error")

    def goto_login(self):
        """打开登录页"""
        self.goto("/")
        logger.info("打开登录页")

    def login(self, username: str, password: str):
        """执行登录操作"""
        logger.info(f"登录: {username}")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.wait_loading()

    def login_as_admin(self):
        """使用管理员账号登录"""
        self.goto_login()
        self.login(Config.ADMIN_USER, Config.ADMIN_PASS)

    def get_error_text(self) -> str:
        """获取登录错误提示文本"""
        if self.error_message.count() > 0:
            return self.error_message.first.text_content()
        return ""

    def is_login_page(self) -> bool:
        """判断当前是否在登录页"""
        return self.login_button.count() > 0

    def assert_login_success(self):
        """断言登录成功（跳转到首页/数据概况）"""
        expect(self.page).not_to_have_url("/login", timeout=Config.ELEMENT_TIMEOUT)
        logger.info("登录成功")

    def assert_login_failed(self, expected_msg: str = None):
        """断言登录失败"""
        expect(self.error_message.first).to_be_visible(timeout=Config.ELEMENT_TIMEOUT)
        if expected_msg:
            error_text = self.get_error_text()
            assert expected_msg in error_text, f"期望包含 '{expected_msg}'，实际: '{error_text}'"
        logger.info("登录失败（符合预期）")
