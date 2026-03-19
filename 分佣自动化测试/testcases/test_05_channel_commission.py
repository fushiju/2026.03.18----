"""
场景五（P5）：渠道商推广下单（重点场景）
核心矩阵：时效内/外 × 换绑/不换绑 = 4种场景
佣金承担顺序：技师 → 技师上级代理 → 平台(兜底)
"""
import allure
import jsonpath
import pytest

from config import config


@allure.epic("今夜到家分佣系统")
@allure.feature("渠道商分佣")
class TestChannelCommission:
    """渠道商推广下单 - 时效/换绑矩阵测试"""

    SERVICE_FEE = 168
    MATERIAL_FEE = 10

    # ---- 时效内场景 ----

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-5.1 时效内+不换绑扫码下单")
    @allure.description(
        "渠道商绑定时效内，设置不换绑模式\n"
        "用户扫渠道商A码后再扫B码，渠道商应保持为A"
    )
    def test_in_validity_no_rebind(self, order_api, complete_order_flow):
        with allure.step("用户扫渠道商A码绑定"):
            order_api.scan_channel_qrcode("channel_A_id")

        with allure.step("时效内扫渠道商B码（不换绑模式下应无效）"):
            order_api.scan_channel_qrcode("channel_B_id")

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-时效内不换绑",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证渠道商仍为A（未换绑）"):
            channel_id = jsonpath.jsonpath(data, "$..channel.id")
            assert channel_id, "未找到渠道商分佣数据"
            assert channel_id[0] == "channel_A_id", \
                f"不换绑模式下渠道商应保持为A，实际为{channel_id[0]}"

        with allure.step("验证渠道商A获得佣金"):
            channel_amount = jsonpath.jsonpath(data, "$..channel.amount")
            assert channel_amount and float(channel_amount[0]) > 0, \
                "渠道商A应获得佣金"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-5.2 时效内+换绑扫码下单")
    @allure.description(
        "渠道商绑定时效内，设置可换绑模式\n"
        "用户扫渠道商B码后渠道商变更为B"
    )
    def test_in_validity_with_rebind(self, order_api, complete_order_flow):
        with allure.step("用户扫渠道商A码绑定"):
            order_api.scan_channel_qrcode("channel_A_id")

        with allure.step("时效内扫渠道商B码（可换绑模式）"):
            order_api.scan_channel_qrcode("channel_B_id")

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-时效内换绑",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证渠道商已变更为B"):
            channel_id = jsonpath.jsonpath(data, "$..channel.id")
            assert channel_id, "未找到渠道商分佣数据"
            assert channel_id[0] == "channel_B_id", \
                f"换绑后渠道商应为B，实际为{channel_id[0]}"

        with allure.step("验证渠道商B获得佣金"):
            channel_amount = jsonpath.jsonpath(data, "$..channel.amount")
            assert channel_amount and float(channel_amount[0]) > 0

    # ---- 时效外场景 ----

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-5.3 时效外+不换绑扫码下单")
    @allure.description("渠道商绑定已超时效，渠道商不参与分佣")
    def test_out_validity_no_rebind(self, complete_order_flow, order_api,
                                    calculator):
        expected = calculator.calc_with_channel(
            self.SERVICE_FEE, channel_rate=0.05,
            tech_bear_rate=0.5, agent_bear_rate=0.5,
            material_fee=self.MATERIAL_FEE,
            in_validity=False,
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-时效外不换绑",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证渠道商不分佣"):
            channel_amount = jsonpath.jsonpath(data, "$..channel.amount")
            if channel_amount:
                assert float(channel_amount[0]) == 0, \
                    "时效外渠道商不应获得佣金"

        with allure.step("验证仅三方分佣"):
            tech = jsonpath.jsonpath(data, "$..technician.amount")
            agent = jsonpath.jsonpath(data, "$..agent.amount")
            assert tech and float(tech[0]) == expected["technician"]
            assert agent and float(agent[0]) == expected["agent"]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-5.4 时效外+换绑扫码下单")
    @allure.description("时效外即使扫了新渠道商码，渠道商仍不分佣")
    def test_out_validity_with_rebind(self, order_api, complete_order_flow):
        with allure.step("时效外扫渠道商C码"):
            order_api.scan_channel_qrcode("channel_C_id")

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-时效外换绑",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证渠道商C不分佣（时效外）"):
            channel_amount = jsonpath.jsonpath(data, "$..channel.amount")
            if channel_amount:
                assert float(channel_amount[0]) == 0, \
                    "时效外渠道商不应获得佣金"

    # ---- 佣金承担逻辑 ----

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-5.5 渠道商佣金承担顺序验证")
    @allure.description(
        "技师+代理商=100%时平台不承担；<100%时平台承担差额"
    )
    @pytest.mark.parametrize(
        "tech_bear,agent_bear,platform_should_bear",
        [
            (0.60, 0.40, False),   # 100%，平台不承担
            (0.40, 0.40, True),    # 80%，平台承担20%
            (0.50, 0.50, False),   # 100%，平台不承担
            (0.30, 0.30, True),    # 60%，平台承担40%
        ],
        ids=[
            "tech60_agent40_no_platform",
            "tech40_agent40_platform20",
            "tech50_agent50_no_platform",
            "tech30_agent30_platform40",
        ],
    )
    def test_channel_bear_order(self, calculator, complete_order_flow,
                                 order_api, tech_bear, agent_bear,
                                 platform_should_bear):
        channel_rate = 0.05
        expected = calculator.calc_with_channel(
            self.SERVICE_FEE, channel_rate,
            tech_bear, agent_bear,
            self.MATERIAL_FEE,
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address=f"测试地址-承担{tech_bear}_{agent_bear}",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step(f"验证平台{'应' if platform_should_bear else '不应'}承担差额"):
            platform_bear = jsonpath.jsonpath(data, "$..channel.fromPlatform")
            if platform_should_bear:
                assert platform_bear and float(platform_bear[0]) > 0, \
                    "技师+代理商<100%时平台应承担差额"
                assert float(platform_bear[0]) == expected["channel_from_platform"]
            else:
                if platform_bear:
                    assert float(platform_bear[0]) == 0, \
                        "技师+代理商=100%时平台不应承担"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-5.6 全局时效vs单独时效设置")
    @allure.description("单独设置优先于全局设置")
    def test_channel_validity_priority(self, complete_order_flow, order_api):
        """全局30天, 单独60天 -> 第45天下单渠道商仍获佣"""
        # 前置条件：全局30天，某渠道商单独设置60天
        # 第45天下单
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-时效优先级",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证渠道商仍获佣（单独时效60天内）"):
            channel = jsonpath.jsonpath(data, "$..channel.amount")
            assert channel and float(channel[0]) > 0, \
                "单独设置60天优先，第45天应获佣"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-5.7 渠道商所属上级修改后分佣")
    @allure.description("修改后佣金承担按新上级代理商")
    def test_channel_parent_change(self, complete_order_flow, order_api):
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-渠道商上级修改",
        )

        with allure.step("查询分佣"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()
            agent = jsonpath.jsonpath(data, "$..channel.parentAgent")
            allure.attach(str(agent), "渠道商所属上级")

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-5.8 时效内不扫码直接下单")
    @allure.description("时效内不扫其他码，佣金返给原绑定渠道商")
    def test_in_validity_direct_order(self, complete_order_flow, order_api):
        """已绑定渠道商A，不扫码直接下单 -> 佣金归A"""
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-不扫码直接下单",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证佣金归原绑定渠道商"):
            channel = jsonpath.jsonpath(data, "$..channel.amount")
            assert channel and float(channel[0]) > 0, \
                "时效内不扫码应保持原渠道商绑定并分佣"
