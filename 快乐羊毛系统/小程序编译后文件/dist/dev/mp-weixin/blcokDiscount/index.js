"use strict";
const common_vendor = require("../common/vendor.js");
const api_link = require("../api/link.js");
const api_blcokDiscount = require("../api/blcokDiscount.js");
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const iconList = common_vendor.ref([]);
    const initPage = async (id) => {
      let temp = await api_link.goodsList({ categoryId: id });
      let list = await api_blcokDiscount.brandList({ coachType: 1 });
      console.log(list);
      if (!temp.data)
        return;
      iconList.value = temp.data;
      iconList.value.map((i) => {
        i.id = i.id;
        i.name = i.goods_name;
        i.icon = i.goods_img;
      });
    };
    common_vendor.onLoad((e) => {
      initPage(e.id);
    });
    const goUrl = async (e) => {
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
      common_vendor.index.navigateToMiniProgram({
        appId: e.appid,
        path: e.link_url,
        success(res) {
        }
      });
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.f(common_vendor.unref(iconList), (item, index, i0) => {
          return {
            a: item.icon,
            b: common_vendor.t(item.name),
            c: index,
            d: common_vendor.o(($event) => goUrl(item.link_info), index)
          };
        })
      };
    };
  }
};
wx.createPage(_sfc_main);
