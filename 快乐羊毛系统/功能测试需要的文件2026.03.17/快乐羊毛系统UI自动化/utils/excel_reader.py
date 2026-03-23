"""读取 Excel 测试用例数据

测试用例目录结构：
  测试用例/
    登录/登录.xlsx
    品牌管理/新增品牌.xlsx
    品牌管理/品牌编辑.xlsx
    品牌管理/品牌查看.xlsx
    品牌管理/品牌搜索.xlsx
"""
from pathlib import Path
import openpyxl
from config.settings import TESTCASE_DIR


def read_test_cases(file_path: str, sheet_name: str = None) -> list[dict]:
    """读取指定 Excel 文件，返回字典列表。

    Args:
        file_path: 相对于 TESTCASE_DIR 的路径，如 "品牌管理/新增品牌.xlsx"
        sheet_name: 工作表名称，默认读取第一个
    """
    full_path = TESTCASE_DIR / file_path
    wb = openpyxl.load_workbook(full_path, read_only=True)
    ws = wb[sheet_name] if sheet_name else wb.active
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    if len(rows) < 2:
        return []
    headers = [str(h).strip() if h else f"col_{i}" for i, h in enumerate(rows[0])]
    result = []
    for row in rows[1:]:
        values = [str(v).strip() if v else "" for v in row]
        if any(values):
            result.append(dict(zip(headers, values)))
    return result


def read_login_cases() -> list[dict]:
    """读取登录测试用例"""
    return read_test_cases("登录/登录.xlsx", "测试用例")


def read_brand_add_cases() -> list[dict]:
    """读取新增品牌测试用例"""
    return read_test_cases("品牌管理/新增品牌.xlsx")


def read_brand_edit_cases() -> list[dict]:
    """读取品牌编辑测试用例"""
    return read_test_cases("品牌管理/品牌编辑.xlsx")


def read_brand_view_cases() -> list[dict]:
    """读取品牌查看测试用例"""
    return read_test_cases("品牌管理/品牌查看.xlsx")


def read_brand_search_cases() -> list[dict]:
    """读取品牌搜索测试用例"""
    return read_test_cases("品牌管理/品牌搜索.xlsx")
