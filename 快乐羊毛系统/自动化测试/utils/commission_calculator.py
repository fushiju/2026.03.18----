"""
分佣计算器 - 本地验算工具

用于对比系统计算结果和本地预期结果,验证分佣计算的精确性。
所有金额精确到分(小数点后2位),四舍五入。
"""
from decimal import Decimal, ROUND_HALF_UP


def round_to_cent(amount):
    """金额四舍五入到分（小数点后2位）"""
    return float(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calc_profit(paid_amount, cost):
    """
    计算利润
    :param paid_amount: 用户实付金额
    :param cost: 投入成本(后台设置的原价/进货价)
    :return: 利润
    """
    profit = round_to_cent(paid_amount - cost)
    return max(profit, 0)  # 利润不应为负


def calc_discount_amount(original_price, discount_rate):
    """
    计算折扣后金额
    :param original_price: 原价
    :param discount_rate: 折扣率(如8折传0.8, 8.5折传0.85)
    :return: (实付金额, 优惠金额)
    """
    paid = round_to_cent(original_price * discount_rate)
    # 最低支付1分钱
    paid = max(paid, 0.01) if original_price > 0 else 0
    saving = round_to_cent(original_price - paid)
    return paid, saving


def calc_commission(
    paid_amount,
    cost,
    platform_ratio,
    agent_ratio,
    level1_ratio=0,
    level2_ratio=0,
):
    """
    计算分佣（快乐羊毛分佣模型）

    规则:
    - 利润 = 实付金额 - 投入成本
    - 平台佣金 = 利润 x 平台比例
    - 代理商总份额 = 利润 x 代理商比例
    - 一级分销员 = 利润 x 一级比例（从代理商扣）
    - 二级分销员 = 利润 x 二级比例（从代理商扣）
    - 代理商实得 = 代理商总份额 - 一级佣金 - 二级佣金

    :param paid_amount: 实付金额
    :param cost: 投入成本
    :param platform_ratio: 平台比例(百分比,如50表示50%)
    :param agent_ratio: 代理商比例(百分比)
    :param level1_ratio: 一级分销员比例(百分比,默认0)
    :param level2_ratio: 二级分销员比例(百分比,默认0)
    :return: dict 包含各方佣金明细
    """
    profit = calc_profit(paid_amount, cost)

    platform_commission = round_to_cent(profit * platform_ratio / 100)
    level1_commission = round_to_cent(profit * level1_ratio / 100)
    level2_commission = round_to_cent(profit * level2_ratio / 100)

    # 代理商总份额 = 利润 - 平台佣金（用减法避免四舍五入尾差）
    agent_total = round_to_cent(profit - platform_commission)
    agent_actual = round_to_cent(agent_total - level1_commission - level2_commission)

    total_distributed = round_to_cent(
        platform_commission + agent_actual + level1_commission + level2_commission
    )

    return {
        "profit": profit,
        "platform_commission": platform_commission,
        "agent_total": agent_total,
        "agent_actual": agent_actual,
        "level1_commission": level1_commission,
        "level2_commission": level2_commission,
        "total_distributed": total_distributed,
        # 尾差记录（便于排查）
        "rounding_diff": round_to_cent(total_distributed - profit),
    }


def calc_commission_cps(imported_commission, platform_ratio, agent_ratio,
                        level1_ratio=0, level2_ratio=0):
    """
    CPS跳转类分佣（Excel导入佣金，不扣成本直接分）

    :param imported_commission: Excel导入的佣金金额
    :param platform_ratio: 平台比例
    :param agent_ratio: 代理商比例
    :return: dict 各方佣金
    """
    platform = round_to_cent(imported_commission * platform_ratio / 100)
    agent_total = round_to_cent(imported_commission * agent_ratio / 100)
    level1 = round_to_cent(imported_commission * level1_ratio / 100)
    level2 = round_to_cent(imported_commission * level2_ratio / 100)
    agent_actual = round_to_cent(agent_total - level1 - level2)

    return {
        "profit": imported_commission,
        "platform_commission": platform,
        "agent_total": agent_total,
        "agent_actual": agent_actual,
        "level1_commission": level1,
        "level2_commission": level2,
    }


def calc_refund_commission_impact(original_result, refund_amount, paid_amount, cost):
    """
    计算退款对分佣的影响

    :param original_result: 原始分佣结果(calc_commission的返回值)
    :param refund_amount: 退款金额
    :param paid_amount: 原实付金额
    :param cost: 原投入成本
    :return: dict 冲抵金额
    """
    new_paid = round_to_cent(paid_amount - refund_amount)
    new_profit = calc_profit(new_paid, cost)

    # 按新利润重算各方佣金，差额就是冲抵金额
    offset_platform = round_to_cent(
        original_result["platform_commission"]
        - round_to_cent(new_profit * 50 / 100)  # 注意：实际应使用对应比例
    )
    offset_agent = round_to_cent(
        original_result["agent_actual"]
        - round_to_cent(new_profit * 50 / 100)
    )

    return {
        "new_paid": new_paid,
        "new_profit": new_profit,
        "is_full_refund": refund_amount >= paid_amount,
        "offset_platform": -offset_platform,
        "offset_agent": -offset_agent,
    }


def validate_commission_ratios(platform_ratio, agent_ratio, level1_ratio=0, level2_ratio=0):
    """
    校验分佣比例是否合法

    规则:
    - 平台 + 代理商 = 100%
    - 比例不能为负
    - 比例不能超过100%
    - 一级+二级 <= 代理商比例
    """
    errors = []

    if platform_ratio < 0 or agent_ratio < 0 or level1_ratio < 0 or level2_ratio < 0:
        errors.append("分佣比例不能为负数")

    if platform_ratio > 100 or agent_ratio > 100:
        errors.append("比例不能超过100%")

    total = platform_ratio + agent_ratio
    if abs(total - 100) > 0.01:
        errors.append(f"平台和代理商比例之和必须等于100%，当前为{total}%")

    distributor_total = level1_ratio + level2_ratio
    if distributor_total > agent_ratio:
        errors.append(
            f"分销员分佣比例({distributor_total}%)不能超过代理商比例({agent_ratio}%)"
        )

    return {"valid": len(errors) == 0, "errors": errors}
