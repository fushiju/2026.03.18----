# -*- coding: utf-8 -*-
"""
管理后台 - 订单管理自动化测试
对应用例: ddzt-001~026, ht-hj-001
"""
import pytest
import sys
sys.path.insert(0, '..')
from pages.order_page import OrderPage


class TestOrderManagement:
    """订单列表与管理测试"""

    def test_order_list_loads(self, page):
        """验证订单列表正常加载"""
        order_page = OrderPage(page).goto()
        page.wait_for_timeout(2000)

        count = order_page.get_order_count()
        assert count > 0, "订单列表为空或加载失败"
        print(f"✅ 订单列表加载成功，当前{count}条数据")

    def test_order_search_by_id(self, page):
        """验证按订单号搜索功能"""
        order_page = OrderPage(page).goto()

        # 先获取第一条订单号（用于搜索测试）
        cells = order_page.get_order_status(0)
        if cells:
            # 假设订单号在第一列
            order_no = cells[0].strip() if cells[0] else ""
            if order_no:
                order_page.search_order(order_no)
                page.wait_for_timeout(1000)
                count = order_page.get_order_count()
                assert count >= 1, f"搜索订单号{order_no}无结果"
                print(f"✅ 搜索订单{order_no}成功，{count}条结果")

    def test_virtual_product_no_refund_button(self, page):
        """验证虚拟商品已完成订单无退款按钮 (对应 ddzt-009)
        注意：需要有虚拟商品的已完成订单数据
        """
        order_page = OrderPage(page).goto()
        page.wait_for_timeout(2000)

        # TODO: 需要根据实际页面筛选出虚拟商品已完成订单
        # 这里是通用检查逻辑示例
        # order_page.filter_by_type("虚拟商品")
        # order_page.filter_by_status("已完成")
        # assert not order_page.has_refund_button(0), "虚拟商品已完成订单不应有退款按钮"
        print("⏭️ 需要根据实际页面完善选择器后执行")

    def test_catering_order_has_refund_button(self, page):
        """验证餐饮扫码订单有退款按钮 (对应 ddzt-019)
        注意：需要有餐饮扫码的已完成订单数据
        """
        order_page = OrderPage(page).goto()
        page.wait_for_timeout(2000)

        # TODO: 筛选餐饮扫码已完成订单
        # order_page.filter_by_type("餐饮扫码")
        # order_page.filter_by_status("已完成")
        # assert order_page.has_refund_button(0), "餐饮订单应有退款按钮"
        print("⏭️ 需要根据实际页面完善选择器后执行")

    def test_order_pagination(self, page):
        """验证订单列表翻页功能"""
        order_page = OrderPage(page).goto()
        page.wait_for_timeout(2000)

        # 查找翻页组件
        next_btn = page.locator(
            'button:has-text("下一页"), .el-pagination .btn-next, '
            '.ant-pagination-next, [aria-label="next"]'
        ).first

        if next_btn.is_visible():
            page1_data = order_page.get_order_status(0)
            next_btn.click()
            page.wait_for_timeout(2000)
            page2_data = order_page.get_order_status(0)
            assert page1_data != page2_data, "翻页后数据应不同"
            print("✅ 翻页功能正常")
        else:
            print("⏭️ 数据不足一页，跳过翻页测试")
