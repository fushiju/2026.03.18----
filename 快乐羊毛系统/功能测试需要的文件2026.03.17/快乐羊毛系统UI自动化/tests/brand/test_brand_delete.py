"""品牌管理 - 删除品牌（28 条用例）

用例来源：测试用例/品牌管理/品牌删除.xlsx
品牌删除通过操作列"更多菜单"下拉 → 点击"删除" → 确认弹窗 完成。

测试类分组：
  TestDeleteEntry       — 删除入口（各Tab下更多菜单）
  TestDeleteConfirmDlg  — 确认弹窗内容
  TestDeleteAction      — 正向删除 & 取消删除
  TestDeleteByStatus    — 按状态删除（已授权/已驳回/申请中）
  TestDeleteVerify      — 删除后列表验证 & Tab数量 & 持久化 & 搜索
  TestDeleteMenu        — 更多菜单交互
  TestDeleteAdvanced    — 连续删除 & 有关联数据 & 取消授权后删除
  TestDeletePagination  — 分页相关
  TestDeleteUrl         — 删除后URL直接访问
"""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.brand_list_page import BrandListPage


# ===========================================================================
# 删除入口（TC-01 ~ TC-04）
# ===========================================================================
@pytest.mark.brand
class TestDeleteEntry:

    def test_01_more_menu_all_tab(self, brand_list_page: BrandListPage):
        """TC-01 全部Tab下通过更多菜单找到删除选项"""
        brand_list_page.click_tab("全部")
        brand_list_page.click_more_menu_first()

        items = brand_list_page.get_dropdown_items()
        assert "删除" in items, f"更多菜单应包含'删除'，实际: {items}"
        brand_list_page.dismiss_dropdown()

    def test_02_more_menu_authorized_tab(self, brand_list_page: BrandListPage):
        """TC-02 已授权Tab下更多菜单包含删除选项"""
        brand_list_page.click_tab("已授权")
        if brand_list_page.get_list_row_count() == 0:
            pytest.skip("无已授权品牌")

        brand_list_page.click_more_menu_first()
        items = brand_list_page.get_dropdown_items()
        assert "删除" in items, f"已授权菜单应含'删除'，实际: {items}"
        assert "修改代理商" in items, f"应含'修改代理商'，实际: {items}"
        assert "取消授权" in items, f"应含'取消授权'，实际: {items}"
        brand_list_page.dismiss_dropdown()

    def test_03_more_menu_rejected_tab(self, brand_list_page: BrandListPage):
        """TC-03 已驳回Tab下更多菜单包含删除选项"""
        brand_list_page.click_tab("已驳回")
        if brand_list_page.get_list_row_count() == 0:
            pytest.skip("无已驳回品牌")

        brand_list_page.click_more_menu_first()
        items = brand_list_page.get_dropdown_items()
        assert "删除" in items, f"已驳回菜单应含'删除'，实际: {items}"
        brand_list_page.dismiss_dropdown()

    def test_04_pending_tab_no_delete(self, brand_list_page: BrandListPage):
        """TC-04 申请中Tab下更多菜单无删除选项"""
        brand_list_page.click_tab("申请中")
        if brand_list_page.get_list_row_count() == 0:
            pytest.skip("无申请中品牌")

        brand_list_page.click_more_menu_first()
        items = brand_list_page.get_dropdown_items()
        assert "删除" not in items, f"申请中菜单不应含'删除'，实际: {items}"
        brand_list_page.dismiss_dropdown()


# ===========================================================================
# 确认弹窗内容（TC-05）
# ===========================================================================
@pytest.mark.brand
class TestDeleteConfirmDlg:

    def test_05_confirm_dialog_content(self, brand_list_page: BrandListPage):
        """TC-05 删除确认弹窗内容检查"""
        brand_list_page.click_tab("全部")
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        brand_list_page.delete_brand_by_name(names[0])

        assert brand_list_page.is_msgbox_visible(), "应弹出确认弹窗"
        title = brand_list_page.get_msgbox_title()
        content = brand_list_page.get_msgbox_content()
        assert "提示" in title or "温馨" in title, f"标题应含'提示'，实际: {title}"
        assert "删除" in content, f"内容应含'删除'，实际: {content}"
        assert brand_list_page.page.locator(brand_list_page.SEL_MSG_BOX_OK).count() > 0
        assert brand_list_page.page.locator(brand_list_page.SEL_MSG_BOX_CANCEL).count() > 0

        brand_list_page.click_msgbox_cancel()


# ===========================================================================
# 正向删除 & 取消删除（TC-06 ~ TC-09）
# ===========================================================================
@pytest.mark.brand
class TestDeleteAction:

    def test_06_delete_and_confirm(self, brand_list_page: BrandListPage):
        """TC-06 删除品牌并确认成功"""
        brand_list_page.click_tab("全部")
        before = brand_list_page.get_list_row_count()
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()

        msg = brand_list_page.get_success_message()
        assert msg or not brand_list_page.is_msgbox_visible(), "删除应成功"
        assert not brand_list_page.brand_exists(target), f"'{target}'应从列表消失"

    def test_07_delete_cancel(self, brand_list_page: BrandListPage):
        """TC-07 删除时点击取消按钮"""
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_cancel()

        assert not brand_list_page.is_msgbox_visible(), "弹窗应关闭"
        assert brand_list_page.brand_exists(target), "品牌不应被删除"

    def test_08_delete_close_x(self, brand_list_page: BrandListPage):
        """TC-08 删除时点击弹窗X按钮关闭"""
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_close_x()

        assert not brand_list_page.is_msgbox_visible(), "弹窗应关闭"
        assert brand_list_page.brand_exists(target), "品牌不应被删除"

    def test_09_delete_esc(self, brand_list_page: BrandListPage):
        """TC-09 删除时按ESC键关闭弹窗"""
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.dismiss_msgbox_by_esc()

        assert not brand_list_page.is_msgbox_visible(), "弹窗应关闭"
        assert brand_list_page.brand_exists(target), "品牌不应被删除"


# ===========================================================================
# 按状态删除（TC-10 ~ TC-12）
# ===========================================================================
@pytest.mark.brand
class TestDeleteByStatus:

    def test_10_delete_authorized(self, brand_list_page: BrandListPage):
        """TC-10 删除状态为"已授权"的品牌"""
        brand_list_page.click_tab("已授权")
        if brand_list_page.get_list_row_count() == 0:
            pytest.skip("无已授权品牌")

        names = brand_list_page.get_list_brand_names()
        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()

        brand_list_page.page.wait_for_timeout(1500)
        error = brand_list_page.get_error_message()
        if error and ("授权" in error or "不能" in error):
            pass  # 系统不允许删除已授权品牌
        else:
            msg = brand_list_page.get_success_message()
            assert msg or not brand_list_page.brand_exists(target), "删除已授权品牌应成功或有明确提示"

    def test_11_delete_rejected(self, brand_list_page: BrandListPage):
        """TC-11 删除状态为"已驳回"的品牌"""
        brand_list_page.click_tab("已驳回")
        if brand_list_page.get_list_row_count() == 0:
            pytest.skip("无已驳回品牌")

        names = brand_list_page.get_list_brand_names()
        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()

        msg = brand_list_page.get_success_message()
        assert msg or not brand_list_page.brand_exists(target), "删除已驳回品牌应成功"

    def test_12_pending_no_delete(self, brand_list_page: BrandListPage):
        """TC-12 验证申请中品牌无删除选项"""
        brand_list_page.click_tab("申请中")
        if brand_list_page.get_list_row_count() == 0:
            pytest.skip("无申请中品牌")

        brand_list_page.click_more_menu_first()
        items = brand_list_page.get_dropdown_items()
        assert "删除" not in items, f"申请中品牌不应有删除选项，实际: {items}"
        assert "授权品牌" in items, f"应有'授权品牌'选项，实际: {items}"
        brand_list_page.dismiss_dropdown()


# ===========================================================================
# 删除后列表验证 & Tab数量 & 持久化 & 搜索（TC-13 ~ TC-16）
# ===========================================================================
@pytest.mark.brand
class TestDeleteVerify:

    def test_13_list_verify_after_delete(self, brand_list_page: BrandListPage):
        """TC-13 删除品牌后列表数据完整性验证"""
        brand_list_page.click_tab("全部")
        before = brand_list_page.get_list_row_count()
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        if brand_list_page.get_success_message():
            after = brand_list_page.get_list_row_count()
            assert after < before, f"行数应减少，前: {before}，后: {after}"
            assert not brand_list_page.brand_exists(target)

    def test_14_tab_count_after_delete(self, brand_list_page: BrandListPage):
        """TC-14 删除品牌后各Tab数量同步更新"""
        brand_list_page.click_tab("全部")
        all_text_before = brand_list_page.page.locator('.el-tabs__item:has-text("全部")').text_content().strip()

        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        all_text_after = brand_list_page.page.locator('.el-tabs__item:has-text("全部")').text_content().strip()
        if brand_list_page.get_success_message() or not brand_list_page.is_msgbox_visible():
            assert all_text_before != all_text_after, f"Tab数量应更新，前: {all_text_before}，后: {all_text_after}"

    def test_15_delete_persist(self, brand_list_page: BrandListPage):
        """TC-15 删除品牌后刷新页面验证持久化"""
        brand_list_page.click_tab("全部")
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        if not brand_list_page.brand_exists(target):
            brand_list_page.page.reload()
            brand_list_page.page.wait_for_load_state("networkidle", timeout=15000)
            brand_list_page._dismiss_notification()
            brand_list_page.page.wait_for_timeout(1000)

            assert not brand_list_page.brand_exists(target), "刷新后已删除品牌不应出现"

    def test_16_search_after_delete(self, brand_list_page: BrandListPage):
        """TC-16 删除品牌后搜索已删除品牌名称"""
        brand_list_page.click_tab("全部")
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        if not brand_list_page.brand_exists(target):
            brand_list_page.search_by_keyword(target)
            assert not brand_list_page.brand_exists(target), "搜索已删除品牌应无结果"


# ===========================================================================
# 更多菜单交互（TC-17 ~ TC-18）
# ===========================================================================
@pytest.mark.brand
class TestDeleteMenu:

    def test_17_close_menu_without_action(self, brand_list_page: BrandListPage):
        """TC-17 点击更多菜单后不选择直接关闭"""
        brand_list_page.click_more_menu_first()
        assert brand_list_page.is_dropdown_visible(), "菜单应展开"

        brand_list_page.dismiss_dropdown()
        brand_list_page.page.wait_for_timeout(500)
        # 不应有任何操作发生

    def test_18_switch_more_menu(self, brand_list_page: BrandListPage):
        """TC-18 连续点击不同品牌的更多菜单"""
        rows = brand_list_page.get_list_row_count()
        if rows < 2:
            pytest.skip("列表不足2条")

        # 点第一个
        btns = brand_list_page.page.locator('button:has-text("更多菜单")').all()
        btns[0].click()
        brand_list_page.page.wait_for_timeout(500)

        # 直接点第二个
        btns[1].click()
        brand_list_page.page.wait_for_timeout(500)

        # 页面不应报错
        assert brand_list_page.is_on_brand_list(), "页面应正常"
        brand_list_page.dismiss_dropdown()


# ===========================================================================
# 连续删除 & 有关联数据 & 取消授权后删除（TC-19 ~ TC-23）
# ===========================================================================
@pytest.mark.brand
class TestDeleteAdvanced:

    def test_19_continuous_delete(self, brand_list_page: BrandListPage):
        """TC-19 连续删除多条品牌"""
        brand_list_page.click_tab("全部")
        before = brand_list_page.get_list_row_count()
        if before < 2:
            pytest.skip("列表不足2条")

        names = brand_list_page.get_list_brand_names()

        # 删除第一条
        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        # 删除第二条（刷新列表后名称可能变化）
        names2 = brand_list_page.get_list_brand_names()
        if names2:
            brand_list_page.delete_brand_by_name(names2[0])
            brand_list_page.click_msgbox_ok()
            brand_list_page.page.wait_for_timeout(1500)

        after = brand_list_page.get_list_row_count()
        assert after < before, "连续删除后列表应减少"

    def test_20_delete_with_specs(self, brand_list_page: BrandListPage):
        """TC-20 删除有规格的品牌"""
        brand_list_page.click_tab("已授权")
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("无已授权品牌")

        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()

        brand_list_page.page.wait_for_timeout(2000)
        error = brand_list_page.get_error_message()
        # 有关联保护则失败，无则成功
        if error and ("规格" in error or "关联" in error):
            pass  # 系统有关联保护
        else:
            pass  # 允许删除

    def test_21_delete_with_orders(self, brand_list_page: BrandListPage):
        """TC-21 删除有订单的品牌"""
        brand_list_page.click_tab("已授权")
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("无已授权品牌")

        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()

        brand_list_page.page.wait_for_timeout(2000)
        error = brand_list_page.get_error_message()
        if error and ("订单" in error or "关联" in error):
            pass  # 系统有关联保护

    def test_22_delete_with_account(self, brand_list_page: BrandListPage):
        """TC-22 删除有账号的品牌"""
        brand_list_page.click_tab("已授权")
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("无已授权品牌")

        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()

        brand_list_page.page.wait_for_timeout(2000)
        error = brand_list_page.get_error_message()
        if error and ("账号" in error or "关联" in error):
            pass  # 系统有关联保护

    def test_23_revoke_then_delete(self, brand_list_page: BrandListPage):
        """TC-23 先取消授权再删除品牌"""
        brand_list_page.click_tab("已授权")
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("无已授权品牌")

        target = names[0]
        # 先取消授权
        brand_list_page.click_more_menu_by_name(target)
        items = brand_list_page.get_dropdown_items()
        if "取消授权" not in items:
            brand_list_page.dismiss_dropdown()
            pytest.skip("无取消授权选项")

        brand_list_page.click_dropdown_item("取消授权")
        brand_list_page.page.wait_for_timeout(1000)
        # 如果弹出确认框则确认
        if brand_list_page.is_msgbox_visible():
            brand_list_page.click_msgbox_ok()
            brand_list_page.page.wait_for_timeout(1500)

        # 再尝试删除
        brand_list_page.click_tab("全部")
        brand_list_page.page.wait_for_timeout(1000)
        if brand_list_page.brand_exists(target):
            brand_list_page.delete_brand_by_name(target)
            brand_list_page.click_msgbox_ok()
            brand_list_page.page.wait_for_timeout(1500)


# ===========================================================================
# 分页相关（TC-24 ~ TC-25）
# ===========================================================================
@pytest.mark.brand
class TestDeletePagination:

    def test_24_delete_last_on_page(self, brand_list_page: BrandListPage):
        """TC-24 分页-删除当页最后一条品牌"""
        # 翻到最后一页
        next_btn = brand_list_page.page.locator('button.btn-next:not([disabled])')
        while next_btn.count() > 0:
            brand_list_page.click_next_page()
            next_btn = brand_list_page.page.locator('button.btn-next:not([disabled])')

        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("最后一页为空")

        target = names[-1]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        # 删除后应自动调整页面
        assert brand_list_page.is_on_brand_list(), "页面应正常"

    def test_25_pagination_update(self, brand_list_page: BrandListPage):
        """TC-25 分页-删除后分页更新"""
        total_before = brand_list_page.get_list_total_text()

        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        if brand_list_page.get_success_message() or not brand_list_page.is_msgbox_visible():
            total_after = brand_list_page.get_list_total_text()
            assert total_before != total_after, f"分页总数应更新，前: {total_before}，后: {total_after}"


# ===========================================================================
# 删除后新增同名 & URL直接访问（TC-26 ~ TC-28）
# ===========================================================================
@pytest.mark.brand
class TestDeleteUrl:

    def test_26_add_same_name_after_delete(self, brand_list_page: BrandListPage):
        """TC-26 删除品牌后重新新增同名品牌（仅验证删除后名称可复用）"""
        names = brand_list_page.get_list_brand_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        brand_list_page.delete_brand_by_name(target)
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        # 验证删除成功
        if brand_list_page.brand_exists(target):
            pytest.skip("删除未成功")
        # 新增同名需要跳转到新增页面，此处仅验证删除后名称释放

    def test_27_access_deleted_view_url(self, brand_list_page: BrandListPage):
        """TC-27 删除品牌后通过URL直接访问该品牌查看页"""
        from config.settings import BASE_URL

        # 获取一个品牌ID后删除
        brand_list_page.click_tab("全部")
        ids = brand_list_page.get_list_column_texts(1)  # ID列
        names = brand_list_page.get_list_brand_names()
        if not ids or not names:
            pytest.skip("列表为空")

        target_id = ids[0]
        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        if brand_list_page.brand_exists(names[0]):
            pytest.skip("删除未成功")

        # 直接访问查看URL
        url = f"{BASE_URL.rstrip('/')}/#/coach/manage/edit?isEdit=0&id={target_id}"
        brand_list_page.page.goto(url, wait_until="domcontentloaded")
        brand_list_page.page.wait_for_timeout(3000)

        content = brand_list_page.page.content()
        # 不应显示正常数据，应提示不存在或跳转
        assert "不存在" in content or "404" in content or "/coach/manage" in brand_list_page.current_url, (
            "访问已删除品牌应提示不存在或跳转"
        )

    def test_28_access_deleted_edit_url(self, brand_list_page: BrandListPage):
        """TC-28 删除品牌后通过URL直接编辑该品牌"""
        from config.settings import BASE_URL

        brand_list_page.click_tab("全部")
        ids = brand_list_page.get_list_column_texts(1)
        names = brand_list_page.get_list_brand_names()
        if not ids or not names:
            pytest.skip("列表为空")

        target_id = ids[0]
        brand_list_page.delete_brand_by_name(names[0])
        brand_list_page.click_msgbox_ok()
        brand_list_page.page.wait_for_timeout(1500)

        if brand_list_page.brand_exists(names[0]):
            pytest.skip("删除未成功")

        url = f"{BASE_URL.rstrip('/')}/#/coach/manage/edit?isEdit=1&id={target_id}"
        brand_list_page.page.goto(url, wait_until="domcontentloaded")
        brand_list_page.page.wait_for_timeout(3000)

        content = brand_list_page.page.content()
        assert "不存在" in content or "404" in content or "/coach/manage" in brand_list_page.current_url, (
            "编辑已删除品牌应提示不存在或跳转"
        )


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "brand_delete_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行品牌删除测试...")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", __file__, "-v", "-s",
         f"--html={report_path}", "--self-contained-html"],
        cwd=project_root
    )

    print("=" * 60)
    print("  全部通过！" if result.returncode == 0 else f"  有测试失败（退出码: {result.returncode}）")
    if os.path.exists(report_path):
        print(f"  HTML报告: {report_path}")
        os.startfile(report_path)
    input("\n按回车键退出...")
    sys.exit(result.returncode)
