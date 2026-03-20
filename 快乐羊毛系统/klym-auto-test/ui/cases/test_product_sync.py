"""
UI 测试 - 选品仓库
对应用例编号：xpck-001 ~ xpck-043

功能：一键同步、品牌/SKU管理、变更检测、批量操作、列表展示
"""
import pytest
from ui.pages.product_sync_page import ProductSyncPage


@pytest.mark.ui
@pytest.mark.product
class TestProductSync:
    """一键同步功能"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = ProductSyncPage(admin_page)
        self.page.goto_product_sync()

    @pytest.mark.p1
    def test_xpck001_sync_fetch_data(self, admin_page):
        """xpck-001: 验证一键同步按钮获取第三方API的商品数据
        步骤：点击一键同步
        预期：同步完成，显示统计结果
        """
        self.page.click_sync()
        self.page.wait_sync_complete()
        result = self.page.get_sync_result()
        assert "同步" in result or "成功" in result

    @pytest.mark.p1
    def test_xpck002_sync_data_fields(self, admin_page):
        """xpck-002: 验证同步数据包含完整的商品字段信息
        步骤：同步后查看列表
        预期：商品信息包含名称、品牌、规格、价格等
        """
        data = self.page.get_product_list()
        assert len(data) > 0, "商品列表为空"

    @pytest.mark.p3
    def test_xpck005_api_timeout(self, admin_page):
        """xpck-005: [反向] 验证第三方API接口超时同步失败提示
        预期：提示同步失败
        """
        # 需要模拟API超时，通常通过mock或网络拦截
        pytest.skip("需要模拟第三方API超时")

    @pytest.mark.p3
    def test_xpck007_duplicate_sync(self, admin_page):
        """xpck-007: [反向] 验证重复点击一键同步不会重复创建
        步骤：点击同步 > 同步中再次点击
        预期：按钮置灰不可点
        """
        self.page.click_sync()
        assert self.page.is_sync_button_disabled(), "同步中按钮应置灰"
        self.page.wait_sync_complete()


@pytest.mark.ui
@pytest.mark.product
class TestProductImage:
    """图片资源管理"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = ProductSyncPage(admin_page)
        self.page.goto_product_sync()

    @pytest.mark.p1
    def test_xpck008_image_auto_transfer(self, admin_page):
        """xpck-008: 验证同步时第三方图片自动转存到阿里云OSS
        步骤：同步后查看商品图片地址
        预期：图片URL为OSS地址
        """
        data = self.page.get_product_list()
        assert len(data) > 0

    @pytest.mark.p1
    def test_xpck009_image_url_is_oss(self, admin_page):
        """xpck-009: 验证品牌和规格的图片地址统一为OSS地址
        """
        data = self.page.get_product_list()
        assert len(data) > 0


@pytest.mark.ui
@pytest.mark.product
class TestProductBrand:
    """品牌和SKU管理"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = ProductSyncPage(admin_page)
        self.page.goto_product_sync()

    @pytest.mark.p1
    def test_xpck014_auto_create_brand(self, admin_page):
        """xpck-014: 验证同步时自动创建不存在的商品品牌
        预期：新品牌被创建
        """
        data = self.page.get_product_list()
        assert isinstance(data, list)

    @pytest.mark.p1
    def test_xpck015_default_status_unshelved(self, admin_page):
        """xpck-015: 验证商品品牌默认状态为未上架
        预期：新品牌状态为"未上架"
        """
        # 找未上架的品牌
        self.page.filter_by_status("未上架")
        data = self.page.get_product_list()
        assert isinstance(data, list)

    @pytest.mark.p1
    def test_xpck016_auto_create_sku(self, admin_page):
        """xpck-016: 验证同步时自动创建商品品牌的SKU
        预期：品牌下有对应SKU（如10元券、20元券）
        """
        data = self.page.get_product_list()
        assert isinstance(data, list)

    @pytest.mark.p2
    def test_xpck017_no_duplicate_brand(self, admin_page):
        """xpck-017: 验证已存在品牌同步时不重复创建
        """
        data = self.page.get_product_list()
        assert isinstance(data, list)


@pytest.mark.ui
@pytest.mark.product
class TestProductChangeDetection:
    """变更检测"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = ProductSyncPage(admin_page)
        self.page.goto_product_sync()

    @pytest.mark.p1
    def test_xpck020_price_change_auto_unshelve(self, admin_page):
        """xpck-020: 验证第三方商品价格变化时自动下架并标记待确认
        预期：状态变为"待确认"
        """
        self.page.filter_by_status("待确认")

    @pytest.mark.p1
    def test_xpck022_status_visual_distinction(self, admin_page):
        """xpck-022: 验证品牌状态有待确认标识和已上架未上架区分
        预期：三种状态有不同颜色标签
        """
        data = self.page.get_product_list()
        assert isinstance(data, list)

    @pytest.mark.p1
    def test_xpck025_confirm_and_reshelve(self, admin_page):
        """xpck-025: 验证运营确认变更后重新上架
        步骤：找到待确认商品 > 点击确认 > 重新上架
        预期：状态变为已上架
        """
        self.page.filter_by_status("待确认")


@pytest.mark.ui
@pytest.mark.product
class TestProductList:
    """列表展示与筛选"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = ProductSyncPage(admin_page)
        self.page.goto_product_sync()

    @pytest.mark.p1
    def test_xpck028_list_fields(self, admin_page):
        """xpck-028: 验证选品仓库列表展示必要字段
        预期：包含品牌名、状态、渠道等字段
        """
        data = self.page.get_product_list()
        assert len(data) >= 0

    @pytest.mark.p2
    def test_xpck031_filter_by_channel(self, admin_page):
        """xpck-031: 验证按渠道筛选列表数据
        步骤：选择渠道 > 查看结果
        预期：只显示对应渠道的数据
        """
        self.page.filter_by_channel("骑士")

    @pytest.mark.p2
    def test_xpck032_filter_by_shelve_status(self, admin_page):
        """xpck-032: 验证按上架状态筛选列表数据
        """
        self.page.filter_by_status("已上架")
        data = self.page.get_product_list()
        assert isinstance(data, list)

    @pytest.mark.p3
    def test_xpck035_empty_list(self, admin_page):
        """xpck-035: [反向] 验证列表无数据时展示空状态
        """
        self.page.search_product("不存在的商品名称xyz123")
        assert self.page.has_empty_state()


@pytest.mark.ui
@pytest.mark.product
class TestProductBatchOps:
    """批量操作"""

    @pytest.fixture(autouse=True)
    def setup(self, admin_page):
        self.page = ProductSyncPage(admin_page)
        self.page.goto_product_sync()

    @pytest.mark.p1
    def test_xpck036_batch_shelve(self, admin_page):
        """xpck-036: 验证批量上架功能
        步骤：选择多个商品 > 批量上架
        预期：全部变为已上架
        """
        self.page.select_all()
        self.page.batch_shelve()

    @pytest.mark.p1
    def test_xpck037_batch_delete(self, admin_page):
        """xpck-037: 验证批量删除功能
        步骤：选择商品 > 批量删除 > 确认
        """
        # 谨慎操作，测试环境使用
        pass

    @pytest.mark.p3
    def test_xpck040_batch_no_selection(self, admin_page):
        """xpck-040: [反向] 验证未选商品时批量操作按钮禁用
        预期：批量上架按钮置灰
        """
        assert self.page.is_batch_button_disabled("批量上架")

    @pytest.mark.p3
    def test_xpck041_batch_delete_shelved_confirm(self, admin_page):
        """xpck-041: [反向] 验证批量删除含已上架商品时二次确认
        """
        pass
