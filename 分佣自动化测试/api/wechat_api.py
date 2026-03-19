"""
微信公众号/小程序接口封装
覆盖：用户下单、技师操作、分佣查询等核心接口
"""
import allure

from utils.api_client import ApiClient


class WechatOrderAPI:
    """微信端 - 用户下单相关接口"""

    PREFIX = "/massage/wechat"

    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step("用户登录获取token")
    def user_login(self, phone, sms_code="123456"):
        return self.client.post(
            f"{self.PREFIX}/User/login",
            json_data={"phone": phone, "smsCode": sms_code},
        )

    @allure.step("获取技师列表")
    def get_technician_list(self, agent_id=None, page=1, limit=10):
        params = {"page": page, "limit": limit}
        if agent_id:
            params["agentId"] = agent_id
        return self.client.get(f"{self.PREFIX}/Coach/list", params=params)

    @allure.step("获取服务项目列表")
    def get_service_list(self, tech_id):
        return self.client.get(
            f"{self.PREFIX}/Service/list", params={"coachId": tech_id}
        )

    @allure.step("创建订单")
    def create_order(self, tech_id, service_id, address, coupon_id=None,
                     card_id=None, source_type=None, source_id=None):
        """
        创建订单
        source_type: 来源类型 (distributor/broker/salesman/channel/scan)
        source_id: 来源角色ID
        """
        data = {
            "coachId": tech_id,
            "serviceId": service_id,
            "address": address,
        }
        if coupon_id:
            data["couponId"] = coupon_id
        if card_id:
            data["cardId"] = card_id
        if source_type:
            data["sourceType"] = source_type
        if source_id:
            data["sourceId"] = source_id
        return self.client.post(f"{self.PREFIX}/Order/create", json_data=data)

    @allure.step("查询订单详情")
    def get_order_detail(self, order_id):
        return self.client.get(
            f"{self.PREFIX}/Order/detail", params={"orderId": order_id}
        )

    @allure.step("查询订单分佣明细")
    def get_order_commission(self, order_id):
        return self.client.get(
            f"{self.PREFIX}/Order/commission", params={"orderId": order_id}
        )

    @allure.step("用户申请退款")
    def apply_refund(self, order_id, refund_type="service", reason="测试退款"):
        """
        refund_type: service(服务费) / travel(车费) / all(全额)
        """
        return self.client.post(
            f"{self.PREFIX}/Order/refund",
            json_data={
                "orderId": order_id,
                "refundType": refund_type,
                "reason": reason,
            },
        )

    @allure.step("用户扫渠道商二维码绑定")
    def scan_channel_qrcode(self, channel_id):
        return self.client.post(
            f"{self.PREFIX}/Channel/bindUser",
            json_data={"channelId": channel_id},
        )


class TechnicianAPI:
    """技师端操作接口"""

    PREFIX = "/massage/wechat"

    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step("技师登录")
    def login(self, phone, sms_code="123456"):
        return self.client.post(
            f"{self.PREFIX}/Coach/login",
            json_data={"phone": phone, "smsCode": sms_code},
        )

    @allure.step("技师接单")
    def accept_order(self, order_id):
        return self.client.post(
            f"{self.PREFIX}/Coach/acceptOrder",
            json_data={"orderId": order_id},
        )

    @allure.step("技师拒绝接单")
    def reject_order(self, order_id, reason="测试拒单"):
        return self.client.post(
            f"{self.PREFIX}/Coach/rejectOrder",
            json_data={"orderId": order_id, "reason": reason},
        )

    @allure.step("技师确认出发")
    def confirm_departure(self, order_id):
        return self.client.post(
            f"{self.PREFIX}/Coach/confirmDeparture",
            json_data={"orderId": order_id},
        )

    @allure.step("技师拍照到达")
    def confirm_arrival(self, order_id, photo_url="https://test.com/arrival.jpg"):
        return self.client.post(
            f"{self.PREFIX}/Coach/confirmArrival",
            json_data={"orderId": order_id, "photo": photo_url},
        )

    @allure.step("技师开始服务")
    def start_service(self, order_id):
        return self.client.post(
            f"{self.PREFIX}/Coach/startService",
            json_data={"orderId": order_id},
        )

    @allure.step("技师拍照完成服务")
    def complete_service(self, order_id, photo_url="https://test.com/complete.jpg"):
        return self.client.post(
            f"{self.PREFIX}/Coach/completeService",
            json_data={"orderId": order_id, "photo": photo_url},
        )


class AdminAPI:
    """管理后台接口"""

    PREFIX = "/massage/admin"

    def __init__(self, client: ApiClient):
        self.client = client

    @allure.step("管理员登录")
    def login(self, username=None, password=None, code_text=None):
        from config import config as cfg
        admin = cfg["admin"]
        return self.client.post(
            f"{self.PREFIX}/Admin/login",
            json_data={
                "username": username or admin["username"],
                "passwd": password or admin["password"],
                "codeText": code_text or admin["codeText"],
            },
            headers={"Cookie": f"codeText={code_text or admin['codeText']}"},
        )

    @allure.step("审核退款")
    def audit_refund(self, refund_id, status="approved"):
        return self.client.post(
            f"{self.PREFIX}/Order/auditRefund",
            json_data={"refundId": refund_id, "status": status},
        )

    @allure.step("查询订单分佣详情(管理端)")
    def get_commission_detail(self, order_id):
        return self.client.get(
            f"{self.PREFIX}/Commission/detail",
            params={"orderId": order_id},
        )
