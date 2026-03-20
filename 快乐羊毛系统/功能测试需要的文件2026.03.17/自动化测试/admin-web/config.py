# -*- coding: utf-8 -*-
"""环境配置"""

# 测试环境
BASE_URL = "https://red.jinyedaojia.com"
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# 超时设置(毫秒)
DEFAULT_TIMEOUT = 10000
NAVIGATION_TIMEOUT = 30000

# 截图目录
SCREENSHOT_DIR = "screenshots"

# 浏览器配置
HEADLESS = False  # True=无头模式跑CI, False=有界面看操作过程
SLOW_MO = 500     # 每步间隔毫秒，调试时设500看得清，跑CI设0
