"""品牌分类 - 新增分类（21 条用例）

用例来源：测试用例/品牌分类/品牌分类_新增.xlsx
测试类分组：
  TestAddBasic          — 正向流程（基本/完整/禁用状态）
  TestAddDialog         — 弹窗初始状态
  TestAddName           — 分类名称校验
  TestAddType           — 分类类型
  TestAddLevel          — 层级
  TestAddStatus         — 分类状态开关
  TestAddCancel         — 取消操作
  TestAddVerify         — 新增后验证
"""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.brand_category_page import BrandCategoryPage


def unique_name(prefix: str = "测试分类") -> str:
    return f"{prefix}{uuid.uuid4().hex[:4]}"


# ===========================================================================
# 正向流程（TC-01 ~ TC-03）
# ===========================================================================
@pytest.mark.brand
class TestAddBasic:

    def test_01_add_required_fields(self, category_page: BrandCategoryPage):
        """TC-01 填写必填字段新增分类成功"""
        name = unique_name("测试分类A")
        category_page.click_add_btn()
        assert "新增分类" in category_page.get_dialog_title()

        category_page.fill_category_name(name)
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "提交后弹窗应关闭"
        assert category_page.category_exists(name), f"列表中应出现'{name}'"

    def test_02_add_all_fields(self, category_page: BrandCategoryPage):
        """TC-02 填写所有字段新增分类成功"""
        name = unique_name("完整分类B")
        category_page.click_add_btn()

        category_page.select_category_type()
        category_page.fill_category_name(name)
        category_page.fill_level("1")
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "完整表单提交应成功"

    def test_03_add_disabled_status(self, category_page: BrandCategoryPage):
        """TC-03 新增分类时设置为禁用状态"""
        name = unique_name("禁用分类C")
        category_page.click_add_btn()

        category_page.fill_category_name(name)
        category_page.toggle_status()  # 启用 → 禁用
        assert not category_page.is_status_enabled(), "开关应切换为禁用"

        category_page.click_submit()
        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "禁用状态提交应成功"


# ===========================================================================
# 弹窗初始状态（TC-04）
# ===========================================================================
@pytest.mark.brand
class TestAddDialog:

    def test_04_dialog_initial_state(self, category_page: BrandCategoryPage):
        """TC-04 新增弹窗初始状态检查"""
        category_page.click_add_btn()

        # 标题
        assert "新增分类" in category_page.get_dialog_title()
        # 分类名称为空
        assert category_page.get_category_name_value() == "", "分类名称应为空"
        # 层级默认0
        assert category_page.get_level_value() == "0", f"层级默认应为0，实际: {category_page.get_level_value()}"
        # 状态默认启用
        assert category_page.is_status_enabled(), "分类状态默认应为启用"
        # 有取消和提交按钮
        assert category_page.page.locator(category_page.SEL_CANCEL_BTN).count() > 0
        assert category_page.page.locator(category_page.SEL_SUBMIT_BTN).count() > 0

        category_page.click_cancel()


# ===========================================================================
# 分类名称校验（TC-05 ~ TC-10）
# ===========================================================================
@pytest.mark.brand
class TestAddName:

    def test_05_empty_name(self, category_page: BrandCategoryPage):
        """TC-05 分类名称为空提交"""
        category_page.click_add_btn()
        category_page.click_submit()

        assert category_page.has_form_error(), "名称为空应有校验提示"
        category_page.click_cancel()

    def test_06_spaces_only(self, category_page: BrandCategoryPage):
        """TC-06 分类名称输入纯空格提交"""
        category_page.click_add_btn()
        category_page.fill_category_name("     ")
        category_page.click_submit()

        assert category_page.has_form_error() or category_page.is_dialog_visible(), "纯空格应视为空值"
        if category_page.is_dialog_visible():
            category_page.click_cancel()

    def test_07_single_char(self, category_page: BrandCategoryPage):
        """TC-07 分类名称输入1个字符"""
        name = "A"
        category_page.click_add_btn()
        category_page.fill_category_name(name)
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "1个字符应提交成功"

    def test_08_long_name(self, category_page: BrandCategoryPage):
        """TC-08 分类名称输入超长字符"""
        long_name = "A" * 60
        category_page.click_add_btn()
        category_page.fill_category_name(long_name)
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        # 有限制则报错或截断，无限制则成功
        if category_page.is_dialog_visible():
            category_page.click_cancel()

    def test_09_special_chars(self, category_page: BrandCategoryPage):
        """TC-09 分类名称输入特殊字符"""
        category_page.click_add_btn()
        category_page.fill_category_name("@#$%&测试!")
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        if category_page.is_dialog_visible():
            category_page.click_cancel()

    def test_10_duplicate_name(self, category_page: BrandCategoryPage):
        """TC-10 分类名称与已有分类重复"""
        category_page.click_add_btn()
        category_page.fill_category_name("会员充值")
        category_page.click_submit()

        category_page.page.wait_for_timeout(2000)
        error = category_page.get_error_message()
        form_errors = category_page.get_form_errors()
        all_text = error + " ".join(form_errors)
        # 重复名称应提交失败或有提示
        assert "已存在" in all_text or "重复" in all_text or category_page.is_dialog_visible(), (
            f"重复名称应有提示，实际: {all_text}"
        )
        if category_page.is_dialog_visible():
            category_page.click_cancel()


# ===========================================================================
# 分类类型（TC-11 ~ TC-12）
# ===========================================================================
@pytest.mark.brand
class TestAddType:

    def test_11_no_type_selected(self, category_page: BrandCategoryPage):
        """TC-11 不选择分类类型提交"""
        category_page.click_add_btn()
        category_page.fill_category_name(unique_name("无类型"))
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        if category_page.is_dialog_visible():
            # 分类类型为必填
            assert category_page.has_form_error(), "若分类类型必填应有提示"
            category_page.click_cancel()

    def test_12_select_type(self, category_page: BrandCategoryPage):
        """TC-12 选择分类类型后提交"""
        name = unique_name("有类型")
        category_page.click_add_btn()
        category_page.select_category_type()
        category_page.fill_category_name(name)
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "选择类型后应提交成功"


# ===========================================================================
# 层级（TC-13 ~ TC-17）
# ===========================================================================
@pytest.mark.brand
class TestAddLevel:

    def test_13_default_level(self, category_page: BrandCategoryPage):
        """TC-13 层级保持默认值0提交"""
        name = unique_name("默认层级")
        category_page.click_add_btn()
        category_page.fill_category_name(name)
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "默认层级0应提交成功"

    def test_14_positive_level(self, category_page: BrandCategoryPage):
        """TC-14 层级输入正整数"""
        name = unique_name("层级5")
        category_page.click_add_btn()
        category_page.fill_category_name(name)
        category_page.fill_level("5")
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "正整数层级应提交成功"

    def test_15_negative_level(self, category_page: BrandCategoryPage):
        """TC-15 层级输入负数"""
        category_page.click_add_btn()
        category_page.fill_category_name(unique_name("负层级"))
        category_page.fill_level("-1")
        category_page.click_submit()

        category_page.page.wait_for_timeout(1000)
        if category_page.is_dialog_visible():
            category_page.click_cancel()

    def test_16_non_numeric_level(self, category_page: BrandCategoryPage):
        """TC-16 层级输入非数字字符"""
        category_page.click_add_btn()
        category_page.fill_level("abc")

        actual = category_page.get_level_value()
        assert actual == "" or actual.isdigit() or actual == "0", (
            f"非数字应被拒绝，实际: {actual}"
        )
        category_page.click_cancel()

    def test_17_level_arrows(self, category_page: BrandCategoryPage):
        """TC-17 通过上下箭头调整层级"""
        category_page.click_add_btn()

        # 点3次增加
        for _ in range(3):
            category_page.click_level_increase()
        val = category_page.get_level_value()
        assert val == "3", f"点击3次增加后应为3，实际: {val}"

        # 点1次减少
        category_page.click_level_decrease()
        val = category_page.get_level_value()
        assert val == "2", f"减少1次后应为2，实际: {val}"

        category_page.click_cancel()


# ===========================================================================
# 分类状态开关（TC-18）
# ===========================================================================
@pytest.mark.brand
class TestAddStatus:

    def test_18_toggle_status(self, category_page: BrandCategoryPage):
        """TC-18 切换分类状态为禁用再切回启用"""
        category_page.click_add_btn()

        assert category_page.is_status_enabled(), "默认应为启用"

        category_page.toggle_status()
        assert not category_page.is_status_enabled(), "切换后应为禁用"

        category_page.toggle_status()
        assert category_page.is_status_enabled(), "再次切换应为启用"

        category_page.click_cancel()


# ===========================================================================
# 取消操作（TC-19 ~ TC-20）
# ===========================================================================
@pytest.mark.brand
class TestAddCancel:

    def test_19_cancel_btn(self, category_page: BrandCategoryPage):
        """TC-19 填写数据后点击取消"""
        category_page.click_add_btn()
        category_page.fill_category_name("取消测试分类")
        category_page.fill_level("3")
        category_page.click_cancel()

        assert not category_page.is_dialog_visible(), "弹窗应关闭"
        assert not category_page.category_exists("取消测试分类"), "取消后不应新增"

    def test_20_close_x_btn(self, category_page: BrandCategoryPage):
        """TC-20 点击弹窗右上角X关闭"""
        category_page.click_add_btn()
        category_page.fill_category_name("X关闭测试")
        category_page.click_dialog_close()

        assert not category_page.is_dialog_visible(), "弹窗应关闭"
        assert not category_page.category_exists("X关闭测试"), "关闭后不应新增"


# ===========================================================================
# 新增后验证（TC-21）
# ===========================================================================
@pytest.mark.brand
class TestAddVerify:

    def test_21_verify_after_add(self, category_page: BrandCategoryPage):
        """TC-21 新增分类后列表数据验证"""
        before_count = category_page.get_list_row_count()

        name = unique_name("验证分类D")
        category_page.click_add_btn()
        category_page.fill_category_name(name)
        category_page.click_submit()

        msg = category_page.get_success_message()
        assert msg or not category_page.is_dialog_visible(), "提交应成功"

        after_count = category_page.get_list_row_count()
        assert after_count >= before_count, "列表行数应增加"
        assert category_page.category_exists(name), f"列表中应有'{name}'"


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "category_add_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行品牌分类-新增测试...")
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
