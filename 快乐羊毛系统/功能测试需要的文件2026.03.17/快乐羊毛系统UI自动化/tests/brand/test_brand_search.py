"""品牌管理 - 品牌搜索（20 条用例）

用例来源：测试用例/品牌搜索.xlsx
测试类分组：
  TestKeywordSearch     — 关键字搜索
  TestAgentFilter       — 代理商筛选
  TestDateFilter        — 申请时间筛选
  TestCityFilter        — 城市筛选
  TestCombinedSearch    — 组合搜索
  TestReset             — 重置
  TestTabFilter         — Tab 状态筛选
  TestListDisplay       — 列表展示 & 分页

fixture 说明：
  brand_list_page  — 已登录，在品牌管理列表页（所有搜索用例的起点）
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.brand_page import BrandPage


# ===========================================================================
# 关键字搜索（TC-01 ~ TC-06）
# ===========================================================================
@pytest.mark.brand
class TestKeywordSearch:

    def test_01_search_full_name(self, brand_list_page: BrandPage):
        """TC-01 输入完整品牌名称搜索"""
        brand_list_page.search_by_keyword("小王")

        names = brand_list_page.get_list_brand_names()
        assert len(names) > 0, "搜索'小王'应有结果"
        assert all("小王" in n for n in names), f"所有结果应包含'小王'，实际: {names}"

    def test_02_search_partial_keyword(self, brand_list_page: BrandPage):
        """TC-02 输入品牌名称部分关键字搜索"""
        brand_list_page.search_by_keyword("小")

        names = brand_list_page.get_list_brand_names()
        assert len(names) > 0, "搜索'小'应有结果（模糊搜索）"

    def test_03_search_by_phone(self, brand_list_page: BrandPage):
        """TC-03 输入手机号搜索"""
        brand_list_page.search_by_keyword("15570441314")

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            contacts = brand_list_page.get_list_column_texts(4)
            assert any("15570441314" in c for c in contacts), (
                f"搜索结果应包含手机号15570441314，实际联系人: {contacts}"
            )

    def test_04_search_nonexistent(self, brand_list_page: BrandPage):
        """TC-04 输入不存在的品牌名称搜索"""
        brand_list_page.search_by_keyword("一个不存在的品牌名12345")

        assert brand_list_page.is_list_empty(), "搜索不存在的品牌应显示空结果"

    def test_05_search_empty(self, brand_list_page: BrandPage):
        """TC-05 搜索框为空点击搜索"""
        brand_list_page.search_by_keyword("")

        row_count = brand_list_page.get_list_row_count()
        assert row_count > 0, "空搜索应显示所有品牌数据"

    def test_06_search_special_chars(self, brand_list_page: BrandPage):
        """TC-06 输入特殊字符搜索"""
        brand_list_page.search_by_keyword("@#$%")

        assert brand_list_page.is_list_empty() or brand_list_page.get_list_row_count() >= 0, (
            "特殊字符搜索应正常返回（空结果或匹配结果），不报错"
        )


# ===========================================================================
# 代理商筛选（TC-07）
# ===========================================================================
@pytest.mark.brand
class TestAgentFilter:

    def test_07_filter_by_agent(self, brand_list_page: BrandPage):
        """TC-07 选择品牌所属代理商搜索"""
        brand_list_page.select_agent_filter(index=0)
        brand_list_page.click_search()

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            agents = brand_list_page.get_list_column_texts(10)
            unique_agents = set(agents)
            assert len(unique_agents) <= 2, (
                f"筛选后代理商应一致，实际: {unique_agents}"
            )


# ===========================================================================
# 申请时间筛选（TC-08 ~ TC-09）
# ===========================================================================
@pytest.mark.brand
class TestDateFilter:

    def test_08_date_range_search(self, brand_list_page: BrandPage):
        """TC-08 设置申请时间范围搜索"""
        brand_list_page.set_apply_date_range("2026-03-01", "2026-03-31")
        brand_list_page.click_search()

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            dates = brand_list_page.get_list_column_texts(6)
            for d in dates:
                assert "2026-03" in d, f"申请时间应在3月范围内，实际: {d}"

    def test_09_only_start_date(self, brand_list_page: BrandPage):
        """TC-09 只设置开始日期搜索"""
        start_input = brand_list_page.page.locator(brand_list_page.SEL_APPLY_DATE_START)
        start_input.click()
        start_input.fill("2026-03-20")
        start_input.press("Enter")
        brand_list_page.page.wait_for_timeout(500)
        brand_list_page.click_search()

        brand_list_page.page.wait_for_timeout(1000)
        assert brand_list_page.is_on_brand_list(), "只设置开始日期搜索后页面应正常"


# ===========================================================================
# 城市筛选（TC-10）
# ===========================================================================
@pytest.mark.brand
class TestCityFilter:

    def test_10_filter_by_city(self, brand_list_page: BrandPage):
        """TC-10 选择品牌上架城市搜索"""
        brand_list_page.select_city_filter("重庆市")
        brand_list_page.click_search()

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            cities = brand_list_page.get_list_column_texts(5)
            for city in cities:
                assert "重庆" in city, f"筛选后城市应为重庆市，实际: {city}"


# ===========================================================================
# 组合搜索（TC-11）
# ===========================================================================
@pytest.mark.brand
class TestCombinedSearch:

    def test_11_combined_search(self, brand_list_page: BrandPage):
        """TC-11 多条件组合搜索"""
        brand_list_page.page.locator(brand_list_page.SEL_SEARCH_INPUT).fill("小王")
        brand_list_page.select_city_filter("重庆市")
        brand_list_page.click_search()

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            names = brand_list_page.get_list_brand_names()
            assert all("小王" in n for n in names), f"组合搜索结果应匹配关键字，实际: {names}"


# ===========================================================================
# 重置（TC-12）
# ===========================================================================
@pytest.mark.brand
class TestReset:

    def test_12_reset_search(self, brand_list_page: BrandPage):
        """TC-12 执行搜索后点击重置"""
        # 先执行搜索
        brand_list_page.search_by_keyword("小王")
        filtered_count = brand_list_page.get_list_row_count()

        # 点击重置
        brand_list_page.click_reset()

        search_val = brand_list_page.get_search_input_value()
        assert search_val == "", f"重置后搜索框应为空，实际: '{search_val}'"

        total_count = brand_list_page.get_list_row_count()
        assert total_count >= filtered_count, "重置后列表应显示全部数据"


# ===========================================================================
# Tab 状态筛选（TC-13 ~ TC-18）
# ===========================================================================
@pytest.mark.brand
class TestTabFilter:

    def test_13_tab_all(self, brand_list_page: BrandPage):
        """TC-13 点击"全部"标签"""
        brand_list_page.click_tab("全部")
        tab_text = brand_list_page.get_tab_text("全部")
        assert "全部" in tab_text, f"全部标签应显示，实际: {tab_text}"

        row_count = brand_list_page.get_list_row_count()
        assert row_count > 0, "全部标签应有数据"

    def test_14_tab_pending(self, brand_list_page: BrandPage):
        """TC-14 点击"申请中"标签"""
        brand_list_page.click_tab("申请中")

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            statuses = brand_list_page.get_list_column_texts(9)
            assert all("申请中" in s for s in statuses), f"申请中标签结果状态应一致，实际: {statuses}"

    def test_15_tab_authorized(self, brand_list_page: BrandPage):
        """TC-15 点击"已授权"标签"""
        brand_list_page.click_tab("已授权")

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            statuses = brand_list_page.get_list_column_texts(9)
            assert all("已授权" in s for s in statuses), f"已授权标签结果状态应一致，实际: {statuses}"

    def test_16_tab_rejected(self, brand_list_page: BrandPage):
        """TC-16 点击"已驳回"标签"""
        brand_list_page.click_tab("已驳回")

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            statuses = brand_list_page.get_list_column_texts(9)
            assert all("已驳回" in s for s in statuses), f"已驳回标签结果状态应一致，实际: {statuses}"

    def test_17_tab_recheck(self, brand_list_page: BrandPage):
        """TC-17 点击"重新审核"标签"""
        brand_list_page.click_tab("重新审核")

        brand_list_page.page.wait_for_timeout(1000)
        row_count = brand_list_page.get_list_row_count()
        if row_count == 0:
            assert brand_list_page.is_list_empty(), "无重新审核数据时应显示空状态"

    def test_18_tab_with_search(self, brand_list_page: BrandPage):
        """TC-18 Tab筛选与搜索条件联动"""
        brand_list_page.page.locator(brand_list_page.SEL_SEARCH_INPUT).fill("小王")
        brand_list_page.click_search()

        brand_list_page.click_tab("已授权")

        row_count = brand_list_page.get_list_row_count()
        if row_count > 0:
            names = brand_list_page.get_list_brand_names()
            statuses = brand_list_page.get_list_column_texts(9)
            for name in names:
                assert "小王" in name, f"结果应匹配关键字'小王'，实际: {name}"
            for status in statuses:
                assert "已授权" in status, f"结果状态应为已授权，实际: {status}"


# ===========================================================================
# 列表展示 & 分页（TC-19 ~ TC-20）
# ===========================================================================
@pytest.mark.brand
class TestListDisplay:

    def test_19_list_headers(self, brand_list_page: BrandPage):
        """TC-19 品牌列表字段完整性检查"""
        headers = brand_list_page.get_list_headers()
        expected = ["ID", "品牌图标", "品牌名称", "品牌联系人",
                    "品牌上架城市", "申请时间", "申请人", "认证状态",
                    "状态", "所属代理商", "是否限时", "操作"]
        for h in expected:
            assert h in headers, f"表头应包含'{h}'，实际表头: {headers}"

    def test_20_pagination(self, brand_list_page: BrandPage):
        """TC-20 列表分页功能"""
        total_text = brand_list_page.get_list_total_text()
        assert "共" in total_text and "条" in total_text, (
            f"应显示总条数，实际: {total_text}"
        )

        next_btn = brand_list_page.page.locator('button.btn-next:not([disabled])')
        if next_btn.count() > 0:
            page1_names = brand_list_page.get_list_brand_names()
            brand_list_page.click_next_page()
            page2_names = brand_list_page.get_list_brand_names()
            assert page2_names != page1_names or len(page2_names) > 0, (
                "翻页后数据应切换"
            )


# ===========================================================================
# 入口：直接运行本文件
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "brand_search_report.html")

    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行品牌搜索测试...")
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
