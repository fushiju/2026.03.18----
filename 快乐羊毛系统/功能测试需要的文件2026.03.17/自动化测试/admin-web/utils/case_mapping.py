# -*- coding: utf-8 -*-
"""
用例映射核心模块
把Excel用例编号绑定到自动化测试函数上，实现双向追踪
"""
import pytest
import functools

# 全局注册表：记录所有已绑定的用例编号
_CASE_REGISTRY = {}  # {case_id: {func, file, module, priority, title}}


def case(*case_ids, title="", priority=""):
    """
    装饰器：将测试函数绑定到Excel用例编号

    用法：
        @case("mfzl-001", title="验证资料列表正常加载", priority="P1")
        def test_material_list_loads(page):
            ...

        # 一个函数覆盖多条用例
        @case("mfzl-001", "mfzl-002", title="列表加载+分类筛选")
        def test_material_list_and_filter(page):
            ...
    """
    def decorator(func):
        # 注册到全局表
        for cid in case_ids:
            _CASE_REGISTRY[cid] = {
                'func': func.__name__,
                'file': func.__module__ or '',
                'title': title,
                'priority': priority,
            }

        # 添加pytest marker，方便按用例编号筛选运行
        # 用法: pytest -m "mfzl_001" 只跑这一条
        for cid in case_ids:
            marker_name = cid.replace('-', '_')
            func = pytest.mark.parametrize([], [])(func) if False else func
            # 存到函数属性上
            if not hasattr(func, '_case_ids'):
                func._case_ids = []
            func._case_ids.append(cid)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            case_str = ', '.join(case_ids)
            print(f"\n▶ 执行用例 [{case_str}] {title}")
            result = func(*args, **kwargs)
            print(f"  ✅ 用例 [{case_str}] 通过")
            return result

        wrapper._case_ids = list(case_ids)
        wrapper._case_title = title
        wrapper._case_priority = priority
        return wrapper

    return decorator


def get_registry():
    """获取所有已注册的用例映射"""
    return _CASE_REGISTRY.copy()


def get_automated_case_ids():
    """获取所有已自动化的用例编号集合"""
    return set(_CASE_REGISTRY.keys())
