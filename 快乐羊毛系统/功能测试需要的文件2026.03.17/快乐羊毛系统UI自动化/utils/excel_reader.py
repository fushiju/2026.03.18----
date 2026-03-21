"""读取 Excel 测试用例数据"""
from pathlib import Path
import openpyxl
from config.settings import TESTCASE_DIR


def read_test_cases(file_name: str, sheet_name: str = None) -> list[dict]:
    """读取指定 Excel 文件，返回字典列表。第1行为表头，第2行起为数据。"""
    file_path = TESTCASE_DIR / file_name
    wb = openpyxl.load_workbook(file_path, read_only=True)
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
    return read_test_cases("登录.xlsx", "测试用例")
