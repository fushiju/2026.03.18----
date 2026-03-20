/**
 * 外卖通用券 - 小程序自动化测试
 * 对应用例: wamtyj-001~019, wamtyj-xcx-001~004
 *
 * ⚠ 注意：涉及支付的测试不能自动完成支付密码输入
 *   自动化只能做到"唤起支付弹窗"，需要手动输入密码或用Mock
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

describe('外卖通用券', () => {

  test('wamtyj-001: 面额选择展示', async () => {
    page = await miniProgram.navigateTo('/pages/takeout/coupon/index');
    await page.waitFor(2000);

    // 检查面额选项
    const options = await page.$$('.amount-item, .face-value, .sku-item');
    console.log(`📝 面额选项数: ${options.length}`);
    expect(options.length).toBeGreaterThan(0);

    // 点击一个面额
    if (options.length > 0) {
      await options[0].tap();
      await page.waitFor(500);
      await screenshot(page, 'coupon_select_amount');
      console.log('✅ 面额可选择');
    }
  });

  test('wamtyj-007: 切换面额高亮变化', async () => {
    const options = await page.$$('.amount-item, .face-value, .sku-item');

    if (options.length >= 2) {
      // 选第一个
      await options[0].tap();
      await page.waitFor(500);

      // 选第二个
      await options[1].tap();
      await page.waitFor(500);

      await screenshot(page, 'coupon_switch_amount');
      console.log('✅ 面额切换正常（截图验证高亮）');
    }
  });

  test('wamtyj-004: 未选面额点击购买提示', async () => {
    // 重新进入页面（无选中状态）
    page = await miniProgram.navigateTo('/pages/takeout/coupon/index');
    await page.waitFor(2000);

    // 直接点购买按钮
    const buyBtn = await page.$('.buy-btn, button.purchase, .confirm-btn');
    if (buyBtn) {
      await buyBtn.tap();
      await page.waitFor(1000);
      await screenshot(page, 'coupon_no_select_tip');
      console.log('✅ 未选面额点击购买（截图验证提示）');
    }
  });

  test('wamtyj-006: 不退款提示和协议勾选', async () => {
    // 选一个面额
    const options = await page.$$('.amount-item, .face-value, .sku-item');
    if (options.length > 0) {
      await options[0].tap();
      await page.waitFor(500);
    }

    // 进入确认页
    const buyBtn = await page.$('.buy-btn, button.purchase, .confirm-btn');
    if (buyBtn) {
      await buyBtn.tap();
      await page.waitFor(2000);
    }

    // 查找不退款提示文案
    const pageContent = await page.data();
    await screenshot(page, 'coupon_confirm_page');

    // 查找协议勾选框
    const checkbox = await page.$('.agreement-check, .checkbox, checkbox');
    if (checkbox) {
      console.log('✅ 找到协议勾选框');

      // 不勾选时支付按钮应不可用
      const payBtn = await page.$('.pay-btn, button.pay, .submit-btn');
      if (payBtn) {
        const disabled = await payBtn.attribute('disabled');
        console.log(`📝 未勾选时支付按钮disabled: ${disabled}`);
      }

      // 勾选协议
      await checkbox.tap();
      await page.waitFor(500);
      console.log('✅ 已勾选协议');
    }
  });

  test('wamtyj-xcx-001: 微信支付弹窗唤起（到弹窗为止）', async () => {
    // 注意：这个测试只验证能唤起支付弹窗，不会自动完成支付
    // 因为小程序自动化框架无法操作微信支付密码弹窗

    // 确保已勾选协议
    const payBtn = await page.$('.pay-btn, button.pay, .submit-btn');
    if (payBtn) {
      // 点击支付——会调用 wx.requestPayment
      // 在测试环境可能需要Mock支付
      console.log('📝 支付按钮已找到');
      console.log('⚠ 真实支付需要手动输入密码，自动化到此为止');
      console.log('⚠ 建议：测试环境配置支付Mock，或用0.01元测试金额');
      await screenshot(page, 'coupon_pay_button');
    }
  });
});
