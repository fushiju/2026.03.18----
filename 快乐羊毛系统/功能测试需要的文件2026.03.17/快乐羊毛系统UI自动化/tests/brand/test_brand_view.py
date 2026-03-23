"""品牌管理 - 品牌查看（16 条用例）

用例来源：测试用例/品牌查看.xlsx
测试类分组：
  TestViewEntry          — 进入查看页
  TestViewHeader         — 顶部信息 & 账号密码
  TestViewStats          — 统计数据面板
  TestViewTabs           — 标签页切换（基础信息/服务记录/已关联规格/余额修改记录）
  TestViewButtons        — 操作按钮（修改经纪人/新增编辑账号密码/返回）
  TestViewDataConsist    — 数据一致性
  TestViewStatus         — 不同状态查看
  TestViewReadOnly       — 只读验证

fixture 说明：
  brand_list_page  — 已登录，在品牌列表页（TC-01 从列表进入查看、TC-12/13/14/15 从列表操作）
  brand_view_page  — 已登录，在品牌"周六"的查看页（大部分查看用例）
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.brand_page import BrandPage
from tests.brand.conftest import VIEW_BRAND_NAME

VIEW_BRAND_PHONE = "15570441314"
VIEW_BRAND_CITY = "重庆市"


# ===========================================================================
# 进入查看页（TC-01）
# ===========================================================================
@pytest.mark.brand
class TestViewEntry:

    def test_01_enter_view_page(self, brand_list_page: BrandPage):
        """TC-01 从列表点击查看按钮进入查看页"""
        brand_list_page.click_view_by_name(VIEW_BRAND_NAME)

        assert brand_list_page.is_on_view_page(), f"应跳转到查看页面，实际URL: {brand_list_page.current_url}"
        title = brand_list_page.get_view_title()
        assert "查看" in title, f"页面标题应含'查看品牌'，实际: {title}"


# ===========================================================================
# 顶部信息（TC-02 ~ TC-03）
# ===========================================================================
@pytest.mark.brand
class TestViewHeader:

    def test_02_header_overview(self, brand_view_page: BrandPage):
        """TC-02 查看品牌顶部概览信息"""
        content = brand_view_page.page.content()

        assert VIEW_BRAND_NAME in content, f"顶部应显示品牌名称'{VIEW_BRAND_NAME}'"
        assert "未认证" in content or "已认证" in content, "应显示认证状态"
        assert any(s in content for s in ("已授权", "已驳回", "申请中")), "应显示审核状态"
        assert brand_view_page.view_page_has_text("ID"), "应显示ID字段"
        assert VIEW_BRAND_PHONE in content, f"应显示手机号 {VIEW_BRAND_PHONE}"
        assert brand_view_page.view_page_has_text("申请时间"), "应显示申请时间"
        assert brand_view_page.view_page_has_text("所属经纪人"), "应显示所属经纪人"

    def test_03_account_password_info(self, brand_view_page: BrandPage):
        """TC-03 查看品牌账号密码信息"""
        content = brand_view_page.page.content()
        assert "账号" in content, "应显示账号字段"
        assert "密码" in content, "应显示密码字段"
        assert brand_view_page.page.locator('button:has-text("新增编辑账号密码")').count() > 0, (
            "应显示'新增编辑账号密码'按钮"
        )


# ===========================================================================
# 统计数据面板（TC-04）
# ===========================================================================
@pytest.mark.brand
class TestViewStats:

    def test_04_stats_panel(self, brand_view_page: BrandPage):
        """TC-04 查看品牌统计数据面板"""
        content = brand_view_page.page.content()
        expected_labels = ["账户余额", "评分", "服务时长", "在线时长",
                           "本期业绩", "加钟率", "积分", "本期提成比例"]
        for label in expected_labels:
            assert label in content, f"统计面板应包含'{label}'"


# ===========================================================================
# 标签页切换（TC-05 ~ TC-08）
# ===========================================================================
@pytest.mark.brand
class TestViewTabs:

    def test_05_basic_info_tab(self, brand_view_page: BrandPage):
        """TC-05 查看基础信息标签页内容"""
        assert brand_view_page.is_tab_active("基础信息"), "基础信息应默认选中"

        content = brand_view_page.page.content()
        expected_fields = ["姓名", "性别", "手机号", "品牌分类",
                           "所属经纪人", "所属代理商"]
        for field in expected_fields:
            assert field in content, f"基础信息应包含'{field}'"

    def test_06_service_record_tab(self, brand_view_page: BrandPage):
        """TC-06 查看服务记录标签页"""
        brand_view_page.click_view_tab("服务记录")
        assert brand_view_page.is_tab_active("服务记录"), "服务记录标签应处于选中状态"

    def test_07_linked_specs_tab(self, brand_view_page: BrandPage):
        """TC-07 查看已关联规格标签页"""
        brand_view_page.click_view_tab("已关联规格")
        assert brand_view_page.is_tab_active("已关联规格"), "已关联规格标签应处于选中状态"

    def test_08_balance_record_tab(self, brand_view_page: BrandPage):
        """TC-08 查看余额修改记录标签页"""
        brand_view_page.click_view_tab("余额修改记录")
        assert brand_view_page.is_tab_active("余额修改记录"), "余额修改记录标签应处于选中状态"


# ===========================================================================
# 操作按钮（TC-09 ~ TC-11）
# ===========================================================================
@pytest.mark.brand
class TestViewButtons:

    def test_09_modify_agent_btn(self, brand_view_page: BrandPage):
        """TC-09 点击修改经纪人按钮"""
        brand_view_page.click_modify_agent_btn()
        assert brand_view_page.has_dialog_visible(), "应弹出修改经纪人弹窗"
        brand_view_page.close_dialog()

    def test_10_edit_account_btn(self, brand_view_page: BrandPage):
        """TC-10 点击新增编辑账号密码按钮"""
        brand_view_page.click_edit_account_btn()
        assert brand_view_page.has_dialog_visible(), "应弹出账号密码编辑弹窗"
        brand_view_page.close_dialog()

    def test_11_return_btn(self, brand_view_page: BrandPage):
        """TC-11 点击返回按钮"""
        brand_view_page.click_view_return_btn()
        brand_view_page.page.wait_for_timeout(1000)
        assert brand_view_page.is_on_brand_list(), "点击返回后应回到品牌列表页"


# ===========================================================================
# 数据一致性（TC-12）
# ===========================================================================
@pytest.mark.brand
class TestViewDataConsist:

    def test_12_list_data_matches_view(self, brand_list_page: BrandPage):
        """TC-12 列表数据与查看页数据一致"""
        list_content = brand_list_page.page.content()
        assert VIEW_BRAND_NAME in list_content

        brand_list_page.click_view_by_name(VIEW_BRAND_NAME)
        view_content = brand_list_page.page.content()

        assert VIEW_BRAND_NAME in view_content, "查看页品牌名称应与列表一致"
        assert VIEW_BRAND_PHONE in view_content, "查看页手机号应与列表一致"
        assert VIEW_BRAND_CITY in view_content, "查看页上架城市应与列表一致"


# ===========================================================================
# 不同状态查看（TC-13 ~ TC-15）
# ===========================================================================
@pytest.mark.brand
class TestViewStatus:

    def test_13_view_authorized(self, brand_list_page: BrandPage):
        """TC-13 查看"已授权"状态品牌"""
        brand_list_page.click_tab("已授权")

        content = brand_list_page.page.content()
        assert "已授权" in content, "已授权标签页应显示已授权品牌"

    def test_14_view_rejected(self, brand_list_page: BrandPage):
        """TC-14 查看"已驳回"状态品牌"""
        brand_list_page.click_tab("已驳回")

        row_count = brand_list_page.get_list_row_count()
        if row_count == 0:
            pytest.skip("无已驳回品牌")

        brand_list_page.click_first_view_btn()
        content = brand_list_page.page.content()
        assert "已驳回" in content, "查看页应显示已驳回状态"
        assert "查看品牌" in content, "页面标题应为查看品牌"

    def test_15_view_pending(self, brand_list_page: BrandPage):
        """TC-15 查看"申请中"状态品牌"""
        brand_list_page.click_tab("申请中")

        row_count = brand_list_page.get_list_row_count()
        if row_count == 0:
            pytest.skip("无申请中品牌")

        content = brand_list_page.page.content()
        assert "申请中" in content, "申请中标签页应显示申请中品牌"


# ===========================================================================
# 只读验证（TC-16）
# ===========================================================================
@pytest.mark.brand
class TestViewReadOnly:

    def test_16_fields_readonly(self, brand_view_page: BrandPage):
        """TC-16 查看页面字段不可编辑"""
        editable_inputs = brand_view_page.page.locator(
            'input[placeholder="请输入品牌名称"], '
            'input[placeholder="请输入品牌联系人手机号"], '
            'textarea[placeholder="请输入品牌简介"]'
        )
        assert editable_inputs.count() == 0, (
            f"查看页不应有可编辑的输入框，但找到 {editable_inputs.count()} 个"
        )

        submit_btn = brand_view_page.page.locator('.el-form button:has-text("提交")')
        assert submit_btn.count() == 0, "查看页不应有提交按钮"


# ===========================================================================
# 入口：直接运行本文件
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "brand_view_report.html")

    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行品牌查看测试...")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", "pytest", __file__, "-v", "-s",
         f"--html={report_path}", "--self-contained-html"],
        cwd=project_root
    )

    print("=" * 60)
    if result.returncode == 0:
        print("  测试全部通过！")
    else:
        print(f"  有测试失败（退出码: {result.returncode}）")

    if os.path.exists(report_path):
        print(f"  HTML报告: {report_path}")
        os.startfile(report_path)

    input("\n按回车键退出...")
    sys.exit(result.returncode)
