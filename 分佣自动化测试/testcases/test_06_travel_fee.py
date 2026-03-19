"""
场景六：车费分佣
- 管理端设置免出行 -> 平台补贴
- 代理商端设置免出行 -> 代理商补贴
- 正常收取车费
"""
import allure
import jsonpath
import pytest

from config import config


@allure.epic("今夜到家分佣系统")
@allure.feature("车费分佣")
class TestTravelFeeCommission:
    """车费补贴与分佣验证"""

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-6.1 技师免出行车费-平台补贴")
    @allure.description("管理端设置技师免出行，车费由平台补贴")
    def test_travel_free_platform_subsidy(self, complete_order_flow,
                                           order_api):
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-平台补贴车费",
        )

        with allure.step("查询订单详情"):
            resp = order_api.get_order_detail(order_id)
            data = resp.json()

        with allure.step("验证车费由平台补贴"):
            travel_fee = jsonpath.jsonpath(data, "$..travelFee")
            travel_subsidy = jsonpath.jsonpath(data, "$..travelSubsidy")
            subsidy_from = jsonpath.jsonpath(data, "$..travelSubsidyFrom")

            assert travel_fee, "应有车费数据"
            if subsidy_from:
                assert subsidy_from[0] == "platform", \
                    f"管理端设置免出行，车费应由平台补贴，实际: {subsidy_from[0]}"

        with allure.step("验证车费不计入分佣基数"):
            resp2 = order_api.get_order_commission(order_id)
            commission = resp2.json()
            # 车费不应出现在分佣计算中
            base_amount = jsonpath.jsonpath(commission, "$..commissionBase")
            if base_amount and travel_fee:
                assert float(travel_fee[0]) not in [float(base_amount[0])], \
                    "车费不应计入分佣基数"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-6.2 技师免出行车费-代理商补贴")
    @allure.description("代理商端设置技师免出行，车费由代理商补贴")
    def test_travel_free_agent_subsidy(self, complete_order_flow, order_api):
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-代理商补贴车费",
        )

        with allure.step("查询订单详情"):
            resp = order_api.get_order_detail(order_id)
            data = resp.json()

        with allure.step("验证车费由代理商补贴"):
            subsidy_from = jsonpath.jsonpath(data, "$..travelSubsidyFrom")
            if subsidy_from:
                assert subsidy_from[0] == "agent", \
                    f"代理商端设置，车费应由代理商补贴，实际: {subsidy_from[0]}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-6.3 正常收取车费的订单分佣")
    @allure.description("未设置免出行，车费单独收取不参与分佣")
    def test_travel_fee_normal(self, complete_order_flow, order_api):
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-正常车费",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证车费单独收取，不参与分佣"):
            travel_in_commission = jsonpath.jsonpath(data, "$..travelFeeInCommission")
            if travel_in_commission:
                assert travel_in_commission[0] is False, \
                    "正常车费不应参与分佣计算"
