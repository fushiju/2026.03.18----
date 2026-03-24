"use strict";
const common_vendor = require("../common/vendor.js");
const api_brand = require("../api/brand.js");
const api_order = require("../api/order.js");
const api_common = require("../api/common.js");
if (!Math) {
  (Icon + Navbar + Price + Checkbox + Popup)();
}
const Navbar = () => "../components/NavBar/Navbar.js";
const Icon = () => "../components/Icon/Icon.js";
const Checkbox = () => "../components/Checkbox/Checkbox.js";
const Popup = () => "../components/Popup/Popup.js";
const Price = () => "../components/Price/Price.js";
const _sfc_main = {
  __name: "recharge",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    let isShowSubsidy = common_vendor.ref(false);
    const showSubsidy = () => {
      isShowSubsidy.value = !isShowSubsidy.value;
    };
    common_vendor.ref(false);
    const isCollect = common_vendor.ref(false);
    const collect = async () => {
      const p = {
        coach_id: id.value
      };
      if (!isCollect.value) {
        let res = await api_common.addCollect(p);
        if (res.code == 200)
          common_vendor.index.showToast({
            title: "收藏成功",
            icon: "none"
          });
      } else {
        let res = await api_common.delCollect(p);
        if (res.code == 200)
          common_vendor.index.showToast({
            title: "取消收藏",
            icon: "none"
          });
      }
      isCollect.value = !isCollect.value;
    };
    let isAgree = common_vendor.ref(false);
    let showPrice = common_vendor.ref(0);
    let sheng = common_vendor.ref(0);
    common_vendor.ref("");
    const payList = common_vendor.ref([
      {
        id: 1,
        icon: "weChatPay",
        name: "微信支付",
        ischeck: true
      },
      {
        id: 3,
        icon: "aliPay",
        name: "支付宝支付",
        ischeck: false
      },
      {
        id: 2,
        icon: "yuezhifu",
        name: "余额支付",
        ischeck: false
      }
    ]);
    const pay_model = common_vendor.ref(1);
    const selPay = (index) => {
      payList.value.forEach((item) => {
        item.ischeck = false;
      });
      payList.value[index].ischeck = true;
      pay_model.value = payList.value[index].id;
    };
    let selVip = common_vendor.ref(0);
    let selVipItem = common_vendor.ref(0);
    const selVipNameFun = (i, e) => {
      var _a;
      checkVipCategroy.value = i.title;
      selVip.value = e;
      selVipItem.value = 0;
      const firstItem = (_a = i == null ? void 0 : i.list) == null ? void 0 : _a[0];
      if (firstItem) {
        tags.value = firstItem.tag;
        params.value.service_id = firstItem.id;
        getPayOrderInfo();
      }
    };
    const checkVipCategroy = common_vendor.ref("");
    const checkVip = common_vendor.ref("");
    const oldPrice = common_vendor.ref(0);
    const getSpecificationId = common_vendor.ref(0);
    const selVipItemFun = (i, e) => {
      selVipItem.value = e;
      showPrice.value = i.price;
      checkVip.value = i.name;
      oldPrice.value = i.old;
      sheng.value = (i.old - showPrice.value).toFixed(2);
      tags.value = i.tag;
      params.value.service_id = i.id;
      getSpecificationId.value = i.id;
      getPayOrderInfo();
    };
    let isShowDiscountDetail = common_vendor.ref(false);
    const showDiscountDetail = () => {
      isShowDiscountDetail.value = !isShowDiscountDetail.value;
    };
    const rechargeList = common_vendor.ref([]);
    const formatRechargeList = (data) => {
      const map = {};
      data.forEach((item) => {
        const isFirst = item.title && item.title.includes("连续");
        if (!map[item.cate_id]) {
          map[item.cate_id] = {
            id: item.cate_id,
            title: item.cate_title,
            list: []
          };
        }
        map[item.cate_id].list.push({
          id: item.id,
          name: item.sub_title,
          price: item.price,
          old: item.init_price,
          isFirst,
          tag: item.position_title
          // 默认空，可根据后端字段补充
        });
        map[item.cate_id].list.reverse();
      });
      return Object.values(map);
    };
    const params = common_vendor.ref({
      // is_store: 0, //是否到店
      service_id: 0,
      //当前规格 id
      coach_id: 0,
      //品牌 id
      // car_type: 1, //出行方式
      coupon_id: 0,
      //优惠券 id
      address_id: 0
      //默认账号位置信息 id
      // start_time: 0, //服务时间
    });
    common_vendor.onShow(() => {
      common_vendor.index.$on("coupon", (e) => {
        coupon.value = e;
      });
    });
    const initData = async (id2) => {
      var _a;
      getPayOrderInfo();
      let res = await api_brand.getSpecificationList({ coach_id: id2 });
      res.data.data.map((i) => {
        if (i.cate_list !== null) {
          i.cate_id = i.cate_list[0].id;
          i.cate_title = i.cate_list[0].title;
          delete i.cate_list;
        }
      });
      rechargeList.value = formatRechargeList(res.data.data);
      if (rechargeList.value.length > 0) {
        const firstCategory = rechargeList.value[0];
        const firstItem = (_a = firstCategory == null ? void 0 : firstCategory.list) == null ? void 0 : _a[0];
        if (firstItem) {
          selVip.value = 0;
          checkVipCategroy.value = firstCategory.title;
          selVipItem.value = 0;
          checkVip.value = firstItem.name;
          params.value.service_id = firstItem.id;
          showPrice.value = firstItem.price;
          oldPrice.value = firstItem.old;
          sheng.value = (firstItem.old - firstItem.price).toFixed(2);
          tags.value = firstItem.tag;
          getSpecificationId.value = firstItem.id;
        }
      }
    };
    const coupon = common_vendor.ref({});
    const getPayOrderInfo = async () => {
      params.value.coach_id = id.value;
      let payOrder = await api_order.payOrderInfo(params.value);
      coupon.value = {
        coupon_id: payOrder.data.coupon_id,
        discount: payOrder.data.discount
      };
      isCollect.value = payOrder.data.coach_info.collect_num ? true : false;
      account.value = payOrder.data.address_info.mobile;
      accountAddressId.value = payOrder.data.address_info.id;
      await api_order.payOrderInfoConfig();
    };
    const id = common_vendor.ref(0);
    const title = common_vendor.ref("");
    common_vendor.ref(0);
    const tags = common_vendor.ref([]);
    common_vendor.onLoad(async (e) => {
      title.value = e.title;
      id.value = e.id;
      initData(id.value);
    });
    const accountAddressId = common_vendor.ref(0);
    const account = common_vendor.ref(0);
    common_vendor.index.$on("selCity", (data) => {
      accountAddressId.value = data.id;
      account.value = data.mobile;
    });
    const payParams = common_vendor.ref({
      is_store: 0,
      coach_id: "995",
      car_type: 1,
      coupon_id: 0,
      address_id: 7698,
      start_time: 1773462600,
      text: "",
      pay_model: 1
    });
    common_vendor.ref({});
    const handlePay = async () => {
      if (!isAgree.value)
        return common_vendor.index.showToast({
          title: "请先阅读并同意《用户协议》",
          icon: "none"
        });
      common_vendor.index.showLoading({
        title: "正在提交订单..."
      });
      setTimeout(async () => {
        payParams.value.is_store = 0;
        payParams.value.num = 1;
        payParams.value.service_id = getSpecificationId.value;
        payParams.value.coach_id = Number(id.value);
        payParams.value.car_type = 1;
        payParams.value.coupon_id = coupon.value.id || coupon.value.coupon_id;
        payParams.value.address_id = accountAddressId.value;
        payParams.value.start_time = Math.floor(Date.now() / 1e3);
        payParams.value.text = "";
        payParams.value.pay_model = pay_model.value;
        let result = await api_order.payOrder(payParams.value);
        if (pay_model.value === 1) {
          common_vendor.wx$1.requestPayment({
            provider: "wxpay",
            timeStamp: result.data.pay_list.timeStamp,
            nonceStr: result.data.pay_list.nonceStr,
            package: result.data.pay_list.package,
            signType: "MD5",
            paySign: result.data.pay_list.paySign,
            success: function(res) {
              common_vendor.index.showToast({
                title: "支付成功",
                icon: "none",
                duration: 1500,
                complete: function() {
                  proxy.$u.goUrl("/subPages/order/list?tab=0");
                  common_vendor.index.hideLoading();
                }
              });
            }
          });
        }
        if (pay_model.value === 3) {
          const pay_list_now = {
            orderInfo: result.data.data.pay_list,
            provider: "alipay"
          };
          let alipay_params = `?autograph=${common_vendor.index.getStorageSync("autograph")}&id=${result.data.order_id}`;
          const obj = Object.assign(pay_list_now, {
            order_id: result.data.order_id,
            page_url: `/subPages/order/list?tab=0`,
            alipay_params
          });
          common_vendor.index.setStorageSync("pay_list", obj);
          common_vendor.index.redirectTo({
            url: `/subPages/alipay${alipay_params}`
          });
          common_vendor.index.hideLoading();
          return;
        }
        if (result.data && pay_model.value == 2) {
          common_vendor.index.showToast({
            title: "支付成功",
            icon: "none",
            duration: 1500,
            complete: function() {
              proxy.$u.goUrl("/subPages/order/list?tab=0");
              common_vendor.index.hideLoading();
            }
          });
        }
      }, 1e3);
    };
    return (_ctx, _cache) => {
      var _a, _b, _c, _d, _e;
      return common_vendor.e({
        a: common_vendor.p({
          name: "left",
          size: "40rpx"
        }),
        b: common_vendor.t(title.value),
        c: common_vendor.p({
          fixed: true,
          ["safe-area-inset-top"]: true
        }),
        d: common_vendor.t(account.value ? account.value : "请输入手机号码"),
        e: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/addressAccount/list")),
        f: common_vendor.t(title.value),
        g: common_vendor.t(checkVipCategroy.value),
        h: common_vendor.t(checkVip.value),
        i: common_vendor.p({
          name: isCollect.value ? "myCollect-full" : "myCollect",
          size: isCollect.value ? "44rpx" : "46rpx",
          color: isCollect.value ? "#ff0000" : "#bababa"
        }),
        j: common_vendor.o(collect),
        k: common_vendor.f(tags.value, (item, index, i0) => {
          return {
            a: common_vendor.t(item),
            b: index
          };
        }),
        l: common_vendor.p({
          value: common_vendor.unref(showPrice)
        }),
        m: coupon.value.coupon_id || coupon.value.id
      }, coupon.value.coupon_id || coupon.value.id ? {
        n: common_vendor.t(coupon.value.discount)
      } : {
        o: common_vendor.p({
          name: "right",
          size: "24rpx",
          color: "#bababa"
        })
      }, {
        p: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/coupon/list?coach_id=${id.value}&type=use`)),
        q: common_vendor.p({
          name: "right",
          size: "24rpx",
          color: "#bababa"
        }),
        r: common_vendor.o(showSubsidy),
        s: common_vendor.f(rechargeList.value, (item, index, i0) => {
          return common_vendor.e({
            a: item.title
          }, item.title ? {
            b: common_vendor.t(item.title),
            c: common_vendor.n({
              act: common_vendor.unref(selVip) === index
            }),
            d: common_vendor.o(($event) => selVipNameFun(item, index), index)
          } : {}, {
            e: index
          });
        }),
        t: (_b = (_a = rechargeList.value[common_vendor.unref(selVip)]) == null ? void 0 : _a.list) == null ? void 0 : _b.length
      }, ((_d = (_c = rechargeList.value[common_vendor.unref(selVip)]) == null ? void 0 : _c.list) == null ? void 0 : _d.length) ? {
        v: common_vendor.f((_e = rechargeList.value[common_vendor.unref(selVip)]) == null ? void 0 : _e.list, (item, index, i0) => {
          return common_vendor.e({
            a: item.tag
          }, item.tag ? {
            b: common_vendor.t(item.tag[0])
          } : {}, {
            c: common_vendor.t(item.isFirst ? "连续包月" : ""),
            d: common_vendor.t(item.name),
            e: item.isFirst
          }, item.isFirst ? {} : {}, {
            f: "fef14cad-6-" + i0,
            g: common_vendor.p({
              value: item.price,
              color: item.isFirst ? "#fff" : "#333"
            }),
            h: common_vendor.n({
              firstPrice: item.isFirst
            }),
            i: common_vendor.t(item.old),
            j: common_vendor.n({
              act: common_vendor.unref(selVipItem) === index
            }),
            k: index,
            l: common_vendor.o(($event) => selVipItemFun(item, index), index)
          });
        })
      } : {}, {
        w: common_vendor.f(payList.value, (item, index, i0) => {
          return {
            a: "fef14cad-7-" + i0,
            b: common_vendor.p({
              name: item.icon,
              color: "#f9be5f",
              size: "48rpx"
            }),
            c: common_vendor.t(item.name),
            d: "fef14cad-8-" + i0,
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
        x: common_vendor.unref(isShowDiscountDetail)
      }, common_vendor.unref(isShowDiscountDetail) ? {} : {}, {
        y: common_vendor.unref(isShowDiscountDetail)
      }, common_vendor.unref(isShowDiscountDetail) ? {
        z: common_vendor.p({
          name: "close",
          color: "#ccc",
          size: "24rpx"
        }),
        A: common_vendor.o(showDiscountDetail),
        B: common_vendor.t(oldPrice.value)
      } : {}, {
        C: common_vendor.o(($event) => common_vendor.isRef(isAgree) ? isAgree.value = $event : isAgree = $event),
        D: common_vendor.p({
          size: "small",
          checkedColor: "#f9be5f",
          modelValue: common_vendor.unref(isAgree)
        }),
        E: common_vendor.o((...args) => _ctx.showAgreement && _ctx.showAgreement(...args)),
        F: common_vendor.p({
          value: common_vendor.unref(showPrice)
        }),
        G: common_vendor.p({
          name: common_vendor.unref(isShowDiscountDetail) ? "down" : "up",
          color: "#838383",
          size: "30rpx"
        }),
        H: common_vendor.o(showDiscountDetail),
        I: common_vendor.t(common_vendor.unref(showPrice)),
        J: common_vendor.t(common_vendor.unref(sheng)),
        K: common_vendor.o(handlePay),
        L: common_vendor.o(showSubsidy),
        M: common_vendor.o(($event) => common_vendor.isRef(isShowSubsidy) ? isShowSubsidy.value = $event : isShowSubsidy = $event),
        N: common_vendor.p({
          showTitle: false,
          showButtons: false,
          visible: common_vendor.unref(isShowSubsidy)
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-fef14cad"]]);
wx.createPage(MiniProgramPage);
