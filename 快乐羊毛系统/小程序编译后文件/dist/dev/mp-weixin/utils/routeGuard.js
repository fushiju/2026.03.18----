"use strict";
const common_vendor = require("../common/vendor.js");
const authPages = [
  "/pages/my",
  "/subPages/order/list",
  "/subPages/addressAccount/list",
  "/subPages/collect",
  "/subPages/coupon/list",
  "/subPages/setting/list",
  "/subPages/distributor/index",
  "/subPages/distributor/myMembers",
  "/endAgent/index"
];
function isLoggedIn() {
  const autograph = common_vendor.index.getStorageSync("autograph");
  return !!autograph;
}
function needAuth(url) {
  const path = url.split("?")[0];
  return authPages.some((page) => path.includes(page));
}
function redirectToLogin(fromUrl) {
  common_vendor.index.showToast({
    title: "请先登录",
    icon: "none",
    duration: 1500
  });
  setTimeout(() => {
    common_vendor.index.navigateTo({
      url: "/subPages/login",
      fail: () => {
        common_vendor.index.reLaunch({
          url: "/subPages/login"
        });
      }
    });
  }, 1500);
}
function setupRouteGuard() {
  common_vendor.index.addInterceptor("navigateTo", {
    invoke(args) {
      const url = args.url;
      if (needAuth(url) && !isLoggedIn()) {
        redirectToLogin();
        return false;
      }
      return true;
    }
  });
  common_vendor.index.addInterceptor("redirectTo", {
    invoke(args) {
      const url = args.url;
      if (needAuth(url) && !isLoggedIn()) {
        redirectToLogin();
        return false;
      }
      return true;
    }
  });
  common_vendor.index.addInterceptor("reLaunch", {
    invoke(args) {
      const url = args.url;
      if (needAuth(url) && !isLoggedIn()) {
        redirectToLogin();
        return false;
      }
      return true;
    }
  });
  common_vendor.index.addInterceptor("switchTab", {
    invoke(args) {
      const url = args.url;
      if (needAuth(url) && !isLoggedIn()) {
        redirectToLogin();
        return false;
      }
      return true;
    }
  });
}
exports.setupRouteGuard = setupRouteGuard;
