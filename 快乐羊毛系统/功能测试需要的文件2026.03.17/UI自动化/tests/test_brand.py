"""品牌管理模块测试

用例来源：品牌管理.xlsx
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from pages.brand_page import BrandPage
from config.settings import ADMIN_USERNAME, ADMIN_PASSWORD
