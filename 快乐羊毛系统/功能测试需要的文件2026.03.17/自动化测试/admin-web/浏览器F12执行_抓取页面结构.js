/**
 * 在浏览器F12控制台执行这段代码
 *
 * 步骤：
 * 1. 用Chrome打开 https://red.jinyedaojia.com/ 并登录
 * 2. 按F12打开开发者工具
 * 3. 切换到Console（控制台）标签
 * 4. 把这段代码全部复制粘贴进去，按回车
 * 5. 它会自动扫描当前页面 + 所有菜单，输出结构
 * 6. 把输出结果复制给我
 */

(async function scanAdmin() {
    const results = {};

    // 扫描当前页面
    function scanCurrentPage() {
        const info = {
            url: location.hash,
            inputs: [],
            buttons: [],
            tables: [],
            selects: [],
        };

        // 输入框
        document.querySelectorAll('input:not([type=hidden])').forEach(el => {
            if (el.offsetParent !== null) { // 可见的
                info.inputs.push({
                    type: el.type,
                    name: el.name,
                    placeholder: el.placeholder,
                    selector: el.name ? `input[name="${el.name}"]`
                        : el.placeholder ? `input[placeholder="${el.placeholder}"]`
                        : `input[type="${el.type}"]`
                });
            }
        });

        // 按钮
        document.querySelectorAll('button').forEach(el => {
            if (el.offsetParent !== null) {
                const text = el.innerText.trim();
                if (text && text.length < 20) {
                    info.buttons.push({
                        text: text,
                        selector: `button:has-text("${text}")`,
                    });
                }
            }
        });

        // 表格表头
        const headers = [];
        document.querySelectorAll('.el-table__header th, table thead th').forEach(th => {
            const t = th.innerText.trim();
            if (t) headers.push(t);
        });
        const rows = document.querySelectorAll('.el-table__body tr, table tbody tr').length;
        if (headers.length > 0) {
            info.tables.push({ headers, rows });
        }

        // 下拉框
        document.querySelectorAll('.el-select').forEach(el => {
            const input = el.querySelector('input');
            if (input && input.placeholder) {
                info.selects.push({
                    placeholder: input.placeholder,
                    selector: `.el-select:has(input[placeholder="${input.placeholder}"])`,
                });
            }
        });

        return info;
    }

    // 获取所有菜单项
    const menuItems = document.querySelectorAll('.el-menu-item, .el-sub-menu__title');
    const menus = [];
    menuItems.forEach(el => {
        const text = el.innerText.trim().replace(/\n/g, '');
        if (text && !menus.includes(text)) menus.push(text);
    });

    console.log('=== 找到菜单项 ===');
    console.log(menus);

    // 先扫描当前页面
    results['当前页面'] = scanCurrentPage();

    // 逐个点击菜单扫描
    for (const menuText of menus) {
        try {
            // 找到菜单项并点击
            let clicked = false;
            menuItems.forEach(el => {
                if (el.innerText.trim().replace(/\n/g, '') === menuText && !clicked) {
                    el.click();
                    clicked = true;
                }
            });

            if (!clicked) continue;

            // 等待页面加载
            await new Promise(r => setTimeout(r, 2000));

            results[menuText] = scanCurrentPage();
            console.log(`✅ ${menuText}: ${results[menuText].inputs.length}输入框, ${results[menuText].buttons.length}按钮, ${results[menuText].tables.length}表格`);

        } catch (e) {
            console.log(`❌ ${menuText}: ${e.message}`);
        }
    }

    // 输出结果
    const output = JSON.stringify(results, null, 2);
    console.log('\n\n========= 复制下面的内容发给我 =========\n');
    console.log(output);
    console.log('\n========= 复制到这里为止 =========');

    // 同时复制到剪贴板
    try {
        await navigator.clipboard.writeText(output);
        console.log('\n✅ 已自动复制到剪贴板，直接粘贴给我就行');
    } catch (e) {
        console.log('\n⚠ 自动复制失败，请手动选中上面的JSON文本复制');
    }

    return results;
})();
