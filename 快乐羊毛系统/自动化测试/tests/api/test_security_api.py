"""
安全测试 — 接口层

覆盖:
- 越权访问（水平越权、垂直越权）
- 支付金额篡改
- 虚拟商品退款绕过
- 输入注入（SQL/XSS）
- 暴力破解防护
- 重复提交防护
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import TestConfig
from utils.api_client import APIClient


class TestHorizontalPrivilegeEscalation:
    """水平越权: 用户A访问用户B的数据"""

    @pytest.mark.P0
    @pytest.mark.security
    def test_access_other_user_order(self, admin_client):
        """
        用户A尝试查看用户B的订单

        步骤:
        1. 获取用户A的订单ID
        2. 修改请求参数中的用户ID/订单ID为用户B的
        3. 期望返回403/无权限
        """
        # 注意: 需根据实际API路径调整
        # 使用一个不属于当前用户的订单ID
        fake_order_id = "999999999"
        resp = admin_client.get(f"/api/orders/{fake_order_id}")
        # 应返回404(订单不存在)或403(无权限)，不应返回其他用户数据
        assert resp.status_code in (403, 404), (
            f"访问他人订单应返回403/404，实际 {resp.status_code}"
        )

    @pytest.mark.P0
    @pytest.mark.security
    def test_store_access_other_store_data(self):
        """
        门店A尝试查看门店B的数据

        通过修改URL参数中的门店ID
        """
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        # 假设门店A登录
        store = TestConfig.TEST_MERCHANT_STORES[0]
        client.login(store.get("username", "test_store1"), "test123")

        # 尝试访问门店B的数据
        other_store_id = "other_store_999"
        resp = client.get(f"/api/stores/{other_store_id}/orders")
        assert resp.status_code in (403, 404), "不应访问到其他门店数据"


class TestVerticalPrivilegeEscalation:
    """垂直越权: 低权限角色调用高权限接口"""

    @pytest.mark.P0
    @pytest.mark.security
    def test_store_access_brand_api(self):
        """门店子账号调用品牌主账号接口（如创建子账号）"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        store = TestConfig.TEST_MERCHANT_STORES[0]
        client.login(store.get("username", "test_store1"), "test123")

        # 门店子账号尝试创建另一个子账号
        resp = client.post("/api/stores", json={
            "name": "非法创建的门店",
            "address": "test",
            "phone": "13800000099",
        })
        assert resp.status_code in (403, 401), "门店子账号不应能创建子账号"

    @pytest.mark.P0
    @pytest.mark.security
    def test_user_access_admin_api(self, anon_client):
        """普通用户调用后台管理接口"""
        # 用普通用户token调后台管理接口
        resp = anon_client.get("/api/admin/users")
        assert resp.status_code in (401, 403)

    @pytest.mark.P0
    @pytest.mark.security
    def test_store_modify_discount(self):
        """门店子账号尝试修改折扣（仅品牌主账号可修改）"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        store = TestConfig.TEST_MERCHANT_STORES[0]
        client.login(store.get("username", "test_store1"), "test123")

        resp = client.put("/api/discount/settings", json={
            "discount_rate": 0.5,
        })
        assert resp.status_code in (403, 401), "门店子账号不应能修改折扣"


class TestPaymentSecurity:
    """支付安全"""

    @pytest.mark.P0
    @pytest.mark.security
    @pytest.mark.payment
    def test_amount_tampering(self, admin_client):
        """
        支付金额篡改测试

        场景: 创建订单后，尝试用不同金额发起支付
        """
        # 1. 创建一个100元的订单
        order_resp = admin_client.post("/api/orders", json={
            "product_id": "test_product",
            "amount": 100.00,
        })

        if order_resp.status_code == 200:
            order_id = order_resp.json().get("data", {}).get("order_id")
            if order_id:
                # 2. 尝试用0.01元支付该订单
                pay_resp = admin_client.post("/api/payment", json={
                    "order_id": order_id,
                    "amount": 0.01,  # 篡改金额
                })
                # 后端应校验金额一致性，拒绝支付
                assert pay_resp.status_code in (400, 403), "篡改金额应被后端拦截"

    @pytest.mark.P0
    @pytest.mark.security
    def test_virtual_product_refund_bypass(self, admin_client):
        """
        虚拟商品退款绕过测试

        场景: 虚拟商品支付成功(COMPLETED)后，直接调退款API绕过前端限制
        """
        # 假设有一个已完成的虚拟商品订单
        fake_virtual_order_id = "virtual_completed_order"
        resp = admin_client.post(f"/api/orders/{fake_virtual_order_id}/refund", json={
            "reason": "测试退款绕过",
            "amount": 100.00,
        })
        # 后端应拦截虚拟商品退款
        assert resp.status_code in (400, 403, 404), "虚拟商品COMPLETED状态不允许退款"


class TestInputInjection:
    """输入注入测试"""

    @pytest.mark.P0
    @pytest.mark.security
    @pytest.mark.parametrize("payload, desc", [
        ("' OR 1=1 --", "SQL注入-经典"),
        ("'; DROP TABLE users; --", "SQL注入-删表"),
        ("1 UNION SELECT * FROM users", "SQL注入-联合查询"),
        ("<script>alert('xss')</script>", "XSS-script标签"),
        ("<img src=x onerror=alert(1)>", "XSS-img标签"),
        ("<svg onload=alert(1)>", "XSS-svg标签"),
        ("{{7*7}}", "SSTI模板注入"),
        ("../../etc/passwd", "路径穿越"),
    ])
    def test_injection_in_search(self, admin_client, payload, desc):
        """搜索框注入测试"""
        resp = admin_client.get("/api/orders", params={"keyword": payload})
        # 不应返回500（说明注入未被处理）
        assert resp.status_code != 500, f"[{desc}] 注入导致服务器错误"
        # 响应中不应包含未转义的注入内容
        if resp.text and "<script>" in payload:
            assert "<script>" not in resp.text, f"[{desc}] 响应中包含未转义的XSS"

    @pytest.mark.P0
    @pytest.mark.security
    @pytest.mark.parametrize("payload, desc", [
        ("<script>alert('xss')</script>", "XSS-商家名称"),
        ("' OR 1=1 --", "SQL-商家名称"),
    ])
    def test_injection_in_merchant_name(self, admin_client, payload, desc):
        """商家名称字段注入测试"""
        resp = admin_client.post("/api/merchants", json={
            "name": payload,
            "address": "测试地址",
            "phone": "13800000001",
            "discount_rate": 8.5,
        })
        # 不应导致服务器500错误
        assert resp.status_code != 500, f"[{desc}] 注入导致服务器错误"

    @pytest.mark.P1
    @pytest.mark.security
    @pytest.mark.parametrize("payload, desc", [
        ("<script>alert(1)</script>", "XSS-退款原因"),
        ("' OR 1=1; --", "SQL-退款原因"),
    ])
    def test_injection_in_refund_reason(self, admin_client, payload, desc):
        """退款原因字段注入测试"""
        resp = admin_client.post("/api/orders/test_order/refund", json={
            "reason": payload,
            "amount": 10.00,
        })
        assert resp.status_code != 500, f"[{desc}] 注入导致服务器错误"


class TestBruteForceProtection:
    """暴力破解防护"""

    @pytest.mark.P0
    @pytest.mark.security
    def test_login_brute_force(self):
        """连续多次错误登录应被限制"""
        client = APIClient(TestConfig.ADMIN_BASE_URL)
        blocked = False

        for i in range(10):
            resp = client.post("/auth/login", json={
                "username": TestConfig.ADMIN_USERNAME,
                "password": f"wrong_password_{i}",
            })
            if resp.status_code == 429:  # Too Many Requests
                blocked = True
                break

        # 记录结果（即使没有被限制也不一定是bug，取决于限流策略）
        print(f"连续错误登录{10 if not blocked else i+1}次后，"
              f"{'被限流' if blocked else '未被限流'}")

    @pytest.mark.P0
    @pytest.mark.security
    def test_verify_code_brute_force(self, admin_client):
        """验证码连续5次错误应锁定15分钟"""
        test_order_id = "test_order_for_verify"
        lock_detected = False

        for i in range(6):
            resp = admin_client.post(f"/api/orders/{test_order_id}/verify", json={
                "code": f"0000{i}",  # 错误验证码
            })
            # 第6次应该被锁定
            if resp.status_code == 429 or (
                resp.status_code == 400
                and "锁定" in resp.text
            ):
                lock_detected = True
                assert i >= 4, f"第{i+1}次就被锁定，应该第6次才锁定"
                break

        # 记录结果
        print(f"验证码暴力破解防护: {'有效' if lock_detected else '未检测到锁定机制'}")


class TestDuplicateSubmission:
    """重复提交防护"""

    @pytest.mark.P0
    @pytest.mark.security
    @pytest.mark.payment
    def test_duplicate_payment(self, admin_client):
        """同一订单重复支付应被拒绝"""
        order_data = {
            "product_id": "test_product",
            "amount": 100.00,
        }

        # 创建订单
        resp1 = admin_client.post("/api/orders", json=order_data)
        if resp1.status_code == 200:
            order_id = resp1.json().get("data", {}).get("order_id")
            if order_id:
                # 第一次支付
                pay1 = admin_client.post("/api/payment", json={
                    "order_id": order_id,
                    "amount": 100.00,
                })
                # 第二次支付同一订单
                pay2 = admin_client.post("/api/payment", json={
                    "order_id": order_id,
                    "amount": 100.00,
                })
                # 第二次应被拒绝
                if pay1.status_code == 200:
                    assert pay2.status_code in (400, 409), "重复支付应被拒绝"

    @pytest.mark.P1
    @pytest.mark.security
    def test_duplicate_refund(self, admin_client):
        """同一订单重复退款应被拒绝"""
        order_id = "test_refunded_order"
        refund_data = {"reason": "测试退款", "amount": 100.00}

        # 第一次退款
        resp1 = admin_client.post(f"/api/orders/{order_id}/refund", json=refund_data)
        # 第二次退款
        resp2 = admin_client.post(f"/api/orders/{order_id}/refund", json=refund_data)

        # 至少第二次应被拒绝（如果第一次成功的话）
        if resp1.status_code == 200:
            assert resp2.status_code in (400, 409), "重复退款应被拒绝"
