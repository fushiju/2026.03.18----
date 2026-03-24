"use strict";
const common_vendor = require("../common/vendor.js");
if (!Math) {
  (Price + Icon + Popup)();
}
const Icon = () => "../components/Icon/Icon.js";
const Popup = () => "../components/Popup/Popup.js";
const Price = () => "../components/Price/Price.js";
const _sfc_main = {
  __name: "orderConfirm",
  setup(__props) {
    let isShowSubsidy = common_vendor.ref(false);
    const showSubsidy = () => {
      isShowSubsidy.value = !isShowSubsidy.value;
    };
    let isShowCoupon = common_vendor.ref(false);
    const showCoupon = () => {
      isShowCoupon.value = !isShowCoupon.value;
    };
    let couponTypeStatus = common_vendor.ref(0);
    const selCouponType = (index) => {
      couponTypeStatus.value = index;
    };
    const couponType = common_vendor.ref([
      {
        id: 1,
        name: "可以优惠券",
        num: 1
      },
      {
        id: 2,
        name: "不可以优惠券",
        num: 0
      }
    ]);
    const couponList = common_vendor.ref([
      {
        id: 1,
        price: "1.00",
        couponDesc: "领券减1元",
        title: "充值无门槛通用券",
        time: "领取当日起2天有效",
        type: "充值券",
        detail: "现充值会员直充产现充值会员直充产品使用现充值会员直充产品使用现充值会员直充产品使用品使用",
        isDetail: false
      }
    ]);
    const openDetail = (e) => {
      e.isDetail = !e.isDetail;
    };
    const payList = common_vendor.ref([
      {
        id: 1,
        icon: "aliPay",
        name: "支付宝支付",
        ischeck: true
      },
      {
        id: 2,
        icon: "weChatPay",
        name: "微信支付",
        ischeck: false
      }
    ]);
    let isShowDiscountDetail = common_vendor.ref(false);
    const showDiscountDetail = () => {
      isShowDiscountDetail.value = !isShowDiscountDetail.value;
    };
    const selPay = (index) => {
      payList.value.forEach((item) => {
        item.ischeck = false;
      });
      payList.value[index].ischeck = true;
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.p({
          value: "24"
        }),
        b: common_vendor.p({
          name: "right",
          size: "34rpx",
          color: "#ccc"
        }),
        c: common_vendor.o(showCoupon),
        d: common_vendor.p({
          name: "ask",
          size: "24rpx",
          color: "#ccc",
          customStyle: {
            marginLeft: "10rpx"
          }
        }),
        e: common_vendor.o(showSubsidy),
        f: common_vendor.f(common_vendor.unref(payList), (item, index, i0) => {
          return {
            a: "7fc4faaa-3-" + i0,
            b: common_vendor.p({
              name: item.icon,
              color: "#f9be5f"
            }),
            c: common_vendor.t(item.name),
            d: "7fc4faaa-4-" + i0,
            e: common_vendor.p({
              name: `${item.ischeck ? "xuanzhongduigou" : "check_normal"}`,
              size: "28rpx",
              color: item.ischeck ? "#f5954f" : "#ccc"
            }),
            f: index,
            g: common_vendor.o(($event) => selPay(index), index)
          };
        }),
        g: common_vendor.unref(isShowDiscountDetail)
      }, common_vendor.unref(isShowDiscountDetail) ? {} : {}, {
        h: common_vendor.unref(isShowDiscountDetail)
      }, common_vendor.unref(isShowDiscountDetail) ? {
        i: common_vendor.p({
          name: "close",
          color: "#ccc",
          size: "24rpx"
        }),
        j: common_vendor.o(showDiscountDetail)
      } : {}, {
        k: common_vendor.p({
          value: "24"
        }),
        l: common_vendor.p({
          name: common_vendor.unref(isShowDiscountDetail) ? "down" : "up",
          color: "#838383",
          size: "30rpx"
        }),
        m: common_vendor.o(showDiscountDetail),
        n: common_vendor.o(showSubsidy),
        o: common_vendor.o(($event) => common_vendor.isRef(isShowSubsidy) ? isShowSubsidy.value = $event : isShowSubsidy = $event),
        p: common_vendor.p({
          showTitle: false,
          showButtons: false,
          visible: common_vendor.unref(isShowSubsidy)
        }),
        q: common_vendor.f(common_vendor.unref(couponType), (item, index, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: common_vendor.t(item.num),
            c: common_vendor.unref(couponTypeStatus) === index ? 1 : "",
            d: index,
            e: common_vendor.o(($event) => selCouponType(index), index)
          };
        }),
        r: common_vendor.f(common_vendor.unref(couponList), (item, index, i0) => {
          return common_vendor.e({
            a: "7fc4faaa-10-" + i0 + ",7fc4faaa-9",
            b: common_vendor.p({
              value: item.price
            }),
            c: common_vendor.t(item.couponDesc),
            d: common_vendor.t(item.type),
            e: common_vendor.t(item.title),
            f: common_vendor.t(item.time),
            g: "7fc4faaa-11-" + i0 + ",7fc4faaa-9",
            h: common_vendor.p({
              name: item.isDetail ? "up" : "down",
              ["custom-color"]: "##3c3c3c",
              size: "30rpx"
            }),
            i: common_vendor.o(($event) => openDetail(item), index),
            j: item.isDetail
          }, item.isDetail ? {
            k: common_vendor.t(item.detail)
          } : {}, {
            l: !item.isDetail
          }, !item.isDetail ? {} : {}, {
            m: index
          });
        }),
        s: common_vendor.o(($event) => common_vendor.isRef(isShowCoupon) ? isShowCoupon.value = $event : isShowCoupon = $event),
        t: common_vendor.p({
          position: "bottom",
          title: "优惠券",
          [":mask-closable"]: true,
          animation: "slide",
          ["animation-direction"]: "bottom",
          width: 1900,
          maxHeight: 500,
          showButtons: false,
          visible: common_vendor.unref(isShowCoupon)
        })
      });
    };
  }
};
wx.createPage(_sfc_main);
