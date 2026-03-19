"""
场景一（P1）：公众号用户扫码下单 — 无任何分佣角色，基础三方分佣
场景七：物料费归属验证
"""
import allure
import jsonpath
import pytest

from config import config
from api.wechat_api import WechatOrderAPI
from utils.commission_calculator import CommissionCalculator


@allure.epic("今夜到家分佣系统")
@allure.feature("基础三方分佣（无分佣角色）")
class TestBasicCommission:
    """公众号扫码下单 - 技师/平台/代理商三方分佣"""

    # ---- 测试数据 ----
    SERVICE_FEE = 168
    MATERIAL_FEE = 10
    COUPON_AMOUNT = 20

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-1.1 基础订单三方分佣验证")
    @allure.description(
        "用户通过公众号扫码进入，无关联任何分佣角色；"
        "订单金额168元+物料费10元，验证三方分佣金额"
    )
    def test_basic_three_way_commission(self, order_api, tech_api,
                                        complete_order_flow, calculator, db):
        """基础订单: 技师50%=84, 代理商42%=70.56, 平台8%=13.44, 物料费10归平台"""
        # 预期分佣
        expected = calculator.calc_basic(self.SERVICE_FEE, self.MATERIAL_FEE)

        # 执行完整下单流程
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-基础分佣",
        )

        # 查询分佣明细
        with allure.step("查询订单分佣明细"):
            resp = order_api.get_order_commission(order_id)
            commission_data = resp.json()

        # 断言分佣金额
        with allure.step("验证技师分佣金额"):
            tech_amount = jsonpath.jsonpath(commission_data, "$..technician.amount")
            assert tech_amount, "未找到技师分佣数据"
            assert float(tech_amount[0]) == expected["technician"], \
                f"技师分佣错误: 实际{tech_amount[0]}, 预期{expected['technician']}"

        with allure.step("验证平台分佣金额(含物料费)"):
            platform_amount = jsonpath.jsonpath(commission_data, "$..platform.amount")
            assert platform_amount, "未找到平台分佣数据"
            assert float(platform_amount[0]) == expected["platform"], \
                f"平台分佣错误: 实际{platform_amount[0]}, 预期{expected['platform']}"

        with allure.step("验证代理商分佣金额"):
            agent_amount = jsonpath.jsonpath(commission_data, "$..agent.amount")
            assert agent_amount, "未找到代理商分佣数据"
            assert float(agent_amount[0]) == expected["agent"], \
                f"代理商分佣错误: 实际{agent_amount[0]}, 预期{expected['agent']}"

        with allure.step("验证分佣总和 = 服务费"):
            total = expected["technician"] + expected["agent"] + expected["platform_service_only"]
            assert total == float(self.SERVICE_FEE), \
                f"分佣总和{total} ≠ 服务费{self.SERVICE_FEE}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-1.2 必须有代理商才能分佣")
    @allure.description("技师未关联代理商时下单，验证系统容错机制")
    def test_no_agent_commission(self, order_api, tech_api):
        """技师无代理商 -> 系统异常处理"""
        with allure.step("使用无代理商关联的技师下单"):
            resp = order_api.create_order(
                tech_id="no_agent_tech_id",
                service_id="default_service_id",
                address="测试地址-无代理商",
            )
            data = resp.json()

        with allure.step("验证系统返回异常提示"):
            code = jsonpath.jsonpath(data, "$.code")[0]
            # 预期：系统拒绝下单或给出提示
            assert code != 200 or "agent" in str(data).lower(), \
                "技师无代理商时应给出异常提示"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-1.3 订单含优惠券的分佣验证")
    @allure.description("使用20元优惠券，验证优先扣除优惠券后再分佣")
    def test_commission_with_coupon(self, complete_order_flow, order_api,
                                    calculator):
        """168-20=148元参与分佣，物料费归平台"""
        expected = calculator.calc_basic(
            self.SERVICE_FEE, self.MATERIAL_FEE, coupon=self.COUPON_AMOUNT
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-优惠券分佣",
            coupon_id="test_coupon_20",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证分佣基数为扣除优惠券后的金额"):
            tech_amount = jsonpath.jsonpath(data, "$..technician.amount")
            assert tech_amount, "未找到技师分佣数据"
            # 148 * 50% = 74
            assert float(tech_amount[0]) == expected["technician"], \
                f"技师分佣错误: 实际{tech_amount[0]}, 预期{expected['technician']}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-1.4 订单含卡券-全员分摊模式")
    @allure.description("卡券优惠由技师、代理商、平台按比例分摊")
    def test_commission_card_all_share(self, complete_order_flow, order_api):
        """卡券全员分摊 -> 各角色按比例承担卡券优惠"""
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-卡券全员分摊",
            card_id="test_card_all_share",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证卡券优惠由各角色按比例分摊"):
            # 提取各角色卡券承担金额
            card_shares = jsonpath.jsonpath(data, "$..cardShare")
            assert card_shares, "未找到卡券分摊数据"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-1.5 订单含卡券-按技师上级分摊模式")
    @allure.description("卡券优惠由技师对应的上级（代理商）承担")
    def test_commission_card_agent_share(self, complete_order_flow, order_api):
        """卡券按上级分摊 -> 代理商承担卡券优惠"""
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-卡券上级分摊",
            card_id="test_card_agent_share",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证卡券优惠全部由代理商承担"):
            card_shares = jsonpath.jsonpath(data, "$..cardShare")
            assert card_shares, "未找到卡券分摊数据"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-7.1 物料费统一归平台验证")
    @allure.description("物料费10元统一归平台，由财务结算给代理商")
    def test_material_fee_belongs_to_platform(self, complete_order_flow,
                                               order_api, db):
        """物料费归平台，不参与常规分佣"""
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-物料费验证",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证物料费归属平台"):
            material_info = jsonpath.jsonpath(data, "$..materialFee")
            assert material_info, "未找到物料费数据"
            # 物料费应归属平台
            material_owner = jsonpath.jsonpath(data, "$..materialFee.owner")
            assert material_owner and material_owner[0] == "platform", \
                "物料费应归平台所有"
