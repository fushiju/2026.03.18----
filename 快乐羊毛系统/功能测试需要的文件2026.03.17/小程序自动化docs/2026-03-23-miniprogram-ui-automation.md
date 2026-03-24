# 快乐羊毛小程序 UI 自动化 - 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 搭建基于 miniprogram-automator + Jest + POM 的小程序 UI 自动化框架，从项目骨架到登录模块完整落地。

**Architecture:** 四层架构（环境层 → 驱动层 → 公共能力层 → 测试用例层），Page Object Model 隔离页面操作与业务断言，全局 setup/teardown 管理开发者工具生命周期。

**Tech Stack:** miniprogram-automator >= 0.12.0, Jest, Node.js

**Spec:** `docs/superpowers/specs/2026-03-23-miniprogram-ui-automation-design.md`

---

## 文件结构总览

```
miniprogram-auto-test/
├── package.json                  # 创建：项目依赖与脚本
├── jest.config.js                # 创建：Jest 配置
├── global-setup.js               # 创建：全局启动开发者工具
├── global-teardown.js            # 创建：全局关闭开发者工具
├── config/
│   └── env.js                    # 创建：环境配置
├── helpers/
│   ├── launcher.js               # 创建：launch/connect 封装
│   ├── screenshot.js             # 创建：截图工具
│   └── wx-mock.js                # 创建：wx API Mock 工具
├── pages/
│   └── login.page.js             # 创建：登录页 Page Object
├── tests/
│   └── login.test.js             # 创建：登录模块测试用例
└── outputs/
    └── screenshots/              # 运行时自动创建
```

---

## Task 1：初始化项目与安装依赖

**Files:**
- Create: `miniprogram-auto-test/package.json`

- [ ] **Step 1: 创建项目目录**

```bash
mkdir -p C:/Users/Administrator/miniprogram-auto-test
cd C:/Users/Administrator/miniprogram-auto-test
```

- [ ] **Step 2: 初始化 package.json**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
npm init -y
```

- [ ] **Step 3: 安装依赖**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
npm install --save-dev miniprogram-automator jest
```

Expected: `node_modules` 目录生成，`package.json` 中包含 `miniprogram-automator` 和 `jest`。

- [ ] **Step 4: 验证 miniprogram-automator 版本 >= 0.12.0**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "const pkg = require('miniprogram-automator/package.json'); console.log(pkg.version)"
```

Expected: 输出版本号 >= 0.12.0。如果低于此版本会导致 CLI 命令格式不兼容。

- [ ] **Step 5: 在 package.json 中添加 test 脚本**

将 `package.json` 的 `scripts` 改为：

```json
{
  "scripts": {
    "test": "jest --runInBand --forceExit",
    "test:verbose": "jest --runInBand --forceExit --verbose"
  }
}
```

> `--runInBand`：串行执行，因为所有用例共享同一个开发者工具实例。
> `--forceExit`：防止 WebSocket 连接未完全关闭导致 Jest 挂起。

- [ ] **Step 6: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git init
git add package.json package-lock.json
git commit -m "chore: init project with miniprogram-automator and jest"
```

---

## Task 2：创建环境配置

**Files:**
- Create: `miniprogram-auto-test/config/env.js`

- [ ] **Step 1: 创建 config 目录和 env.js**

```js
// config/env.js
const path = require('node:path')

module.exports = {
  // 微信开发者工具 CLI 路径（Windows 默认）
  cliPath: process.env.WECHAT_DEVTOOLS_CLI
    || 'C:\\Program Files (x86)\\Tencent\\微信web开发者工具\\cli.bat',

  // 小程序项目目录（含 project.config.json 的目录）
  // 拿到开发同事的项目后，修改此路径或设置环境变量
  projectPath: process.env.MINIPROGRAM_PROJECT_PATH
    || 'C:\\miniprogram-project\\dist',

  // 启动超时（首次启动需要用户手动确认信任，给足 2 分钟）
  launchTimeout: Number(process.env.LAUNCH_TIMEOUT || 120000),

  // 自动化 WebSocket 端口（connect 模式用）
  autoPort: Number(process.env.WECHAT_AUTO_PORT || 9420),

  // 截图输出目录
  outputDir: path.resolve(__dirname, '../outputs/screenshots'),

  // 测试账号（根据小程序实际登录方式调整字段名）
  testAccount: {
    phone: process.env.TEST_PHONE || '13800138000',
    password: process.env.TEST_PWD || 'admin123',
  },
}
```

- [ ] **Step 2: 验证配置可加载**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "const c = require('./config/env'); console.log(JSON.stringify(c, null, 2))"
```

Expected: 输出完整配置 JSON，无报错。

- [ ] **Step 3: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add config/env.js
git commit -m "feat: add environment config with env var support"
```

---

## Task 3：创建启动器（launcher）

**Files:**
- Create: `miniprogram-auto-test/helpers/launcher.js`

- [ ] **Step 1: 创建 helpers 目录和 launcher.js**

```js
// helpers/launcher.js
const automator = require('miniprogram-automator')
const { spawnSync } = require('node:child_process')
const config = require('../config/env')

/**
 * 方式一：launch
 * 前提：开发者工具必须完全退出（Windows 下要在任务管理器确认进程已结束）
 * 首次运行会弹出「信任项目」确认框，需手动点击
 */
async function launch() {
  return automator.launch({
    cliPath: config.cliPath,
    projectPath: config.projectPath,
    timeout: config.launchTimeout,
  })
}

/**
 * 方式二：CLI v2 + connect
 * 适用于开发者工具已在运行的场景，不需要关闭工具
 * close() 只断开 WebSocket 连接，不会关闭开发者工具窗口
 */
async function connect() {
  const args = [
    'auto',
    '--project', config.projectPath,
    '--auto-port', String(config.autoPort),
  ]
  const result = spawnSync(config.cliPath, args, {
    encoding: 'utf8',
    timeout: 20000,
  })
  if (result.status !== 0) {
    throw new Error(
      `CLI auto 命令失败:\n${result.stdout || ''}\n${result.stderr || ''}`
    )
  }
  return automator.connect({
    wsEndpoint: `ws://127.0.0.1:${config.autoPort}`,
  })
}

module.exports = { launch, connect }
```

- [ ] **Step 2: 语法验证**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "require('./helpers/launcher'); console.log('launcher OK')"
```

Expected: 输出 `launcher OK`，无语法错误。

- [ ] **Step 3: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add helpers/launcher.js
git commit -m "feat: add launcher helper with launch and connect modes"
```

---

## Task 4：创建截图工具

**Files:**
- Create: `miniprogram-auto-test/helpers/screenshot.js`

- [ ] **Step 1: 创建 screenshot.js**

```js
// helpers/screenshot.js
const path = require('node:path')
const fs = require('node:fs/promises')
const config = require('../config/env')

/**
 * 截取当前小程序模拟器画面
 * @param {object} miniProgram - automator 返回的小程序实例
 * @param {string} name - 截图文件名（不含扩展名），支持子目录如 'login/TC-F-001'
 * @returns {string} 截图文件的绝对路径
 *
 * 注意：截图仅支持开发者工具模拟器，不支持真机
 */
async function takeScreenshot(miniProgram, name) {
  const filePath = path.join(config.outputDir, `${name}.png`)
  await fs.mkdir(path.dirname(filePath), { recursive: true })
  await miniProgram.screenshot({ path: filePath })
  return filePath
}

module.exports = { takeScreenshot }
```

- [ ] **Step 2: 语法验证**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "require('./helpers/screenshot'); console.log('screenshot OK')"
```

Expected: 输出 `screenshot OK`。

- [ ] **Step 3: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add helpers/screenshot.js
git commit -m "feat: add screenshot helper with auto directory creation"
```

---

## Task 5：创建 wx API Mock 工具

**Files:**
- Create: `miniprogram-auto-test/helpers/wx-mock.js`

- [ ] **Step 1: 创建 wx-mock.js**

```js
// helpers/wx-mock.js

/**
 * Mock wx.request，使其返回自定义数据
 * 注意：mockWxMethod 的函数体会被序列化执行，不能引用外部闭包变量
 *
 * @param {object} miniProgram - automator 返回的小程序实例
 * @param {object} responseData - 要返回的 data 字段内容
 * @param {number} [statusCode=200] - HTTP 状态码
 */
async function mockRequest(miniProgram, responseData, statusCode = 200) {
  // 因为函数体会被序列化，responseData 需要通过参数传入
  // 这里用简单对象形式传入 mock 结果
  await miniProgram.mockWxMethod('request', (options = {}) => {
    const res = {
      data: responseData,
      statusCode: statusCode,
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

/**
 * 恢复被 mock 的 wx.request
 * 必须在 afterAll 或 finally 中调用，防止污染后续用例
 */
async function restoreRequest(miniProgram) {
  await miniProgram.restoreWxMethod('request').catch(() => {})
}

/**
 * Mock 任意 wx 方法（通用）
 * @param {object} miniProgram
 * @param {string} methodName - 如 'getLocation', 'getStorage'
 * @param {*} result - 直接返回的结果对象
 */
async function mockWxMethod(miniProgram, methodName, result) {
  await miniProgram.mockWxMethod(methodName, result)
}

/**
 * 恢复任意被 mock 的 wx 方法
 */
async function restoreWxMethod(miniProgram, methodName) {
  await miniProgram.restoreWxMethod(methodName).catch(() => {})
}

module.exports = { mockRequest, restoreRequest, mockWxMethod, restoreWxMethod }
```

- [ ] **Step 2: 语法验证**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "require('./helpers/wx-mock'); console.log('wx-mock OK')"
```

Expected: 输出 `wx-mock OK`。

- [ ] **Step 3: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add helpers/wx-mock.js
git commit -m "feat: add wx API mock helper with request mock and restore"
```

---

## Task 6：创建 Jest 配置与全局 setup/teardown

**Files:**
- Create: `miniprogram-auto-test/jest.config.js`
- Create: `miniprogram-auto-test/global-setup.js`
- Create: `miniprogram-auto-test/global-teardown.js`

- [ ] **Step 1: 创建 jest.config.js**

```js
// jest.config.js
const config = require('./config/env')

module.exports = {
  // 测试文件匹配规则
  testMatch: ['**/tests/**/*.test.js'],

  // 全局启动/关闭开发者工具
  globalSetup: './global-setup.js',
  globalTeardown: './global-teardown.js',

  // 每个测试文件的超时（登录、页面跳转等操作需要较长时间）
  testTimeout: 60000,

  // 串行执行（所有用例共享一个开发者工具实例）
  // 注意：这里不设置 maxWorkers，由 npm script 的 --runInBand 控制
}
```

- [ ] **Step 2: 创建 global-setup.js**

```js
// global-setup.js
const { launch } = require('./helpers/launcher')

module.exports = async function globalSetup() {
  // 启动开发者工具，将 wsEndpoint 存入环境变量供各测试文件使用
  // 注意：globalSetup 和测试文件运行在不同进程
  // Jest globalSetup 不能直接传对象，需要通过 wsEndpoint 让测试文件自行 connect
  const miniProgram = await launch()
  const wsEndpoint = miniProgram.wsEndpoint || `ws://127.0.0.1:${require('./config/env').autoPort}`

  // 存入环境变量，测试文件通过 process.env 读取
  process.env.__MP_WS_ENDPOINT__ = wsEndpoint

  // 将 miniProgram 挂到 global 上，供 teardown 使用
  globalThis.__MP__ = miniProgram
}
```

- [ ] **Step 3: 创建 global-teardown.js**

```js
// global-teardown.js
module.exports = async function globalTeardown() {
  if (globalThis.__MP__) {
    await globalThis.__MP__.close().catch(() => {})
  }
}
```

- [ ] **Step 4: 语法验证**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "require('./jest.config.js'); console.log('jest config OK')"
node -e "require('./global-setup.js'); console.log('global-setup OK')"
node -e "require('./global-teardown.js'); console.log('global-teardown OK')"
```

Expected: 三个文件均输出 OK，无语法错误。

- [ ] **Step 5: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add jest.config.js global-setup.js global-teardown.js
git commit -m "feat: add Jest config with global setup and teardown"
```

---

## Task 7：创建登录页 Page Object

**Files:**
- Create: `miniprogram-auto-test/pages/login.page.js`

- [ ] **Step 1: 创建 pages 目录和 login.page.js**

```js
// pages/login.page.js

/**
 * 登录页 Page Object
 *
 * 注意：下面的选择器（.login-form, .phone-input 等）是占位符，
 * 拿到小程序项目后需要根据实际 WXML 结构替换为真实选择器。
 *
 * 如果输入框在自定义组件内部，需要先选组件再选内部元素：
 *   const component = await this.page.$('custom-input')
 *   const input = await component.$('input')
 */
class LoginPage {
  constructor(miniProgram) {
    this.mp = miniProgram
    this.page = null

    // === 选择器集中管理，拿到真实项目后只需改这里 ===
    this.selectors = {
      loginForm: '.login-form',      // 登录表单容器（用于 waitFor 判断页面加载完成）
      phoneInput: '.phone-input',    // 手机号输入框
      passwordInput: '.pwd-input',   // 密码输入框
      loginButton: '.login-btn',     // 登录按钮
      errorMessage: '.error-msg',    // 错误提示文字
      userNickname: '.user-nickname', // 登录后的用户昵称
    }
  }

  /** 打开登录页 */
  async open() {
    this.page = await this.mp.reLaunch('/pages/login/index')
    await this.page.waitFor(this.selectors.loginForm)
    return this
  }

  /** 输入手机号 */
  async inputPhone(phone) {
    const input = await this.page.$(this.selectors.phoneInput)
    if (!input) throw new Error(`未找到手机号输入框: ${this.selectors.phoneInput}`)
    await input.input(phone)
  }

  /** 输入密码 */
  async inputPassword(pwd) {
    const input = await this.page.$(this.selectors.passwordInput)
    if (!input) throw new Error(`未找到密码输入框: ${this.selectors.passwordInput}`)
    await input.input(pwd)
  }

  /** 点击登录按钮 */
  async tapLogin() {
    const btn = await this.page.$(this.selectors.loginButton)
    if (!btn) throw new Error(`未找到登录按钮: ${this.selectors.loginButton}`)
    await btn.tap()
    await this.page.waitFor(2000) // 等待登录请求完成，后续可替换为更精确的等待条件
  }

  /** 一步完成登录（输入手机号 + 密码 + 点击登录） */
  async loginAs(phone, pwd) {
    await this.inputPhone(phone)
    await this.inputPassword(pwd)
    await this.tapLogin()
  }

  /** 获取页面上的错误提示文字 */
  async getErrorMsg() {
    const el = await this.page.$(this.selectors.errorMessage)
    return el ? await el.text() : ''
  }

  /** 获取当前页面路径 */
  async getCurrentPath() {
    const current = await this.mp.currentPage()
    return current.path
  }

  /** 获取当前页面的 data */
  async getPageData() {
    return await this.page.data()
  }
}

module.exports = LoginPage
```

- [ ] **Step 2: 语法验证**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "require('./pages/login.page'); console.log('login page OK')"
```

Expected: 输出 `login page OK`。

- [ ] **Step 3: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add pages/login.page.js
git commit -m "feat: add LoginPage page object with centralized selectors"
```

---

## Task 8：创建登录模块测试用例

**Files:**
- Create: `miniprogram-auto-test/tests/login.test.js`

- [ ] **Step 1: 创建 tests 目录和 login.test.js**

```js
// tests/login.test.js
const automator = require('miniprogram-automator')
const LoginPage = require('../pages/login.page')
const { takeScreenshot } = require('../helpers/screenshot')
const config = require('../config/env')

let miniProgram
let loginPage

beforeAll(async () => {
  // 方式一：如果全局 setup 传了 wsEndpoint，用 connect
  if (process.env.__MP_WS_ENDPOINT__) {
    miniProgram = await automator.connect({
      wsEndpoint: process.env.__MP_WS_ENDPOINT__,
    })
  } else {
    // 方式二：独立启动（方便单独调试本文件）
    const { launch } = require('../helpers/launcher')
    miniProgram = await launch()
  }
  loginPage = new LoginPage(miniProgram)
}, config.launchTimeout)

afterAll(async () => {
  // 如果是独立启动的，关闭；connect 模式不关闭（由 global-teardown 负责）
  if (!process.env.__MP_WS_ENDPOINT__ && miniProgram) {
    await miniProgram.close().catch(() => {})
  }
})

describe('登录模块', () => {
  // 每个用例前都重新打开登录页，保证状态干净
  beforeEach(async () => {
    await loginPage.open()
  })

  test('TC-F-001: 正常登录 - 输入正确账号密码后跳转首页', async () => {
    await loginPage.loginAs(
      config.testAccount.phone,
      config.testAccount.password,
    )

    const currentPath = await loginPage.getCurrentPath()
    expect(currentPath).toContain('home') // 根据实际首页路径调整

    await takeScreenshot(miniProgram, 'login/TC-F-001_登录成功')
  })

  test('TC-E-001: 空手机号 - 点击登录提示错误', async () => {
    // 只输入密码，不输入手机号
    await loginPage.inputPassword(config.testAccount.password)
    await loginPage.tapLogin()

    const errorMsg = await loginPage.getErrorMsg()
    expect(errorMsg).toContain('请输入')

    await takeScreenshot(miniProgram, 'login/TC-E-001_空手机号')
  })

  test('TC-E-002: 空密码 - 点击登录提示错误', async () => {
    // 只输入手机号，不输入密码
    await loginPage.inputPhone(config.testAccount.phone)
    await loginPage.tapLogin()

    const errorMsg = await loginPage.getErrorMsg()
    expect(errorMsg).toContain('请输入')

    await takeScreenshot(miniProgram, 'login/TC-E-002_空密码')
  })

  test('TC-E-003: 错误密码 - 提示账号或密码错误', async () => {
    await loginPage.loginAs(config.testAccount.phone, 'wrongpassword')

    const errorMsg = await loginPage.getErrorMsg()
    expect(errorMsg).toContain('错误')

    await takeScreenshot(miniProgram, 'login/TC-E-003_错误密码')
  })
})
```

- [ ] **Step 2: 语法验证**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "require('./tests/login.test.js'); console.log('syntax OK')" 2>&1 || echo "语法检查完成（Jest 相关报错可忽略，只要没有 SyntaxError）"
```

Expected: 无 `SyntaxError`。可能有 Jest 全局变量（describe/test）未定义的错误，这是正常的，Jest 运行时会注入。

- [ ] **Step 3: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add tests/login.test.js
git commit -m "feat: add login module test cases (TC-F-001, TC-E-001~003)"
```

---

## Task 9：添加 .gitignore 和收尾

**Files:**
- Create: `miniprogram-auto-test/.gitignore`

- [ ] **Step 1: 创建 .gitignore**

```
node_modules/
outputs/
*.png
```

- [ ] **Step 2: 创建 outputs 目录占位**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
mkdir -p outputs/screenshots
```

- [ ] **Step 3: 验证完整目录结构**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
find . -not -path './node_modules/*' -not -path './.git/*' | sort
```

Expected:
```
.
./config
./config/env.js
./global-setup.js
./global-teardown.js
./helpers
./helpers/launcher.js
./helpers/screenshot.js
./helpers/wx-mock.js
./jest.config.js
./outputs
./outputs/screenshots
./package-lock.json
./package.json
./pages
./pages/login.page.js
./tests
./tests/login.test.js
./.gitignore
```

- [ ] **Step 4: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add .gitignore
git commit -m "chore: add gitignore and finalize project structure"
```

---

## Task 10：连通性验证（需要小程序项目文件）

> 此任务在拿到开发同事的小程序编译产物后执行。

**前置条件：**
1. 微信开发者工具已安装
2. 开发者工具 → 设置 → 安全设置 → 已开启服务端口
3. 已获取小程序编译产物目录，并更新 `config/env.js` 中的 `projectPath`
4. 已获取小程序页面的真实选择器，并更新 `pages/login.page.js` 中的 `selectors`

- [ ] **Step 1: 更新 config/env.js 中的 projectPath**

将 `projectPath` 改为开发同事提供的实际目录路径（含 `project.config.json` 的目录）。

- [ ] **Step 2: 更新 login.page.js 中的选择器**

根据小程序实际 WXML 结构，替换 `selectors` 对象中的占位选择器。

- [ ] **Step 3: 确保开发者工具完全退出**

Windows 下在任务管理器中确认没有"微信开发者工具"相关进程。

- [ ] **Step 4: 运行独立连通测试**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
node -e "
const { launch } = require('./helpers/launcher');
(async () => {
  const mp = await launch();
  console.log('连接成功');
  const page = await mp.reLaunch('/pages/login/index');
  console.log('页面路径:', page.path);
  await mp.screenshot({ path: './outputs/screenshots/connectivity-test.png' });
  console.log('截图成功');
  await mp.close();
  console.log('关闭成功');
})().catch(e => { console.error('失败:', e.message); process.exit(1); });
"
```

Expected:
```
连接成功
页面路径: pages/login/index
截图成功
关闭成功
```

- [ ] **Step 5: 运行 Jest 测试套件**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
npm test
```

Expected: 登录模块用例运行通过（或根据实际页面行为调整断言后通过）。

- [ ] **Step 6: Commit**

```bash
cd C:/Users/Administrator/miniprogram-auto-test
git add config/env.js pages/login.page.js
git commit -m "feat: update config and selectors for actual miniprogram project"
```

---

## 后续扩展方向（拿到项目并验证 Task 10 后）

以下为第二、三阶段的工作方向，不在本次实施范围内：

1. **逐模块添加 Page Object 和用例** — 按业务优先级，每个模块一个 `pages/xxx.page.js` + `tests/xxx.test.js`
2. **引入 Mock** — 对网络异常、空数据、边界场景使用 `wx-mock.js` 进行覆盖
3. **截图回归** — 建立 baseline 截图，对比运行结果
4. **接入 CI** — 在构建服务器上安装开发者工具，配合 `npm test` 自动执行
