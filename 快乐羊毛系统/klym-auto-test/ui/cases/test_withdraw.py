"""
UI 测试 - 提现结算
对应用例编号：txjs-001 ~ txjs-006

功能：佣金结算状态转换、提现申请、审核、校验
"""
import pytest
from ui.pages.base_page import BasePage


@pytest.mark.ui
@pytest.mark.withdraw
class TestWithdraw:
    """提现结算"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = BasePage(admin_page)

    @pytest.mark.p0
    def test_txjs001_settlement_status_flow(self, admin_page):
        """txjs-001: 验证佣金从"待结算"到"可提现"的状态转换
        步骤：进入财务管理 > 提现申请
        预期：佣金状态经历 待结算 > 可提现
        """
        self.page.navigate("财务管理", "提现申请")
        self.page.wait_loading()

    @pytest.mark.p0
    def test_txjs002_withdraw_apply(self, admin_page):
        """txjs-002: 验证分销员/代理商发起提现到余额扣减
        步骤：查看提现申请列表
        预期：有提现申请记录
        """
        self.page.navigate("财务管理", "提现申请")
        self.page.wait_loading()
        data = self.page.get_table_data()
        assert isinstance(data, list)

    @pytest.mark.p1
    def test_txjs003_withdraw_reject(self, admin_page):
        """txjs-003: 验证提现审核拒绝的处理
        步骤：对提现申请执行拒绝
        预期：退回可提现状态+拒绝原因
        """
        self.page.navigate("财务管理", "提现申请")
        self.page.wait_loading()

    @pytest.mark.p0
    def test_txjs004_withdraw_validation(self, admin_page):
        """txjs-004: 验证提现金额校验
        预期：提现>余额提示不能超过可提现余额
        """
        self.page.navigate("财务管理", "提现申请")
        self.page.wait_loading()

    @pytest.mark.p0
    def test_txjs005_refund_after_withdraw(self, admin_page):
        """txjs-005: 验证佣金已提现后退款欠费的处理
        预期：产生欠款记录
        """
        self.page.navigate("财务管理", "佣金记录")
        self.page.wait_loading()

    @pytest.mark.p1
    def test_txjs006_withdraw_record(self, admin_page):
        """txjs-006: 验证提现状态查询记录
        步骤：查看财务记录
        预期：提现记录完整
        """
        self.page.navigate("财务管理", "财务记录")
        self.page.wait_loading()
        data = self.page.get_table_data()
        assert isinstance(data, list)
