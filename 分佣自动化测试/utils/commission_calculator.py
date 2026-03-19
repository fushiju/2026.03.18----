"""
分佣计算器 - 根据业务规则计算预期分佣金额
用于测试断言时生成期望值
"""
from decimal import Decimal, ROUND_HALF_UP
from config import config


def to_decimal(value):
    return Decimal(str(value))


def round_money(value):
    """金额精确到分（2位小数）"""
    return to_decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class CommissionCalculator:
    """分佣计算器"""

    def __init__(self, tech_rate=None, agent_rate=None, platform_rate=None):
        rates = config["commission_rate"]
        self.tech_rate = to_decimal(tech_rate or rates["technician"])
        self.agent_rate = to_decimal(agent_rate or rates["agent"])
        self.platform_rate = to_decimal(platform_rate or rates["platform"])

    def calc_basic(self, service_fee, material_fee=0, coupon=0):
        """
        基础三方分佣（无额外分佣角色）
        Returns: dict with technician, agent, platform, material amounts
        """
        service = to_decimal(service_fee) - to_decimal(coupon)
        material = to_decimal(material_fee)

        tech_amount = round_money(service * self.tech_rate)
        agent_amount = round_money(service * self.agent_rate)
        platform_amount = round_money(service * self.platform_rate)

        return {
            "service_fee": float(service),
            "material_fee": float(material),
            "technician": float(tech_amount),
            "agent": float(agent_amount),
            "platform": float(platform_amount) + float(material),
            "platform_service_only": float(platform_amount),
            "total_check": float(tech_amount + agent_amount + platform_amount),
        }

    def calc_with_distributor(self, service_fee, distributor_rate,
                              material_fee=0, coupon=0,
                              level2_rate=0):
        """
        含分销员的分佣（分销员佣金从代理商份额扣除）
        """
        base = self.calc_basic(service_fee, material_fee, coupon)
        service = to_decimal(service_fee) - to_decimal(coupon)

        dist_amount = round_money(service * to_decimal(distributor_rate))
        dist2_amount = round_money(service * to_decimal(level2_rate))

        agent_actual = round_money(
            to_decimal(base["agent"]) - dist_amount - dist2_amount
        )

        return {
            **base,
            "distributor_level1": float(dist_amount),
            "distributor_level2": float(dist2_amount),
            "agent": float(agent_actual),
            "agent_original": base["agent"],
        }

    def calc_with_broker(self, service_fee, broker_rate,
                         tech_bear_rate, agent_bear_rate,
                         material_fee=0, coupon=0):
        """
        含经纪人的分佣（经纪人佣金由技师和代理商分别承担）
        """
        base = self.calc_basic(service_fee, material_fee, coupon)
        service = to_decimal(service_fee) - to_decimal(coupon)

        broker_total = round_money(service * to_decimal(broker_rate))
        tech_bear = round_money(broker_total * to_decimal(tech_bear_rate))
        agent_bear = round_money(broker_total * to_decimal(agent_bear_rate))

        return {
            **base,
            "broker": float(broker_total),
            "broker_from_tech": float(tech_bear),
            "broker_from_agent": float(agent_bear),
            "technician": float(to_decimal(base["technician"]) - tech_bear),
            "agent": float(to_decimal(base["agent"]) - agent_bear),
            "technician_original": base["technician"],
            "agent_original": base["agent"],
        }

    def calc_with_salesman(self, service_fee, salesman_rate,
                           tech_bear_rate, agent_bear_rate,
                           material_fee=0, coupon=0):
        """
        含业务员的分佣（业务员佣金由技师和代理商分别承担）
        """
        base = self.calc_basic(service_fee, material_fee, coupon)
        service = to_decimal(service_fee) - to_decimal(coupon)

        salesman_total = round_money(service * to_decimal(salesman_rate))
        tech_bear = round_money(salesman_total * to_decimal(tech_bear_rate))
        agent_bear = round_money(salesman_total * to_decimal(agent_bear_rate))

        return {
            **base,
            "salesman": float(salesman_total),
            "salesman_from_tech": float(tech_bear),
            "salesman_from_agent": float(agent_bear),
            "technician": float(to_decimal(base["technician"]) - tech_bear),
            "agent": float(to_decimal(base["agent"]) - agent_bear),
            "technician_original": base["technician"],
            "agent_original": base["agent"],
        }

    def calc_with_channel(self, service_fee, channel_rate,
                          tech_bear_rate, agent_bear_rate,
                          material_fee=0, coupon=0,
                          in_validity=True):
        """
        含渠道商的分佣
        - in_validity=True: 时效内，渠道商参与分佣
        - in_validity=False: 时效外，渠道商不参与分佣
        佣金承担顺序：技师 → 技师上级代理 → 平台(兜底)
        """
        base = self.calc_basic(service_fee, material_fee, coupon)

        if not in_validity:
            return {**base, "channel": 0, "channel_active": False}

        service = to_decimal(service_fee) - to_decimal(coupon)
        channel_total = round_money(service * to_decimal(channel_rate))

        tech_bear = round_money(channel_total * to_decimal(tech_bear_rate))
        agent_bear = round_money(channel_total * to_decimal(agent_bear_rate))
        # 如果技师+代理商承担 < 100%，剩余由平台承担
        platform_bear = channel_total - tech_bear - agent_bear

        result = {
            **base,
            "channel": float(channel_total),
            "channel_active": True,
            "channel_from_tech": float(tech_bear),
            "channel_from_agent": float(agent_bear),
            "channel_from_platform": float(max(platform_bear, Decimal("0"))),
            "technician": float(to_decimal(base["technician"]) - tech_bear),
            "agent": float(to_decimal(base["agent"]) - agent_bear),
            "technician_original": base["technician"],
            "agent_original": base["agent"],
        }

        if platform_bear > 0:
            result["platform"] = float(
                to_decimal(base["platform"]) - platform_bear
            )
            result["platform_original"] = base["platform"]

        return result
