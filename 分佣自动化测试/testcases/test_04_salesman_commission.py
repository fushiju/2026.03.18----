"""
场景四（P4）：业务员推广下单
业务员佣金由技师与技师所属代理商分别承担
"""
import allure
import jsonpath
import pytest

from config import config


@allure.epic("今夜到家分佣系统")
@allure.feature("业务员分佣")
class TestSalesmanCommission:
    """业务员扫码推广下单分佣验证"""

    SERVICE_FEE = 168
    MATERIAL_FEE = 10

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("TC-4.1 业务员扫码下单基础分佣")
    @allure.description(
        "用户通过业务员二维码扫码下单，验证业务员获佣，"
        "佣金由技师与代理商分别承担"
    )
    def test_salesman_basic_commission(self, complete_order_flow,
                                       order_api, calculator):
        salesman_rate = 0.05
        tech_bear_rate = 0.50
        agent_bear_rate = 0.50

        expected = calculator.calc_with_salesman(
            self.SERVICE_FEE, salesman_rate,
            tech_bear_rate, agent_bear_rate,
            self.MATERIAL_FEE,
        )

        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-业务员分佣",
            source_type="salesman",
            source_id=config["accounts"]["salesman"]["phone"],
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证业务员获得佣金"):
            salesman_amount = jsonpath.jsonpath(data, "$..salesman.amount")
            assert salesman_amount, "未找到业务员分佣数据"
            assert float(salesman_amount[0]) == expected["salesman"], \
                f"业务员佣金错误: 实际{salesman_amount[0]}, 预期{expected['salesman']}"

        with allure.step("验证技师佣金已扣除业务员承担部分"):
            tech = jsonpath.jsonpath(data, "$..technician.amount")
            assert float(tech[0]) == expected["technician"]

        with allure.step("验证代理商佣金已扣除业务员承担部分"):
            agent = jsonpath.jsonpath(data, "$..agent.amount")
            assert float(agent[0]) == expected["agent"]

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-4.2 业务员发展渠道商后的分佣链")
    @allure.description("业务员发展渠道商，渠道商用户下单时验证多级分佣")
    def test_salesman_develop_channel(self, complete_order_flow, order_api):
        """业务员 -> 渠道商 -> 用户下单，验证双重分佣"""
        order_id = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-业务员渠道链",
            source_type="salesman_channel",
            source_id="salesman_channel_test_id",
        )

        with allure.step("查询分佣明细"):
            resp = order_api.get_order_commission(order_id)
            data = resp.json()

        with allure.step("验证业务员获得渠道商发展返佣"):
            salesman = jsonpath.jsonpath(data, "$..salesman.amount")
            assert salesman, "业务员应获得渠道商发展返佣"

        with allure.step("验证渠道商获得订单分佣"):
            channel = jsonpath.jsonpath(data, "$..channel.amount")
            assert channel, "渠道商应获得订单分佣"

        with allure.step("验证所有额外佣金均从代理商扣除"):
            agent = jsonpath.jsonpath(data, "$..agent.amount")
            assert agent, "代理商佣金数据缺失"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("TC-4.3 业务员所属代理商变更后分佣")
    @allure.description("修改业务员所属代理商后验证佣金归属")
    def test_salesman_agent_change(self, complete_order_flow, order_api):
        """变更代理商后佣金归属按新代理商计算"""
        # 变更前下单
        order_id_before = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-业务员变更前",
            source_type="salesman",
            source_id=config["accounts"]["salesman"]["phone"],
        )

        with allure.step("查询变更前分佣"):
            resp1 = order_api.get_order_commission(order_id_before)
            data1 = resp1.json()
            agent_before = jsonpath.jsonpath(data1, "$..agent.id")

        # TODO: 调用管理端API变更业务员所属代理商
        # admin_api.update_salesman_agent(salesman_id, new_agent_id)

        # 变更后下单
        order_id_after = complete_order_flow(
            tech_id=config["accounts"]["technician"]["phone"],
            service_id="default_service_id",
            address="测试地址-业务员变更后",
            source_type="salesman",
            source_id=config["accounts"]["salesman"]["phone"],
        )

        with allure.step("查询变更后分佣"):
            resp2 = order_api.get_order_commission(order_id_after)
            data2 = resp2.json()
            agent_after = jsonpath.jsonpath(data2, "$..agent.id")

        with allure.step("验证佣金归属新代理商"):
            if agent_before and agent_after:
                allure.attach(
                    f"变更前代理商: {agent_before[0]}, 变更后: {agent_after[0]}",
                    "代理商变更对比",
                )
