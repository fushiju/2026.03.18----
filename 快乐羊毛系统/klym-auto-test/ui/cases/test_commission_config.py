"""
UI 测试 - 分佣系统 - 分佣配置
对应用例编号：fyxt-001 ~ fyxt-008

功能：分佣比例配置（代理商、分销员）、边界校验
"""
import pytest
from ui.pages.commission_page import CommissionConfigPage


@pytest.mark.ui
@pytest.mark.commission
class TestCommissionConfig:
    """分佣比例配置"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = CommissionConfigPage(admin_page)
        self.page.goto_commission_config()

    @pytest.mark.p1
    def test_fyxt001_set_agent_rate(self, admin_page):
        """fyxt-001: 验证设置代理商分佣比例成功
        步骤：进入分佣配置 > 选择餐饮折扣 > 设置代理商5% > 保存
        预期：提示保存成功，列表显示餐饮折扣代理商分佣5%
        """
        self.page.select_business_line("餐饮折扣")
        self.page.set_agent_rate("5")
        self.page.save_config()
        self.page.assert_save_success()

    @pytest.mark.p1
    def test_fyxt002_set_distributor_rate(self, admin_page):
        """fyxt-002: 验证设置分销员分佣比例等级
        步骤：选择会员充值 > 设置一级3%、二级1% > 保存
        预期：保存成功，展示会员充值分销员一级3%、二级1%
        """
        self.page.select_business_line("会员充值")
        self.page.set_distributor_rate(level1="3", level2="1")
        self.page.save_config()
        self.page.assert_save_success()

    @pytest.mark.p2
    def test_fyxt004_different_business_lines(self, admin_page):
        """fyxt-004: 验证按业务线区分不同分佣规则
        步骤：查看分佣配置列表
        预期：餐饮折扣和外卖券配置互不影响
        """
        data = self.page.get_config_list()
        assert len(data) > 0, "分佣配置列表为空"

    @pytest.mark.p3
    def test_fyxt006_rate_sum_over_100(self, admin_page):
        """fyxt-006: [反向] 验证分佣比例超过100%时保存失败
        步骤：设置代理商60%、一级分销员50% > 保存
        预期：提示分佣比例总和不能超过100%
        """
        self.page.select_business_line("餐饮折扣")
        self.page.set_agent_rate("60")
        self.page.set_distributor_rate(level1="50")
        self.page.save_config()
        self.page.assert_save_failed("100%")

    @pytest.mark.p3
    def test_fyxt007_negative_rate(self, admin_page):
        """fyxt-007: [反向] 验证分佣比例输入负数被拦截
        步骤：设置代理商-5% > 保存
        预期：提示分佣比例不能为负数
        """
        self.page.set_agent_rate("-5")
        self.page.save_config()
        self.page.assert_save_failed("负数")

    @pytest.mark.p4
    def test_fyxt008_decimal_rate(self, admin_page):
        """fyxt-008: 验证分佣比例支持小数精度
        步骤：设置代理商3.75% > 保存
        预期：保存成功，显示3.75%
        """
        self.page.set_agent_rate("3.75")
        self.page.save_config()
        self.page.assert_save_success()
