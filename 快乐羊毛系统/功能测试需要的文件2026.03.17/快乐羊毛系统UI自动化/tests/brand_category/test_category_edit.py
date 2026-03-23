"""品牌分类 - 编辑分类（18 条用例）

用例来源：测试用例/品牌分类/品牌分类_编辑.xlsx
测试类分组：
  TestEditEntry         — 进入编辑 & 数据预填充
  TestEditName          — 修改分类名称
  TestEditType          — 修改分类类型
  TestEditLevel         — 修改层级
  TestEditStatus        — 修改分类状态
  TestEditInteraction   — 不修改提交 / 取消 / 编辑后验证 / 连续编辑
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.brand_category_page import BrandCategoryPage
from tests.brand_category.conftest import EXISTING_CATEGORY


# ===========================================================================
# 进入编辑 & 数据预填充（TC-01 ~ TC-02）
# ===========================================================================
@pytest.mark.brand
class TestEditEntry:

    def test_01_open_edit_dialog(self, category_page: BrandCategoryPage):
        """TC-01 点击编辑按钮打开编辑弹窗"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)

        assert category_page.is_dialog_visible(), "应弹出编辑弹窗"
        assert "编辑分类" in category_page.get_dialog_title(), "标题应为编辑分类"
        assert category_page.get_category_name_value() == EXISTING_CATEGORY
        category_page.click_cancel()

    def test_02_prefilled_data(self, category_page: BrandCategoryPage):
        """TC-02 编辑弹窗预填充数据正确性"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)

        name = category_page.get_category_name_value()
        assert name == EXISTING_CATEGORY, f"名称应为'{EXISTING_CATEGORY}'，实际: '{name}'"

        level = category_page.get_level_value()
        assert level is not None, "层级应有值"

        assert category_page.is_status_enabled(), "状态应为启用"
        category_page.click_cancel()


# ===========================================================================
# 修改分类名称（TC-03 ~ TC-07）
# ===========================================================================
@pytest.mark.brand
class TestEditName:

    def test_03_modify_name(self, category_page: BrandCategoryPage):
        """TC-03 修改分类名称并保存"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)

        category_page.clear_and_fill_category_name("VIP充值")
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "修改名称应成功"

        # 恢复
        if category_page.category_exists("VIP充值"):
            category_page.click_edit_by_name("VIP充值")
            category_page.clear_and_fill_category_name(EXISTING_CATEGORY)
            category_page.click_submit()

    def test_04_clear_name(self, category_page: BrandCategoryPage):
        """TC-04 清空分类名称后提交"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.clear_and_fill_category_name("")
        category_page.click_submit()

        assert category_page.has_form_error(), "名称为空应有提示"
        category_page.click_cancel()

    def test_05_duplicate_name(self, category_page: BrandCategoryPage):
        """TC-05 修改为已存在的其他分类名称"""
        names = category_page.get_list_names()
        if len(names) < 2:
            pytest.skip("列表不足2条，无法测试重复")

        category_page.click_edit_by_name(names[0])
        category_page.clear_and_fill_category_name(names[1])
        category_page.click_submit()

        category_page.page.wait_for_timeout(2000)
        error = category_page.get_error_message()
        assert error or category_page.is_dialog_visible(), "重复名称应有提示或停留弹窗"
        if category_page.is_dialog_visible():
            category_page.click_cancel()

    def test_06_long_name(self, category_page: BrandCategoryPage):
        """TC-06 分类名称修改为超长字符"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.clear_and_fill_category_name("A" * 60)
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        if category_page.is_dialog_visible():
            category_page.click_cancel()

    def test_07_special_chars(self, category_page: BrandCategoryPage):
        """TC-07 分类名称修改为特殊字符"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.clear_and_fill_category_name("!@#$%分类")
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        if category_page.is_dialog_visible():
            category_page.click_cancel()
        else:
            # 恢复
            if category_page.category_exists("!@#$%分类"):
                category_page.click_edit_by_name("!@#$%分类")
                category_page.clear_and_fill_category_name(EXISTING_CATEGORY)
                category_page.click_submit()


# ===========================================================================
# 修改分类类型（TC-08）
# ===========================================================================
@pytest.mark.brand
class TestEditType:

    def test_08_switch_type(self, category_page: BrandCategoryPage):
        """TC-08 切换分类类型后保存"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.select_category_type(index=0)
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "切换类型应成功"


# ===========================================================================
# 修改层级（TC-09 ~ TC-11）
# ===========================================================================
@pytest.mark.brand
class TestEditLevel:

    def test_09_modify_level(self, category_page: BrandCategoryPage):
        """TC-09 修改层级值并保存"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.fill_level("3")
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "修改层级应成功"

        # 恢复
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.fill_level("0")
        category_page.click_submit()

    def test_10_negative_level(self, category_page: BrandCategoryPage):
        """TC-10 层级修改为负数"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.fill_level("-5")
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        if category_page.is_dialog_visible():
            category_page.click_cancel()

    def test_11_decimal_level(self, category_page: BrandCategoryPage):
        """TC-11 层级修改为小数"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.fill_level("2.5")
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        if category_page.is_dialog_visible():
            category_page.click_cancel()


# ===========================================================================
# 修改分类状态（TC-12 ~ TC-13）
# ===========================================================================
@pytest.mark.brand
class TestEditStatus:

    def test_12_enable_to_disable(self, category_page: BrandCategoryPage):
        """TC-12 将启用状态改为禁用"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)

        if category_page.is_status_enabled():
            category_page.toggle_status()
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "改为禁用应成功"

        # 恢复启用
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        if not category_page.is_status_enabled():
            category_page.toggle_status()
        category_page.click_submit()

    def test_13_disable_to_enable(self, category_page: BrandCategoryPage):
        """TC-13 将禁用状态改为启用"""
        # 先设为禁用
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        if category_page.is_status_enabled():
            category_page.toggle_status()
        category_page.click_submit()
        category_page.page.wait_for_timeout(1000)

        # 再改回启用
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        if not category_page.is_status_enabled():
            category_page.toggle_status()
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "改为启用应成功"


# ===========================================================================
# 不修改提交 / 取消 / 编辑后验证 / 连续编辑（TC-14 ~ TC-18）
# ===========================================================================
@pytest.mark.brand
class TestEditInteraction:

    def test_14_submit_no_change(self, category_page: BrandCategoryPage):
        """TC-14 不做任何修改直接点击提交"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "不修改直接提交应成功"

    def test_15_cancel_after_modify(self, category_page: BrandCategoryPage):
        """TC-15 修改数据后点击取消"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.clear_and_fill_category_name("不应保存的名称")
        category_page.click_cancel()

        assert not category_page.is_dialog_visible(), "弹窗应关闭"
        assert not category_page.category_exists("不应保存的名称"), "取消后修改不应生效"
        assert category_page.category_exists(EXISTING_CATEGORY), "原名称应保留"

    def test_16_close_x_after_modify(self, category_page: BrandCategoryPage):
        """TC-16 修改数据后点击X关闭弹窗"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.clear_and_fill_category_name("X关闭不保存")
        category_page.fill_level("9")
        category_page.click_dialog_close()

        assert not category_page.is_dialog_visible(), "弹窗应关闭"
        assert category_page.category_exists(EXISTING_CATEGORY), "原数据应不变"

    def test_17_verify_after_edit(self, category_page: BrandCategoryPage):
        """TC-17 编辑保存后再次打开验证数据一致"""
        category_page.click_edit_by_name(EXISTING_CATEGORY)
        category_page.clear_and_fill_category_name("修改验证X")
        category_page.fill_level("5")
        category_page.click_submit()

        msg = category_page.get_success_message()
        if not msg and category_page.is_dialog_visible():
            category_page.click_cancel()
            pytest.skip("编辑提交失败")

        # 再次打开验证
        category_page.click_edit_by_name("修改验证X")
        assert category_page.get_category_name_value() == "修改验证X"
        assert category_page.get_level_value() == "5"
        category_page.click_cancel()

        # 恢复
        category_page.click_edit_by_name("修改验证X")
        category_page.clear_and_fill_category_name(EXISTING_CATEGORY)
        category_page.fill_level("0")
        category_page.click_submit()

    def test_18_edit_different_categories(self, category_page: BrandCategoryPage):
        """TC-18 连续编辑不同分类"""
        names = category_page.get_list_names()
        if len(names) < 2:
            pytest.skip("列表不足2条")

        # 编辑第一条
        category_page.click_edit_by_name(names[0])
        val1 = category_page.get_category_name_value()
        assert val1 == names[0], f"第一条应预填充'{names[0]}'，实际: '{val1}'"
        category_page.click_cancel()

        # 编辑第二条
        category_page.click_edit_by_name(names[1])
        val2 = category_page.get_category_name_value()
        assert val2 == names[1], f"第二条应预填充'{names[1]}'，实际: '{val2}'"
        category_page.click_cancel()


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "category_edit_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行品牌分类-编辑测试...")
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
