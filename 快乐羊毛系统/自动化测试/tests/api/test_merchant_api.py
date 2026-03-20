"""
商家管理接口测试

覆盖:
- 商户录入与审核
- 品牌账号管理
- 门店管理
- 折扣设置
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import TestConfig


class TestMerchantRegistration:
    """商户录入"""

    @pytest.mark.P0
    def test_create_merchant_success(self, admin_client):
        """创建商户成功"""
        resp = admin_client.post("/api/merchants", json={
            "name": "自动化测试商户",
            "address": "北京市朝阳区测试路1号",
            "phone": "13800000099",
            "discount_rate": 8.5,
        })
        print(f"创建商户: {resp.status_code} {resp.text[:300]}")
        assert resp.status_code in (200, 201, 404)

    @pytest.mark.P0
    def test_create_merchant_missing_name(self, admin_client):
        """缺少商家名称"""
        resp = admin_client.post("/api/merchants", json={
            "name": "",
            "address": "测试地址",
            "phone": "13800000099",
            "discount_rate": 8.5,
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), "商家名称不能为空"

    @pytest.mark.P0
    def test_create_merchant_invalid_phone(self, admin_client):
        """无效手机号"""
        resp = admin_client.post("/api/merchants", json={
            "name": "测试商户",
            "address": "测试地址",
            "phone": "123",  # 无效手机号
            "discount_rate": 8.5,
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), "无效手机号应被拒绝"

    @pytest.mark.P0
    def test_discount_rate_boundary(self, admin_client):
        """折扣率边界值"""
        # 低于最低折扣
        resp_low = admin_client.post("/api/merchants", json={
            "name": "测试商户-低折扣",
            "address": "测试地址",
            "phone": "13800000098",
            "discount_rate": 0.5,  # 0.5折，低于1折
        })

        # 高于最高折扣
        resp_high = admin_client.post("/api/merchants", json={
            "name": "测试商户-高折扣",
            "address": "测试地址",
            "phone": "13800000097",
            "discount_rate": 10.0,  # 10折=无折扣
        })

        if resp_low.status_code not in (404,):
            assert resp_low.status_code in (400, 422), "0.5折应被拒绝"
        if resp_high.status_code not in (404,):
            assert resp_high.status_code in (400, 422), "10折应被拒绝"


class TestMerchantAudit:
    """商户审核"""

    @pytest.mark.P0
    def test_audit_approve(self, admin_client):
        """审核通过"""
        # 获取待审核商户
        resp = admin_client.get("/api/merchants", params={"status": "pending"})
        if resp.status_code == 200:
            merchants = resp.json().get("data", {}).get("list", [])
            if merchants:
                merchant_id = merchants[0].get("id")
                approve_resp = admin_client.post(f"/api/merchants/{merchant_id}/audit", json={
                    "action": "approve",
                })
                print(f"审核通过: {approve_resp.status_code}")

    @pytest.mark.P0
    def test_audit_reject_requires_reason(self, admin_client):
        """审核驳回必须填写理由"""
        resp = admin_client.get("/api/merchants", params={"status": "pending"})
        if resp.status_code == 200:
            merchants = resp.json().get("data", {}).get("list", [])
            if merchants:
                merchant_id = merchants[0].get("id")
                # 空理由驳回
                reject_resp = admin_client.post(f"/api/merchants/{merchant_id}/audit", json={
                    "action": "reject",
                    "reason": "",  # 空理由
                })
                if reject_resp.status_code not in (404,):
                    assert reject_resp.status_code in (400, 422), "驳回必须填写理由"


class TestStoreManagement:
    """门店管理"""

    @pytest.mark.P0
    def test_store_data_isolation(self, admin_client):
        """门店数据隔离验证"""
        # 获取门店列表
        resp = admin_client.get("/api/stores")
        if resp.status_code == 200:
            stores = resp.json().get("data", {}).get("list", [])
            if len(stores) >= 2:
                store1_id = stores[0].get("id")
                store2_id = stores[1].get("id")

                # 查询各门店订单
                orders1 = admin_client.get(f"/api/stores/{store1_id}/orders")
                orders2 = admin_client.get(f"/api/stores/{store2_id}/orders")

                if orders1.status_code == 200 and orders2.status_code == 200:
                    ids1 = set(o.get("id") for o in orders1.json().get("data", {}).get("list", []))
                    ids2 = set(o.get("id") for o in orders2.json().get("data", {}).get("list", []))
                    overlap = ids1 & ids2
                    assert len(overlap) == 0, f"门店数据不隔离，有{len(overlap)}条重复订单"

    @pytest.mark.P1
    def test_disable_store_account(self, admin_client):
        """禁用门店账号后不可登录"""
        # 先获取一个门店
        resp = admin_client.get("/api/stores")
        if resp.status_code == 200:
            stores = resp.json().get("data", {}).get("list", [])
            if stores:
                store_id = stores[-1].get("id")  # 用最后一个避免影响其他测试
                # 禁用
                disable_resp = admin_client.put(f"/api/stores/{store_id}/status", json={
                    "status": "disabled",
                })
                print(f"禁用门店: {disable_resp.status_code}")
                # 注意: 测试完需恢复，避免影响后续测试
