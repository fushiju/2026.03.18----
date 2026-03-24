"use strict";
const common_vendor = require("../common/vendor.js");
const api_order = require("../api/order.js");
const api_brand = require("../api/brand.js");
if (!Math) {
  (Price + Icon)();
}
const Price = () => "../components/Price/Price.js";
const Icon = () => "../components/Icon/Icon.js";
const _sfc_main = {
  __name: "car",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const accountAddressId = common_vendor.ref(0);
    const account = common_vendor.ref(0);
    common_vendor.index.$on("selCity", (data) => {
      accountAddressId.value = data.id;
      account.value = data.mobile;
    });
    const coupon = common_vendor.ref({});
    common_vendor.index.$on("coupon", (e) => {
      coupon.value = e;
    });
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
    const carList = common_vendor.ref([]);
    const carData = common_vendor.ref({});
    const initData = async () => {
      let res = await api_brand.getSpecificationList();
      carList.value = res.data.data.filter((item) => item.car_num != 0);
      carData.value.num = res.data.car_count;
      carData.value.price = res.data.car_price;
    };
    const minus = async (e) => {
      let p = {
        id: e.car_id,
        num: 1
      };
      let result = await api_order.delCar(p);
      if (result.code === 200)
        initData();
    };
    const add = async (e) => {
      let p = {
        coach_id: e.coach_id,
        num: 1,
        service_id: e.id
      };
      let result = await api_order.addCar(p);
      if (result.code === 200)
        initData();
    };
    common_vendor.onLoad(() => {
      initData();
    });
    const payParams = common_vendor.ref({});
    const submit = async () => {
      common_vendor.index.showLoading({
        title: "正在提交订单..."
      });
      setTimeout(async () => {
        payParams.value.is_store = 0;
        payParams.value.coach_id = 0;
        payParams.value.car_type = 1;
        payParams.value.coupon_id = coupon.value.id;
        payParams.value.address_id = accountAddressId.value;
        payParams.value.start_time = Math.floor(Date.now() / 1e3);
        payParams.value.text = "";
        payParams.value.pay_model = pay_model.value;
        return;
      }, 1e3);
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.t(common_vendor.unref(account) ? common_vendor.unref(account) : "请输入手机号码"),
        b: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/addressAccount/list")),
        c: common_vendor.f(common_vendor.unref(carList), (item, index, i0) => {
          return {
            a: item.cover,
            b: common_vendor.t(item.cate_list[0].title),
            c: common_vendor.t(item.title),
            d: common_vendor.t(item.sub_title),
            e: common_vendor.f(item.position_title, (i, k, i1) => {
              return {
                a: common_vendor.t(i),
                b: k
              };
            }),
            f: "9dc856dd-0-" + i0,
            g: common_vendor.p({
              value: item.price
            }),
            h: common_vendor.o(($event) => minus(item), index),
            i: common_vendor.t(item.car_num),
            j: common_vendor.o(($event) => add(item), index),
            k: index
          };
        }),
        d: common_vendor.unref(coupon).id
      }, common_vendor.unref(coupon).id ? {
        e: common_vendor.t(common_vendor.unref(coupon).discount)
      } : {
        f: common_vendor.p({
          name: "right",
          size: "24rpx",
          color: "#bababa"
        })
      }, {
        g: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/coupon/list?type=use`)),
        h: common_vendor.f(common_vendor.unref(payList), (item, index, i0) => {
          return {
            a: "9dc856dd-2-" + i0,
            b: common_vendor.p({
              name: item.icon,
              color: "#f9be5f",
              size: "48rpx"
            }),
            c: common_vendor.t(item.name),
            d: "9dc856dd-3-" + i0,
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
        i: common_vendor.p({
          value: common_vendor.unref(carData).price
        }),
        j: common_vendor.t(common_vendor.unref(carData).num),
        k: common_vendor.o(submit)
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-9dc856dd"]]);
wx.createPage(MiniProgramPage);
