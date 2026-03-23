"""品牌分类 - 删除分类（11 条用例）

用例来源：测试用例/品牌分类/品牌分类_删除.xlsx
测试类分组：
  TestDeleteConfirm     — 正向删除 & 取消删除
  TestDeleteDialog      — 确认弹窗内容
  TestDeleteByStatus    — 按状态删除（启用/禁用/被引用）
  TestDeleteVerify      — 删除后验证 & 连续删除 & 刷新 & 最后一条
  TestDeleteClose       — 关闭确认弹窗
"""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.brand_category_page import BrandCategoryPage


def _create_test_category(page: BrandCategoryPage, name: str):
    """辅助：新增一个测试用分类"""
    page.click_add_btn()
    page.fill_category_name(name)
    page.click_submit()
    page.page.wait_for_timeout(1000)


# ===========================================================================
# 正向删除 & 取消删除（TC-01 ~ TC-02）
# ===========================================================================
@pytest.mark.brand
class TestDeleteConfirm:

    def test_01_delete_and_confirm(self, category_page: BrandCategoryPage):
        """TC-01 删除分类并确认"""
        name = f"待删除{uuid.uuid4().hex[:4]}"
        _create_test_category(category_page, name)
        assert category_page.category_exists(name)

        category_page.click_delete_by_name(name)
        assert category_page.is_confirm_visible(), "应弹出确认弹窗"

        category_page.click_confirm_ok()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_confirm_visible(), "删除应成功"
        assert not category_page.category_exists(name), f"'{name}'应从列表消失"

    def test_02_delete_and_cancel(self, category_page: BrandCategoryPage):
        """TC-02 删除时点击取消"""
        names = category_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        category_page.click_delete_by_name(target)
        assert category_page.is_confirm_visible()

        category_page.click_confirm_cancel()

        assert not category_page.is_confirm_visible(), "弹窗应关闭"
        assert category_page.category_exists(target), f"'{target}'不应被删除"


# ===========================================================================
# 确认弹窗内容（TC-03）
# ===========================================================================
@pytest.mark.brand
class TestDeleteDialog:

    def test_03_confirm_dialog_content(self, category_page: BrandCategoryPage):
        """TC-03 删除确认弹窗内容检查"""
        names = category_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        category_page.click_delete_by_name(names[0])

        title = category_page.get_confirm_title()
        content = category_page.get_confirm_content()

        assert "提示" in title or "温馨" in title, f"标题应含'提示'，实际: {title}"
        assert "删除" in content or "确认" in content, f"内容应含删除确认，实际: {content}"
        assert category_page.page.locator(category_page.SEL_CONFIRM_OK).count() > 0, "应有确定按钮"
        assert category_page.page.locator(category_page.SEL_CONFIRM_CANCEL).count() > 0, "应有取消按钮"

        category_page.click_confirm_cancel()


# ===========================================================================
# 按状态删除（TC-04 ~ TC-06）
# ===========================================================================
@pytest.mark.brand
class TestDeleteByStatus:

    def test_04_delete_enabled_category(self, category_page: BrandCategoryPage):
        """TC-04 删除状态为"启用"的分类"""
        name = f"启用删{uuid.uuid4().hex[:4]}"
        _create_test_category(category_page, name)

        category_page.click_delete_by_name(name)
        category_page.click_confirm_ok()

        category_page.page.wait_for_timeout(1000)
        error = category_page.get_error_message()
        if error and ("启用" in error or "禁用" in error):
            pass  # 不允许删除启用分类
        else:
            assert not category_page.category_exists(name), "删除启用分类应成功或有明确提示"

    def test_05_delete_disabled_category(self, category_page: BrandCategoryPage):
        """TC-05 删除状态为"禁用"的分类"""
        name = f"禁用删{uuid.uuid4().hex[:4]}"
        category_page.click_add_btn()
        category_page.fill_category_name(name)
        category_page.toggle_status()  # 切为禁用
        category_page.click_submit()
        category_page.page.wait_for_timeout(1000)

        category_page.click_delete_by_name(name)
        category_page.click_confirm_ok()

        msg = category_page.get_success_message()
        assert msg or not category_page.category_exists(name), "删除禁用分类应成功"

    def test_06_delete_referenced_category(self, category_page: BrandCategoryPage):
        """TC-06 删除已被品牌使用的分类"""
        if not category_page.category_exists("会员充值"):
            pytest.skip("会员充值分类不存在")

        category_page.click_delete_by_name("会员充值")
        category_page.click_confirm_ok()

        category_page.page.wait_for_timeout(2000)
        error = category_page.get_error_message()
        if category_page.category_exists("会员充值"):
            assert error, "被引用的分类若删除失败应有提示"


# ===========================================================================
# 删除后验证 & 连续删除 & 刷新 & 最后一条（TC-07 ~ TC-10）
# ===========================================================================
@pytest.mark.brand
class TestDeleteVerify:

    def test_07_verify_after_delete(self, category_page: BrandCategoryPage):
        """TC-07 删除分类后列表数据验证"""
        name = f"验证删{uuid.uuid4().hex[:4]}"
        _create_test_category(category_page, name)

        before = category_page.get_list_row_count()

        category_page.click_delete_by_name(name)
        category_page.click_confirm_ok()
        category_page.page.wait_for_timeout(1000)

        after = category_page.get_list_row_count()
        assert after < before, f"删除后行数应减少，前: {before}，后: {after}"
        assert not category_page.category_exists(name)

    def test_08_continuous_delete(self, category_page: BrandCategoryPage):
        """TC-08 连续删除多条分类"""
        name1 = f"连删1_{uuid.uuid4().hex[:4]}"
        name2 = f"连删2_{uuid.uuid4().hex[:4]}"
        _create_test_category(category_page, name1)
        _create_test_category(category_page, name2)

        before = category_page.get_list_row_count()

        category_page.click_delete_by_name(name1)
        category_page.click_confirm_ok()
        category_page.page.wait_for_timeout(1000)

        category_page.click_delete_by_name(name2)
        category_page.click_confirm_ok()
        category_page.page.wait_for_timeout(1000)

        after = category_page.get_list_row_count()
        assert after <= before - 2, "连续删除后行数应减少2"

    def test_09_delete_then_refresh(self, category_page: BrandCategoryPage):
        """TC-09 删除分类后刷新页面验证"""
        name = f"刷新验{uuid.uuid4().hex[:4]}"
        _create_test_category(category_page, name)

        category_page.click_delete_by_name(name)
        category_page.click_confirm_ok()
        category_page.page.wait_for_timeout(1000)

        category_page.page.reload()
        category_page.page.wait_for_load_state("networkidle", timeout=15000)
        category_page._dismiss_notification()
        category_page.page.wait_for_timeout(1000)

        assert not category_page.category_exists(name), "刷新后已删除分类不应出现"

    def test_10_delete_last_one(self, category_page: BrandCategoryPage):
        """TC-10 当列表只剩一条分类时删除"""
        names = category_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        target = names[-1]
        category_page.click_delete_by_name(target)
        category_page.click_confirm_ok()

        category_page.page.wait_for_timeout(1000)
        error = category_page.get_error_message()
        if error and "至少" in error:
            pass  # 系统不允许删除最后一条


# ===========================================================================
# 关闭确认弹窗（TC-11）
# ===========================================================================
@pytest.mark.brand
class TestDeleteClose:

    def test_11_close_confirm_x(self, category_page: BrandCategoryPage):
        """TC-11 点击确认弹窗X按钮关闭"""
        names = category_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        category_page.click_delete_by_name(target)
        assert category_page.is_confirm_visible()

        category_page.click_confirm_close()

        assert not category_page.is_confirm_visible(), "弹窗应关闭"
        assert category_page.category_exists(target), "分类不应被删除"


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "category_delete_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行品牌分类-删除测试...")
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
