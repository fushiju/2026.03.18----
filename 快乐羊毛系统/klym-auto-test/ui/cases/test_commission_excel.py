"""
UI 测试 - 分佣系统 - Excel佣金导入
对应用例编号：fyxt-009 ~ fyxt-016, excel-001 ~ excel-007

功能：Excel导入、预览、校验、异常处理
"""
import os
import pytest
from ui.pages.commission_page import ExcelImportPage
from common.config import Config


@pytest.mark.ui
@pytest.mark.commission
class TestExcelImport:
    """Excel 佣金导入"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = ExcelImportPage(admin_page)
        self.page.goto_import()

    def _test_file(self, name: str) -> str:
        """获取测试文件路径"""
        return os.path.join(Config.TEST_DATA_DIR, "test_files", name)

    @pytest.mark.p1
    def test_fyxt009_import_valid_excel(self, admin_page):
        """fyxt-009: 验证导入正确格式Excel自动计算分佣成功
        步骤：上传含3条记录的Excel > 确认导入 > 查看结果
        预期：提示导入成功共3条记录，佣金正确入账
        """
        self.page.click_import_button()
        self.page.upload_excel(self._test_file("commission_valid.xlsx"))
        preview = self.page.get_preview_data()
        assert len(preview) == 3, f"预览应有3条，实际 {len(preview)}"
        self.page.confirm_import()
        result = self.page.get_import_result()
        assert "成功" in result

    @pytest.mark.p2
    def test_fyxt010_preview_and_cancel(self, admin_page):
        """fyxt-010: 验证Excel预览功能和确认流程
        步骤：上传Excel > 查看预览 > 取消导入
        预期：预览展示正确，取消后数据不入库
        """
        self.page.click_import_button()
        self.page.upload_excel(self._test_file("commission_valid.xlsx"))
        preview = self.page.get_preview_data()
        assert len(preview) > 0, "预览数据为空"
        self.page.cancel_import()

    @pytest.mark.p3
    def test_fyxt011_missing_required_field(self, admin_page):
        """fyxt-011: [反向] 验证Excel缺少必要字段时导入失败
        步骤：上传缺少佣金列的Excel
        预期：提示缺少必要字段
        """
        self.page.click_import_button()
        self.page.upload_excel(self._test_file("commission_missing_field.xlsx"))
        result = self.page.get_import_result()
        assert "缺少" in result or "格式" in result

    @pytest.mark.p3
    def test_fyxt013_empty_excel(self, admin_page):
        """fyxt-013: [反向] 验证上传空Excel文件被拦截
        步骤：上传只有表头的Excel
        预期：提示文件无有效数据
        """
        self.page.click_import_button()
        self.page.upload_excel(self._test_file("commission_empty.xlsx"))
        result = self.page.get_import_result()
        assert "无" in result or "空" in result

    @pytest.mark.p3
    def test_fyxt014_negative_commission(self, admin_page):
        """fyxt-014: [反向] 验证佣金金额为负数时导入失败
        步骤：上传含负数佣金的Excel
        预期：该行标记失败
        """
        self.page.click_import_button()
        self.page.upload_excel(self._test_file("commission_negative.xlsx"))
        result = self.page.get_import_result()
        assert "失败" in result or "负" in result

    @pytest.mark.p3
    def test_fyxt015_non_excel_format(self, admin_page):
        """fyxt-015: [反向] 验证上传非Excel格式文件被拦截
        步骤：上传PDF文件
        预期：提示请上传Excel格式文件
        """
        self.page.click_import_button()
        self.page.upload_excel(self._test_file("fake_file.pdf"))
        result = self.page.get_import_result()
        assert "Excel" in result or "格式" in result
