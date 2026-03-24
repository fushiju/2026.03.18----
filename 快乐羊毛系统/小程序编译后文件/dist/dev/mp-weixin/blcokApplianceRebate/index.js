"use strict";
const common_vendor = require("../common/vendor.js");
const api_link = require("../api/link.js");
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const bannerList = common_vendor.ref([
      {
        img: "https://img1.baidu.com/it/u=3680719198,3966743983&fm=253&app=120&f=JPEG?w=1422&h=800"
      },
      {
        img: "https://img2.baidu.com/it/u=1503597280,1645009600&fm=253&app=120&f=JPEG?w=1422&h=800"
      }
    ]);
    const brandList = common_vendor.ref([]);
    const onBrandClick = (item) => {
      const autograph = common_vendor.index.getStorageSync("autograph");
      if (!autograph) {
        common_vendor.index.showToast({
          title: "请先登录",
          icon: "none",
          duration: 1500
        });
        setTimeout(() => {
          common_vendor.index.navigateTo({
            url: "/subPages/login"
          });
        }, 1500);
        return;
      }
      common_vendor.index.navigateTo({
        url: `/blcokApplianceRebate/applicanceList?brandId=${encodeURIComponent(
          item.id
        )}&brandName=${encodeURIComponent(item.name)}`
      });
    };
    const initPage = async () => {
      try {
        const res = await api_link.categroy();
        const list = Array.isArray(res.data) ? res.data : res.data && Array.isArray(res.data.data) ? res.data.data : [];
        const target = list.find((item) => Number(item.id) === 11);
        const children = (target == null ? void 0 : target.children) || [];
        brandList.value = children.map((child) => ({
          id: child.id,
          name: child.category_name || child.goods_name || "",
          img: child.category_img || child.goods_img || ""
        }));
      } catch (error) {
        brandList.value = [];
      }
    };
    common_vendor.onMounted(() => {
      initPage();
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.f(bannerList.value, (item, idx, i0) => {
          return {
            a: item.img,
            b: idx
          };
        }),
        b: common_vendor.f(brandList.value, (item, k0, i0) => {
          return {
            a: item.img,
            b: common_vendor.t(item.name),
            c: item.id,
            d: common_vendor.o(($event) => onBrandClick(item), item.id)
          };
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-0b293454"]]);
wx.createPage(MiniProgramPage);
