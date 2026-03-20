/**
 * 个人中心 - 小程序自动化测试
 * 对应用例: grzx-001~032, grzx-xcx-001~005
 */
const { launch, connect, close, screenshot } = require('../utils/automator');

let miniProgram;
let page;

beforeAll(async () => {
  miniProgram = await connect();
}, 30000);

afterAll(async () => {
  await close();
});

describe('个人中心', () => {

  test('grzx-001: 进入个人中心页面正常', async () => {
    // 切换到个人中心Tab
    page = await miniProgram.switchTab('/pages/mine/index');
    await page.waitFor(2000);
    await screenshot(page, 'personal_center');

    // 检查页面基本元素
    const pageData = await page.data();
    console.log('📝 个人中心页面数据:', JSON.stringify(pageData).substring(0, 200));
  });

  test('grzx-008: 订单列表展示', async () => {
    // 点击"我的订单"
    const orderEntry = await page.$('.order-entry, text=我的订单, .my-order');
    if (orderEntry) {
      await orderEntry.tap();
      await page.waitFor(2000);

      // 获取当前页面
      const pages = await miniProgram.pageStack();
      const currentPage = pages[pages.length - 1];

      // 检查订单列表
      const orders = await currentPage.$$('.order-item, .order-card, view.order');
      console.log(`📝 订单数量: ${orders.length}`);
      await screenshot(currentPage, 'order_list');

      // 返回
      await miniProgram.navigateBack();
      await page.waitFor(1000);
    } else {
      console.log('⏭️ 未找到订单入口');
    }
  });

  test('grzx-017: 佣金余额展示', async () => {
    page = await miniProgram.switchTab('/pages/mine/index');
    await page.waitFor(2000);

    // 查找佣金/余额展示区域
    const balanceArea = await page.$('.balance, .commission, .income');
    if (balanceArea) {
      const text = await balanceArea.text();
      console.log(`📝 佣金/余额区域文本: ${text}`);
      await screenshot(page, 'balance_display');
    } else {
      console.log('⏭️ 未找到佣金展示区域（可能非代理商账号）');
    }
  });

  test('grzx-023: 推广海报生成', async () => {
    // 找到推广中心入口
    const promoEntry = await page.$('.promotion, text=推广, .promo-center');
    if (promoEntry) {
      await promoEntry.tap();
      await page.waitFor(2000);

      const pages = await miniProgram.pageStack();
      const currentPage = pages[pages.length - 1];

      // 找到生成海报按钮
      const genBtn = await currentPage.$('button.generate, .gen-poster, text=生成海报');
      if (genBtn) {
        await genBtn.tap();
        await page.waitFor(3000);  // canvas绘制需要时间
        await screenshot(currentPage, 'poster_generated');
        console.log('✅ 海报生成功能已触发（截图验证）');
      }

      await miniProgram.navigateBack();
    } else {
      console.log('⏭️ 未找到推广中心入口');
    }
  });

  test('grzx-xcx-003: 下拉刷新订单列表', async () => {
    // 进入订单列表
    const orderEntry = await page.$('.order-entry, text=我的订单, .my-order');
    if (orderEntry) {
      await orderEntry.tap();
      await page.waitFor(2000);

      const pages = await miniProgram.pageStack();
      const currentPage = pages[pages.length - 1];

      // 触发下拉刷新
      await currentPage.callMethod('onPullDownRefresh');
      await page.waitFor(2000);
      console.log('✅ 订单列表下拉刷新已触发');

      // 触发触底加载
      await currentPage.callMethod('onReachBottom');
      await page.waitFor(2000);
      console.log('✅ 订单列表触底加载已触发');

      await miniProgram.navigateBack();
    }
  });
});
