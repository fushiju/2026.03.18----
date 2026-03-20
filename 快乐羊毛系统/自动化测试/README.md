# 快乐羊毛平台 — 自动化测试项目

## 项目结构

```
自动化测试/
├── conftest.py                  # pytest全局配置和fixtures
├── pytest.ini                   # pytest配置文件
├── requirements.txt             # 依赖包
├── config.py                    # 环境配置（URL/账号等）
├── utils/
│   ├── __init__.py
│   ├── api_client.py            # API请求封装
│   ├── commission_calculator.py # 分佣计算器（本地验算工具）
│   └── test_data.py             # 测试数据工厂
├── tests/
│   ├── __init__.py
│   ├── unit/                    # 单元测试（分佣计算逻辑验证）
│   │   ├── __init__.py
│   │   ├── test_commission_calc.py         # 分佣计算精确性
│   │   ├── test_discount_calc.py           # 折扣计算精确性
│   │   └── test_input_validation.py        # 输入校验规则
│   ├── api/                     # 接口测试
│   │   ├── __init__.py
│   │   ├── test_auth_api.py               # 登录鉴权
│   │   ├── test_order_api.py              # 订单接口
│   │   ├── test_commission_api.py         # 分佣接口
│   │   ├── test_product_api.py            # 商品/选品仓库接口
│   │   ├── test_merchant_api.py           # 商家管理接口
│   │   ├── test_refund_api.py             # 退款接口
│   │   ├── test_withdraw_api.py           # 提现结算接口
│   │   ├── test_excel_import_api.py       # Excel佣金导入接口
│   │   └── test_security_api.py           # 安全测试（越权/注入/篡改）
│   └── ui/                      # UI自动化测试（后台管理系统）
│       ├── __init__.py
│       ├── test_admin_login.py            # 后台登录
│       ├── test_admin_order.py            # 订单管理
│       ├── test_admin_commission.py       # 分佣配置与查看
│       ├── test_admin_product.py          # 选品仓库操作
│       └── test_admin_audit.py            # 审核操作
└── reports/                     # 测试报告输出目录
```

## 环境准备

```bash
# 1. 安装Python 3.9+
# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装Playwright浏览器
playwright install chromium
```

## 运行测试

```bash
# 运行全部测试
pytest

# 只运行单元测试（分佣计算验证，无需网络）
pytest tests/unit/ -v

# 只运行接口测试
pytest tests/api/ -v

# 只运行UI测试
pytest tests/ui/ -v

# 运行指定测试文件
pytest tests/unit/test_commission_calc.py -v

# 运行指定测试用例
pytest tests/unit/test_commission_calc.py::TestBasicCommission::test_no_distributor -v

# 生成HTML测试报告
pytest --html=reports/report.html --self-contained-html

# 生成Allure报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# 按标记运行
pytest -m "P0" -v          # 只运行P0用例
pytest -m "commission" -v   # 只运行分佣相关用例
pytest -m "security" -v     # 只运行安全测试
```
