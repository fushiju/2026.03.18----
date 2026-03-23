"""检查品牌管理中删除功能的位置和交互"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r'D:\测试2026.03.09\快乐羊毛系统\功能测试需要的文件2026.03.17\快乐羊毛系统UI自动化')
from playwright.sync_api import sync_playwright
from utils.captcha_solver import solve_captcha


def login(page):
    page.goto('https://red.jinyedaojia.com/#/login', wait_until='domcontentloaded')
    page.wait_for_timeout(3000)
    page.fill('input[name="username"]', 'admin')
    page.fill('input[name="password"]', 'admin123')
    for attempt in range(5):
        canvas = page.locator('canvas#s-canvas')
        img_bytes = canvas.screenshot()
        captcha = solve_captcha(img_bytes)
        page.fill('.el-form-item:nth-child(3) input', captcha)
        page.click('button.el-button--primary')
        page.wait_for_timeout(4000)
        if 'login' not in page.url:
            print('登录成功!', flush=True)
            return True
        canvas.click()
        page.wait_for_timeout(1000)
    return False


def close_popup(page):
    try:
        page.locator('button:has-text("忽")').first.click(timeout=3000)
    except:
        pass
    page.wait_for_timeout(500)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    if not login(page):
        print('登录失败')
        browser.close()
        sys.exit(1)

    page.wait_for_timeout(2000)
    close_popup(page)

    # 品牌管理页面
    page.goto('https://red.jinyedaojia.com/#/coach/manage', wait_until='domcontentloaded')
    page.wait_for_timeout(4000)
    close_popup(page)

    print(f'URL: {page.url}', flush=True)

    # ========== 列表页按钮 ==========
    print('\n========== 列表页操作列 ==========', flush=True)

    # 获取所有行的操作按钮
    rows = page.locator('.el-table__body tr').all()
    print(f'列表行数: {len(rows)}', flush=True)

    if rows:
        first_row = rows[0]
        row_btns = first_row.locator('button').all()
        print(f'第一行操作按钮:', flush=True)
        for btn in row_btns:
            t = btn.text_content().strip()
            if t:
                print(f'  [{t}]', flush=True)

    # 检查是否有直接的删除按钮
    del_btns = page.locator('button:has-text("删除")').all()
    print(f'\n页面上"删除"按钮数量: {len(del_btns)}', flush=True)

    # ========== 更多菜单 ==========
    print('\n========== 更多菜单 ==========', flush=True)
    more_btn = page.locator('button:has-text("更多菜单")')
    print(f'"更多菜单"按钮数量: {more_btn.count()}', flush=True)

    if more_btn.count() > 0:
        more_btn.first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=r'D:\brand_more_menu.png')

        # 下拉菜单选项
        dropdown_items = page.locator('.el-dropdown-menu__item, .el-popper li, [role="menuitem"]').all()
        print(f'下拉菜单选项:', flush=True)
        for item in dropdown_items:
            if item.is_visible():
                text = item.text_content().strip()
                print(f'  - {text}', flush=True)

        # 检查是否有删除选项
        del_item = page.locator('.el-dropdown-menu__item:has-text("删除"), [role="menuitem"]:has-text("删除")')
        print(f'\n菜单中"删除"选项数量: {del_item.count()}', flush=True)

        if del_item.count() > 0:
            del_item.first.click()
            page.wait_for_timeout(2000)
            page.screenshot(path=r'D:\brand_delete_confirm.png')

            # 确认弹窗
            confirms = page.locator('.el-message-box, .el-dialog').all()
            for ct in confirms:
                if ct.is_visible():
                    text = ct.text_content().strip()[:200]
                    print(f'\n删除确认弹窗: {text}', flush=True)

                    # 弹窗按钮
                    dialog_btns = ct.locator('button').all()
                    print('弹窗按钮:', flush=True)
                    for btn in dialog_btns:
                        if btn.is_visible():
                            print(f'  [{btn.text_content().strip()}]', flush=True)

            # 取消
            try:
                page.locator('button:has-text("取消")').first.click(timeout=3000)
                page.wait_for_timeout(500)
            except:
                pass
        else:
            # 没有删除选项，看看所有可见的菜单项
            all_visible = page.locator('[class*="dropdown"], [class*="popper"], [class*="menu"]').all()
            for el in all_visible:
                if el.is_visible():
                    print(f'  可见元素: {el.text_content().strip()[:100]}', flush=True)

        # 关闭下拉菜单
        page.keyboard.press('Escape')
        page.wait_for_timeout(500)

    # ========== Tab筛选检查各状态下的操作 ==========
    print('\n========== 不同Tab下的操作按钮 ==========', flush=True)
    tabs = page.locator('.el-tabs__item, [role="tab"]').all()
    for tab in tabs:
        if tab.is_visible():
            tab_text = tab.text_content().strip()
            tab.click()
            page.wait_for_timeout(2000)

            rows = page.locator('.el-table__body tr').all()
            if rows:
                first_row_btns = rows[0].locator('button').all()
                btn_texts = [b.text_content().strip() for b in first_row_btns if b.text_content().strip()]
                print(f'  Tab[{tab_text}]: 第一行按钮 = {btn_texts}', flush=True)

                # 检查更多菜单
                more_in_row = rows[0].locator('button:has-text("更多菜单")')
                if more_in_row.count() > 0:
                    more_in_row.first.click()
                    page.wait_for_timeout(1500)
                    menu_items = page.locator('.el-dropdown-menu__item').all()
                    visible_items = [m.text_content().strip() for m in menu_items if m.is_visible()]
                    print(f'    更多菜单项: {visible_items}', flush=True)
                    page.keyboard.press('Escape')
                    page.wait_for_timeout(500)
            else:
                print(f'  Tab[{tab_text}]: 无数据', flush=True)

    browser.close()
    print('\n完成!', flush=True)
