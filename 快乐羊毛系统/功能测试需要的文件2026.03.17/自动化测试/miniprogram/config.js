/**
 * 小程序自动化配置
 *
 * 使用前必须：
 * 1. 安装微信开发者工具
 * 2. 打开开发者工具 → 设置 → 安全设置 → 开启"服务端口"
 * 3. 如果有源码：填 projectPath
 * 4. 如果没源码：用 connect() 连接已打开的项目
 */
module.exports = {
  // 微信开发者工具CLI路径
  cliPath: 'D:/微信开发者工具/微信web开发者工具/cli.bat',

  // 小程序项目路径（有源码时填，没源码留空）
  projectPath: '',  // 例: 'D:/projects/klym-miniprogram'

  // 连接已打开的开发者工具（没源码时用这种方式）
  wsEndpoint: '',  // 开发者工具控制台会显示 ws://127.0.0.1:xxxx

  // 超时设置
  launchTimeout: 30000,
  operationTimeout: 10000,
};
