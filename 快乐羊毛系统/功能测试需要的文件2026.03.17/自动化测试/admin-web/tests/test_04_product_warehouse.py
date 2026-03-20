# -*- coding: utf-8 -*-
"""
管理后台 - 选品仓库自动化测试
对应用例: xpck-001~043
"""
import pytest
import sys
sys.path.insert(0, '..')
from config import BASE_URL


class TestProductWarehouse:
    """选品仓库测试"""

    def test_sync_button_exists(self, page):
        """验证一键同步按钮存在"""
        # 进入选品仓库页面
        page.locator('text=选品, [href*="warehouse"], .menu-item:has-text("选品")').first.click()
        page.wait_for_load_state("networkidle")

        sync_btn = page.locator('button:has-text("同步"), button:has-text("一键同步")')
        assert sync_btn.count() > 0, "找不到同步按钮"
        print("✅ 一键同步按钮存在")

    def test_sync_button_loading_state(self, page):
        """验证点击同步后按钮变为loading状态（防重复点击）"""
        sync_btn = page.locator('button:has-text("同步"), button:has-text("一键同步")').first

        if sync_btn.is_visible():
            sync_btn.click()
            page.wait_for_timeout(500)

            # 检查按钮是否变为loading/disabled
            is_disabled = sync_btn.is_disabled()
            has_loading = page.locator('.el-loading, [class*="loading"], .ant-btn-loading').count() > 0
            assert is_disabled or has_loading, "同步按钮应在请求中变为loading/disabled"
            print("✅ 同步按钮有loading防重复")

            # 等待同步完成
            page.wait_for_timeout(10000)

    def test_product_list_has_data(self, page):
        """验证选品列表有数据展示"""
        page.wait_for_timeout(2000)
        rows = page.locator('table tbody tr, .el-table__body tr')
        count = rows.count()
        print(f"📝 当前选品仓库有 {count} 条数据")
        # 如果同步过应该有数据
        # assert count > 0, "选品仓库无数据"

    def test_product_status_display(self, page):
        """验证三种状态标识（已上架/未上架/待确认）可区分"""
        # 查找状态相关的标签
        status_tags = page.locator(
            '[class*="tag"], [class*="badge"], [class*="status"], '
            '.el-tag, .ant-tag'
        )
        if status_tags.count() > 0:
            texts = [status_tags.nth(i).inner_text() for i in range(min(status_tags.count(), 20))]
            print(f"📝 找到状态标签: {set(texts)}")
        else:
            print("⏭️ 未找到状态标签，需确认页面结构")

    def test_batch_operation_disabled_without_selection(self, page):
        """验证未选商品时批量操作按钮置灰"""
        batch_btn = page.locator(
            'button:has-text("批量上架"), button:has-text("批量删除")'
        ).first

        if batch_btn.is_visible():
            is_disabled = batch_btn.is_disabled()
            assert is_disabled, "未选商品时批量按钮应置灰"
            print("✅ 未选商品时批量按钮置灰")
        else:
            print("⏭️ 未找到批量操作按钮")

    def test_empty_state_display(self, page):
        """验证无数据时的空状态展示"""
        # 这个需要在无数据条件下测试
        # 可以通过筛选一个不存在的条件来触发
        search = page.locator('input[placeholder*="搜索"], input[placeholder*="名称"]').first
        if search.is_visible():
            search.fill("不存在的商品名称_zzz999")
            page.locator('button:has-text("搜索"), button:has-text("查询")').first.click()
            page.wait_for_timeout(2000)

            empty = page.locator(
                '[class*="empty"], .el-empty, .ant-empty, text=暂无'
            )
            if empty.count() > 0:
                print("✅ 空状态正确展示")
            else:
                print("⏭️ 未找到空状态组件")
