from utils.excel_reader import read_login_cases


def test_read_login_cases_returns_list():
    cases = read_login_cases()
    assert isinstance(cases, list)
    assert len(cases) > 0


def test_read_login_cases_has_required_fields():
    cases = read_login_cases()
    first = cases[0]
    assert "用例标题" in first
    assert "预期结果（断言）" in first
