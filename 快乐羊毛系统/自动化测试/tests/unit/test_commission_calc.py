"""
分佣计算精确性测试

本模块验证分佣计算逻辑的正确性，无需网络环境即可运行。
覆盖: 基础分佣、一级分销、二级分销、CPS导入、退款冲抵、比例校验。
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from utils.commission_calculator import (
    calc_commission,
    calc_commission_cps,
    calc_profit,
    round_to_cent,
    validate_commission_ratios,
)
from utils.test_data import (
    COMMISSION_BASIC_CASES,
    COMMISSION_LEVEL1_CASES,
    COMMISSION_LEVEL2_CASES,
    RATIO_VALIDATION_CASES,
)


# ============================================================
# 一、基础分佣测试（无分销员）
# ============================================================
class TestBasicCommission:
    """基础分佣: 平台 + 代理商"""

    @pytest.mark.P0
    @pytest.mark.commission
    @pytest.mark.parametrize("case", COMMISSION_BASIC_CASES, ids=[c["id"] for c in COMMISSION_BASIC_CASES])
    def test_basic_commission(self, case):
        """参数化测试: 基础分佣各种场景"""
        result = calc_commission(
            paid_amount=case["paid"],
            cost=case["cost"],
            platform_ratio=case["platform_ratio"],
            agent_ratio=case["agent_ratio"],
        )

        assert result["profit"] == case["expected_profit"], (
            f"[{case['id']}] {case['desc']} - 利润计算错误: "
            f"期望 {case['expected_profit']}, 实际 {result['profit']}"
        )
        assert result["platform_commission"] == case["expected_platform"], (
            f"[{case['id']}] {case['desc']} - 平台佣金错误: "
            f"期望 {case['expected_platform']}, 实际 {result['platform_commission']}"
        )
        assert result["agent_actual"] == case["expected_agent"], (
            f"[{case['id']}] {case['desc']} - 代理商佣金错误: "
            f"期望 {case['expected_agent']}, 实际 {result['agent_actual']}"
        )

    @pytest.mark.P0
    @pytest.mark.commission
    def test_profit_non_negative(self):
        """利润不应为负数"""
        profit = calc_profit(paid_amount=50, cost=100)
        assert profit >= 0, "利润不应为负数"

    @pytest.mark.P0
    @pytest.mark.commission
    def test_commission_sum_equals_profit(self):
        """验证: 平台佣金 + 代理商实得 = 利润（无分销员时）"""
        result = calc_commission(
            paid_amount=100, cost=60,
            platform_ratio=50, agent_ratio=50,
        )
        total = round_to_cent(result["platform_commission"] + result["agent_actual"])
        assert total == result["profit"], (
            f"分佣总和 {total} != 利润 {result['profit']}"
        )

    @pytest.mark.P0
    @pytest.mark.commission
    def test_zero_profit_zero_commission(self):
        """利润为0时所有佣金为0"""
        result = calc_commission(
            paid_amount=60, cost=60,
            platform_ratio=50, agent_ratio=50,
            level1_ratio=10, level2_ratio=5,
        )
        assert result["profit"] == 0
        assert result["platform_commission"] == 0
        assert result["agent_actual"] == 0
        assert result["level1_commission"] == 0
        assert result["level2_commission"] == 0


# ============================================================
# 二、一级分销员分佣测试
# ============================================================
class TestLevel1Commission:
    """一级分销员参与分佣"""

    @pytest.mark.P0
    @pytest.mark.commission
    @pytest.mark.parametrize("case", COMMISSION_LEVEL1_CASES, ids=[c["id"] for c in COMMISSION_LEVEL1_CASES])
    def test_level1_commission(self, case):
        """参数化测试: 一级分销各种场景"""
        result = calc_commission(
            paid_amount=case["paid"],
            cost=case["cost"],
            platform_ratio=case["platform_ratio"],
            agent_ratio=case["agent_ratio"],
            level1_ratio=case["level1_ratio"],
        )

        assert result["platform_commission"] == case["expected_platform"], (
            f"[{case['id']}] 平台佣金: 期望 {case['expected_platform']}, 实际 {result['platform_commission']}"
        )
        assert result["level1_commission"] == case["expected_level1"], (
            f"[{case['id']}] 一级佣金: 期望 {case['expected_level1']}, 实际 {result['level1_commission']}"
        )
        assert result["agent_actual"] == case["expected_agent_actual"], (
            f"[{case['id']}] 代理商实得: 期望 {case['expected_agent_actual']}, 实际 {result['agent_actual']}"
        )

    @pytest.mark.P0
    @pytest.mark.commission
    def test_level1_deducted_from_agent(self):
        """验证: 一级分销员佣金从代理商份额中扣除"""
        result = calc_commission(
            paid_amount=100, cost=60,
            platform_ratio=50, agent_ratio=50,
            level1_ratio=10,
        )
        # 代理商实得 = 代理商总份额 - 一级佣金
        expected_agent = round_to_cent(result["agent_total"] - result["level1_commission"])
        assert result["agent_actual"] == expected_agent

    @pytest.mark.P0
    @pytest.mark.commission
    def test_level1_takes_all_agent_share(self):
        """分销员比例等于代理商比例时，代理商实得为0"""
        result = calc_commission(
            paid_amount=100, cost=60,
            platform_ratio=50, agent_ratio=50,
            level1_ratio=50,
        )
        assert result["agent_actual"] == 0.00
        assert result["level1_commission"] == 20.00


# ============================================================
# 三、二级分销员分佣测试
# ============================================================
class TestLevel2Commission:
    """一级+二级分销员参与分佣"""

    @pytest.mark.P0
    @pytest.mark.commission
    @pytest.mark.parametrize("case", COMMISSION_LEVEL2_CASES, ids=[c["id"] for c in COMMISSION_LEVEL2_CASES])
    def test_level2_commission(self, case):
        """参数化测试: 二级分销各种场景"""
        result = calc_commission(
            paid_amount=case["paid"],
            cost=case["cost"],
            platform_ratio=case["platform_ratio"],
            agent_ratio=case["agent_ratio"],
            level1_ratio=case["level1_ratio"],
            level2_ratio=case["level2_ratio"],
        )

        assert result["platform_commission"] == case["expected_platform"]
        assert result["level1_commission"] == case["expected_level1"]
        assert result["level2_commission"] == case["expected_level2"]
        assert result["agent_actual"] == case["expected_agent_actual"]

    @pytest.mark.P0
    @pytest.mark.commission
    def test_all_parties_sum_equals_profit(self):
        """验证: 平台 + 代理商实得 + 一级 + 二级 = 利润"""
        result = calc_commission(
            paid_amount=100, cost=60,
            platform_ratio=50, agent_ratio=50,
            level1_ratio=10, level2_ratio=5,
        )
        total = round_to_cent(
            result["platform_commission"]
            + result["agent_actual"]
            + result["level1_commission"]
            + result["level2_commission"]
        )
        assert total == result["profit"], (
            f"分佣总和 {total} != 利润 {result['profit']}\n"
            f"平台={result['platform_commission']}, 代理商={result['agent_actual']}, "
            f"一级={result['level1_commission']}, 二级={result['level2_commission']}"
        )

    @pytest.mark.P0
    @pytest.mark.commission
    def test_both_distributors_from_agent(self):
        """一级+二级都从代理商扣除"""
        result = calc_commission(
            paid_amount=100, cost=60,
            platform_ratio=50, agent_ratio=50,
            level1_ratio=10, level2_ratio=5,
        )
        expected_agent = round_to_cent(
            result["agent_total"] - result["level1_commission"] - result["level2_commission"]
        )
        assert result["agent_actual"] == expected_agent


# ============================================================
# 四、CPS导入分佣测试
# ============================================================
class TestCPSCommission:
    """CPS跳转类: Excel导入佣金直接分配，不扣成本"""

    @pytest.mark.P0
    @pytest.mark.commission
    def test_cps_no_cost_deduction(self):
        """CPS佣金不扣成本，直接按比例分"""
        result = calc_commission_cps(
            imported_commission=10.00,
            platform_ratio=50, agent_ratio=50,
        )
        assert result["profit"] == 10.00
        assert result["platform_commission"] == 5.00
        assert result["agent_actual"] == 5.00

    @pytest.mark.P0
    @pytest.mark.commission
    def test_cps_with_distributors(self):
        """CPS佣金含分销员"""
        result = calc_commission_cps(
            imported_commission=100.00,
            platform_ratio=50, agent_ratio=50,
            level1_ratio=10, level2_ratio=5,
        )
        assert result["platform_commission"] == 50.00
        assert result["level1_commission"] == 10.00
        assert result["level2_commission"] == 5.00
        assert result["agent_actual"] == 35.00  # 50 - 10 - 5

    @pytest.mark.P1
    @pytest.mark.commission
    def test_cps_small_commission(self):
        """CPS极小佣金"""
        result = calc_commission_cps(
            imported_commission=0.01,
            platform_ratio=50, agent_ratio=50,
        )
        assert result["platform_commission"] >= 0
        assert result["agent_actual"] >= 0


# ============================================================
# 五、分佣比例校验测试
# ============================================================
class TestRatioValidation:
    """分佣比例合法性校验"""

    @pytest.mark.P0
    @pytest.mark.commission
    @pytest.mark.parametrize(
        "platform, agent, l1, l2, valid, desc",
        RATIO_VALIDATION_CASES,
        ids=[c[5] for c in RATIO_VALIDATION_CASES],
    )
    def test_ratio_validation(self, platform, agent, l1, l2, valid, desc):
        """参数化测试: 分佣比例校验"""
        result = validate_commission_ratios(platform, agent, l1, l2)
        assert result["valid"] == valid, (
            f"[{desc}] 比例({platform}/{agent}/{l1}/{l2}) "
            f"期望 {'合法' if valid else '非法'}, 实际 {'合法' if result['valid'] else '非法'}"
            f" 错误: {result['errors']}"
        )

    @pytest.mark.P0
    @pytest.mark.commission
    def test_platform_plus_agent_must_equal_100(self):
        """平台+代理商必须=100%"""
        result = validate_commission_ratios(60, 30)
        assert not result["valid"]
        assert any("100%" in e for e in result["errors"])

    @pytest.mark.P0
    @pytest.mark.commission
    def test_distributor_cannot_exceed_agent(self):
        """分销员比例不能超过代理商"""
        result = validate_commission_ratios(50, 50, 30, 25)
        assert not result["valid"]
        assert any("不能超过" in e for e in result["errors"])

    @pytest.mark.P0
    @pytest.mark.commission
    def test_negative_ratio_rejected(self):
        """负数比例被拒绝"""
        result = validate_commission_ratios(-10, 110)
        assert not result["valid"]


# ============================================================
# 六、四舍五入精度测试
# ============================================================
class TestRoundingPrecision:
    """金额四舍五入精度"""

    @pytest.mark.P0
    @pytest.mark.commission
    @pytest.mark.parametrize("value, expected", [
        (19.995, 20.00),
        (19.994, 19.99),
        (0.005, 0.01),    # 五入
        (0.004, 0.00),
        (99.999, 100.00),
        (0.001, 0.00),
        (1.555, 1.56),
        (1.545, 1.55),    # 注意: banker's rounding vs half-up
    ])
    def test_round_to_cent(self, value, expected):
        """四舍五入到分"""
        result = round_to_cent(value)
        assert result == expected, f"round_to_cent({value}): 期望 {expected}, 实际 {result}"

    @pytest.mark.P1
    @pytest.mark.commission
    def test_rounding_does_not_create_money(self):
        """四舍五入不应凭空产生金额（各方之和不超过利润）"""
        # 利润39.99，50/50分配
        # 39.99 * 0.5 = 19.995 -> 20.00 (四舍五入)
        # 20.00 + 20.00 = 40.00 > 39.99 (超出!)
        result = calc_commission(
            paid_amount=99.99, cost=60.00,
            platform_ratio=50, agent_ratio=50,
        )
        total = result["platform_commission"] + result["agent_actual"]
        # 记录此场景，系统应有尾差处理策略
        print(f"利润={result['profit']}, 分佣合计={total}, 差额={total - result['profit']}")
        # 差额不应超过1分钱
        assert abs(total - result["profit"]) <= 0.01, (
            f"尾差超过1分钱: 利润={result['profit']}, 分佣合计={total}"
        )


# ============================================================
# 七、批量数据压力验证
# ============================================================
class TestBatchCommission:
    """批量分佣计算正确性"""

    @pytest.mark.P1
    @pytest.mark.commission
    def test_1000_orders_commission(self):
        """1000笔订单的分佣计算全部正确"""
        import random
        errors = []

        for i in range(1000):
            paid = round_to_cent(random.uniform(0.01, 50000))
            cost = round_to_cent(random.uniform(0, paid))
            profit = calc_profit(paid, cost)

            result = calc_commission(
                paid_amount=paid, cost=cost,
                platform_ratio=50, agent_ratio=50,
                level1_ratio=10, level2_ratio=5,
            )

            total = round_to_cent(
                result["platform_commission"]
                + result["agent_actual"]
                + result["level1_commission"]
                + result["level2_commission"]
            )

            # 允许1分钱尾差
            if abs(total - profit) > 0.01:
                errors.append(
                    f"订单{i}: paid={paid}, cost={cost}, profit={profit}, total={total}"
                )

        assert len(errors) == 0, f"有 {len(errors)} 笔订单分佣总和偏差超过1分钱:\n" + "\n".join(errors[:10])
