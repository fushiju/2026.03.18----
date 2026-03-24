"use strict";
const common_vendor = require("../common/vendor.js");
const api_link = require("../api/link.js");
if (!Math) {
  Category();
}
const Category = () => "../components/Category/Category.js";
const _sfc_main = {
  __name: "applicanceList",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const categoryRef = common_vendor.ref(null);
    const brandCategories = common_vendor.ref([]);
    const initialBrandId = common_vendor.ref(null);
    const loadBrandCategories = async () => {
      const res = await api_link.categroy();
      const list = Array.isArray(res.data) ? res.data : res.data && Array.isArray(res.data.data) ? res.data.data : [];
      const target = list.find((item) => Number(item.id) === 11);
      const children = (target == null ? void 0 : target.children) || [];
      brandCategories.value = children.map((child) => ({
        id: child.id,
        name: child.category_name || child.goods_name || "",
        // 这里不用 subCategories，直接用 content 作为右侧商品列表
        subCategories: [],
        content: []
      }));
    };
    const loadGoodsByCategory = async (categoryId) => {
      if (!categoryId)
        return;
      const res = await api_link.goodsList({ categoryId });
      const list = Array.isArray(res) ? res : res && Array.isArray(res.data) ? res.data : [];
      const mapped = list.map((it) => {
        const link = it.link_info || {};
        return {
          id: it.id,
          img: it.goods_img,
          title: it.goods_name,
          desc: it.desc || "",
          price: it.price || it.goods_price || "",
          // 从 link_info 里取跳转配置
          jump_type: link.jump_type,
          jump_url: link.link_url,
          appid: link.appid
        };
      });
      brandCategories.value = brandCategories.value.map(
        (cat) => Number(cat.id) === Number(categoryId) ? { ...cat, content: mapped } : cat
      );
    };
    const onCategoryChange = (data) => {
      var _a;
      const categoryId = (_a = data == null ? void 0 : data.category) == null ? void 0 : _a.id;
      loadGoodsByCategory(categoryId);
    };
    const onConsult = (e) => {
      switch (e.jump_type) {
        case 1:
          common_vendor.index.navigateToMiniProgram({
            appId: e.appid,
            path: e.jump_url
          });
          break;
        case 2:
          return proxy.$u.goUrl(`/subPages/webview?url=${e.jump_url}`);
        case 3:
          return proxy.$u.goUrl(`${e.jump_url}?id=${e.id}`);
      }
    };
    common_vendor.onLoad(async (query) => {
      var _a;
      const brandId = Number(query == null ? void 0 : query.brandId);
      initialBrandId.value = Number.isNaN(brandId) ? null : brandId;
      await loadBrandCategories();
      if (!brandCategories.value.length)
        return;
      let activeIndex = 0;
      let activeId = brandCategories.value[0].id;
      if (initialBrandId.value) {
        const idx = brandCategories.value.findIndex((b) => Number(b.id) === initialBrandId.value);
        if (idx >= 0) {
          activeIndex = idx;
          activeId = brandCategories.value[idx].id;
        }
      }
      await common_vendor.nextTick$1();
      (_a = categoryRef.value) == null ? void 0 : _a.updateActiveIndex(activeIndex);
      loadGoodsByCategory(activeId);
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.w(({
          item
        }, s0, i0) => {
          return common_vendor.e({
            a: item.img,
            b: common_vendor.t(item.title),
            c: common_vendor.t(item.desc),
            d: item.price
          }, item.price ? {
            e: common_vendor.t(item.price)
          } : {}, {
            f: common_vendor.o(($event) => onConsult(item)),
            g: i0,
            h: s0
          });
        }, {
          name: "d",
          path: "a",
          vueId: "6988950f-0"
        }),
        b: common_vendor.sr(categoryRef, "6988950f-0", {
          "k": "categoryRef"
        }),
        c: common_vendor.o(onCategoryChange),
        d: common_vendor.p({
          categories: brandCategories.value,
          height: "100vh",
          rightWidth: "550rpx"
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-6988950f"]]);
wx.createPage(MiniProgramPage);
