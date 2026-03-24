"use strict";
const common_vendor = require("../../common/vendor.js");
const api_endAgent = require("../../api/endAgent.js");
if (!Math) {
  (Price + BackTop)();
}
const BackTop = () => "../../components/BackTop/BackTop.js";
const Price = () => "../../components/Price/Price.js";
const _sfc_main = {
  __name: "list",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const activeIndex = common_vendor.ref(0);
    const list = common_vendor.ref([]);
    const status = [
      {
        value: -1,
        label: "已取消"
      },
      {
        value: 1,
        label: "待付款"
      },
      {
        value: 2,
        label: "已支付"
      },
      {
        value: 6,
        label: "发货中"
      },
      {
        value: 7,
        label: "已完成"
      },
      {
        title: "待审核",
        value: 12
      }
    ];
    const orderStatus = common_vendor.ref([
      {
        title: "全部",
        value: 0
      },
      {
        title: "待付款",
        value: 1
      },
      {
        title: "发货中",
        value: 6
      },
      {
        title: "已完成",
        value: 7
      },
      {
        title: "待审核",
        value: 12
      }
    ]);
    const getCurPayType = (pay_type) => {
      const item = status.find((val) => val.value == pay_type);
      return item ? item.label : "";
    };
    const onTabClick = (index) => {
      activeIndex.value = index;
      initData();
    };
    const initData = async () => {
      let params = {
        page: 1,
        pay_type: orderStatus.value[activeIndex.value].value
      };
      const res = await api_endAgent.agentStatus(params);
      list.value = res.data.data;
      console.log(list.value);
    };
    common_vendor.onLoad(async (e) => {
      activeIndex.value = orderStatus.value.findIndex(
        (item) => item.value === Number(e.tab)
      );
      console.log(activeIndex.value);
      initData();
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.f(common_vendor.unref(orderStatus), (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.unref(activeIndex) === index ? 1 : "",
            c: index,
            d: common_vendor.o(($event) => onTabClick(index), index)
          };
        }),
        b: common_vendor.f(common_vendor.unref(list), (item, index, i0) => {
          return common_vendor.e({
            a: common_vendor.t(item.order_code),
            b: common_vendor.t(getCurPayType(item.pay_type)),
            c: common_vendor.f(item.order_goods, (i, k, i1) => {
              return {
                a: i.goods_cover,
                b: common_vendor.t(i.goods_name),
                c: k
              };
            }),
            d: common_vendor.t(item.create_time),
            e: "82bfec46-0-" + i0,
            f: common_vendor.p({
              value: item.pay_price
            }),
            g: item.pay_type == 1
          }, item.pay_type == 1 ? {} : {}, {
            h: item.pay_type == -1 || item.pay_type == 7
          }, item.pay_type == -1 || item.pay_type == 7 ? {} : {}, {
            i: item.can_refund > 0
          }, item.can_refund > 0 ? {
            j: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/refund/apply?id=${item.id}`), index)
          } : {}, {
            k: item.coach_id && item.pay_type == 7
          }, item.coach_id && item.pay_type == 7 ? {
            l: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/evaluate"), index)
          } : {}, {
            m: index,
            n: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/order/detail?id=${item.id}`), index)
          });
        }),
        c: common_vendor.sr("backToTopRef", "82bfec46-1"),
        d: common_vendor.p({
          threshold: 300,
          position: "bottom-right",
          size: 70,
          ["background-color"]: "#cacaca",
          color: "#ffffff"
        })
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-82bfec46"]]);
wx.createPage(MiniProgramPage);
