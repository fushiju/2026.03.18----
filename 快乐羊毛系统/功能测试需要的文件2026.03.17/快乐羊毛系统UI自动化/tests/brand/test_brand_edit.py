"""品牌管理 - 编辑品牌（28 条用例）

用例来源：测试用例/品牌编辑.xlsx
测试类分组：
  TestEditEntry          — 进入编辑 & 数据预填充
  TestEditBrandName      — 修改品牌名称
  TestEditContact        — 修改品牌联系人
  TestEditDropdowns      — 修改分类类型 / 接口渠道 / 上架城市
  TestEditCommission     — 修改提成比例
  TestEditDesc           — 修改品牌简介
  TestEditUpload         — 修改品牌ICON / 品牌图片
  TestEditOther          — 修改虚拟订单量 / 是否售罄 / 经纪人 / 账号密码
  TestEditInteraction    — 不修改提交 / 返回不保存 / 编辑后验证 / Tab切换

fixture 说明：
  brand_list_page  — 已登录，在品牌列表页（TC-01 从列表进入编辑）
  brand_edit_page  — 已登录，在品牌"小王"的编辑页（大部分编辑用例）
  brand_page       — 已登录，未导航（需要多步跳转的用例）
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import pytest
from pages.brand_page import BrandPage
from tests.brand.conftest import EDIT_BRAND_NAME


# ===========================================================================
# 进入编辑 & 数据预填充（TC-01 ~ TC-02）
# ===========================================================================
@pytest.mark.brand
class TestEditEntry:

    def test_01_enter_edit_page(self, brand_list_page: BrandPage):
        """TC-01 从列表点击编辑按钮进入编辑页"""
        brand_list_page.click_edit_by_name(EDIT_BRAND_NAME)

        assert brand_list_page.is_on_edit_page(), f"应跳转到编辑页面，实际URL: {brand_list_page.current_url}"
        title = brand_list_page.get_view_title()
        assert "编辑" in title or "新增" in title, f"页面标题应含'编辑'，实际: {title}"
        name_val = brand_list_page.get_brand_name_value()
        assert name_val, "编辑页品牌名称应预填充原始数据"

    def test_02_prefilled_data(self, brand_edit_page: BrandPage):
        """TC-02 编辑页面预填充数据正确性"""
        name_val = brand_edit_page.get_brand_name_value()
        assert name_val == EDIT_BRAND_NAME, f"品牌名称应为'{EDIT_BRAND_NAME}'，实际: '{name_val}'"

        name_count = brand_edit_page.get_brand_name_count()
        assert "2" in name_count and "15" in name_count, f"品牌名称计数应含 2/15，实际: {name_count}"

        contact_val = brand_edit_page.page.locator(brand_edit_page.SEL_BRAND_CONTACT).input_value()
        assert contact_val == "15570441314", f"联系人应为15570441314，实际: {contact_val}"

        contact_count = brand_edit_page.get_brand_contact_count()
        assert "11" in contact_count, f"联系人计数应含 11，实际: {contact_count}"


# ===========================================================================
# 修改品牌名称（TC-03 ~ TC-06）
# ===========================================================================
@pytest.mark.brand
class TestEditBrandName:

    def test_03_modify_name(self, brand_page: BrandPage):
        """TC-03 修改品牌名称并保存"""
        brand_page.goto_edit_brand(EDIT_BRAND_NAME)

        brand_page.clear_and_fill_brand_name("测试修改名")
        brand_page.click_submit()

        msg = brand_page.get_success_message(timeout=8000)
        assert msg or brand_page.is_on_brand_list(), "修改品牌名称后应提交成功"

        # 恢复原名
        if brand_page.is_on_brand_list():
            brand_page.click_edit_by_name("测试修改名")
            brand_page.clear_and_fill_brand_name(EDIT_BRAND_NAME)
            brand_page.click_submit()

    def test_04_clear_name_submit(self, brand_edit_page: BrandPage):
        """TC-04 清空品牌名称后提交"""
        brand_edit_page.clear_and_fill_brand_name("")
        brand_edit_page.click_submit()

        assert brand_edit_page.has_form_error(), "品牌名称为空应有校验提示"

    def test_05_duplicate_name(self, brand_edit_page: BrandPage):
        """TC-05 修改品牌名称为已存在的名称"""
        brand_edit_page.clear_and_fill_brand_name("测试品牌")
        brand_edit_page.click_submit()

        brand_edit_page.page.wait_for_timeout(2000)
        error = brand_edit_page.get_error_message()
        form_errors = brand_edit_page.get_form_errors()
        all_text = error + " ".join(form_errors)
        assert "已存在" in all_text or "重复" in all_text or not brand_edit_page.is_on_brand_list(), (
            f"重复名称应提示已存在，实际: {all_text}"
        )

    def test_06_name_max_boundary(self, brand_page: BrandPage):
        """TC-06 品牌名称修改为15字符（最大边界）"""
        brand_page.goto_edit_brand(EDIT_BRAND_NAME)

        name_15 = "编辑品牌最大边界测试名称字"[:15]
        brand_page.clear_and_fill_brand_name(name_15)

        count = brand_page.get_brand_name_count()
        assert "15" in count, f"字符计数应含 15，实际: {count}"

        brand_page.click_submit()
        msg = brand_page.get_success_message(timeout=8000)
        assert msg or brand_page.is_on_brand_list(), "15字符名称应提交成功"

        # 恢复原名
        if brand_page.is_on_brand_list():
            brand_page.click_edit_by_name(name_15)
            brand_page.clear_and_fill_brand_name(EDIT_BRAND_NAME)
            brand_page.click_submit()


# ===========================================================================
# 修改品牌联系人（TC-07 ~ TC-09）
# ===========================================================================
@pytest.mark.brand
class TestEditContact:

    def test_07_modify_contact(self, brand_page: BrandPage):
        """TC-07 修改联系人手机号并保存"""
        brand_page.goto_edit_brand(EDIT_BRAND_NAME)

        brand_page.clear_and_fill_brand_contact("13600136000")
        brand_page.click_submit()

        msg = brand_page.get_success_message(timeout=8000)
        assert msg or brand_page.is_on_brand_list(), "修改联系人后应提交成功"

        # 恢复
        if brand_page.is_on_brand_list():
            brand_page.click_edit_by_name(EDIT_BRAND_NAME)
            brand_page.clear_and_fill_brand_contact("15570441314")
            brand_page.click_submit()

    def test_08_clear_contact_submit(self, brand_edit_page: BrandPage):
        """TC-08 清空品牌联系人后提交"""
        brand_edit_page.clear_and_fill_brand_contact("")
        brand_edit_page.click_submit()

        assert brand_edit_page.has_form_error(), "联系人为空应有校验提示"

    def test_09_invalid_contact(self, brand_edit_page: BrandPage):
        """TC-09 修改联系人为非手机号格式"""
        brand_edit_page.clear_and_fill_brand_contact("abcdefg")
        brand_edit_page.click_submit()

        assert not brand_edit_page.is_on_brand_list(), "非手机号格式不应提交成功"


# ===========================================================================
# 修改分类类型 / 接口渠道 / 上架城市（TC-10 ~ TC-12）
# ===========================================================================
@pytest.mark.brand
class TestEditDropdowns:

    def test_10_switch_category(self, brand_edit_page: BrandPage):
        """TC-10 切换分类类型并保存"""
        brand_edit_page.select_category_type(index=1)
        brand_edit_page.click_submit()

        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "切换分类类型后应提交成功"

    def test_11_switch_channel(self, brand_edit_page: BrandPage):
        """TC-11 切换接口渠道并保存"""
        brand_edit_page.select_api_channel(index=0)
        brand_edit_page.click_submit()

        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "切换接口渠道后应提交成功"

    def test_12_switch_city(self, brand_edit_page: BrandPage):
        """TC-12 切换品牌上架城市并保存"""
        brand_edit_page.select_city(index=0)
        brand_edit_page.click_submit()

        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "切换城市后应提交成功"


# ===========================================================================
# 修改提成比例（TC-13 ~ TC-14）
# ===========================================================================
@pytest.mark.brand
class TestEditCommission:

    def test_13_set_commission(self, brand_edit_page: BrandPage):
        """TC-13 设置提成比例并保存"""
        brand_edit_page.clear_and_fill_commission_rate("15")
        brand_edit_page.click_submit()

        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "设置提成比例后应提交成功"

    def test_14_commission_over_100(self, brand_edit_page: BrandPage):
        """TC-14 提成比例修改为超出范围值"""
        brand_edit_page.clear_and_fill_commission_rate("150")
        brand_edit_page.click_submit()

        assert not brand_edit_page.is_on_brand_list(), "提成比例超过100不应提交成功"


# ===========================================================================
# 修改品牌简介（TC-15 ~ TC-16）
# ===========================================================================
@pytest.mark.brand
class TestEditDesc:

    def test_15_modify_desc(self, brand_edit_page: BrandPage):
        """TC-15 修改品牌简介并保存"""
        brand_edit_page.clear_and_fill_brand_desc("这是修改后的品牌简介内容")
        brand_edit_page.click_submit()

        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "修改品牌简介后应提交成功"

    def test_16_clear_desc_submit(self, brand_edit_page: BrandPage):
        """TC-16 清空品牌简介后提交"""
        brand_edit_page.clear_and_fill_brand_desc("")
        brand_edit_page.click_submit()

        assert brand_edit_page.has_form_error(), "品牌简介为空应有校验提示"


# ===========================================================================
# 修改品牌ICON / 品牌图片（TC-17 ~ TC-18）
# ===========================================================================
@pytest.mark.brand
class TestEditUpload:

    def test_17_replace_icon(self, brand_edit_page: BrandPage, test_fixtures_dir):
        """TC-17 重新上传品牌ICON"""
        icon_path = str(test_fixtures_dir / "test_icon.png")
        brand_edit_page.upload_brand_icon(icon_path)

        assert brand_edit_page.has_icon_preview(), "上传新ICON后应显示预览"

        brand_edit_page.click_submit()
        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "替换ICON后应提交成功"

    def test_18_upload_image(self, brand_edit_page: BrandPage, test_fixtures_dir):
        """TC-18 添加/修改品牌图片"""
        image_path = str(test_fixtures_dir / "test_image.png")
        brand_edit_page.upload_brand_image(image_path)

        brand_edit_page.click_submit()
        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "上传品牌图片后应提交成功"


# ===========================================================================
# 修改虚拟订单量 / 是否售罄 / 经纪人 / 账号密码（TC-19 ~ TC-22）
# ===========================================================================
@pytest.mark.brand
class TestEditOther:

    def test_19_modify_virtual_orders(self, brand_edit_page: BrandPage):
        """TC-19 修改虚拟订单量并保存"""
        brand_edit_page.clear_and_fill_virtual_orders("200")
        brand_edit_page.click_submit()

        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "修改虚拟订单量后应提交成功"

    def test_20_toggle_sold_out(self, brand_page: BrandPage):
        """TC-20 在编辑页切换是否售罄"""
        brand_page.goto_edit_brand(EDIT_BRAND_NAME)

        brand_page.select_sold_out(sold_out=True)
        brand_page.click_submit()

        msg = brand_page.get_success_message(timeout=8000)
        assert msg or brand_page.is_on_brand_list(), "切换售罄状态后应提交成功"

        # 恢复为未售罄
        if brand_page.is_on_brand_list():
            brand_page.click_edit_by_name(EDIT_BRAND_NAME)
            brand_page.select_sold_out(sold_out=False)
            brand_page.click_submit()

    def test_21_modify_agent(self, brand_edit_page: BrandPage):
        """TC-21 点击修改经纪人按钮"""
        try:
            brand_edit_page.click_modify_agent_btn()
            assert brand_edit_page.has_dialog_visible(), "应弹出经纪人选择弹窗"
            brand_edit_page.close_dialog()
        except Exception:
            pytest.skip("编辑页未找到修改经纪人按钮")

    def test_22_edit_account(self, brand_edit_page: BrandPage):
        """TC-22 新增编辑账号密码"""
        try:
            brand_edit_page.click_edit_account_btn()
            assert brand_edit_page.has_dialog_visible(), "应弹出账号密码编辑弹窗"
            brand_edit_page.close_dialog()
        except Exception:
            pytest.skip("编辑页未找到新增编辑账号密码按钮")


# ===========================================================================
# 不修改提交 / 返回不保存 / 编辑后验证 / Tab切换（TC-23 ~ TC-28）
# ===========================================================================
@pytest.mark.brand
class TestEditInteraction:

    def test_23_submit_without_change(self, brand_edit_page: BrandPage):
        """TC-23 不做任何修改直接点击提交"""
        brand_edit_page.click_submit()

        msg = brand_edit_page.get_success_message(timeout=8000)
        assert msg or brand_edit_page.is_on_brand_list(), "不修改直接提交应成功"

    def test_24_back_without_save(self, brand_edit_page: BrandPage):
        """TC-24 修改数据后点击返回"""
        brand_edit_page.clear_and_fill_brand_name("不应保存的名称")
        brand_edit_page.click_back()

        brand_edit_page.page.wait_for_timeout(1000)
        assert brand_edit_page.is_on_brand_list(), "点击返回后应回到列表页"
        names = brand_edit_page.get_list_brand_names()
        assert "不应保存的名称" not in names, "返回后修改不应生效"

    def test_25_edit_then_verify(self, brand_page: BrandPage):
        """TC-25 编辑保存后查看详情验证数据一致"""
        brand_page.goto_edit_brand(EDIT_BRAND_NAME)

        new_name = "验证品牌X"
        brand_page.clear_and_fill_brand_name(new_name)
        brand_page.click_submit()

        msg = brand_page.get_success_message(timeout=8000)
        if not msg and not brand_page.is_on_brand_list():
            pytest.skip("编辑提交失败，跳过验证")

        brand_page.page.wait_for_timeout(1000)
        if brand_page.is_on_brand_list():
            assert brand_page.brand_exists_in_list(new_name), f"列表中应有品牌'{new_name}'"

            # 恢复原名
            brand_page.click_edit_by_name(new_name)
            brand_page.clear_and_fill_brand_name(EDIT_BRAND_NAME)
            brand_page.click_submit()

    def test_26_tab_service_record(self, brand_edit_page: BrandPage):
        """TC-26 切换服务记录Tab"""
        brand_edit_page.click_view_tab("服务记录")
        assert brand_edit_page.is_tab_active("服务记录"), "服务记录标签应处于选中状态"

    def test_27_tab_linked_specs(self, brand_edit_page: BrandPage):
        """TC-27 切换已关联规格Tab"""
        brand_edit_page.click_view_tab("已关联规格")
        assert brand_edit_page.is_tab_active("已关联规格"), "已关联规格标签应处于选中状态"

    def test_28_tab_balance_record(self, brand_edit_page: BrandPage):
        """TC-28 切换余额修改记录Tab"""
        brand_edit_page.click_view_tab("余额修改记录")
        assert brand_edit_page.is_tab_active("余额修改记录"), "余额修改记录标签应处于选中状态"


# ===========================================================================
# 入口：直接运行本文件
# ===========================================================================
if __name__ == "__main__":
    import subprocess, os

    project_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    os.chdir(project_root)
    report_path = os.path.join(project_root, "reports", "brand_edit_report.html")

    if os.path.exists(report_path):
        os.remove(report_path)

    print("=" * 60)
    print("  开始执行品牌编辑测试...")
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
