"""
快乐羊毛管理后台 - UI自动化测试（全量执行）
在 VSCode 中点击右上角 ▶ 运行全部测试模块
"""
import subprocess
import sys
import os
from pathlib import Path

project_root = Path(__file__).parent
os.chdir(project_root)
report_path = project_root / "reports" / "all_report.html"

# 删除旧报告
if report_path.exists():
    report_path.unlink()

print("=" * 60)
print("  快乐羊毛管理后台 - 全量测试执行")
print("=" * 60)

# 按顺序执行 tests/ 下所有测试模块
result = subprocess.run([
    sys.executable, "-m", "pytest",
    "tests/", "-v", "-s",
    f"--html={report_path}", "--self-contained-html"
])

print("=" * 60)
if result.returncode == 0:
    print("  全部测试通过！")
else:
    print(f"  有测试失败（退出码: {result.returncode}）")

if report_path.exists():
    print(f"  HTML报告: {report_path}")
    os.startfile(str(report_path))
else:
    print("  警告: HTML报告未生成")
