"""检查品牌分类页面的字段和功能"""
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

    # 品牌分类页面
    page.goto('https://red.jinyedaojia.com/#/coach/category', wait_until='domcontentloaded')
    page.wait_for_timeout(4000)
    close_popup(page)

    print(f'URL: {page.url}', flush=True)
    page.screenshot(path=r'D:\category_list.png')

    # 按钮
    print('\n========== 列表页 ==========', flush=True)
    btns = page.locator('button').all()
    print('按钮:', flush=True)
    for btn in btns:
        if btn.is_visible():
            t = btn.text_content().strip()
            if t:
                print(f'  [{t}]', flush=True)

    # 表头
    th_cells = page.locator('.el-table__header th').all()
    print('\n列表表头:', flush=True)
    for th in th_cells:
        text = th.text_content().strip()
        if text:
            print(f'  - {text}', flush=True)

    # 列表数据
    rows = page.locator('.el-table__body tr').all()
    print(f'\n列表数据 ({len(rows)}行):', flush=True)
    for i, row in enumerate(rows[:5]):
        cells = row.locator('td').all()
        vals = [c.text_content().strip()[:25] for c in cells]
        print(f'  第{i+1}行: {vals}', flush=True)

    # 新增
    print('\n========== 新增品牌分类 ==========', flush=True)
    add_btn = page.locator('button:has-text("新增"), button:has-text("添加")')
    if add_btn.count() > 0:
        print(f'点击: {add_btn.first.text_content().strip()}', flush=True)
        add_btn.first.click()
        page.wait_for_timeout(3000)
        page.screenshot(path=r'D:\category_add.png')

        # 弹窗
        for selector_prefix in ['.el-dialog', '.el-drawer', '']:
            prefix = selector_prefix + ' ' if selector_prefix else ''
            labels = page.locator(f'{prefix}.el-form-item__label').all()
            visible_labels = [l for l in labels if l.is_visible()]
            if visible_labels:
                print(f'表单标签 ({selector_prefix or "页面"}):', flush=True)
                for label in visible_labels:
                    print(f'  - {label.text_content().strip()}', flush=True)

            inputs = page.locator(f'{prefix}input, {prefix}textarea').all()
            visible_inputs = [i for i in inputs if i.is_visible()]
            if visible_inputs:
                print(f'输入框:', flush=True)
                for inp in visible_inputs:
                    ph = inp.get_attribute('placeholder') or ''
                    tp = inp.get_attribute('type') or 'text'
                    maxlen = inp.get_attribute('maxlength') or ''
                    print(f'  - type={tp} placeholder="{ph}" maxlength={maxlen}', flush=True)

            uploads = page.locator(f'{prefix}.el-upload').all()
            visible_uploads = [u for u in uploads if u.is_visible()]
            print(f'上传区域: {len(visible_uploads)}个', flush=True)

            switches = page.locator(f'{prefix}.el-switch').all()
            visible_switches = [s for s in switches if s.is_visible()]
            print(f'开关: {len(visible_switches)}个', flush=True)

            radios = page.locator(f'{prefix}.el-radio, {prefix}.el-radio-button').all()
            visible_radios = [r for r in radios if r.is_visible()]
            if visible_radios:
                print('单选:', flush=True)
                for r in visible_radios:
                    print(f'  - {r.text_content().strip()}', flush=True)

            selects = page.locator(f'{prefix}.el-select').all()
            visible_selects = [s for s in selects if s.is_visible()]
            if visible_selects:
                print(f'下拉框: {len(visible_selects)}个', flush=True)
                for sel in visible_selects:
                    inp = sel.locator('input')
                    if inp.count() > 0:
                        ph = inp.first.get_attribute('placeholder') or ''
                        print(f'  - placeholder="{ph}"', flush=True)

            if visible_labels:
                break

        # 弹窗按钮
        dialog_btns = page.locator('.el-dialog button, .el-drawer button').all()
        print('弹窗按钮:', flush=True)
        for btn in dialog_btns:
            if btn.is_visible():
                t = btn.text_content().strip()
                if t:
                    print(f'  [{t}]', flush=True)

        # 关闭弹窗
        try:
            page.locator('button:has-text("取消"), .el-dialog__headerbtn').first.click(timeout=3000)
            page.wait_for_timeout(1000)
        except:
            pass

    # 编辑
    print('\n========== 编辑品牌分类 ==========', flush=True)
    edit_btn = page.locator('button:has-text("编辑")')
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(3000)
        page.screenshot(path=r'D:\category_edit.png')

        for selector_prefix in ['.el-dialog', '.el-drawer', '']:
            prefix = selector_prefix + ' ' if selector_prefix else ''
            labels = page.locator(f'{prefix}.el-form-item__label').all()
            visible_labels = [l for l in labels if l.is_visible()]
            if visible_labels:
                print(f'编辑标签 ({selector_prefix or "页面"}):', flush=True)
                for label in visible_labels:
                    print(f'  - {label.text_content().strip()}', flush=True)

            inputs = page.locator(f'{prefix}input, {prefix}textarea').all()
            visible_inputs = [i for i in inputs if i.is_visible()]
            if visible_inputs:
                print('编辑输入框:', flush=True)
                for inp in visible_inputs:
                    ph = inp.get_attribute('placeholder') or ''
                    val = inp.input_value()
                    maxlen = inp.get_attribute('maxlength') or ''
                    print(f'  - placeholder="{ph}" value="{val}" maxlength={maxlen}', flush=True)

            uploads = page.locator(f'{prefix}.el-upload').all()
            visible_uploads = [u for u in uploads if u.is_visible()]
            print(f'上传区域: {len(visible_uploads)}个', flush=True)

            switches = page.locator(f'{prefix}.el-switch').all()
            visible_switches = [s for s in switches if s.is_visible()]
            print(f'开关: {len(visible_switches)}个', flush=True)

            if visible_labels:
                break

        try:
            page.locator('button:has-text("取消"), .el-dialog__headerbtn').first.click(timeout=3000)
            page.wait_for_timeout(1000)
        except:
            pass

    # 删除
    print('\n========== 删除品牌分类 ==========', flush=True)
    del_btn = page.locator('button:has-text("删除")')
    print(f'删除按钮数量: {del_btn.count()}', flush=True)
    if del_btn.count() > 0:
        del_btn.first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=r'D:\category_delete.png')
        # 确认弹窗
        confirm_text = page.locator('.el-message-box, .el-dialog').all()
        for ct in confirm_text:
            if ct.is_visible():
                print(f'删除确认弹窗: {ct.text_content().strip()[:100]}', flush=True)
        # 取消
        try:
            page.locator('button:has-text("取消")').first.click(timeout=3000)
            page.wait_for_timeout(500)
        except:
            pass

    browser.close()
    print('\n完成!', flush=True)
