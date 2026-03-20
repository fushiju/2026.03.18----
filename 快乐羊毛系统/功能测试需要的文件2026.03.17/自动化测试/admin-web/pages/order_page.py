# -*- coding: utf-8 -*-
"""订单管理页面 Page Object"""
from config import BASE_URL


class OrderPage:
    def __init__(self, page):
        self.page = page
        # ====== 选择器（根据实际页面修改）======
        self.menu_order = 'text=订单, [href*="order"], .menu-item:has-text("订单")'
        self.table_rows = 'table tbody tr, .el-table__body tr'
        self.search_input = 'input[placeholder*="订单号"], input[placeholder*="搜索"]'
        self.search_btn = 'button:has-text("搜索"), button:has-text("查询")'
        self.type_filter = 'select[name*="type"], .el-select:has-text("类型")'
        self.status_filter = 'select[name*="status"], .el-select:has-text("状态")'
        self.refund_btn = 'button:has-text("退款")'
        self.retry_btn = 'button:has-text("重试")'

    def goto(self):
        """进入订单管理页"""
        # 尝试点击左侧菜单
        try:
            self.page.locator(self.menu_order).first.click()
            self.page.wait_for_load_state("networkidle")
        except Exception:
            # 直接URL访问
            self.page.goto(f"{BASE_URL}/order")
            self.page.wait_for_load_state("networkidle")
        return self

    def get_order_count(self):
        """获取当前列表订单数"""
        return self.page.locator(self.table_rows).count()

    def search_order(self, order_no):
        """搜索订单"""
        self.page.locator(self.search_input).first.fill(order_no)
        self.page.locator(self.search_btn).first.click()
        self.page.wait_for_load_state("networkidle")
        return self

    def has_refund_button(self, row_index=0):
        """某行订单是否有退款按钮"""
        row = self.page.locator(self.table_rows).nth(row_index)
        return row.locator(self.refund_btn).count() > 0

    def has_retry_button(self, row_index=0):
        """某行订单是否有重试发货按钮"""
        row = self.page.locator(self.table_rows).nth(row_index)
        return row.locator(self.retry_btn).count() > 0

    def click_refund(self, row_index=0):
        """点击退款"""
        row = self.page.locator(self.table_rows).nth(row_index)
        row.locator(self.refund_btn).first.click()
        return self

    def get_order_status(self, row_index=0):
        """获取订单状态文本"""
        row = self.page.locator(self.table_rows).nth(row_index)
        # 状态通常在某一列，这里取所有td的文本
        cells = row.locator("td").all_inner_texts()
        return cells
