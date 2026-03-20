/**
 * 小程序自动化启动/连接工具
 *
 * 两种用法：
 * 1. 有源码 → launch() 自动打开项目
 * 2. 没源码 → connect() 连接已打开的开发者工具
 */
const automator = require('miniprogram-automator');
const config = require('../config');

let miniProgram = null;

/**
 * 方式1：有源码，自动启动项目
 */
async function launch() {
  if (miniProgram) return miniProgram;

  if (!config.projectPath) {
    throw new Error('config.projectPath 未配置，请填入小程序项目路径');
  }

  miniProgram = await automator.launch({
    cliPath: config.cliPath,
    projectPath: config.projectPath,
  });

  console.log('✅ 小程序已启动');
  return miniProgram;
}

/**
 * 方式2：没源码，连接已打开的开发者工具
 *
 * 步骤：
 * 1. 手动打开微信开发者工具，打开小程序项目
 * 2. 在开发者工具菜单 → 设置 → 安全设置 → 开启服务端口
 * 3. 运行测试，会自动连接
 */
async function connect() {
  if (miniProgram) return miniProgram;

  miniProgram = await automator.connect({
    wsEndpoint: config.wsEndpoint || 'ws://127.0.0.1:9420',
  });

  console.log('✅ 已连接到开发者工具');
  return miniProgram;
}

/**
 * 获取当前小程序实例（launch或connect后调用）
 */
function getMiniProgram() {
  return miniProgram;
}

/**
 * 关闭小程序
 */
async function close() {
  if (miniProgram) {
    await miniProgram.close();
    miniProgram = null;
    console.log('小程序已关闭');
  }
}

/**
 * 截图保存
 */
async function screenshot(page, name) {
  const path = `screenshots/${name}.png`;
  await page.screenshot({ path });
  console.log(`  📸 截图: ${path}`);
  return path;
}

module.exports = { launch, connect, getMiniProgram, close, screenshot };
