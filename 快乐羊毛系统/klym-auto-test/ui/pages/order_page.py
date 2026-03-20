"""
OrderPage - 订单管理页面

导航路径：订单管理 > 服务订单 / 退款管理
功能：订单列表、订单详情、状态流转、退款操作
"""
from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage
from common.logger import logger


class OrderListPage(BasePage):
    """订单列表页面"""

    def __init__(self, page: Page):
        super().__init__(page)

    def goto_order_list(self):
        """导航到服务订单页面"""
        self.navigate("订单管理", "服务订单")

    def search_order(self, order_no: str):
        """搜索订单"""
        self.search(order_no, "请输入订单号")

    def filter_by_status(self, status: str):
        """按状态筛选（待支付/已完成/已退款等）"""
        logger.info(f"筛选状态: {status}")
        status_select = self.page.locator(".el-select").first
        status_select.click()
        self.page.get_by_text(status, exact=True).click()
        self.wait_loading()

    def filter_by_type(self, type_name: str):
        """按订单类型筛选（type_id）"""
        logger.info(f"筛选类型: {type_name}")
        # 根据实际页面调整
        self.page.get_by_text(type_name).click()
        self.wait_loading()

    def get_order_list(self) -> list:
        """获取订单列表数据"""
        return self.get_table_data()

    def click_order_detail(self, order_no: str):
        """点击进入订单详情"""
        row = self.page.locator(f"tr:has-text('{order_no}')")
        row.locator("text=详情, text=查看").first.click()
        self.wait_loading()

    def get_order_status(self, order_no: str) -> str:
        """获取订单状态"""
        row = self.page.locator(f"tr:has-text('{order_no}')")
        # 通常状态在某一列，用标签展示
        status = row.locator(".el-tag, td:nth-child(5)").first.text_content()
        return status.strip() if status else ""


class OrderDetailPage(BasePage):
    """订单详情页面"""

    def __init__(self, page: Page):
        super().__init__(page)

    def get_order_info(self) -> dict:
        """获取订单详情信息"""
        info = {}
        # 常见的描述列表布局
        items = self.page.locator(".el-descriptions-item, .detail-item")
        for i in range(items.count()):
            text = items.nth(i).text_content()
            if "：" in text:
                key, val = text.split("：", 1)
                info[key.strip()] = val.strip()
        return info

    def click_refund(self):
        """点击退款按钮"""
        self.click_button("退款")

    def click_retry_delivery(self):
        """点击重试发货按钮"""
        self.click_button("重试发货")

    def fill_refund_reason(self, reason: str):
        """填写退款原因"""
        textarea = self.page.locator(
            "textarea[placeholder*='退款原因'], textarea[placeholder*='原因']"
        )
        textarea.fill(reason)

    def fill_refund_amount(self, amount: str):
        """填写退款金额"""
        amount_input = self.page.locator(
            "input[placeholder*='退款金额'], input[placeholder*='金额']"
        )
        amount_input.fill(str(amount))

    def confirm_refund(self):
        """确认退款"""
        self.confirm_dialog()
        self.wait_loading()

    def has_refund_button(self) -> bool:
        """是否有退款按钮"""
        return self.page.get_by_role("button", name="退款").count() > 0

    def has_retry_button(self) -> bool:
        """是否有重试发货按钮"""
        return self.page.get_by_role("button", name="重试发货").count() > 0

    def assert_no_refund_button(self):
        """断言没有退款按钮（虚拟商品已完成状态）"""
        assert not self.has_refund_button(), "不应显示退款按钮"


class RefundPage(BasePage):
    """退款管理页面"""

    def __init__(self, page: Page):
        super().__init__(page)

    def goto_refund(self):
        """导航到退款管理"""
        self.navigate("订单管理", "退款管理")

    def approve_refund(self, order_no: str):
        """审核通过退款"""
        row = self.page.locator(f"tr:has-text('{order_no}')")
        row.get_by_text("通过").click()
        self.confirm_dialog()
        self.wait_loading()

    def reject_refund(self, order_no: str, reason: str):
        """驳回退款"""
        row = self.page.locator(f"tr:has-text('{order_no}')")
        row.get_by_text("驳回").click()
        textarea = self.page.locator("textarea")
        textarea.fill(reason)
        self.confirm_dialog()
        self.wait_loading()
