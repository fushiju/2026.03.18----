@echo off
chcp 65001 >nul
echo ============================================
echo   快乐羊毛后台 页面探测器
echo   会自动打开浏览器，你手动输验证码并登录
echo   登录后脚本自动扫描所有菜单页面
echo ============================================
echo.
cd /d "%~dp0"
"C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe" -X utf8 explore_and_generate.py
echo.
echo 探测完成！结果在 page_structures\all_pages.json
echo.
pause
