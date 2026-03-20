"""
BasePage - 所有页面的基类
封装后台管理系统通用操作：侧边栏导航、表格操作、等待加载等
"""
import os
from playwright.sync_api import Page, expect
from common.config import Config
from common.logger import logger


class BasePage:
    """后台管理系统页面基类"""

    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str = "/"):
        """导航到指定路径"""
        url = f"{Config.BASE_URL}{path}"
        logger.info(f"导航到: {url}")
        self.page.goto(url, timeout=Config.PAGE_LOAD_TIMEOUT)

    def navigate(self, menu: str, submenu: str = None):
        """通过侧边栏菜单导航

        Args:
            menu: 一级菜单名称，如"订单管理"
            submenu: 二级菜单名称，如"订单列表"
        """
        logger.info(f"导航菜单: {menu}" + (f" > {submenu}" if submenu else ""))
        # 点击一级菜单
        self.page.get_by_text(menu, exact=False).first.click()
        if submenu:
            self.page.get_by_text(submenu, exact=False).first.click()
        self.wait_loading()

    def wait_loading(self, timeout: int = None):
        """等待页面加载完成（loading 消失）"""
        timeout = timeout or Config.ELEMENT_TIMEOUT
        try:
            loading = self.page.locator(".el-loading-mask, .ant-spin, .loading")
            if loading.count() > 0:
                loading.first.wait_for(state="hidden", timeout=timeout)
        except Exception:
            pass  # loading 不存在则直接继续

    def get_table_data(self, table_selector: str = "table"):
        """获取表格数据，返回字典列表"""
        table = self.page.locator(table_selector).first
        headers = table.locator("thead th").all_text_contents()
        rows = table.locator("tbody tr").all()
        data = []
        for row in rows:
            cells = row.locator("td").all_text_contents()
            if len(cells) == len(headers):
                data.append(dict(zip(headers, cells)))
        return data

    def search(self, keyword: str, input_placeholder: str = "请输入"):
        """搜索框输入并搜索"""
        search_input = self.page.get_by_placeholder(input_placeholder)
        search_input.fill(keyword)
        self.page.get_by_role("button", name="搜索").click()
        self.wait_loading()

    def click_button(self, name: str):
        """点击按钮"""
        self.page.get_by_role("button", name=name).click()

    def confirm_dialog(self):
        """确认弹窗"""
        self.page.get_by_role("button", name="确定").click()

    def cancel_dialog(self):
        """取消弹窗"""
        self.page.get_by_role("button", name="取消").click()

    def get_message(self) -> str:
        """获取页面提示消息（Element UI / Ant Design 消息组件）"""
        msg = self.page.locator(
            ".el-message, .ant-message, .el-notification"
        ).first
        return msg.text_content()

    def screenshot(self, name: str):
        """保存截图"""
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)
        path = os.path.join(Config.SCREENSHOTS_DIR, f"{name}.png")
        self.page.screenshot(path=path)
        logger.info(f"截图已保存: {path}")
        return path
