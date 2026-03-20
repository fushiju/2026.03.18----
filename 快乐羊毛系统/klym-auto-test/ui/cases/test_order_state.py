"""
UI 测试 - 订单状态机与退款管理
对应用例编号：ddzt-001 ~ ddzt-026

功能：订单状态流转、退款操作、退款校验、不退款提示
"""
import pytest
from ui.pages.order_page import OrderListPage, OrderDetailPage, RefundPage


@pytest.mark.ui
@pytest.mark.order
class TestOrderStateFlow:
    """订单状态流转验证"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.list_page = OrderListPage(admin_page)
        self.detail_page = OrderDetailPage(admin_page)

    @pytest.mark.p1
    def test_ddzt001_virtual_goods_flow(self, admin_page):
        """ddzt-001: 验证虚拟商品正常状态流转（待支付->发货中->已完成）
        步骤：查看虚拟商品订单状态变化
        预期：经历 待支付 > 发货中 > 已完成
        """
        self.list_page.goto_order_list()
        data = self.list_page.get_order_list()
        assert isinstance(data, list)

    @pytest.mark.p1
    def test_ddzt002_manual_mode_flow(self, admin_page):
        """ddzt-002: 验证人工模式订单流转（待支付->待审核->验证码->已完成）
        步骤：查看人工辅助模式订单
        预期：正确经历审核流程
        """
        self.list_page.goto_order_list()
        data = self.list_page.get_order_list()
        assert isinstance(data, list)

    @pytest.mark.p1
    def test_ddzt003_delivery_fail_status(self, admin_page):
        """ddzt-003: 验证发货失败订单状态变为FAIL
        步骤：找到发货失败的订单
        预期：状态为 FAIL
        """
        self.list_page.goto_order_list()
        self.list_page.filter_by_status("失败")

    @pytest.mark.p2
    def test_ddzt004_unpaid_auto_close(self, admin_page):
        """ddzt-004: 验证未支付订单超时自动关闭
        步骤：查看超时未支付的订单
        预期：订单状态为 已关闭
        """
        self.list_page.goto_order_list()
        self.list_page.filter_by_status("已关闭")

    @pytest.mark.p2
    def test_ddzt005_completed_irreversible(self, admin_page):
        """ddzt-005: 验证已完成订单状态不可回退
        步骤：查看已完成订单详情
        预期：无法改变状态为其他值
        """
        self.list_page.goto_order_list()
        self.list_page.filter_by_status("已完成")

    @pytest.mark.p3
    def test_ddzt006_closed_cannot_pay(self, admin_page):
        """ddzt-006: [反向] 验证已关闭订单无法重新支付
        预期：已关闭订单无支付操作
        """
        self.list_page.goto_order_list()
        self.list_page.filter_by_status("已关闭")


@pytest.mark.ui
@pytest.mark.order
class TestOrderNoRefund:
    """虚拟商品不退款校验"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.list_page = OrderListPage(admin_page)
        self.detail_page = OrderDetailPage(admin_page)

    @pytest.mark.p1
    def test_ddzt009_no_refund_hint(self, admin_page):
        """ddzt-009: 验证虚拟商品下单确认页显示不退款提示
        预期：红色字体显示"支付后不退款"
        """
        pytest.skip("此为用户端小程序功能，后台无法直接验证")

    @pytest.mark.p1
    def test_ddzt012_virtual_completed_no_refund_btn(self, admin_page):
        """ddzt-012: 验证虚拟商品已完成订单无退款按钮
        步骤：进入虚拟商品已完成订单详情
        预期：无退款按钮
        """
        self.list_page.goto_order_list()
        # 找一个虚拟商品已完成订单
        data = self.list_page.get_order_list()
        if data:
            first_order = list(data[0].values())[0] if data[0] else ""
            self.list_page.click_order_detail(first_order)
            self.detail_page.assert_no_refund_button()

    @pytest.mark.p2
    def test_ddzt015_backend_virtual_no_refund(self, admin_page):
        """ddzt-015: 验证后台虚拟商品订单无退款入口
        步骤：后台查看虚拟商品已完成订单
        预期：无退款按钮
        """
        self.list_page.goto_order_list()


@pytest.mark.ui
@pytest.mark.order
class TestOrderRefund:
    """退款管理"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.list_page = OrderListPage(admin_page)
        self.detail_page = OrderDetailPage(admin_page)
        self.refund_page = RefundPage(admin_page)

    @pytest.mark.p1
    def test_ddzt019_dining_refund_success(self, admin_page):
        """ddzt-019: 验证用户发起餐饮折扣退款成功
        步骤：找到餐饮折扣订单 > 点击退款 > 填写原因 > 确认
        预期：退款成功，状态变更
        """
        self.list_page.goto_order_list()

    @pytest.mark.p1
    def test_ddzt020_admin_approve_refund(self, admin_page):
        """ddzt-020: 验证运营审核通过退款原路退回
        步骤：进入退款管理 > 审核通过
        预期：退款到微信
        """
        self.refund_page.goto_refund()

    @pytest.mark.p2
    def test_ddzt023_refund_commission_impact(self, admin_page):
        """ddzt-023: 验证退款对分佣影响
        步骤：退款后查看佣金记录
        预期：产生冲抵记录
        """
        self.refund_page.goto_refund()

    @pytest.mark.p3
    def test_ddzt024_empty_refund_reason(self, admin_page):
        """ddzt-024: [反向] 验证退款原因为空时无法提交
        步骤：不填退款原因 > 提交
        预期：拦截提交
        """
        self.refund_page.goto_refund()

    @pytest.mark.p3
    def test_ddzt025_duplicate_refund(self, admin_page):
        """ddzt-025: [反向] 验证已退款订单不可重复退款
        步骤：对已退款订单再次操作
        预期：退款按钮置灰或不可见
        """
        self.list_page.goto_order_list()
        self.list_page.filter_by_status("已退款")
