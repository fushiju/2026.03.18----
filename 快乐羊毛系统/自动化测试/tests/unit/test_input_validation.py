"""
输入校验规则测试

验证各类用户输入的校验逻辑:
- 金额输入校验
- 手机号校验
- 折扣率设置校验
"""
import re
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from utils.test_data import AMOUNT_INPUT_CASES
from config import TestConfig


# ============================================================
# 金额校验函数（模拟系统校验逻辑）
# ============================================================
def validate_amount(value_str):
    """
    校验金额输入
    规则:
    - 不能为空
    - 必须为合法数字
    - 大于0
    - 不超过50000
    - 最多2位小数
    """
    if not value_str or not value_str.strip():
        return False, "请输入消费金额"

    value_str = value_str.strip()

    # 不允许特殊字符（只允许数字和小数点）
    if not re.match(r"^[\d.]+$", value_str):
        return False, "只允许数字和小数点"

    # 不允许多个小数点
    if value_str.count(".") > 1:
        return False, "只允许一个小数点"

    # 纯小数点
    if value_str == ".":
        return False, "不允许纯小数点"

    try:
        value = float(value_str)
    except ValueError:
        return False, "非法数字"

    if value <= 0:
        return False, "消费金额必须大于0"

    if value > TestConfig.MAX_SINGLE_AMOUNT:
        return False, f"单笔消费金额不能超过{TestConfig.MAX_SINGLE_AMOUNT}元"

    # 检查小数位数
    if "." in value_str:
        decimal_part = value_str.split(".")[1]
        if len(decimal_part) > 2:
            return False, "小数点后最多2位"

    return True, "校验通过"


def validate_phone(phone):
    """
    校验手机号
    规则: 11位，1开头，纯数字
    """
    if not phone:
        return False, "请输入手机号"
    if not re.match(r"^1\d{10}$", phone):
        return False, "手机号格式不正确"
    return True, "校验通过"


def validate_discount_rate(rate):
    """
    校验折扣率
    规则: 1.0-9.9
    """
    if rate < TestConfig.MIN_DISCOUNT:
        return False, f"折扣不能低于{TestConfig.MIN_DISCOUNT}折"
    if rate > TestConfig.MAX_DISCOUNT:
        return False, f"折扣不能高于{TestConfig.MAX_DISCOUNT}折"
    return True, "校验通过"


# ============================================================
# 金额输入校验测试
# ============================================================
class TestAmountValidation:
    """金额输入校验"""

    @pytest.mark.P0
    @pytest.mark.parametrize(
        "value, expected_valid, desc",
        AMOUNT_INPUT_CASES,
        ids=[c[2] for c in AMOUNT_INPUT_CASES],
    )
    def test_amount_input(self, value, expected_valid, desc):
        """参数化测试: 金额输入校验"""
        valid, msg = validate_amount(value)
        assert valid == expected_valid, (
            f"输入 '{value}' ({desc}): 期望 {'合法' if expected_valid else '非法'}, "
            f"实际 {'合法' if valid else '非法'}, 消息: {msg}"
        )

    @pytest.mark.P0
    def test_zero_amount(self):
        valid, msg = validate_amount("0")
        assert not valid
        assert "大于0" in msg

    @pytest.mark.P0
    def test_negative_amount(self):
        valid, msg = validate_amount("-100")
        assert not valid

    @pytest.mark.P0
    def test_max_boundary(self):
        valid, _ = validate_amount("50000")
        assert valid

    @pytest.mark.P0
    def test_over_max(self):
        valid, msg = validate_amount("50000.01")
        assert not valid
        assert "50000" in msg

    @pytest.mark.P0
    def test_min_valid(self):
        valid, _ = validate_amount("0.01")
        assert valid

    @pytest.mark.P1
    def test_multiple_decimal_points(self):
        valid, msg = validate_amount("1.2.3")
        assert not valid

    @pytest.mark.P1
    def test_pure_dot(self):
        valid, _ = validate_amount(".")
        assert not valid

    @pytest.mark.P1
    def test_leading_spaces(self):
        """前导空格应被trim"""
        valid, _ = validate_amount(" 100")
        assert valid

    @pytest.mark.P2
    def test_scientific_notation(self):
        """科学计数法不允许"""
        valid, _ = validate_amount("1e5")
        assert not valid


# ============================================================
# 手机号校验测试
# ============================================================
class TestPhoneValidation:
    """手机号校验"""

    @pytest.mark.P0
    @pytest.mark.parametrize("phone, expected, desc", [
        ("13800138000", True, "正常手机号"),
        ("15912345678", True, "159开头"),
        ("18600000000", True, "186开头"),
        ("", False, "空输入"),
        ("1380013800", False, "10位-少1位"),
        ("138001380001", False, "12位-多1位"),
        ("23800138000", False, "非1开头"),
        ("1380013800a", False, "含字母"),
        ("138-0013-8000", False, "含横杠"),
        ("1380013 000", False, "含空格"),
        ("01380013800", False, "0开头"),
    ])
    def test_phone_validation(self, phone, expected, desc):
        """参数化测试: 手机号校验"""
        valid, _ = validate_phone(phone)
        assert valid == expected, f"手机号 '{phone}' ({desc})"

    @pytest.mark.P1
    def test_all_carrier_prefixes(self):
        """常见运营商号段全覆盖"""
        # 移动: 134-139, 147, 150-152, 157-159, 178, 182-184, 187-188, 198
        # 联通: 130-132, 155-156, 166, 175-176, 185-186
        # 电信: 133, 149, 153, 173, 177, 180-181, 189, 199
        prefixes = [
            "134", "135", "136", "137", "138", "139",  # 移动
            "130", "131", "132", "155", "156",           # 联通
            "133", "153", "180", "181", "189",           # 电信
        ]
        for prefix in prefixes:
            phone = prefix + "0" * (11 - len(prefix))
            valid, _ = validate_phone(phone)
            assert valid, f"号段 {prefix} 应该合法"


# ============================================================
# 折扣率设置校验测试
# ============================================================
class TestDiscountRateValidation:
    """折扣率设置校验"""

    @pytest.mark.P0
    @pytest.mark.parametrize("rate, expected, desc", [
        (1.0, True, "最低折扣1折"),
        (5.0, True, "5折"),
        (8.0, True, "8折"),
        (8.5, True, "8.5折"),
        (9.9, True, "最高折扣9.9折"),
        (0.5, False, "低于最低折扣"),
        (0.9, False, "接近但低于最低"),
        (10.0, False, "10折=无折扣"),
        (15.0, False, "超过10折"),
        (0, False, "0折"),
        (-1, False, "负数折扣"),
    ])
    def test_discount_rate_validation(self, rate, expected, desc):
        """参数化测试: 折扣率校验"""
        valid, _ = validate_discount_rate(rate)
        assert valid == expected, f"折扣率 {rate} ({desc})"
