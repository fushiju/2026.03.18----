"use strict";
const common_vendor = require("../common/vendor.js");
const api_link = require("../api/link.js");
if (!Math) {
  (Icon + Navbar)();
}
const Navbar = () => "../components/NavBar/Navbar.js";
const Icon = () => "../components/Icon/Icon.js";
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const navList = common_vendor.ref([]);
    const userInfo = common_vendor.ref({
      id: 0
    });
    let placeholderList = common_vendor.ref(["搜淘宝/京东/拼多多优惠", "大牌折扣享不停", "山姆年卡"]);
    const currentPlaceholderIndex = common_vendor.ref(0);
    const isSliding = common_vendor.ref(false);
    let intervalId = null;
    const changePlaceholder = async () => {
      isSliding.value = true;
      setTimeout(() => {
        currentPlaceholderIndex.value = (currentPlaceholderIndex.value + 1) % placeholderList.value.length;
        isSliding.value = false;
      }, 300);
    };
    const goUrl = (e) => {
      switch (e.jump_type) {
        case 1:
          common_vendor.index.navigateToMiniProgram({
            appId: e.appid,
            path: e.link_url,
            success(res) {
            }
          });
          break;
        case 2:
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
          return proxy.$u.goUrl(`/subPages/webview?url=${e.jump_url}`);
        case 3:
          return proxy.$u.goUrl(`${e.jump_url}?id=${e.id}`);
      }
    };
    const startRotation = () => {
      intervalId = setInterval(() => {
        changePlaceholder();
      }, 3e3);
    };
    const stopRotation = () => {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    };
    const initPage = async () => {
      let res = await api_link.categroy();
      navList.value = res.data.reverse();
    };
    common_vendor.onMounted(() => {
      initPage();
      startRotation();
    });
    common_vendor.onUnmounted(() => {
      stopRotation();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.unref(userInfo).id
      }, common_vendor.unref(userInfo).id ? {} : {
        b: common_vendor.p({
          name: "my",
          size: 36,
          color: "#333"
        })
      }, {
        c: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/pages/my")),
        d: common_vendor.p({
          name: "search",
          size: 30,
          color: "#333"
        }),
        e: common_vendor.f(common_vendor.unref(placeholderList), (item, index, i0) => {
          return {
            a: common_vendor.t(item),
            b: index,
            c: index === common_vendor.unref(currentPlaceholderIndex)
          };
        }),
        f: common_vendor.unref(isSliding) ? 1 : "",
        g: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/search/search")),
        h: common_vendor.f(common_vendor.unref(navList), (item, index, i0) => {
          return {
            a: item.category_img,
            b: common_vendor.t(item.category_name),
            c: common_vendor.t(item.desc),
            d: index,
            e: common_vendor.o(($event) => goUrl(item), index)
          };
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-d1d3d0d7"]]);
wx.createPage(MiniProgramPage);
