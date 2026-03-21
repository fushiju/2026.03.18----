@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================================
echo   快乐羊毛管理后台 - 登录测试
echo ============================================================
echo.

C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe -m pytest tests/test_login.py -v -s --html=reports/login_report.html --self-contained-html

echo.
echo ============================================================
if exist "reports\login_report.html" (
    echo   HTML报告已生成，正在打开浏览器...
    start "" "reports\login_report.html"
) else (
    echo   警告: HTML报告未生成
)
echo ============================================================
pause
