"""
折扣计算精确性测试

验证餐饮折扣场景下的折扣计算:
- 标准折扣计算
- 小数精度
- 边界值（最小金额、最大金额、极端折扣率）
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from utils.commission_calculator import calc_discount_amount, round_to_cent
from utils.test_data import DISCOUNT_CALC_CASES


class TestDiscountCalculation:
    """折扣计算精确性"""

    @pytest.mark.P0
    @pytest.mark.parametrize("case", DISCOUNT_CALC_CASES, ids=[c["id"] for c in DISCOUNT_CALC_CASES])
    def test_discount_calculation(self, case):
        """参数化测试: 折扣计算各种场景"""
        paid, saving = calc_discount_amount(case["price"], case["rate"])

        assert paid == case["expected_paid"], (
            f"[{case['id']}] {case['desc']} - 实付金额: "
            f"期望 {case['expected_paid']}, 实际 {paid}"
        )
        assert saving == case["expected_saving"], (
            f"[{case['id']}] {case['desc']} - 优惠金额: "
            f"期望 {case['expected_saving']}, 实际 {saving}"
        )

    @pytest.mark.P0
    def test_paid_plus_saving_equals_original(self):
        """实付 + 优惠 = 原价"""
        test_cases = [
            (100.00, 0.8),
            (99.00, 0.85),
            (200.00, 0.7),
            (50000.00, 0.8),
        ]
        for price, rate in test_cases:
            paid, saving = calc_discount_amount(price, rate)
            total = round_to_cent(paid + saving)
            assert total == price, (
                f"原价{price}, {rate}折: 实付{paid} + 优惠{saving} = {total} != {price}"
            )

    @pytest.mark.P0
    def test_minimum_payment_one_cent(self):
        """折后价最低为1分钱（微信支付最低限制）"""
        paid, _ = calc_discount_amount(0.01, 0.1)
        assert paid >= 0.01, f"折后价 {paid} 低于1分钱"

    @pytest.mark.P1
    def test_discount_rate_boundary(self):
        """折扣率边界: 1折和9.9折"""
        # 1折（最大折扣）
        paid_min, saving_min = calc_discount_amount(100.00, 0.1)
        assert paid_min == 10.00
        assert saving_min == 90.00

        # 9.9折（最小折扣）
        paid_max, saving_max = calc_discount_amount(100.00, 0.99)
        assert paid_max == 99.00
        assert saving_max == 1.00

    @pytest.mark.P1
    def test_various_discount_rates(self):
        """各种折扣率的计算"""
        rates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]
        for rate in rates:
            paid, saving = calc_discount_amount(100.00, rate)
            assert paid > 0, f"{rate}折时实付不应为0"
            assert saving >= 0, f"{rate}折时优惠不应为负"
            assert round_to_cent(paid + saving) == 100.00, (
                f"{rate}折: {paid} + {saving} != 100.00"
            )

    @pytest.mark.P1
    def test_large_amount_precision(self):
        """大金额下的精度"""
        paid, saving = calc_discount_amount(50000.00, 0.85)
        assert paid == 42500.00
        assert saving == 7500.00

    @pytest.mark.P1
    def test_complex_decimal(self):
        """复杂小数场景"""
        # 123.45 * 0.73 = 90.1185 -> 90.12
        paid, saving = calc_discount_amount(123.45, 0.73)
        assert paid == 90.12
        assert saving == 33.33  # 123.45 - 90.12 = 33.33


class TestDiscountInputValidation:
    """折扣率输入校验（本地规则验证）"""

    @pytest.mark.P0
    def test_valid_discount_range(self):
        """合法折扣范围: 1折-9.9折"""
        valid_rates = [1.0, 2.0, 5.0, 8.0, 8.5, 9.0, 9.5, 9.9]
        for rate in valid_rates:
            discount_float = rate / 10  # 8折 -> 0.8
            paid, _ = calc_discount_amount(100.00, discount_float)
            assert 0 < paid <= 100, f"{rate}折时实付金额异常: {paid}"

    @pytest.mark.P0
    def test_boundary_discount_values(self):
        """边界折扣值"""
        # 0.9折 (低于最低折扣1折) — 系统应拒绝设置，但计算器不拦截
        paid_low, _ = calc_discount_amount(100.00, 0.09)
        assert paid_low == 9.00  # 计算上可以算，但系统不应允许设置

        # 10折 (等于原价) — 系统应拒绝
        paid_full, saving_full = calc_discount_amount(100.00, 1.0)
        assert paid_full == 100.00
        assert saving_full == 0.00
