"use strict";
const common_vendor = require("../common/vendor.js");
const api_link = require("../api/link.js");
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const iconList = common_vendor.ref([]);
    const initPage = async () => {
      try {
        const res = await api_link.categroy();
        const list = Array.isArray(res.data) ? res.data : res.data && Array.isArray(res.data.data) ? res.data.data : [];
        const target = list.find((item) => Number(item.id) === 8);
        const children = (target == null ? void 0 : target.children) || [];
        iconList.value = children.map((child) => ({
          ...child,
          goods_img: child.goods_img || child.category_img || "",
          goods_name: child.goods_name || child.category_name || ""
        }));
      } catch (error) {
        iconList.value = [];
      }
    };
    const handleItemClick = (e) => {
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
    common_vendor.onMounted(() => {
      initPage();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(iconList.value, (item, k0, i0) => {
          return {
            a: item.goods_img,
            b: common_vendor.t(item.goods_name),
            c: item.id,
            d: common_vendor.o(($event) => handleItemClick(item), item.id)
          };
        }),
        b: iconList.value.length === 0
      }, iconList.value.length === 0 ? {} : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-a5a2e46e"]]);
wx.createPage(MiniProgramPage);
