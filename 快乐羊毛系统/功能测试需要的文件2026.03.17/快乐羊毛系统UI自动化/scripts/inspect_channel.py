"""检查渠道管理页面的字段和功能"""
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


def inspect_dialog(page, title):
    """检查弹窗内容"""
    print(f'\n--- {title} 弹窗内容 ---', flush=True)
    for prefix_name, prefix in [('.el-dialog', '.el-dialog '), ('.el-drawer', '.el-drawer '), ('页面', '')]:
        labels = page.locator(f'{prefix}.el-form-item__label').all()
        visible = [l for l in labels if l.is_visible()]
        if visible:
            print(f'表单标签 ({prefix_name}):', flush=True)
            for l in visible:
                print(f'  - {l.text_content().strip()}', flush=True)

            inputs = page.locator(f'{prefix}input, {prefix}textarea').all()
            for inp in inputs:
                if inp.is_visible():
                    ph = inp.get_attribute('placeholder') or ''
                    tp = inp.get_attribute('type') or 'text'
                    val = inp.input_value()
                    maxlen = inp.get_attribute('maxlength') or ''
                    print(f'  输入框: type={tp} placeholder="{ph}" value="{val}" maxlength={maxlen}', flush=True)

            uploads = [u for u in page.locator(f'{prefix}.el-upload').all() if u.is_visible()]
            print(f'  上传区域: {len(uploads)}个', flush=True)

            switches = [s for s in page.locator(f'{prefix}.el-switch').all() if s.is_visible()]
            print(f'  开关: {len(switches)}个', flush=True)

            selects = [s for s in page.locator(f'{prefix}.el-select').all() if s.is_visible()]
            if selects:
                print(f'  下拉框: {len(selects)}个', flush=True)
                for sel in selects:
                    inp = sel.locator('input')
                    if inp.count() > 0:
                        ph = inp.first.get_attribute('placeholder') or ''
                        val = inp.first.input_value()
                        print(f'    placeholder="{ph}" value="{val}"', flush=True)

            radios = [r for r in page.locator(f'{prefix}.el-radio, {prefix}.el-radio-button').all() if r.is_visible()]
            if radios:
                print(f'  单选:', flush=True)
                for r in radios:
                    print(f'    - {r.text_content().strip()}', flush=True)

            checkboxes = [c for c in page.locator(f'{prefix}.el-checkbox').all() if c.is_visible()]
            if checkboxes:
                print(f'  复选:', flush=True)
                for c in checkboxes:
                    print(f'    - {c.text_content().strip()}', flush=True)

            # 按钮
            dialog_btns = page.locator(f'{prefix_name} button').all() if prefix_name != '页面' else []
            if dialog_btns:
                print(f'  按钮:', flush=True)
                for btn in dialog_btns:
                    if btn.is_visible():
                        t = btn.text_content().strip()
                        if t:
                            print(f'    [{t}]', flush=True)
            break


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

    # 渠道管理页面
    page.goto('https://red.jinyedaojia.com/#/coach/coachLabel', wait_until='domcontentloaded')
    page.wait_for_timeout(4000)
    close_popup(page)

    print(f'URL: {page.url}', flush=True)
    page.screenshot(path=r'D:\channel_list.png')

    # ========== 列表页 ==========
    print('\n========== 渠道管理列表页 ==========', flush=True)

    # 按钮
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
    for i, row in enumerate(rows[:8]):
        cells = row.locator('td').all()
        vals = [c.text_content().strip()[:30] for c in cells]
        print(f'  第{i+1}行: {vals}', flush=True)

    # ========== 新增 ==========
    print('\n========== 新增渠道 ==========', flush=True)
    add_btn = page.locator('button:has-text("新增"), button:has-text("添加"), button:has-text("创建")')
    if add_btn.count() > 0:
        print(f'点击: {add_btn.first.text_content().strip()}', flush=True)
        add_btn.first.click()
        page.wait_for_timeout(3000)
        page.screenshot(path=r'D:\channel_add.png')
        inspect_dialog(page, '新增渠道')

        # 关闭
        try:
            page.locator('button:has-text("取消"), .el-dialog__headerbtn').first.click(timeout=3000)
            page.wait_for_timeout(1000)
        except:
            pass

    # ========== 编辑 ==========
    print('\n========== 编辑渠道 ==========', flush=True)
    edit_btn = page.locator('button:has-text("编辑")')
    if edit_btn.count() > 0:
        edit_btn.first.click()
        page.wait_for_timeout(3000)
        page.screenshot(path=r'D:\channel_edit.png')
        inspect_dialog(page, '编辑渠道')

        try:
            page.locator('button:has-text("取消"), .el-dialog__headerbtn').first.click(timeout=3000)
            page.wait_for_timeout(1000)
        except:
            pass

    # ========== 删除 ==========
    print('\n========== 删除渠道 ==========', flush=True)
    del_btn = page.locator('button:has-text("删除")')
    print(f'删除按钮数量: {del_btn.count()}', flush=True)
    if del_btn.count() > 0:
        del_btn.first.click()
        page.wait_for_timeout(2000)
        page.screenshot(path=r'D:\channel_delete.png')
        confirms = page.locator('.el-message-box, .el-dialog').all()
        for ct in confirms:
            if ct.is_visible():
                text = ct.text_content().strip()[:150]
                print(f'删除确认弹窗: {text}', flush=True)
        try:
            page.locator('button:has-text("取消")').first.click(timeout=3000)
            page.wait_for_timeout(500)
        except:
            pass

    browser.close()
    print('\n完成!', flush=True)
