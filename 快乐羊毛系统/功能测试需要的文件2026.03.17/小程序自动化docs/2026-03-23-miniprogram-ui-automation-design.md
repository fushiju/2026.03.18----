# 快乐羊毛小程序 UI 自动化设计方案

## 1. 背景与目标

### 1.1 背景
- 快乐羊毛系统包含 Web 后台管理端和微信小程序端
- 后台 Web 端已有 Playwright 自动化基础
- 小程序端已有手工测试用例文档，尚未实现自动化
- 小程序源码在开发同事处，本地暂无编译产物

### 1.2 目标
- 基于 `miniprogram-automator` 搭建小程序 UI 自动化框架
- 将已有的手工测试用例逐步转化为自动化用例
- 为后续持续集成和回归测试打下基础

### 1.3 技术选型
| 项 | 选择 | 理由 |
|---|---|---|
| 自动化驱动 | miniprogram-automator >= 0.12.0 | 官方 SDK，贴近真实小程序运行环境 |
| 测试框架 | Jest | 与后台自动化统一技术栈，生态成熟 |
| 设计模式 | Page Object Model (POM) | 页面操作与用例逻辑分离，维护成本低 |
| 运行环境 | 微信开发者工具模拟器 | miniprogram-automator 仅支持模拟器 |

---

## 2. 整体架构

```
┌─────────────────────────────────────────────┐
│            小程序 UI 自动化框架               │
├──────────────┬──────────────────────────────┤
│  测试用例层   │  Jest test suites (.test.js) │
├──────────────┼──────────────────────────────┤
│  页面对象层   │  Page Object Model (POM)     │
│              │  每个页面/组件封装为一个类      │
├──────────────┼──────────────────────────────┤
│  公共能力层   │  登录、截图、等待、Mock 工具   │
├──────────────┼──────────────────────────────┤
│  驱动层      │  miniprogram-automator        │
│              │  launch / connect 开发者工具   │
├──────────────┼──────────────────────────────┤
│  环境层      │  微信开发者工具 + 小程序项目    │
└──────────────┴──────────────────────────────┘
```

---

## 3. 项目目录结构

```
miniprogram-auto-test/
├── config/
│   └── env.js                    # 环境配置（CLI路径、项目路径、超时等）
├── pages/                        # Page Object 层
│   ├── login.page.js             # 登录页
│   ├── home.page.js              # 首页
│   └── ...                       # 其他页面按需添加
├── helpers/
│   ├── launcher.js               # 启动/连接开发者工具的封装
│   ├── screenshot.js             # 截图工具（自动按用例名保存）
│   └── wx-mock.js                # 常用 wx API Mock 封装
├── tests/                        # 测试用例层
│   ├── login.test.js             # 登录模块用例
│   ├── home.test.js              # 首页模块用例
│   └── ...                       # 按模块组织
├── outputs/                      # 运行产物
│   └── screenshots/              # 截图输出
├── jest.config.js                # Jest 配置
├── global-setup.js               # 全局 beforeAll：启动小程序
├── global-teardown.js            # 全局 afterAll：关闭小程序
└── package.json
```

---

## 4. 核心模块设计

### 4.1 环境配置 (config/env.js)

通过环境变量管理，不同机器免改代码：

```js
module.exports = {
  // 微信开发者工具 CLI 路径
  cliPath: process.env.WECHAT_DEVTOOLS_CLI
    || 'C:\\Program Files (x86)\\Tencent\\微信web开发者工具\\cli.bat',

  // 小程序项目目录（开发者工具实际打开的目录，含 project.config.json）
  projectPath: process.env.MINIPROGRAM_PROJECT_PATH
    || 'C:\\path\\to\\miniprogram\\dist',

  // 启动超时（首次启动 + 信任确认需要较长时间）
  launchTimeout: Number(process.env.LAUNCH_TIMEOUT || 120000),

  // 自动化 WebSocket 端口（connect 模式用）
  autoPort: Number(process.env.WECHAT_AUTO_PORT || 9420),

  // 截图输出目录
  outputDir: process.env.OUTPUT_DIR || './outputs/screenshots',

  // 测试账号
  testAccount: {
    phone: process.env.TEST_PHONE || '13800138000',
    password: process.env.TEST_PWD || 'admin123',
  },
}
```

### 4.2 启动器 (helpers/launcher.js)

封装两种连接方式，自动选择：

```js
const automator = require('miniprogram-automator')
const { spawnSync } = require('node:child_process')
const config = require('../config/env')

// 方式一：launch（开发者工具必须完全退出）
async function launch() {
  return automator.launch({
    cliPath: config.cliPath,
    projectPath: config.projectPath,
    timeout: config.launchTimeout,
  })
}

// 方式二：CLI v2 + connect（开发者工具已在运行）
async function connect() {
  const args = ['auto', '--project', config.projectPath,
                '--auto-port', String(config.autoPort)]
  const result = spawnSync(config.cliPath, args,
    { encoding: 'utf8', timeout: 20000 })
  if (result.status !== 0) {
    throw new Error(`CLI auto 失败:\n${result.stdout}\n${result.stderr}`)
  }
  return automator.connect({
    wsEndpoint: `ws://127.0.0.1:${config.autoPort}`,
  })
}

module.exports = { launch, connect }
```

### 4.3 Page Object 示例 (pages/login.page.js)

```js
class LoginPage {
  constructor(miniProgram) {
    this.mp = miniProgram
    this.page = null
  }

  async open() {
    this.page = await this.mp.reLaunch('/pages/login/index')
    await this.page.waitFor('.login-form')
    return this
  }

  async inputPhone(phone) {
    const input = await this.page.$('.phone-input')
    await input.input(phone)
  }

  async inputPassword(pwd) {
    const input = await this.page.$('.pwd-input')
    await input.input(pwd)
  }

  async tapLogin() {
    const btn = await this.page.$('.login-btn')
    await btn.tap()
    await this.page.waitFor(2000)
  }

  async loginAs(phone, pwd) {
    await this.inputPhone(phone)
    await this.inputPassword(pwd)
    await this.tapLogin()
  }

  async getErrorMsg() {
    const el = await this.page.$('.error-msg')
    return el ? await el.text() : ''
  }

  async getCurrentPath() {
    const current = await this.mp.currentPage()
    return current.path
  }
}

module.exports = LoginPage
```

### 4.4 测试用例示例 (tests/login.test.js)

```js
const { launch } = require('../helpers/launcher')
const LoginPage = require('../pages/login.page')
const config = require('../config/env')

let miniProgram
let loginPage

beforeAll(async () => {
  miniProgram = await launch()
  loginPage = new LoginPage(miniProgram)
}, config.launchTimeout)

afterAll(async () => {
  if (miniProgram) await miniProgram.close()
})

describe('登录模块', () => {
  test('TC-F-001: 正常登录 - 跳转首页', async () => {
    await loginPage.open()
    await loginPage.loginAs(config.testAccount.phone, config.testAccount.password)
    expect(await loginPage.getCurrentPath()).toBe('pages/home/index')
  })

  test('TC-E-001: 空手机号 - 提示错误', async () => {
    await loginPage.open()
    await loginPage.inputPassword('admin123')
    await loginPage.tapLogin()
    expect(await loginPage.getErrorMsg()).toContain('请输入')
  })
})
```

### 4.5 截图工具 (helpers/screenshot.js)

```js
const path = require('node:path')
const fs = require('node:fs/promises')
const config = require('../config/env')

async function takeScreenshot(miniProgram, name) {
  const dir = config.outputDir
  await fs.mkdir(dir, { recursive: true })
  const filePath = path.join(dir, `${name}.png`)
  await miniProgram.screenshot({ path: filePath })
  return filePath
}

module.exports = { takeScreenshot }
```

### 4.6 wx API Mock 工具 (helpers/wx-mock.js)

```js
// Mock wx.request 返回自定义数据
async function mockRequest(miniProgram, responseData) {
  await miniProgram.mockWxMethod('request', (options = {}) => {
    const res = {
      data: responseData,
      statusCode: 200,
      header: { 'content-type': 'application/json' },
      cookies: [],
      errMsg: 'request:ok',
    }
    Promise.resolve().then(() => {
      if (typeof options.success === 'function') options.success(res)
      if (typeof options.complete === 'function') options.complete(res)
    })
    return {
      abort() {},
      onHeadersReceived() {},
      offHeadersReceived() {},
      onChunkReceived() {},
      offChunkReceived() {},
    }
  })
}

async function restoreRequest(miniProgram) {
  await miniProgram.restoreWxMethod('request').catch(() => {})
}

module.exports = { mockRequest, restoreRequest }
```

---

## 5. 测试执行流程

```
jest 启动
  │
  ├── global-setup.js
  │     └── automator.launch() 启动开发者工具
  │         将 miniProgram 实例存入全局
  │
  ├── login.test.js
  │     ├── beforeAll → 拿到 miniProgram，创建 LoginPage
  │     ├── test TC-F-001 → open → loginAs → 断言跳转 → 截图
  │     ├── test TC-E-001 → open → 空输入 → 断言错误提示
  │     └── afterAll → 清理
  │
  ├── home.test.js
  │     ├── beforeAll → loginPage.loginAs() 确保已登录
  │     ├── test → homePage 操作 → 断言
  │     └── afterAll → 清理
  │
  └── global-teardown.js
        └── miniProgram.close() 关闭开发者工具
```

---

## 6. 登录状态处理策略

| 场景 | 策略 |
|---|---|
| 登录模块用例 | 每个 case 主动 reLaunch 到登录页，独立测试 |
| 其他模块用例 | beforeAll 里统一调用 loginAs() 完成登录，后续用例共享登录态 |
| 需要跳过登录 | 通过 mockWxMethod('request') 注入 token，直接访问目标页 |

---

## 7. 等待策略

按优先级使用：

| 优先级 | 方式 | 适用场景 |
|--------|------|---------|
| 1（优先） | `page.waitFor('.选择器')` | 等待目标元素出现 |
| 2（次选） | `page.waitFor(() => 条件)` | 等待异步数据加载完成 |
| 3（兜底） | `page.waitFor(500)` | 短时间兜底，仅在前两种不适用时使用 |

---

## 8. 截图策略

```
outputs/screenshots/
  ├── login/
  │   ├── TC-F-001_登录成功.png
  │   ├── TC-E-001_空手机号错误提示.png
  │   └── ...
  └── home/
      └── ...
```

- 每个用例关键节点自动截图
- 失败时自动截图用于排查
- 截图仅支持开发者工具模拟器，不支持真机

---

## 9. 自定义组件选择器规则

小程序中 `page.$()` 不能穿透自定义组件边界：

```js
// 错误：直接从页面查组件内部元素
const input = await page.$('form-panel input')  // 找不到

// 正确：先选组件，再在组件作用域内查找
const panel = await page.$('form-panel')
const input = await panel.$('input')
```

编写 Page Object 时需注意页面中哪些是自定义组件，分层查找。

---

## 10. 落地前置条件清单

| 序号 | 前置条件 | 状态 |
|------|---------|------|
| 1 | 安装微信开发者工具 | 待确认 |
| 2 | 开发者工具 → 设置 → 安全设置 → 开启服务端口 | 待操作 |
| 3 | 从开发同事获取小程序编译产物目录（含 project.config.json） | 待获取 |
| 4 | 获取小程序页面路径清单 | 待获取 |
| 5 | 获取关键页面的选择器（class 名/组件名） | 待获取 |
| 6 | 确认是否使用了自定义组件及嵌套关系 | 待确认 |
| 7 | 获取小程序端测试账号 | 待获取 |
| 8 | 安装 miniprogram-automator >= 0.12.0 | 待安装 |

---

## 11. 分阶段落地计划

### 第一阶段：环境搭建 + 登录模块
- 搭建项目骨架（目录结构、配置、Jest）
- 完成 launcher 封装，验证 launch/connect 连通性
- 编写 LoginPage，实现登录模块全部用例自动化
- 产出：登录模块可自动运行并输出截图

### 第二阶段：核心业务模块
- 根据小程序实际功能，逐模块编写 Page Object 和用例
- 优先覆盖高优先级用例（High）
- 建立截图基线

### 第三阶段：稳定性与扩展
- 处理用例不稳定问题（等待策略调优、重试机制）
- 引入 Mock 覆盖网络异常、边界场景
- 可选：接入 CI，自动运行回归

---

## 12. 常见问题与排障

| 问题 | 排查方向 |
|------|---------|
| launch 超时/失败 | SDK 版本 >= 0.12.0？开发者工具已退出？服务端口已开启？ |
| 选不到元素 | 选择器是否稳定？是否在自定义组件内？页面是否仍在渲染？ |
| Mock 没生效 | 是否在页面请求前安装了 Mock？是否有前一轮残留？ |
| 截图失败 | 是否在模拟器环境？页面是否已稳定？输出目录是否可写？ |
| launch 和已运行的工具冲突 | 改用 CLI v2 + connect 方式 |
