"use strict";
Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
const common_vendor = require("./common/vendor.js");
const api_common = require("./api/common.js");
const common_utils = require("./common/utils.js");
const utils_routeGuard = require("./utils/routeGuard.js");
if (!Math) {
  "./pages/index.js";
  "./pages/my.js";
  "./subPages/login.js";
  "./subPages/bindPhone.js";
  "./subPages/search/search.js";
  "./subPages/search/searchResult.js";
  "./subPages/order/list.js";
  "./subPages/order/detail.js";
  "./subPages/collect.js";
  "./subPages/distributor/index.js";
  "./subPages/distributor/invitation.js";
  "./subPages/distributor/myMembers.js";
  "./subPages/coupon/list.js";
  "./subPages/coupon/record.js";
  "./subPages/setting/list.js";
  "./subPages/webview.js";
  "./subPages/selCity.js";
  "./subPages/addressAccount/list.js";
  "./subPages/addressAccount/update.js";
  "./subPages/refund/apply.js";
  "./subPages/myPrice.js";
  "./subPages/refund/list.js";
  "./subPages/refund/detail.js";
  "./subPages/returnGoods/orderStatusDetail.js";
  "./subPages/complaints/complaints.js";
  "./subPages/complaints/list.js";
  "./subPages/complaints/detail.js";
  "./subPages/evaluate.js";
  "./subPages/alipay.js";
  "./subPages/car.js";
  "./blcokApplianceRebate/index.js";
  "./blcokApplianceRebate/applicanceList.js";
  "./blcokDiscount/index.js";
  "./blockFreeSouce/index.js";
  "./blockMemberRecharge/index.js";
  "./blockMemberRecharge/recharge.js";
  "./blockMemberRecharge/orderConfirm.js";
  "./blockTakeoutDiscount/index.js";
  "./blockTakeoutDiscount/discountDetail.js";
  "./blockTaxi/index.js";
  "./endAgent/index.js";
  "./endAgent/agent/index.js";
  "./endAgent/order/list.js";
  "./endAgent/addBrand/list.js";
  "./endAgent/addBrand/add.js";
  "./endAgent/order/ordertui.js";
  "./blockMovie/index.js";
  "./blockMovie/selCinema.js";
  "./blockMovie/selTime.js";
  "./blockMovie/seatSelection.js";
  "./blockMovie/myOrder.js";
  "./blockMovie/myOrders.js";
  "./blockMovie/orderDetail.js";
}
const _sfc_main = {
  __name: "App",
  setup(__props) {
    common_vendor.onLaunch(async () => {
      let config = await api_common.configInfo();
      common_vendor.index.setStorageSync("config", config);
    });
    return () => {
    };
  }
};
utils_routeGuard.setupRouteGuard();
function createApp() {
  const app = common_vendor.createSSRApp(_sfc_main);
  app.config.globalProperties.$u = common_utils.u;
  return {
    app
  };
}
createApp().app.mount("#app");
exports.createApp = createApp;
