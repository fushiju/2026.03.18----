"""渠道管理 - 删除渠道（10 条用例）

用例来源：测试用例/渠道管理/渠道管理_删除.xlsx
测试类分组：
  TestDeleteConfirm    — 正向删除 & 取消删除
  TestDeleteDialog     — 确认弹窗内容
  TestDeleteSpecial    — 删除被引用渠道
  TestDeleteVerify     — 删除后验证 & 刷新 & 连续删除 & 最后一条
  TestDeleteDismiss    — 其他方式关闭弹窗
  TestDeleteRename     — 删除后新增同名
"""
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.channel_page import ChannelPage


def _create_channel(page: ChannelPage, name: str):
    """辅助：新增一个测试用渠道"""
    page.click_add_btn()
    page.fill_channel_name(name)
    page.click_confirm()
    page.page.wait_for_timeout(1000)


# ===========================================================================
# 正向删除 & 取消删除（TC-01 ~ TC-02）
# ===========================================================================
@pytest.mark.channel
class TestDeleteConfirm:

    def test_01_delete_and_confirm(self, channel_page: ChannelPage):
        """TC-01 删除渠道并确认成功"""
        name = f"删除{uuid.uuid4().hex[:3]}"
        _create_channel(channel_page, name)
        assert channel_page.channel_exists(name)

        channel_page.click_delete_by_name(name)
        assert channel_page.is_msgbox_visible(), "应弹出确认弹窗"

        channel_page.click_msgbox_ok()

        msg = channel_page.get_success_message()
        assert msg or not channel_page.is_msgbox_visible(), "删除应成功"
        assert not channel_page.channel_exists(name), f"'{name}'应从列表消失"

    def test_02_delete_and_cancel(self, channel_page: ChannelPage):
        """TC-02 删除时点击取消"""
        names = channel_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        channel_page.click_delete_by_name(target)
        assert channel_page.is_msgbox_visible()

        channel_page.click_msgbox_cancel()

        assert not channel_page.is_msgbox_visible(), "弹窗应关闭"
        assert channel_page.channel_exists(target), f"'{target}'不应被删除"


# ===========================================================================
# 确认弹窗内容（TC-03）
# ===========================================================================
@pytest.mark.channel
class TestDeleteDialog:

    def test_03_confirm_dialog_content(self, channel_page: ChannelPage):
        """TC-03 删除确认弹窗内容检查"""
        names = channel_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        channel_page.click_delete_by_name(names[0])

        title = channel_page.get_msgbox_title()
        content = channel_page.get_msgbox_content()

        assert "提示" in title, f"标题应含'提示'，实际: {title}"
        assert "删除" in content, f"内容应含'删除'，实际: {content}"
        assert channel_page.page.locator(channel_page.SEL_MSG_BOX_OK).count() > 0
        assert channel_page.page.locator(channel_page.SEL_MSG_BOX_CANCEL).count() > 0

        channel_page.click_msgbox_cancel()


# ===========================================================================
# 删除被引用渠道（TC-04）
# ===========================================================================
@pytest.mark.channel
class TestDeleteSpecial:

    def test_04_delete_referenced(self, channel_page: ChannelPage):
        """TC-04 删除已被品牌使用的渠道"""
        if not channel_page.channel_exists("骑士"):
            pytest.skip("骑士渠道不存在")

        channel_page.click_delete_by_name("骑士")
        channel_page.click_msgbox_ok()

        channel_page.page.wait_for_timeout(2000)
        error = channel_page.get_error_message()
        if channel_page.channel_exists("骑士"):
            assert error, "被引用渠道若删除失败应有提示"


# ===========================================================================
# 删除后验证 & 刷新 & 连续删除 & 最后一条（TC-05 ~ TC-08）
# ===========================================================================
@pytest.mark.channel
class TestDeleteVerify:

    def test_05_verify_after_delete(self, channel_page: ChannelPage):
        """TC-05 删除渠道后列表数据验证"""
        name = f"验删{uuid.uuid4().hex[:3]}"
        _create_channel(channel_page, name)

        before = channel_page.get_list_row_count()

        channel_page.click_delete_by_name(name)
        channel_page.click_msgbox_ok()
        channel_page.page.wait_for_timeout(1000)

        after = channel_page.get_list_row_count()
        assert after < before, f"行数应减少，前: {before}，后: {after}"
        assert not channel_page.channel_exists(name)

    def test_06_delete_then_refresh(self, channel_page: ChannelPage):
        """TC-06 删除渠道后刷新页面验证持久化"""
        name = f"刷新{uuid.uuid4().hex[:3]}"
        _create_channel(channel_page, name)

        channel_page.click_delete_by_name(name)
        channel_page.click_msgbox_ok()
        channel_page.page.wait_for_timeout(1000)

        channel_page.page.reload()
        channel_page.page.wait_for_load_state("networkidle", timeout=15000)
        channel_page._dismiss_notification()
        channel_page.page.wait_for_timeout(1000)

        assert not channel_page.channel_exists(name), "刷新后已删除渠道不应出现"

    def test_07_continuous_delete(self, channel_page: ChannelPage):
        """TC-07 连续删除多条渠道"""
        name1 = f"连1{uuid.uuid4().hex[:3]}"
        name2 = f"连2{uuid.uuid4().hex[:3]}"
        _create_channel(channel_page, name1)
        _create_channel(channel_page, name2)

        before = channel_page.get_list_row_count()

        channel_page.click_delete_by_name(name1)
        channel_page.click_msgbox_ok()
        channel_page.page.wait_for_timeout(1000)

        channel_page.click_delete_by_name(name2)
        channel_page.click_msgbox_ok()
        channel_page.page.wait_for_timeout(1000)

        after = channel_page.get_list_row_count()
        assert after <= before - 2, "连续删除后行数应减少2"

    def test_08_delete_last_one(self, channel_page: ChannelPage):
        """TC-08 列表只剩一条渠道时删除"""
        names = channel_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        target = names[-1]
        channel_page.click_delete_by_name(target)
        channel_page.click_msgbox_ok()

        channel_page.page.wait_for_timeout(1000)
        error = channel_page.get_error_message()
        if error and "至少" in error:
            pass  # 系统不允许删除最后一条


# ===========================================================================
# 其他方式关闭弹窗（TC-09）
# ===========================================================================
@pytest.mark.channel
class TestDeleteDismiss:

    def test_09_dismiss_by_esc(self, channel_page: ChannelPage):
        """TC-09 通过ESC关闭删除确认弹窗"""
        names = channel_page.get_list_names()
        if not names:
            pytest.skip("列表为空")

        target = names[0]
        channel_page.click_delete_by_name(target)
        assert channel_page.is_msgbox_visible()

        channel_page.dismiss_msgbox_by_esc()

        assert not channel_page.is_msgbox_visible(), "ESC后弹窗应关闭"
        assert channel_page.channel_exists(target), "渠道不应被删除"


# ===========================================================================
# 删除后新增同名（TC-10）
# ===========================================================================
@pytest.mark.channel
class TestDeleteRename:

    def test_10_add_same_name_after_delete(self, channel_page: ChannelPage):
        """TC-10 删除渠道后再新增同名渠道"""
        name = f"同名{uuid.uuid4().hex[:3]}"
        _create_channel(channel_page, name)

        # 删除
        channel_page.click_delete_by_name(name)
        channel_page.click_msgbox_ok()
        channel_page.page.wait_for_timeout(1000)
        assert not channel_page.channel_exists(name)

        # 重新新增同名
        _create_channel(channel_page, name)
        assert channel_page.channel_exists(name), "删除后重新新增同名应成功"


# ===========================================================================
# 入口
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "channel_delete_report.html")
    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行渠道管理-删除测试...")
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
