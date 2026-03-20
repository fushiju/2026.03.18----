# -*- coding: utf-8 -*-
"""
🔍 页面探测器 + 代码生成器
在你的电脑上运行，它会：
1. 自动打开浏览器访问后台
2. 自动破解前端验证码并登录
3. 逐个点击菜单，抓取每个页面的HTML结构
4. 输出每个页面的表单、按钮、表格等元素选择器
5. 你把输出结果发给我，我帮你填代码

用法：
  cd admin-web
  python explore_and_generate.py

⚠ 必须在你自己的电脑上运行（不是远程服务器），因为需要打开浏览器窗口
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

BASE_URL = "https://red.jinyedaojia.com"
USERNAME = "admin"
PASSWORD = "admin123"

os.makedirs('screenshots', exist_ok=True)
os.makedirs('page_structures', exist_ok=True)


def extract_captcha(page):
    """从Vue组件提取前端验证码"""
    code = page.evaluate('''() => {
        // s-canvas是前端生成的验证码组件
        // 验证码值存在父组件的data里
        function findInVue(el) {
            if (!el) return null;
            // 向上找Vue组件实例
            let node = el;
            while (node) {
                if (node.__vueParentComponent) {
                    const state = node.__vueParentComponent.setupState || {};
                    for (const key of Object.keys(state)) {
                        const val = state[key];
                        if (typeof val === 'string' && val.length >= 4 && val.length <= 6) {
                            // 检查是否看起来像验证码（字母数字混合）
                            if (/^[a-zA-Z0-9]+$/.test(val)) {
                                return val;
                            }
                        }
                    }
                }
                // 也检查proxy
                if (node.__vueParentComponent && node.__vueParentComponent.proxy) {
                    const proxy = node.__vueParentComponent.proxy;
                    for (const key of ['code', 'captcha', 'identifyCode', 'verifyCode', 'imgCode', 'codeStr']) {
                        if (proxy[key] && typeof proxy[key] === 'string') return proxy[key];
                    }
                    // 看proxy的$data
                    if (proxy.$data) {
                        for (const key of Object.keys(proxy.$data)) {
                            const val = proxy.$data[key];
                            if (typeof val === 'string' && val.length >= 4 && val.length <= 6 && /^[a-zA-Z0-9]+$/.test(val)) {
                                return val;
                            }
                        }
                    }
                }
                node = node.parentElement;
            }
            return null;
        }
        // 从验证码canvas开始向上找
        const canvas = document.querySelector('#s-canvas');
        if (canvas) return findInVue(canvas);
        // 从form开始找
        const form = document.querySelector('form');
        if (form) return findInVue(form);
        // 从app开始找
        return findInVue(document.querySelector('#app'));
    }''')
    return code


def login(page):
    """登录后台"""
    page.goto(f"{BASE_URL}/", timeout=60000, wait_until='networkidle')
    page.wait_for_timeout(3000)

    if '/login' not in page.url:
        print("✅ 已经是登录状态")
        return True

    print(f"📝 登录页: {page.url}")

    # 填写账号密码
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)

    # 提取并填写验证码
    captcha = extract_captcha(page)
    if captcha:
        print(f"🔑 提取到验证码: {captcha}")
        page.fill('input[placeholder="验证码"]', captcha)
    else:
        print("⚠ 无法自动提取验证码，请手动输入...")
        page.wait_for_timeout(15000)  # 给你15秒手动输入

    # 点击登录
    page.click('button:has-text("登")')
    page.wait_for_timeout(5000)

    if '/login' not in page.url:
        print(f"✅ 登录成功！当前页: {page.url}")
        page.screenshot(path='screenshots/login_success.png')
        return True
    else:
        print("❌ 登录失败，请检查账号密码或手动操作")
        page.screenshot(path='screenshots/login_failed.png')
        return False


def explore_page(page, page_name):
    """探测单个页面结构，输出所有可交互元素"""
    result = {
        'name': page_name,
        'url': page.url,
        'inputs': [],
        'buttons': [],
        'tables': [],
        'selects': [],
        'tabs': [],
        'menus': [],
    }

    # 等待页面加载
    page.wait_for_timeout(2000)

    # 1. 所有输入框
    inputs = page.locator('input:visible').all()
    for inp in inputs:
        try:
            info = page.evaluate('''(el) => ({
                type: el.type,
                name: el.name,
                placeholder: el.placeholder,
                id: el.id,
                selector: el.name ? 'input[name="'+el.name+'"]'
                    : el.placeholder ? 'input[placeholder="'+el.placeholder+'"]'
                    : el.id ? '#'+el.id : 'input[type="'+el.type+'"]'
            })''', inp.element_handle())
            result['inputs'].append(info)
        except Exception:
            pass

    # 2. 所有按钮
    buttons = page.locator('button:visible').all()
    for btn in buttons:
        try:
            text = btn.inner_text().strip()
            if text:
                result['buttons'].append({
                    'text': text,
                    'selector': f'button:has-text("{text}")',
                })
        except Exception:
            pass

    # 3. 表格
    tables = page.locator('table:visible, .el-table:visible').all()
    if tables:
        try:
            # 获取表头
            headers = page.locator('table thead th, .el-table__header th').all()
            header_texts = [h.inner_text().strip() for h in headers if h.inner_text().strip()]
            rows_count = page.locator('table tbody tr, .el-table__body tr').count()
            result['tables'].append({
                'headers': header_texts,
                'rows': rows_count,
                'row_selector': '.el-table__body tr',
            })
        except Exception:
            pass

    # 4. 下拉选择框
    selects = page.locator('.el-select:visible').all()
    for sel in selects:
        try:
            placeholder = sel.locator('input').first.get_attribute('placeholder') or ''
            result['selects'].append({
                'placeholder': placeholder,
                'selector': f'.el-select:has(input[placeholder="{placeholder}"])',
            })
        except Exception:
            pass

    # 5. Tab标签页
    tabs = page.locator('.el-tabs__item:visible').all()
    for tab in tabs:
        try:
            text = tab.inner_text().strip()
            if text:
                result['tabs'].append({'text': text})
        except Exception:
            pass

    return result


def main():
    print("=" * 60)
    print("  快乐羊毛后台 · 页面探测器")
    print("  自动登录 → 逐页扫描 → 输出选择器")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # 有界面，你能看到操作
            slow_mo=500,     # 每步慢0.5秒，看得清
        )
        page = browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True,
        )

        # 登录
        if not login(page):
            print("\n请在浏览器中手动登录，登录成功后按回车继续...")
            input()

        # 抓取侧边栏菜单
        print("\n📌 抓取菜单结构...")
        page.wait_for_timeout(3000)

        menu_items = page.locator('.el-menu-item:visible, .el-sub-menu__title:visible').all()
        menus = []
        for item in menu_items:
            try:
                text = item.inner_text().strip()
                if text and text not in ['', '\n']:
                    menus.append(text)
            except Exception:
                pass

        print(f"找到 {len(menus)} 个菜单项:")
        for m in menus:
            print(f"  📌 {m}")

        # 逐个菜单页面探测
        all_pages = {}
        for menu_text in menus:
            try:
                print(f"\n{'='*40}")
                print(f"探测: {menu_text}")
                print(f"{'='*40}")

                # 点击菜单
                page.locator(f'.el-menu-item:has-text("{menu_text}"), .el-sub-menu__title:has-text("{menu_text}")').first.click()
                page.wait_for_timeout(3000)

                # 探测页面
                result = explore_page(page, menu_text)
                all_pages[menu_text] = result

                print(f"  URL: {result['url']}")
                print(f"  输入框: {len(result['inputs'])}个")
                for inp in result['inputs']:
                    print(f"    {inp['selector']}  (placeholder: {inp.get('placeholder','')})")
                print(f"  按钮: {len(result['buttons'])}个")
                for btn in result['buttons']:
                    print(f"    {btn['selector']}")
                print(f"  表格: {len(result['tables'])}个")
                for tbl in result['tables']:
                    print(f"    表头: {tbl['headers']}")
                    print(f"    行数: {tbl['rows']}")
                print(f"  下拉框: {len(result['selects'])}个")
                for sel in result['selects']:
                    print(f"    {sel['selector']}")

                # 截图
                safe_name = menu_text.replace('/', '_').replace('\\', '_')
                page.screenshot(path=f'screenshots/page_{safe_name}.png')

            except Exception as e:
                print(f"  ❌ 探测失败: {e}")

        # 保存结果
        output_path = 'page_structures/all_pages.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(all_pages, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 探测结果已保存: {output_path}")
        print(f"✅ 截图已保存: screenshots/")

        print("\n" + "=" * 60)
        print("  探测完成！")
        print(f"  把 {output_path} 文件内容发给我")
        print("  我帮你把所有TODO代码填好")
        print("=" * 60)

        # 保持浏览器打开让你检查
        input("\n按回车关闭浏览器...")
        browser.close()


if __name__ == '__main__':
    main()
