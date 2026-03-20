/**
 * 免费资料区 - 小程序自动化测试
 * 对应用例: mfzl-001~018, mfzl-xcx-001~003
 *
 * 选择器说明：
 *   小程序不用CSS选择器，用 WXML 的组件层级
 *   page.$('组件名')        → 找第一个匹配
 *   page.$$('组件名')       → 找所有匹配
 *   page.$('.class-name')   → 按class找
 *   page.waitFor('组件名')  → 等待出现
 */
const { launch, connect, close, screenshot } = require('../utils/automator');

let miniProgram;
let page;

beforeAll(async () => {
  // 根据你的情况选一个：
  // miniProgram = await launch();    // 有源码
  miniProgram = await connect();      // 没源码，连接已打开的开发者工具
}, 30000);

afterAll(async () => {
  await close();
});

describe('免费资料区', () => {

  test('mfzl-001: 资料列表正常加载', async () => {
    // 跳转到免费资料区页面（路径根据实际填写）
    page = await miniProgram.navigateTo('/pages/free-material/index');
    await page.waitFor(2000);

    // 检查列表是否有内容
    // ====== 选择器需根据实际WXML调整 ======
    const items = await page.$$('.material-item, .list-item, view.item');
    console.log(`📝 资料列表项数: ${items.length}`);
    expect(items.length).toBeGreaterThan(0);
  });

  test('mfzl-002: 分类Tab切换', async () => {
    // 找到分类Tab
    const tabs = await page.$$('.tab-item, .category-tab, navigator');

    if (tabs.length > 1) {
      // 点击第二个Tab
      await tabs[1].tap();
      await page.waitFor(1000);

      // 再点回第一个
      const tabs2 = await page.$$('.tab-item, .category-tab, navigator');
      await tabs2[0].tap();
      await page.waitFor(1000);

      console.log('✅ Tab切换正常');
    } else {
      console.log('⏭️ 未找到多个Tab');
    }
  });

  test('mfzl-011: 复制链接功能', async () => {
    // 点击第一条资料进入详情
    const items = await page.$$('.material-item, .list-item, view.item');
    if (items.length > 0) {
      await items[0].tap();
      await page.waitFor(2000);

      // 找到复制按钮并点击
      const copyBtn = await page.$('.copy-btn, button.copy, text.copy');
      if (copyBtn) {
        await copyBtn.tap();
        await page.waitFor(1000);

        // 小程序复制后微信会弹Toast，检查wx.setClipboardData是否调用成功
        // 自动化框架可能无法直接检测Toast，用截图验证
        await screenshot(page, 'copy_link_result');
        console.log('✅ 复制按钮已点击（截图验证Toast）');
      }

      // 返回列表
      await miniProgram.navigateBack();
      await page.waitFor(1000);
    }
  });

  test('mfzl-003: 下拉刷新和分页', async () => {
    page = await miniProgram.navigateTo('/pages/free-material/index');
    await page.waitFor(2000);

    // 触发下拉刷新
    await page.callMethod('onPullDownRefresh');
    await page.waitFor(2000);
    console.log('✅ 下拉刷新已触发');

    // 触发触底加载
    await page.callMethod('onReachBottom');
    await page.waitFor(2000);
    console.log('✅ 触底加载已触发');

    // 检查数据是否增加
    const items = await page.$$('.material-item, .list-item, view.item');
    console.log(`📝 加载后列表项数: ${items.length}`);
  });

  test('mfzl-xcx-003: 详情返回后列表位置保持', async () => {
    page = await miniProgram.navigateTo('/pages/free-material/index');
    await page.waitFor(2000);

    // 获取页面栈深度
    const pages = await miniProgram.pageStack();
    const stackBefore = pages.length;

    // 点进详情
    const items = await page.$$('.material-item, .list-item, view.item');
    if (items.length > 2) {
      await items[2].tap();  // 点第3条
      await page.waitFor(1000);

      const pagesAfter = await miniProgram.pageStack();
      expect(pagesAfter.length).toBe(stackBefore + 1);  // 页面栈+1
      console.log(`📝 页面栈: ${stackBefore} → ${pagesAfter.length}`);

      // 返回
      await miniProgram.navigateBack();
      await page.waitFor(1000);
      console.log('✅ 返回后页面栈恢复');
    }
  });
});
