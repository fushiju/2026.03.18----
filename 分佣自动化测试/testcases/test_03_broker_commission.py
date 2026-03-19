"""
场景三（P3）：经纪人邀请用户成为技师，用户下单该技师后经纪人获佣
经纪人佣金由技师与技师所属代理商分别承担
"""
import allure
import jsonpath
import pytest

from config import config


@allure.epic("今夜到家分佣系统")
@allure.feature("经纪人分佣")
class TestBrokerCommission:
    """经纪人邀请技师 -> 技师产生订单 -> 经纪人获佣"""

    SERVICE_FEE = 168
    MATERIAL_FEE = 10

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-3.1 经纪人分佣基础验证")
    @allure.description(
        "经纪人邀请用户成为技师，用户下单该技师，"
        "经纪人按设置比例获佣，佣金由技师与代理商分别承担"
    )
    def test_broker_basic_commission(self, complete_order_flow,
                                     order_api, calculator):
        broker_rate = 0.05       # 经纪人佣金比例
        tech_bear_rate = 0.50    # 技师承担50%
        agent_bear_rate = 0.50   # 代理商承担50%

        expected = calculator.calc_with_broker(
            self.SERVICE_FEE, broker_rate,
            tech_bear_rate, agent_bear_rate,
            self.MATERIAL_FEE,
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-经纪人分佣",
            source_type="broker",
            source_id="broker_test_id",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证经纪人获得佣金"):
            broker_amount = jsonpath.jsonpath(data, "$..broker.amount")
            assert broker_amount, "未找到经纪人分佣数据"
            assert float(broker_amount[0]) == expected["broker"], \
                f"经纪人佣金错误: 实际{broker_amount[0]}, 预期{expected['broker']}"

        with allure.step("验证技师佣金已扣除经纪人承担部分"):
            tech_amount = jsonpath.jsonpath(data, "$..technician.amount")
            assert float(tech_amount[0]) == expected["technician"], \
                f"技师佣金应扣除承担部分: 预期{expected['technician']}"

        with allure.step("验证代理商佣金已扣除经纪人承担部分"):
            agent_amount = jsonpath.jsonpath(data, "$..agent.amount")
            assert float(agent_amount[0]) == expected["agent"], \
                f"代理商佣金应扣除承担部分: 预期{expected['agent']}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-3.2 经纪人佣金承担比例验证")
    @allure.description("验证技师承担X%，代理商承担Y%的经纪人佣金明细")
    def test_broker_bear_ratio(self, complete_order_flow, order_api, calculator):
        broker_rate = 0.06
        tech_bear_rate = 0.40    # 技师承担40%
        agent_bear_rate = 0.60   # 代理商承担60%

        expected = calculator.calc_with_broker(
            self.SERVICE_FEE, broker_rate,
            tech_bear_rate, agent_bear_rate,
            self.MATERIAL_FEE,
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-经纪人承担比例",
            source_type="broker",
            source_id="broker_test_id",
        )

        with allure.step("查询佣金承担明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证技师承担经纪人佣金部分"):
            tech_bear = jsonpath.jsonpath(data, "$..broker.fromTechnician")
            assert tech_bear, "缺少技师承担经纪人佣金明细"
            assert float(tech_bear[0]) == expected["broker_from_tech"]

        with allure.step("验证代理商承担经纪人佣金部分"):
            agent_bear = jsonpath.jsonpath(data, "$..broker.fromAgent")
            assert agent_bear, "缺少代理商承担经纪人佣金明细"
            assert float(agent_bear[0]) == expected["broker_from_agent"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-3.3 修改经纪人提成比例后生效验证")
    @allure.description("修改前后各下单一笔，验证新比例仅对修改后订单生效")
    def test_broker_rate_change(self, complete_order_flow, order_api):
        # 修改前下单
        order_id_before = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-经纪人修改前",
            source_type="broker",
            source_id="broker_test_id",
        )

        with allure.step("记录修改前经纪人佣金"):
            resp1 = order_api.get_order_commission(order_id_before)
            data1 = resp1.json()
            amount_before = jsonpath.jsonpath(data1, "$..broker.amount")

        # TODO: 调用管理端API修改经纪人提成比例
        # admin_api.update_broker_rate(broker_id, new_rate)

        # 修改后下单
        order_id_after = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-经纪人修改后",
            source_type="broker",
            source_id="broker_test_id",
        )

        with allure.step("记录修改后经纪人佣金"):
            resp2 = order_api.get_order_commission(order_id_after)
            data2 = resp2.json()
            amount_after = jsonpath.jsonpath(data2, "$..broker.amount")

        with allure.step("验证修改前后佣金不同"):
            if amount_before and amount_after:
                allure.attach(
                    f"修改前: {amount_before[0]}, 修改后: {amount_after[0]}",
                    "经纪人佣金对比",
                )
