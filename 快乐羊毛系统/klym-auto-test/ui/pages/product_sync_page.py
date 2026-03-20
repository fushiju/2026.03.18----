"""
ProductSyncPage - 选品仓库页面

导航路径：服务管理 > 服务管理（或独立菜单）
功能：一键同步、品牌管理、SKU管理、变更检测、批量操作
"""
from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage
from common.logger import logger


class ProductSyncPage(BasePage):
    """选品仓库页面"""

    def __init__(self, page: Page):
        super().__init__(page)

    def goto_product_sync(self):
        """导航到选品仓库页面"""
        # 根据实际菜单路径调整
        self.navigate("服务管理", "服务管理")

    def click_sync(self):
        """点击一键同步按钮"""
        logger.info("点击一键同步")
        self.click_button("一键同步")

    def wait_sync_complete(self, timeout: int = 60000):
        """等待同步完成"""
        # 等待同步按钮恢复可用或结果弹窗出现
        self.page.wait_for_timeout(2000)
        sync_btn = self.page.get_by_role("button", name="一键同步")
        sync_btn.wait_for(state="visible", timeout=timeout)
        self.wait_loading()
        logger.info("同步完成")

    def get_sync_result(self) -> str:
        """获取同步结果消息"""
        return self.get_message()

    def is_sync_button_disabled(self) -> bool:
        """同步按钮是否置灰"""
        btn = self.page.get_by_role("button", name="一键同步")
        return btn.is_disabled()

    # ---- 列表操作 ----

    def get_product_list(self) -> list:
        """获取商品列表"""
        return self.get_table_data()

    def filter_by_status(self, status: str):
        """按状态筛选（已上架/未上架/待确认）"""
        logger.info(f"筛选状态: {status}")
        # Element UI 下拉
        self.page.locator(".el-select:has-text('状态')").click()
        self.page.get_by_text(status, exact=True).click()
        self.wait_loading()

    def filter_by_channel(self, channel: str):
        """按渠道筛选"""
        logger.info(f"筛选渠道: {channel}")
        self.page.locator(".el-select:has-text('渠道')").click()
        self.page.get_by_text(channel, exact=True).click()
        self.wait_loading()

    def search_product(self, keyword: str):
        """搜索商品"""
        self.search(keyword)

    # ---- 品牌/商品操作 ----

    def click_brand_detail(self, brand_name: str):
        """点击品牌名进入详情"""
        self.page.get_by_text(brand_name).first.click()
        self.wait_loading()

    def click_edit(self, product_name: str):
        """点击编辑"""
        row = self.page.locator(f"tr:has-text('{product_name}')")
        row.get_by_text("编辑").click()
        self.wait_loading()

    def confirm_change(self, product_name: str):
        """确认变更（待确认状态的商品）"""
        row = self.page.locator(f"tr:has-text('{product_name}')")
        row.get_by_text("确认").click()
        self.confirm_dialog()
        self.wait_loading()

    def shelve_product(self, product_name: str):
        """上架商品"""
        row = self.page.locator(f"tr:has-text('{product_name}')")
        row.get_by_text("上架").click()
        self.wait_loading()

    # ---- 批量操作 ----

    def select_all(self):
        """全选"""
        checkbox = self.page.locator("thead .el-checkbox__input").first
        checkbox.click()

    def select_product(self, product_name: str):
        """选择单个商品"""
        row = self.page.locator(f"tr:has-text('{product_name}')")
        row.locator(".el-checkbox__input").click()

    def batch_shelve(self):
        """批量上架"""
        self.click_button("批量上架")
        self.confirm_dialog()
        self.wait_loading()

    def batch_delete(self):
        """批量删除"""
        self.click_button("批量删除")

    def is_batch_button_disabled(self, name: str) -> bool:
        """批量操作按钮是否置灰"""
        btn = self.page.get_by_role("button", name=name)
        return btn.is_disabled()

    # ---- 状态验证 ----

    def get_product_status(self, product_name: str) -> str:
        """获取商品状态标签"""
        row = self.page.locator(f"tr:has-text('{product_name}')")
        tag = row.locator(".el-tag").first
        return tag.text_content().strip() if tag.count() > 0 else ""

    def has_empty_state(self) -> bool:
        """是否显示空状态"""
        empty = self.page.locator(".el-empty, .el-table__empty-text")
        return empty.count() > 0

    def get_pagination_total(self) -> str:
        """获取分页总数"""
        total = self.page.locator(".el-pagination__total")
        return total.text_content().strip() if total.count() > 0 else ""
