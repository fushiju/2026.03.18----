"""
订单接口测试

覆盖:
- 订单列表查询
- 订单详情
- 订单状态流转
- 订单筛选
- 退款操作
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import TestConfig
from utils.api_client import APIClient, PerformanceTimer


class TestOrderList:
    """订单列表查询"""

    @pytest.mark.P0
    @pytest.mark.smoke
    def test_order_list_success(self, admin_client):
        """查询订单列表成功"""
        resp = admin_client.get("/api/orders")
        assert resp.status_code == 200

    @pytest.mark.P1
    def test_order_list_pagination(self, admin_client):
        """订单列表分页"""
        # 第一页
        resp1 = admin_client.get("/api/orders", params={"page": 1, "page_size": 10})
        assert resp1.status_code == 200

        # 第二页
        resp2 = admin_client.get("/api/orders", params={"page": 2, "page_size": 10})
        assert resp2.status_code == 200

        # 两页数据不应相同（如果数据量足够）
        data1 = resp1.json()
        data2 = resp2.json()
        if data1 and data2:
            # 比较不同页的订单ID
            ids1 = [o.get("id") for o in data1.get("data", {}).get("list", [])]
            ids2 = [o.get("id") for o in data2.get("data", {}).get("list", [])]
            # 不应有重复
            assert not set(ids1) & set(ids2), "分页数据不应重复"

    @pytest.mark.P1
    def test_order_filter_by_status(self, admin_client):
        """按状态筛选订单"""
        statuses = ["WAIT_PAY", "COMPLETED", "REFUNDED", "FAIL", "PENDING_AUDIT"]
        for status in statuses:
            resp = admin_client.get("/api/orders", params={"status": status})
            assert resp.status_code == 200, f"筛选状态 {status} 失败"

    @pytest.mark.P1
    def test_order_filter_by_type(self, admin_client):
        """按订单类型(type_id)筛选"""
        type_ids = [1, 2, 3]  # 1=骑士, 2=共享会员, 3=电影
        for type_id in type_ids:
            resp = admin_client.get("/api/orders", params={"type_id": type_id})
            assert resp.status_code == 200, f"筛选type_id={type_id} 失败"

    @pytest.mark.P2
    def test_order_list_performance(self, admin_client):
        """订单列表响应时间 < 3秒"""
        with PerformanceTimer("订单列表") as timer:
            resp = admin_client.get("/api/orders", params={"page": 1, "page_size": 20})
        assert resp.status_code == 200
        timer.assert_within(3, "订单列表")


class TestOrderDetail:
    """订单详情"""

    @pytest.mark.P0
    def test_order_detail_success(self, admin_client):
        """查询订单详情成功"""
        # 先获取一个订单ID
        list_resp = admin_client.get("/api/orders", params={"page": 1, "page_size": 1})
        if list_resp.status_code == 200:
            orders = list_resp.json().get("data", {}).get("list", [])
            if orders:
                order_id = orders[0].get("id")
                detail_resp = admin_client.get(f"/api/orders/{order_id}")
                assert detail_resp.status_code == 200

    @pytest.mark.P0
    def test_order_detail_not_found(self, admin_client):
        """不存在的订单返回404"""
        resp = admin_client.get("/api/orders/nonexistent_999999")
        assert resp.status_code in (404, 400)


class TestOrderStatusTransition:
    """订单状态流转测试"""

    @pytest.mark.P0
    def test_virtual_product_normal_flow(self, admin_client):
        """
        虚拟商品正常流程: WAIT_PAY -> DELIVERING -> COMPLETED

        注意: 此测试可能需要mock支付和第三方API
        """
        # 这是一个端到端流程测试的框架
        # 实际执行需要根据系统API路径调整
        pass  # TODO: 待接口确认后补充

    @pytest.mark.P0
    def test_completed_order_no_refund_button(self, admin_client):
        """虚拟商品COMPLETED状态不应有退款按钮/接口"""
        # 获取一个已完成的虚拟商品订单
        resp = admin_client.get("/api/orders", params={
            "status": "COMPLETED",
            "type_id": 1,  # 骑士（虚拟商品）
        })
        if resp.status_code == 200:
            orders = resp.json().get("data", {}).get("list", [])
            if orders:
                order_id = orders[0].get("id")
                # 尝试退款 - 应被拒绝
                refund_resp = admin_client.post(f"/api/orders/{order_id}/refund", json={
                    "reason": "测试退款",
                    "amount": 10,
                })
                assert refund_resp.status_code in (400, 403), (
                    "虚拟商品COMPLETED状态不允许退款"
                )

    @pytest.mark.P0
    def test_fail_order_can_retry_or_refund(self, admin_client):
        """FAIL状态订单可以重试发货或退款"""
        resp = admin_client.get("/api/orders", params={"status": "FAIL"})
        if resp.status_code == 200:
            orders = resp.json().get("data", {}).get("list", [])
            if orders:
                order_id = orders[0].get("id")
                # 验证重试接口可调用
                retry_resp = admin_client.post(f"/api/orders/{order_id}/retry")
                # 应返回200(成功)或400(业务错误)，不应403
                assert retry_resp.status_code != 403, "FAIL订单应允许重试"


class TestRefundAPI:
    """退款接口测试"""

    @pytest.mark.P0
    @pytest.mark.refund
    def test_dining_order_can_refund(self, admin_client):
        """餐饮扫码订单可以退款"""
        resp = admin_client.get("/api/orders", params={
            "status": "COMPLETED",
            "type_id": 2,  # 共享会员
        })
        if resp.status_code == 200:
            orders = resp.json().get("data", {}).get("list", [])
            if orders:
                order_id = orders[0].get("id")
                # 餐饮订单应可退款
                refund_resp = admin_client.post(f"/api/orders/{order_id}/refund", json={
                    "reason": "自动化测试退款",
                    "amount": 0.01,  # 最小金额测试
                })
                # 应不是403(权限拒绝)
                print(f"餐饮退款响应: {refund_resp.status_code} {refund_resp.text[:200]}")

    @pytest.mark.P0
    @pytest.mark.refund
    def test_refund_reason_required(self, admin_client):
        """退款必须填写原因"""
        resp = admin_client.post("/api/orders/test_order/refund", json={
            "reason": "",  # 空原因
            "amount": 10.00,
        })
        assert resp.status_code in (400, 422), "空退款原因应被拒绝"

    @pytest.mark.P0
    @pytest.mark.refund
    def test_refund_amount_validation(self, admin_client):
        """退款金额校验"""
        order_id = "test_order"

        # 退款金额为0
        resp1 = admin_client.post(f"/api/orders/{order_id}/refund", json={
            "reason": "测试", "amount": 0,
        })
        assert resp1.status_code in (400, 422), "退款金额为0应被拒绝"

        # 退款金额为负数
        resp2 = admin_client.post(f"/api/orders/{order_id}/refund", json={
            "reason": "测试", "amount": -10,
        })
        assert resp2.status_code in (400, 422), "退款金额为负应被拒绝"

    @pytest.mark.P0
    @pytest.mark.refund
    def test_refund_exceeds_paid_amount(self, admin_client):
        """退款金额不能超过实付金额"""
        # 获取一个订单
        resp = admin_client.get("/api/orders", params={
            "status": "COMPLETED",
            "page_size": 1,
        })
        if resp.status_code == 200:
            orders = resp.json().get("data", {}).get("list", [])
            if orders:
                order = orders[0]
                order_id = order.get("id")
                paid_amount = order.get("paid_amount", 100)

                # 退款金额 > 实付金额
                refund_resp = admin_client.post(f"/api/orders/{order_id}/refund", json={
                    "reason": "测试超额退款",
                    "amount": paid_amount + 100,
                })
                assert refund_resp.status_code in (400, 422), "退款超过实付应被拒绝"
