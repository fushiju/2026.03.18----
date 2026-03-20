# 快乐羊毛 UI自动化测试

## 项目结构

```
自动化测试/
├── admin-web/              # 管理后台自动化（Playwright + Python）
│   ├── conftest.py         # pytest fixtures（登录、浏览器初始化）
│   ├── config.py           # 环境配置
│   ├── pages/              # Page Object 页面封装
│   │   ├── login_page.py
│   │   ├── order_page.py
│   │   ├── commission_page.py
│   │   ├── product_warehouse_page.py
│   │   └── refund_page.py
│   ├── utils/              # 工具类
│   │   └── helpers.py
│   └── tests/              # 测试用例
│       ├── test_01_login.py
│       ├── test_02_order.py
│       ├── test_03_commission.py
│       ├── test_04_product_warehouse.py
│       ├── test_05_refund.py
│       └── test_06_security.py
│
├── miniprogram/            # 小程序自动化（miniprogram-automator + Jest）
│   ├── jest.config.js
│   ├── config.js           # 开发者工具路径、项目路径
│   ├── pages/              # 页面操作封装
│   │   ├── home.js
│   │   ├── order.js
│   │   └── cashier.js
│   ├── utils/
│   │   └── automator.js    # 启动/连接小程序
│   └── tests/
│       ├── free_material.test.js
│       ├── takeout_coupon.test.js
│       ├── restaurant_discount.test.js
│       └── personal_center.test.js
│
├── requirements.txt        # Python依赖
├── package.json            # Node.js依赖
└── README.md               # 本文件
```

## 快速开始

### 管理后台（先搞这个）

```bash
cd admin-web
pip install -r ../requirements.txt
playwright install chromium
pytest tests/ -v --headed     # --headed 看浏览器操作过程
pytest tests/ -v              # 无头模式，跑CI
```

### 小程序（需要开发者工具+源码或体验版）

```bash
cd miniprogram
npm install
npx jest tests/               # 需要先启动微信开发者工具
```
