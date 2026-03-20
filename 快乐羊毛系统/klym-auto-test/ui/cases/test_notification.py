"""
UI 测试 - 消息通知
对应用例编号：xxtz-001 ~ xxtz-012

功能：订阅消息、短信通知、通知内容验证
"""
import pytest
from ui.pages.base_page import BasePage


@pytest.mark.ui
@pytest.mark.p1
class TestNotification:
    """消息通知验证（后台侧）"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = BasePage(admin_page)

    def test_xxtz001_order_success_notification(self, admin_page):
        """xxtz-001: 验证下单成功发送订阅消息
        预期：用户端收到下单成功通知
        """
        pytest.skip("需要配合用户端小程序验证")

    def test_xxtz002_refund_notification(self, admin_page):
        """xxtz-002: 验证退款成功发送订阅消息
        预期：用户收到退款通知
        """
        pytest.skip("需要配合用户端小程序验证")

    def test_xxtz010_refund_success_notify(self, admin_page):
        """xxtz-010: 退款成功知通
        步骤：后台执行退款后检查通知记录
        """
        pytest.skip("需要查看消息推送日志")

    def test_xxtz012_captcha_delivery_notify(self, admin_page):
        """xxtz-012: 餐饮验证码下发通知
        步骤：审核通过人工辅助订单后
        预期：验证码通过订阅消息/短信推送给用户
        """
        pytest.skip("需要配合用户端验证")
