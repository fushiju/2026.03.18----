"use strict";
const common_vendor = require("../../common/vendor.js");
const api_common = require("../../api/common.js");
const api_order = require("../../api/order.js");
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
        label: "待支付"
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
        title: "待支付",
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
      initData(true);
    };
    const page = common_vendor.ref(1);
    const pageSize = common_vendor.ref(10);
    const hasMore = common_vendor.ref(true);
    const loading = common_vendor.ref(false);
    const isRefresh = common_vendor.ref(false);
    const initData = async (refresh = false) => {
      var _a;
      if (loading.value || !hasMore.value && !refresh)
        return;
      loading.value = true;
      isRefresh.value = refresh;
      if (refresh) {
        page.value = 1;
        list.value = [];
        hasMore.value = true;
      }
      try {
        let params = {
          page: page.value,
          page_size: pageSize.value,
          // 确保传递 pageSize
          pay_type: orderStatus.value[activeIndex.value].value
        };
        const res = await api_common.orderList(params);
        const newList = ((_a = res.data) == null ? void 0 : _a.data) || res.data || [];
        if (refresh) {
          list.value = newList;
        } else {
          list.value = [...list.value, ...newList];
        }
        hasMore.value = newList.length >= pageSize.value;
        if (hasMore.value) {
          page.value++;
        }
        if (refresh) {
          common_vendor.index.stopPullDownRefresh();
        }
      } catch (error) {
        common_vendor.index.showToast({ title: "加载失败", icon: "none" });
      } finally {
        loading.value = false;
        isRefresh.value = false;
      }
    };
    common_vendor.onReachBottom(() => {
      if (!loading.value && hasMore.value) {
        initData(false);
      }
    });
    common_vendor.onPullDownRefresh(() => {
      initData(true);
    });
    common_vendor.onShow(() => {
      initData(true);
    });
    common_vendor.onLoad(async (e) => {
      activeIndex.value = orderStatus.value.findIndex((item) => item.value === Number(e.tab));
      initData(true);
    });
    const handleCancelOrder = async (id) => {
      common_vendor.index.showModal({
        title: "提示",
        content: "确定取消订单吗？",
        success: async (res) => {
          if (res.confirm) {
            let params = {
              id
            };
            const res2 = await api_order.cancelOrder(params);
            if (res2.code === 200) {
              common_vendor.index.showToast({
                title: "取消成功",
                icon: "none"
              });
              initData(true);
            }
          }
        }
      });
    };
    const handlePayOrder = async (item) => {
      let params = {
        id: item.id
      };
      const result = await api_order.rePayOrder(params);
      if (result.code === 200) {
        if (item.pay_model === 1) {
          common_vendor.wx$1.requestPayment({
            provider: "wxpay",
            timeStamp: result.data.pay_list.timeStamp,
            nonceStr: result.data.pay_list.nonceStr,
            package: result.data.pay_list.package,
            signType: "MD5",
            paySign: result.data.pay_list.paySign,
            success: function(res) {
              initData(true);
            }
          });
        }
        if (item.pay_model === 3) {
          const pay_list_now = {
            orderInfo: result.data.data.pay_list,
            provider: "alipay"
          };
          let alipay_params = `?autograph=${common_vendor.index.getStorageSync("autograph")}&id=${result.data.order_id}`;
          const obj = Object.assign(pay_list_now, {
            order_id: result.data.order_id,
            page_url: `/subPages/order/list?tab=2`,
            alipay_params
          });
          common_vendor.index.setStorageSync("pay_list", obj);
          common_vendor.index.redirectTo({
            url: `/subPages/alipay${alipay_params}`
          });
          return;
        }
        if (result.data && item.pay_model == 2) {
          proxy.$u.toast(" 支付成功 ");
          setTimeout(() => {
            initData();
          }, 1500);
        }
      }
    };
    const handleDelOrder = async (id) => {
      common_vendor.index.showModal({
        title: "提示",
        content: "确定删除订单吗？",
        success: async (res) => {
          if (res.confirm) {
            let params = {
              id
            };
            const res2 = await api_order.delOrder(params);
            if (res2.code === 200) {
              common_vendor.index.showToast({
                title: "删除成功",
                icon: "none"
              });
              initData(true);
            }
          }
        }
      });
    };
    const handleAgainOrder = async (e) => {
      let params = {
        order_id: e.id
      };
      const res = await api_order.againOrder(params);
      if (res.code === 200) {
        proxy.$u.goUrl(`/blockMemberRecharge/recharge?id=${e.coach_id}&title=${e.coach_info.coach_name}`);
      }
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
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
            e: "24e41399-0-" + i0,
            f: common_vendor.p({
              value: item.pay_price
            }),
            g: item.pay_type == 1
          }, item.pay_type == 1 ? {
            h: common_vendor.o(($event) => handleCancelOrder(item.id), index),
            i: common_vendor.o(($event) => handlePayOrder(item), index)
          } : {}, {
            j: item.pay_type == -1 || item.pay_type == 7
          }, item.pay_type == -1 || item.pay_type == 7 ? {
            k: common_vendor.o(($event) => handleDelOrder(item.id), index)
          } : {}, {
            l: item.can_refund > 0
          }, item.can_refund > 0 ? {
            m: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/refund/apply?id=${item.id}`), index)
          } : {}, {
            n: item.coach_id && item.pay_type == 7
          }, item.coach_id && item.pay_type == 7 ? common_vendor.e({
            o: !item.is_comment
          }, !item.is_comment ? {
            p: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/evaluate?id=${item.id}`), index)
          } : {}, {
            q: item.can_again
          }, item.can_again ? {
            r: common_vendor.o(($event) => handleAgainOrder(item), index)
          } : {}) : {}, {
            s: index,
            t: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/order/detail?id=${item.id}`), index)
          });
        }),
        c: common_vendor.unref(loading) && common_vendor.unref(list).length > 0
      }, common_vendor.unref(loading) && common_vendor.unref(list).length > 0 ? {} : !common_vendor.unref(hasMore) && common_vendor.unref(list).length > 0 ? {} : {}, {
        d: !common_vendor.unref(hasMore) && common_vendor.unref(list).length > 0,
        e: !common_vendor.unref(loading) && common_vendor.unref(list).length === 0
      }, !common_vendor.unref(loading) && common_vendor.unref(list).length === 0 ? {} : {}, {
        f: common_vendor.sr("backToTopRef", "24e41399-1"),
        g: common_vendor.p({
          threshold: 300,
          position: "bottom-right",
          size: 70,
          ["background-color"]: "#cacaca",
          color: "#ffffff"
        })
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-24e41399"]]);
wx.createPage(MiniProgramPage);
