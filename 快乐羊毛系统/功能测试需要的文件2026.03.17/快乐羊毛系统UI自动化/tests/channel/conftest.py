"""渠道管理模块 fixtures

fixture 与测试文件的对应关系：
  channel_page  → test_channel_add.py（新增渠道）
  channel_page  → test_channel_edit.py（编辑渠道）
  channel_page  → test_channel_delete.py（删除渠道）
"""
import pytest
from pages.channel_page import ChannelPage

# 列表中已知的渠道
EXISTING_CHANNEL = "芒果"
EXISTING_CHANNEL_2 = "骑士"


@pytest.fixture
def channel_page(logged_in_page) -> ChannelPage:
    """已登录 → 渠道管理列表页"""
    cp = ChannelPage(logged_in_page)
    cp.goto_channel_list()
    return cp
