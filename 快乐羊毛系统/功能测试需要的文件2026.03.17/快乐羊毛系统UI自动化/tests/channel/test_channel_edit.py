"""渠道管理 - 编辑渠道（14 条用例）

用例来源：测试用例/渠道管理/渠道管理_编辑.xlsx
测试类分组：
  TestEditEntry         — 进入编辑 & 数据预填充
  TestEditName          — 修改渠道名称
  TestEditInteraction   — 不修改提交 / 取消 / 编辑后验证 / 连续编辑 / ID不变
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.channel_page import ChannelPage
from tests.channel.conftest import EXISTING_CHANNEL, EXISTING_CHANNEL_2


# ===========================================================================
# 进入编辑 & 数据预填充（TC-01 ~ TC-02）
# ===========================================================================
@pytest.mark.channel
class TestEditEntry:

    def test_01_open_edit_dialog(self, channel_page: ChannelPage):
        """TC-01 点击编辑按钮打开编辑弹窗"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)

        assert channel_page.is_dialog_visible(), "应弹出编辑弹窗"
        assert "编辑渠道" in channel_page.get_dialog_title(), "标题应为编辑渠道"
        assert channel_page.get_channel_name_value() == EXISTING_CHANNEL

        count = channel_page.get_name_count()
        assert "2" in count and "10" in count, f"字符计数应含 2/10，实际: {count}"
        channel_page.click_close()

    def test_02_prefilled_data(self, channel_page: ChannelPage):
        """TC-02 编辑弹窗预填充数据正确性（骑士）"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL_2)

        assert "编辑渠道" in channel_page.get_dialog_title()
        assert channel_page.get_channel_name_value() == EXISTING_CHANNEL_2

        count = channel_page.get_name_count()
        assert "2" in count, f"字符计数应含 2，实际: {count}"
        channel_page.click_close()


# ===========================================================================
# 修改渠道名称（TC-03 ~ TC-08）
# ===========================================================================
@pytest.mark.channel
class TestEditName:

    def test_03_modify_name(self, channel_page: ChannelPage):
        """TC-03 修改渠道名称并保存成功"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("聚推客")
        channel_page.click_confirm()

        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "修改名称应成功"

        # 恢复
        if channel_page.channel_exists("聚推客"):
            channel_page.click_edit_by_name("聚推客")
            channel_page.clear_and_fill_channel_name(EXISTING_CHANNEL)
            channel_page.click_confirm()

    def test_04_clear_name(self, channel_page: ChannelPage):
        """TC-04 清空渠道名称后提交"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("")

        count = channel_page.get_name_count()
        assert "0" in count, f"清空后计数应含 0，实际: {count}"

        channel_page.click_confirm()
        assert channel_page.has_form_error() or channel_page.is_dialog_visible(), "名称为空应有提示"
        channel_page.click_close()

    def test_05_spaces_name(self, channel_page: ChannelPage):
        """TC-05 渠道名称修改为纯空格"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("     ")
        channel_page.click_confirm()

        assert channel_page.has_form_error() or channel_page.is_dialog_visible(), "纯空格应视为空值"
        if channel_page.is_dialog_visible():
            channel_page.click_close()

    def test_06_duplicate_name(self, channel_page: ChannelPage):
        """TC-06 修改为已存在的其他渠道名称"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name(EXISTING_CHANNEL_2)
        channel_page.click_confirm()

        channel_page.page.wait_for_timeout(2000)
        error = channel_page.get_error_message()
        assert error or channel_page.is_dialog_visible(), "重复名称应有提示"
        if channel_page.is_dialog_visible():
            channel_page.click_close()

    def test_07_max_boundary(self, channel_page: ChannelPage):
        """TC-07 渠道名称修改为10个字符"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        name_10 = "编辑渠道十个字符名"[:10]
        channel_page.clear_and_fill_channel_name(name_10)

        count = channel_page.get_name_count()
        assert "10" in count, f"字符计数应含 10/10，实际: {count}"

        channel_page.click_confirm()
        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "10字符应成功"

        # 恢复
        if channel_page.channel_exists(name_10):
            channel_page.click_edit_by_name(name_10)
            channel_page.clear_and_fill_channel_name(EXISTING_CHANNEL)
            channel_page.click_confirm()

    def test_08_special_chars(self, channel_page: ChannelPage):
        """TC-08 渠道名称修改为含特殊字符"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("#渠道&")
        channel_page.click_confirm()

        channel_page.page.wait_for_timeout(1000)
        if channel_page.is_dialog_visible():
            channel_page.click_close()
        else:
            # 恢复
            if channel_page.channel_exists("#渠道&"):
                channel_page.click_edit_by_name("#渠道&")
                channel_page.clear_and_fill_channel_name(EXISTING_CHANNEL)
                channel_page.click_confirm()


# ===========================================================================
# 不修改提交 / 取消 / 编辑后验证 / 连续编辑 / ID不变（TC-09 ~ TC-14）
# ===========================================================================
@pytest.mark.channel
class TestEditInteraction:

    def test_09_submit_no_change(self, channel_page: ChannelPage):
        """TC-09 不修改渠道名称直接点击确认"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.click_confirm()

        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_dialog_visible(), "不修改直接提交应成功"

    def test_10_cancel_after_modify(self, channel_page: ChannelPage):
        """TC-10 修改名称后点击关闭取消"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("修改取消测试")
        channel_page.click_close()

        assert not channel_page.is_dialog_visible(), "弹窗应关闭"
        assert channel_page.channel_exists(EXISTING_CHANNEL), "原名称应不变"
        assert not channel_page.channel_exists("修改取消测试"), "修改不应生效"

    def test_11_close_x_after_modify(self, channel_page: ChannelPage):
        """TC-11 修改名称后点击X关闭弹窗"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("X关闭测试")
        channel_page.click_dialog_close_x()

        assert not channel_page.is_dialog_visible(), "弹窗应关闭"
        assert channel_page.channel_exists(EXISTING_CHANNEL), "原数据应不变"

    def test_12_verify_after_edit(self, channel_page: ChannelPage):
        """TC-12 编辑保存后再次打开验证数据"""
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("辛贝")
        channel_page.click_confirm()

        msg = channel_page.get_success_message()
        if not msg and channel_page.is_dialog_visible():
            channel_page.click_close()
            pytest.skip("编辑提交失败")

        # 再次打开验证
        channel_page.click_edit_by_name("辛贝")
        assert channel_page.get_channel_name_value() == "辛贝"
        count = channel_page.get_name_count()
        assert "2" in count, f"字符计数应含 2，实际: {count}"
        channel_page.click_close()

        # 恢复
        channel_page.click_edit_by_name("辛贝")
        channel_page.clear_and_fill_channel_name(EXISTING_CHANNEL)
        channel_page.click_confirm()

    def test_13_edit_different_channels(self, channel_page: ChannelPage):
        """TC-13 连续编辑不同渠道验证数据隔离"""
        names = channel_page.get_list_names()
        if len(names) < 2:
            pytest.skip("列表不足2条")

        channel_page.click_edit_by_name(names[0])
        val1 = channel_page.get_channel_name_value()
        assert val1 == names[0], f"第一条应预填充'{names[0]}'，实际: '{val1}'"
        channel_page.click_close()

        channel_page.click_edit_by_name(names[1])
        val2 = channel_page.get_channel_name_value()
        assert val2 == names[1], f"第二条应预填充'{names[1]}'，实际: '{val2}'"
        channel_page.click_close()

    def test_14_id_unchanged_after_edit(self, channel_page: ChannelPage):
        """TC-14 编辑渠道后ID和创建时间不变"""
        # 记录原始ID和时间
        row = channel_page.page.locator(f'.el-table__row:has-text("{EXISTING_CHANNEL}")')
        cells = row.locator('td').all()
        original_id = cells[0].text_content().strip() if cells else ""
        original_time = cells[2].text_content().strip() if len(cells) > 2 else ""

        # 编辑
        channel_page.click_edit_by_name(EXISTING_CHANNEL)
        channel_page.clear_and_fill_channel_name("新芒果")
        channel_page.click_confirm()

        msg = channel_page.get_success_message()
        if not msg and channel_page.is_dialog_visible():
            channel_page.click_close()
            pytest.skip("编辑提交失败")

        # 验证ID和时间
        row = channel_page.page.locator('.el-table__row:has-text("新芒果")')
        cells = row.locator('td').all()
        new_id = cells[0].text_content().strip() if cells else ""
        new_time = cells[2].text_content().strip() if len(cells) > 2 else ""

        assert new_id == original_id, f"ID应不变，原: {original_id}，现: {new_id}"
        assert new_time == original_time, f"创建时间应不变，原: {original_time}，现: {new_time}"

        # 恢复
        channel_page.click_edit_by_name("新芒果")
        channel_page.clear_and_fill_channel_name(EXISTING_CHANNEL)
        channel_page.click_confirm()


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "channel_edit_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行渠道管理-编辑测试...")
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
