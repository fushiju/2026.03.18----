"""
快乐羊毛平台 - 测试环境配置
"""


class TestConfig:
    """测试环境配置"""

    # ============ 后台管理系统 ============
    ADMIN_BASE_URL = "https://red.jinyedaojia.com"
    ADMIN_API_URL = f"{ADMIN_BASE_URL}/api"
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

    # ============ 今夜到家后台（旧系统参照） ============
    OLD_ADMIN_URL = "https://develop1.jinyedaojia.com"
    OLD_ADMIN_USERNAME = "admin"
    OLD_ADMIN_PASSWORD = "admin#$%"

    # ============ 超时配置 ============
    REQUEST_TIMEOUT = 30          # 普通请求超时(秒)
    PAYMENT_TIMEOUT = 60          # 支付相关超时(秒)
    UPLOAD_TIMEOUT = 120          # 文件上传超时(秒)
    QRCODE_EXPIRE_TIME = 15 * 60  # 二维码过期时间(秒): 15分钟
    VERIFY_CODE_EXPIRE = 48 * 60 * 60  # 验证码过期(秒): 48小时
    PAYMENT_ORDER_TIMEOUT = 5 * 60     # 支付订单超时(秒): 5分钟

    # ============ 分佣配置 ============
    # 默认测试用分佣比例
    DEFAULT_PLATFORM_RATIO = 50    # 平台比例 50%
    DEFAULT_AGENT_RATIO = 50       # 代理商比例 50%
    DEFAULT_LEVEL1_RATIO = 10      # 一级分销员 10%
    DEFAULT_LEVEL2_RATIO = 5       # 二级分销员 5%

    # ============ 金额限制 ============
    MAX_SINGLE_AMOUNT = 50000      # 单笔最大金额
    MIN_AMOUNT = 0.01              # 最小金额
    AMOUNT_PRECISION = 2           # 金额精度(小数位数)

    # ============ 折扣限制 ============
    MIN_DISCOUNT = 1.0             # 最低折扣 1折
    MAX_DISCOUNT = 9.9             # 最高折扣 9.9折

    # ============ 验证码安全 ============
    VERIFY_CODE_MAX_RETRY = 5      # 验证码最大错误次数
    VERIFY_CODE_LOCK_TIME = 15 * 60  # 锁定时间(秒): 15分钟

    # ============ 测试账号 ============
    # 用户端测试账号
    TEST_USERS = [
        {"name": "测试用户A", "phone": "13800000001"},
        {"name": "测试用户B", "phone": "13800000002"},
        {"name": "测试用户C", "phone": "13800000003"},
    ]

    # 商家测试账号
    TEST_MERCHANT_BRAND = {"name": "测试品牌主账号", "username": "test_brand"}
    TEST_MERCHANT_STORES = [
        {"name": "测试门店1", "username": "test_store1"},
        {"name": "测试门店2", "username": "test_store2"},
    ]

    # 代理商/分销员
    TEST_AGENT = {"name": "测试代理商", "username": "test_agent"}
    TEST_DISTRIBUTOR_L1 = {"name": "一级分销员", "username": "test_dist_l1"}
    TEST_DISTRIBUTOR_L2 = {"name": "二级分销员", "username": "test_dist_l2"}
