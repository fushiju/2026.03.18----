"""
快乐羊毛管理后台 - UI自动化测试启动器
在 VSCode 中打开此文件，点击右上角 ▶ 运行
"""
import subprocess
import sys
import os
from pathlib import Path

os.chdir(Path(__file__).parent)


def main():
    print("=" * 60)
    print("  快乐羊毛管理后台 - UI自动化测试")
    print("=" * 60)
    print()
    print("请选择运行模式：")
    print("  1 - 登录测试（有头模式，能看到浏览器）")
    print("  2 - 登录测试 + 生成HTML报告")
    print("  3 - 冒烟测试（仅正确登录1条）")
    print("  4 - Excel读取工具测试（不需要网站）")
    print()

    choice = input("请输入数字 (1/2/3/4): ").strip()

    if choice == "1":
        cmd = [sys.executable, "-m", "pytest", "tests/test_login.py", "-v", "-s"]
    elif choice == "2":
        cmd = [sys.executable, "-m", "pytest", "tests/test_login.py", "-v",
               "--html=reports/login_report.html", "--self-contained-html"]
    elif choice == "3":
        cmd = [sys.executable, "-m", "pytest", "tests/test_login.py", "-m", "smoke", "-v", "-s"]
    elif choice == "4":
        cmd = [sys.executable, "-m", "pytest", "tests/test_excel_reader.py", "-v"]
    else:
        print("无效选择，退出")
        return

    print()
    print(f"正在执行...")
    print("-" * 60)

    result = subprocess.run(cmd)

    print("-" * 60)
    if result.returncode == 0:
        print("测试全部通过！")
    else:
        print(f"有测试失败（退出码: {result.returncode}）")

    if choice == "2":
        report = Path("reports/login_report.html").resolve()
        if report.exists():
            print(f"\nHTML报告已生成: {report}")
            os.startfile(str(report))

    input("\n按回车键退出...")


if __name__ == "__main__":
    main()
