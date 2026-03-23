"""渠道管理 - 新增渠道（16 条用例）

用例来源：测试用例/渠道管理/渠道管理_新增.xlsx
测试类分组：
  TestAddBasic       — 正向流程
  TestAddDialog      — 弹窗初始状态
  TestAddName        — 渠道名称校验（空值/空格/边界/超长/特殊字符/数字/重复/混合）
  TestAddCancel      — 取消操作
  TestAddVerify      — 新增后验证 & 连续新增 & 分页
"""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.channel_page import ChannelPage


def unique_name(prefix: str = "渠道") -> str:
    return f"{prefix}{uuid.uuid4().hex[:3]}"[:10]


# ===========================================================================
# 正向流程（TC-01）
# ===========================================================================
@pytest.mark.channel
class TestAddBasic:

    def test_01_add_channel(self, channel_page: ChannelPage):
        """TC-01 输入渠道名称新增成功"""
        name = unique_name("蜂助手")
        channel_page.click_add_btn()
        assert "新增渠道" in channel_page.get_dialog_title()

        channel_page.fill_channel_name(name)
        channel_page.click_confirm()

        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "提交后弹窗应关闭"
        assert channel_page.channel_exists(name), f"列表中应出现'{name}'"


# ===========================================================================
# 弹窗初始状态（TC-02）
# ===========================================================================
@pytest.mark.channel
class TestAddDialog:

    def test_02_dialog_initial_state(self, channel_page: ChannelPage):
        """TC-02 新增弹窗初始状态检查"""
        channel_page.click_add_btn()

        assert "新增渠道" in channel_page.get_dialog_title()
        assert channel_page.get_channel_name_value() == "", "输入框应为空"

        count = channel_page.get_name_count()
        assert "0" in count and "10" in count, f"字符计数应显示 0/10，实际: {count}"

        assert channel_page.page.locator(channel_page.SEL_CLOSE_BTN).count() > 0, "应有关闭按钮"
        assert channel_page.page.locator(channel_page.SEL_CONFIRM_BTN).count() > 0, "应有确认按钮"

        channel_page.click_close()


# ===========================================================================
# 渠道名称校验（TC-03 ~ TC-11）
# ===========================================================================
@pytest.mark.channel
class TestAddName:

    def test_03_empty_name(self, channel_page: ChannelPage):
        """TC-03 渠道名称为空点击确认"""
        channel_page.click_add_btn()
        channel_page.click_confirm()

        assert channel_page.has_form_error() or channel_page.is_dialog_visible(), "名称为空应有提示"
        channel_page.click_close()

    def test_04_spaces_only(self, channel_page: ChannelPage):
        """TC-04 渠道名称输入纯空格提交"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("     ")
        channel_page.click_confirm()

        assert channel_page.has_form_error() or channel_page.is_dialog_visible(), "纯空格应视为空值"
        if channel_page.is_dialog_visible():
            channel_page.click_close()

    def test_05_min_boundary(self, channel_page: ChannelPage):
        """TC-05 渠道名称输入1个字符"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("A")

        count = channel_page.get_name_count()
        assert "1" in count, f"字符计数应含 1，实际: {count}"

        channel_page.click_confirm()
        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "1个字符应提交成功"

    def test_06_max_boundary(self, channel_page: ChannelPage):
        """TC-06 渠道名称输入10个字符"""
        name_10 = "测试渠道名称五个"[:10]
        channel_page.click_add_btn()
        channel_page.fill_channel_name(name_10)

        count = channel_page.get_name_count()
        assert "10" in count, f"字符计数应含 10/10，实际: {count}"

        channel_page.click_confirm()
        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "10个字符应提交成功"

    def test_07_exceed_max(self, channel_page: ChannelPage):
        """TC-07 渠道名称尝试输入超过10个字符"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("A" * 15)

        actual = channel_page.get_channel_name_value()
        assert len(actual) <= 10, f"应限制最多10个字符，实际输入了 {len(actual)} 个"
        channel_page.click_close()

    def test_08_special_chars(self, channel_page: ChannelPage):
        """TC-08 渠道名称输入特殊字符"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("@#$%渠道")
        channel_page.click_confirm()

        channel_page.page.wait_for_timeout(1000)
        if channel_page.is_dialog_visible():
            channel_page.click_close()

    def test_09_numeric_name(self, channel_page: ChannelPage):
        """TC-09 渠道名称输入纯数字"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("123456")
        channel_page.click_confirm()

        channel_page.page.wait_for_timeout(1000)
        if channel_page.is_dialog_visible():
            channel_page.click_close()

    def test_10_duplicate_name(self, channel_page: ChannelPage):
        """TC-10 渠道名称与已有渠道重复"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("骑士")
        channel_page.click_confirm()

        channel_page.page.wait_for_timeout(2000)
        error = channel_page.get_error_message()
        form_errors = channel_page.get_form_errors()
        all_text = error + " ".join(form_errors)
        assert "已存在" in all_text or "重复" in all_text or channel_page.is_dialog_visible(), (
            f"重复名称应有提示，实际: {all_text}"
        )
        if channel_page.is_dialog_visible():
            channel_page.click_close()

    def test_11_mixed_chars(self, channel_page: ChannelPage):
        """TC-11 渠道名称输入中英文混合"""
        name = "Test渠道1"
        channel_page.click_add_btn()
        channel_page.fill_channel_name(name)
        channel_page.click_confirm()

        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "中英文混合应提交成功"


# ===========================================================================
# 取消操作（TC-12 ~ TC-13）
# ===========================================================================
@pytest.mark.channel
class TestAddCancel:

    def test_12_click_close(self, channel_page: ChannelPage):
        """TC-12 填写渠道名称后点击关闭"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("取消测试渠道")
        channel_page.click_close()

        assert not channel_page.is_dialog_visible(), "弹窗应关闭"
        assert not channel_page.channel_exists("取消测试渠道"), "关闭后不应新增"

    def test_13_click_x(self, channel_page: ChannelPage):
        """TC-13 填写数据后点击弹窗X关闭"""
        channel_page.click_add_btn()
        channel_page.fill_channel_name("X关闭测试")
        channel_page.click_dialog_close_x()

        assert not channel_page.is_dialog_visible(), "弹窗应关闭"
        assert not channel_page.channel_exists("X关闭测试"), "关闭后不应新增"


# ===========================================================================
# 新增后验证 & 连续新增 & 分页（TC-14 ~ TC-16）
# ===========================================================================
@pytest.mark.channel
class TestAddVerify:

    def test_14_verify_after_add(self, channel_page: ChannelPage):
        """TC-14 新增渠道后列表数据验证"""
        before = channel_page.get_list_row_count()

        name = unique_name("凡点")
        channel_page.click_add_btn()
        channel_page.fill_channel_name(name)
        channel_page.click_confirm()

        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "提交应成功"

        after = channel_page.get_list_row_count()
        assert after >= before, "列表行数应增加"
        assert channel_page.channel_exists(name), f"列表中应有'{name}'"

    def test_15_continuous_add(self, channel_page: ChannelPage):
        """TC-15 连续新增多个渠道"""
        name_a = unique_name("渠道A")
        name_b = unique_name("渠道B")

        # 第一个
        channel_page.click_add_btn()
        channel_page.fill_channel_name(name_a)
        channel_page.click_confirm()
        channel_page.get_success_message()

        # 第二个
        channel_page.click_add_btn()
        # 弹窗输入框应为空（不残留上次数据）
        assert channel_page.get_channel_name_value() == "", "再次打开弹窗输入框应为空"
        channel_page.fill_channel_name(name_b)
        channel_page.click_confirm()
        channel_page.get_success_message()

        assert channel_page.channel_exists(name_a), f"列表应有'{name_a}'"
        assert channel_page.channel_exists(name_b), f"列表应有'{name_b}'"

    def test_16_pagination_after_add(self, channel_page: ChannelPage):
        """TC-16 新增渠道后分页显示正确"""
        name = unique_name("分页")
        channel_page.click_add_btn()
        channel_page.fill_channel_name(name)
        channel_page.click_confirm()
        channel_page.get_success_message()

        total = channel_page.get_list_total_text()
        assert "共" in total and "条" in total, f"分页应显示总数，实际: {total}"


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "channel_add_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行渠道管理-新增测试...")
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
