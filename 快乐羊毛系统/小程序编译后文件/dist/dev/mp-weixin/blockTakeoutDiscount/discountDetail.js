"use strict";
const common_vendor = require("../common/vendor.js");
const api_brand = require("../api/brand.js");
const api_order = require("../api/order.js");
if (!Math) {
  (Icon + Popup)();
}
const Icon = () => "../components/Icon/Icon.js";
const Popup = () => "../components/Popup/Popup.js";
const _sfc_main = {
  __name: "discountDetail",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const account = common_vendor.ref("");
    const showDetail = common_vendor.ref(false);
    const payList = common_vendor.ref([]);
    const detailInfo = common_vendor.ref(null);
    const serviceList = common_vendor.ref([]);
    const isShowSubsidy = common_vendor.ref(false);
    const orderPreview = common_vendor.ref(null);
    const coachId = common_vendor.ref("");
    const pay_model = common_vendor.ref(1);
    const serviceId = common_vendor.ref("");
    const selPay = (index) => {
      payList.value.forEach((item) => {
        item.ischeck = false;
      });
      payList.value[index].ischeck = true;
      pay_model.value = payList.value[index].id;
    };
    const showSubsidy = () => {
      isShowSubsidy.value = !isShowSubsidy.value;
    };
    const Detail = async (id) => {
      const res = await api_brand.brandListinfo({ id });
      detailInfo.value = res.data;
    };
    const getServiceList = async (id) => {
      const res = await api_brand.getSpecificationList({ coach_id: id });
      serviceList.value = res.data && res.data.data ? res.data.data : [];
      if (serviceList.value.length > 0) {
        serviceId(serviceList.value[0].id);
        getOrderPreview(serviceList.value[0].id, id);
      }
    };
    const accountAddressId = common_vendor.ref(0);
    const getOrderPreview = async (serviceId2, coachId2) => {
      try {
        const res = await api_order.payOrderInfo({
          service_id: serviceId2,
          coach_id: coachId2,
          coupon_id: 0,
          address_id: 0
        });
        orderPreview.value = res.data;
        if (res && res.address_info) {
          account.value = res.address_info.mobile || "";
          accountAddressId.value = res.address_info.id || 0;
        }
      } catch (error) {
      }
    };
    common_vendor.index.$on("selCity", (data) => {
      accountAddressId.value = data.id;
      account.value = data.mobile;
    });
    const onPay = async () => {
      let params = {
        address_id: accountAddressId.value,
        is_store: "0",
        //默认0
        coach_id: coachId.value,
        //商品id
        car_type: 1,
        coupon_id: "0",
        //优惠卷id
        start_time: Date.parse(/* @__PURE__ */ new Date()) / 1e3,
        //获取当前时间戳
        text: "",
        //订单备注
        pay_model: pay_model.value
        //1微信 2余额 3支付宝
      };
      const res = await api_order.payOrder(params);
      if (res.code === 200) {
        common_vendor.index.navigateTo({
          url: "/pages/subPages/alipay?order_id=" + res.data.order_id
        });
      } else {
        common_vendor.index.showToast({
          title: res.msg,
          icon: "none"
        });
      }
    };
    const onaddCar = async () => {
      let params = {
        coach_id: coachId.value,
        num: 1,
        service_id: serviceList.value.length > 0 ? serviceList.value[0].id : 0
      };
      await api_order.addCar(params);
    };
    const handlePay = () => {
      if (!account.value) {
        common_vendor.index.showToast({ title: "请输入充值账号", icon: "none" });
        return;
      }
      onaddCar();
      onPay();
      common_vendor.index.showToast({ title: "正在跳转支付...", icon: "none" });
      common_vendor.index.showToast({ title: "支付成功", icon: "none" });
    };
    common_vendor.onLoad((e) => {
      if (e.id) {
        Detail(e.id);
        getServiceList(e.id);
        coachId.value = e.id;
      }
      const setting = common_vendor.index.getStorageSync("config") || {};
      const allPay = [
        {
          id: 3,
          icon: "aliPay",
          name: "支付宝支付",
          ischeck: false,
          closeKey: "close_alipay"
        },
        {
          id: 1,
          icon: "weChatPay",
          name: "微信支付",
          ischeck: false,
          closeKey: "close_wxpay"
        },
        {
          id: 2,
          icon: "yuezhifu",
          name: "余额支付",
          ischeck: false,
          closeKey: "close_wxpay"
        }
      ];
      payList.value = allPay.filter((item) => setting[item.closeKey] === 0);
      if (payList.value.length > 0) {
        payList.value[0].ischeck = true;
      }
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: detailInfo.value
      }, detailInfo.value ? common_vendor.e({
        b: detailInfo.value.work_img,
        c: common_vendor.t(detailInfo.value.coach_name),
        d: serviceList.value.length > 0
      }, serviceList.value.length > 0 ? {
        e: common_vendor.f(serviceList.value[0].position_title, (tag, i, i0) => {
          return {
            a: common_vendor.t(tag),
            b: i
          };
        })
      } : {}, {
        f: serviceList.value.length > 0
      }, serviceList.value.length > 0 ? {
        g: common_vendor.t(serviceList.value[0].coach_price || ""),
        h: common_vendor.t(serviceList.value[0].init_price)
      } : {}) : {}, {
        i: common_vendor.t(account.value ? account.value : "请选择充值账号"),
        j: !account.value ? 1 : "",
        k: common_vendor.p({
          name: "right",
          size: "28rpx",
          color: "#ccc"
        }),
        l: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/addressAccount/list")),
        m: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/coupon/list")),
        n: common_vendor.p({
          name: "right",
          size: "24rpx",
          color: "#bababa"
        }),
        o: common_vendor.o(showSubsidy),
        p: common_vendor.f(payList.value, (item, index, i0) => {
          return {
            a: "eb44aaa0-2-" + i0,
            b: common_vendor.p({
              name: item.icon,
              color: "#f9be5f",
              size: "48rpx"
            }),
            c: common_vendor.t(item.name),
            d: "eb44aaa0-3-" + i0,
            e: common_vendor.p({
              name: item.ischeck ? "xuanzhongduigou" : "check_normal",
              size: "40rpx",
              color: item.ischeck ? "#ff471f" : "#ccc"
            }),
            f: item.ischeck ? 1 : "",
            g: item.id,
            h: common_vendor.o(($event) => selPay(index), item.id)
          };
        }),
        q: showDetail.value ? 1 : "",
        r: common_vendor.o(($event) => showDetail.value = !showDetail.value),
        s: showDetail.value
      }, showDetail.value ? {} : {}, {
        t: common_vendor.t(serviceList.value.length > 0 ? serviceList.value[0].coach_price : ""),
        v: common_vendor.t(serviceList.value.length > 0 ? serviceList.value[0].init_price - serviceList.value[0].coach_price || 0 : ""),
        w: common_vendor.o(handlePay),
        x: common_vendor.o(showSubsidy),
        y: common_vendor.o(($event) => isShowSubsidy.value = $event),
        z: common_vendor.p({
          showTitle: false,
          showButtons: false,
          visible: isShowSubsidy.value
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-eb44aaa0"]]);
wx.createPage(MiniProgramPage);
