"""
CommissionPage - 分佣配置页面

导航路径：推广管理 > 分销员设置 / 财务管理 > 佣金记录
功能：分佣比例配置、佣金记录查看、Excel佣金导入
"""
from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage
from common.logger import logger


class CommissionConfigPage(BasePage):
    """分佣配置页面"""

    def __init__(self, page: Page):
        super().__init__(page)

    def goto_commission_config(self):
        """导航到分佣配置页面"""
        self.navigate("推广管理", "分销员设置")

    def select_business_line(self, name: str):
        """选择业务线（如：餐饮折扣、会员充值）"""
        logger.info(f"选择业务线: {name}")
        self.page.get_by_text(name, exact=False).first.click()
        self.wait_loading()

    def set_agent_rate(self, rate: str):
        """设置代理商分佣比例"""
        logger.info(f"设置代理商比例: {rate}%")
        # 根据实际页面调整定位器
        agent_input = self.page.locator(
            "input[placeholder*='代理商'], input[placeholder*='比例']"
        ).first
        agent_input.clear()
        agent_input.fill(str(rate))

    def set_distributor_rate(self, level1: str = "", level2: str = ""):
        """设置分销员分佣比例"""
        if level1:
            logger.info(f"设置一级分销员比例: {level1}%")
            inputs = self.page.locator("input[placeholder*='一级'], input[placeholder*='分销']")
            if inputs.count() > 0:
                inputs.first.clear()
                inputs.first.fill(str(level1))
        if level2:
            logger.info(f"设置二级分销员比例: {level2}%")
            inputs = self.page.locator("input[placeholder*='二级']")
            if inputs.count() > 0:
                inputs.first.clear()
                inputs.first.fill(str(level2))

    def save_config(self):
        """点击保存"""
        self.click_button("保存")
        self.wait_loading()

    def get_config_list(self) -> list:
        """获取分佣配置列表数据"""
        return self.get_table_data()

    def assert_save_success(self):
        """断言保存成功"""
        msg = self.get_message()
        assert "成功" in msg, f"期望保存成功，实际: {msg}"

    def assert_save_failed(self, expected_msg: str = None):
        """断言保存失败"""
        msg = self.get_message()
        if expected_msg:
            assert expected_msg in msg, f"期望包含 '{expected_msg}'，实际: {msg}"
        logger.info(f"保存失败（符合预期）: {msg}")


class CommissionRecordPage(BasePage):
    """佣金记录页面"""

    def __init__(self, page: Page):
        super().__init__(page)

    def goto_commission_record(self):
        """导航到佣金记录页面"""
        self.navigate("财务管理", "佣金记录")

    def search_by_order(self, order_no: str):
        """按订单号搜索佣金记录"""
        self.search(order_no, "请输入订单号")

    def filter_by_date(self, start: str, end: str):
        """按时间范围筛选"""
        logger.info(f"筛选日期: {start} ~ {end}")
        date_inputs = self.page.locator(".el-date-editor input")
        if date_inputs.count() >= 2:
            date_inputs.nth(0).fill(start)
            date_inputs.nth(1).fill(end)
        self.click_button("搜索")
        self.wait_loading()

    def get_commission_details(self) -> list:
        """获取佣金明细列表"""
        return self.get_table_data()

    def verify_commission_amount(self, role: str, expected_amount: str):
        """验证某角色的佣金金额"""
        data = self.get_table_data()
        for row in data:
            row_text = str(row)
            if role in row_text and expected_amount in row_text:
                logger.info(f"验证通过: {role} 佣金 {expected_amount}")
                return True
        raise AssertionError(f"未找到 {role} 佣金 {expected_amount}")


class ExcelImportPage(BasePage):
    """Excel 佣金导入页面"""

    def __init__(self, page: Page):
        super().__init__(page)

    def goto_import(self):
        """导航到佣金录入页面"""
        self.navigate("财务管理", "佣金记录")

    def click_import_button(self):
        """点击导入Excel按钮"""
        self.click_button("导入")

    def upload_excel(self, filepath: str):
        """上传 Excel 文件"""
        logger.info(f"上传文件: {filepath}")
        # Element UI 的上传组件通常用 input[type=file]
        file_input = self.page.locator("input[type='file']")
        file_input.set_input_files(filepath)
        self.wait_loading()

    def confirm_import(self):
        """确认导入"""
        self.click_button("确认导入")
        self.wait_loading()

    def cancel_import(self):
        """取消导入"""
        self.click_button("取消")

    def get_preview_data(self) -> list:
        """获取预览数据"""
        return self.get_table_data()

    def get_import_result(self) -> str:
        """获取导入结果消息"""
        return self.get_message()
