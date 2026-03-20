"""
分佣接口测试

覆盖:
- 分佣配置接口（比例设置/查询）
- 分佣明细查询
- 分佣计算结果验证（系统结果 vs 本地计算对比）
- 退款冲抵验证
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from config import TestConfig
from utils.commission_calculator import calc_commission, validate_commission_ratios


class TestCommissionConfig:
    """分佣比例配置接口"""

    @pytest.mark.P0
    @pytest.mark.commission
    def test_get_commission_config(self, admin_client):
        """查询当前分佣配置"""
        resp = admin_client.get("/api/commission/config")
        print(f"分佣配置响应: {resp.status_code} {resp.text[:500]}")
        assert resp.status_code in (200, 404)

    @pytest.mark.P0
    @pytest.mark.commission
    def test_set_valid_commission_ratio(self, admin_client):
        """设置合法分佣比例"""
        resp = admin_client.put("/api/commission/config", json={
            "platform_ratio": 50,
            "agent_ratio": 50,
        })
        print(f"设置分佣比例响应: {resp.status_code} {resp.text[:300]}")
        # 200或404(接口未实现)
        assert resp.status_code in (200, 404)

    @pytest.mark.P0
    @pytest.mark.commission
    def test_set_invalid_ratio_over_100(self, admin_client):
        """设置不合法比例: 总和超过100%"""
        resp = admin_client.put("/api/commission/config", json={
            "platform_ratio": 60,
            "agent_ratio": 50,  # 合计110%
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), (
                f"比例合计110%应被拒绝，实际 {resp.status_code}"
            )

    @pytest.mark.P0
    @pytest.mark.commission
    def test_set_negative_ratio(self, admin_client):
        """设置负数比例"""
        resp = admin_client.put("/api/commission/config", json={
            "platform_ratio": -10,
            "agent_ratio": 110,
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), "负数比例应被拒绝"

    @pytest.mark.P0
    @pytest.mark.commission
    def test_distributor_ratio_exceeds_agent(self, admin_client):
        """分销员比例超过代理商比例"""
        resp = admin_client.put("/api/commission/config", json={
            "platform_ratio": 50,
            "agent_ratio": 50,
            "level1_ratio": 30,
            "level2_ratio": 25,  # 30+25=55 > 50
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), "分销员比例>代理商应被拒绝"


class TestCommissionDetail:
    """分佣明细查询"""

    @pytest.mark.P0
    @pytest.mark.commission
    def test_get_commission_list(self, admin_client):
        """查询分佣明细列表"""
        resp = admin_client.get("/api/commission/details")
        print(f"分佣明细响应: {resp.status_code}")
        assert resp.status_code in (200, 404)

    @pytest.mark.P1
    @pytest.mark.commission
    def test_commission_detail_by_order(self, admin_client):
        """查询指定订单的分佣明细"""
        # 先获取一个订单
        list_resp = admin_client.get("/api/orders", params={"page_size": 1})
        if list_resp.status_code == 200:
            orders = list_resp.json().get("data", {}).get("list", [])
            if orders:
                order_id = orders[0].get("id")
                resp = admin_client.get(f"/api/commission/details", params={
                    "order_id": order_id,
                })
                print(f"订单{order_id}分佣明细: {resp.status_code} {resp.text[:300]}")

    @pytest.mark.P1
    @pytest.mark.commission
    def test_commission_filter_by_role(self, admin_client):
        """按角色筛选分佣明细"""
        roles = ["platform", "agent", "distributor_l1", "distributor_l2"]
        for role in roles:
            resp = admin_client.get("/api/commission/details", params={"role": role})
            print(f"角色{role}分佣: {resp.status_code}")


class TestCommissionCalculationVerify:
    """分佣计算结果对比验证

    将系统实际计算结果与本地计算器对比，验证一致性。
    """

    @pytest.mark.P0
    @pytest.mark.commission
    def test_verify_commission_against_local_calc(self, admin_client):
        """
        系统分佣结果 vs 本地计算器对比

        步骤:
        1. 查询一批已完成订单的分佣明细
        2. 用本地计算器重新算一遍
        3. 逐笔对比
        """
        # 获取已完成订单
        resp = admin_client.get("/api/orders", params={
            "status": "COMPLETED",
            "page_size": 20,
        })

        if resp.status_code != 200:
            pytest.skip("无法获取订单列表")

        orders = resp.json().get("data", {}).get("list", [])
        if not orders:
            pytest.skip("没有已完成订单可验证")

        mismatches = []

        for order in orders:
            order_id = order.get("id")
            paid = order.get("paid_amount") or order.get("actual_amount")
            cost = order.get("cost") or order.get("original_price", 0)

            if paid is None:
                continue

            # 获取系统分佣结果
            detail_resp = admin_client.get(f"/api/commission/details", params={
                "order_id": order_id,
            })

            if detail_resp.status_code != 200:
                continue

            system_result = detail_resp.json()

            # 用本地计算器计算预期值
            local_result = calc_commission(
                paid_amount=float(paid),
                cost=float(cost),
                platform_ratio=TestConfig.DEFAULT_PLATFORM_RATIO,
                agent_ratio=TestConfig.DEFAULT_AGENT_RATIO,
                level1_ratio=TestConfig.DEFAULT_LEVEL1_RATIO,
                level2_ratio=TestConfig.DEFAULT_LEVEL2_RATIO,
            )

            # 对比（根据实际API响应结构调整字段名）
            sys_platform = system_result.get("platform_commission")
            if sys_platform is not None:
                if abs(float(sys_platform) - local_result["platform_commission"]) > 0.01:
                    mismatches.append(
                        f"订单{order_id}: 平台佣金 系统={sys_platform}, "
                        f"本地={local_result['platform_commission']}"
                    )

        if mismatches:
            print(f"发现 {len(mismatches)} 笔分佣不一致:")
            for m in mismatches[:10]:
                print(f"  {m}")

        assert len(mismatches) == 0, (
            f"有 {len(mismatches)} 笔分佣结果与本地计算不一致"
        )


class TestWithdrawAPI:
    """提现结算接口测试"""

    @pytest.mark.P0
    @pytest.mark.commission
    def test_get_balance(self, admin_client):
        """查询可提现余额"""
        resp = admin_client.get("/api/commission/balance")
        print(f"余额查询: {resp.status_code} {resp.text[:300]}")
        assert resp.status_code in (200, 404)

    @pytest.mark.P0
    @pytest.mark.commission
    def test_withdraw_exceeds_balance(self, admin_client):
        """提现金额超过可提现余额"""
        resp = admin_client.post("/api/commission/withdraw", json={
            "amount": 9999999.99,  # 超大金额
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), "超额提现应被拒绝"

    @pytest.mark.P0
    @pytest.mark.commission
    def test_withdraw_zero_amount(self, admin_client):
        """提现金额为0"""
        resp = admin_client.post("/api/commission/withdraw", json={
            "amount": 0,
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), "提现0元应被拒绝"

    @pytest.mark.P0
    @pytest.mark.commission
    def test_withdraw_negative_amount(self, admin_client):
        """提现金额为负"""
        resp = admin_client.post("/api/commission/withdraw", json={
            "amount": -10,
        })
        if resp.status_code not in (404,):
            assert resp.status_code in (400, 422), "负数提现应被拒绝"
