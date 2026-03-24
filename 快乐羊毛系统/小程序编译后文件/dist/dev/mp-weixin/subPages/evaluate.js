"use strict";
const common_vendor = require("../common/vendor.js");
const api_common = require("../api/common.js");
const api_order = require("../api/order.js");
if (!Array) {
  const _easycom_Price2 = common_vendor.resolveComponent("Price");
  _easycom_Price2();
}
const _easycom_Price = () => "../components/Price/Price.js";
if (!Math) {
  (Rating + _easycom_Price)();
}
const Rating = () => "../components/Rating/Rating.js";
const maxWordCount = 200;
const _sfc_main = {
  __name: "evaluate",
  setup(__props) {
    const loading = common_vendor.ref(true);
    const overallRating = common_vendor.ref(5);
    const ratingText = common_vendor.ref("");
    const evaTags = common_vendor.ref([]);
    const wordCount = common_vendor.ref(0);
    const order_id = common_vendor.ref("");
    const orderDetail = common_vendor.ref({ order_goods: [] });
    const selectedTagIds = common_vendor.computed(() => {
      return evaTags.value.filter((tag) => tag.selected).map((tag) => tag.id);
    });
    const handleInput = (event) => {
      wordCount.value = event.detail.value.length;
    };
    const handleTagClick = (item) => {
      item.selected = !item.selected;
    };
    const initData = async () => {
      var _a, _b;
      loading.value = true;
      try {
        const res = await api_common.evaList();
        evaTags.value = (res.data || []).map((item) => ({ ...item, selected: false }));
        const order = await api_order.orderInfo({ id: order_id.value });
        orderDetail.value = order.data || order || {};
        if ((_b = (_a = orderDetail.value) == null ? void 0 : _a.order_goods) == null ? void 0 : _b.length) {
          orderDetail.value.order_goods.forEach((item, index) => {
            if (item.star === void 0 || item.star === null) {
              item.star = 5;
            }
            item.service_id = item.service_id || item.id || 0;
          });
        } else {
          orderDetail.value.order_goods = [];
        }
      } catch (error) {
        common_vendor.index.showToast({ title: "加载失败", icon: "none" });
      } finally {
        loading.value = false;
      }
    };
    common_vendor.onLoad((e) => {
      order_id.value = e.id;
      initData();
    });
    const handleSubmit = async () => {
      var _a;
      if (!overallRating.value) {
        common_vendor.index.showToast({ title: "请选择整体评分", icon: "none" });
        return;
      }
      if (!((_a = orderDetail.value.order_goods) == null ? void 0 : _a.length)) {
        common_vendor.index.showToast({ title: "没有可评价的商品", icon: "none" });
        return;
      }
      const hasUnratedGoods = orderDetail.value.order_goods.some((item) => !item.star);
      if (hasUnratedGoods) {
        common_vendor.index.showToast({ title: "请为所有商品评分", icon: "none" });
        return;
      }
      const params = {
        lable: selectedTagIds.value,
        order_id: order_id.value,
        service_star: orderDetail.value.order_goods.map((item) => ({
          service_id: item.service_id,
          star: item.star
        })),
        star: overallRating.value,
        text: ratingText.value
      };
      try {
        let result = await api_order.evaOrder(params);
        if (result.code == 200) {
          common_vendor.index.showToast({ title: "评价成功", icon: "none" });
          setTimeout(() => {
            common_vendor.index.navigateBack();
          }, 1500);
        } else {
          common_vendor.index.showToast({ title: result.msg || "评价失败", icon: "none" });
        }
      } catch (error) {
        common_vendor.index.showToast({ title: "提交失败", icon: "none" });
      }
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: loading.value
      }, loading.value ? {} : common_vendor.e({
        b: common_vendor.o(($event) => overallRating.value = $event),
        c: common_vendor.p({
          activeIcon: "star-cheack",
          inactiveIcon: "star",
          iconSize: "40rpx",
          showScore: false,
          modelValue: overallRating.value
        }),
        d: orderDetail.value.order_goods && orderDetail.value.order_goods.length > 0
      }, orderDetail.value.order_goods && orderDetail.value.order_goods.length > 0 ? {
        e: common_vendor.f(orderDetail.value.order_goods, (item, index, i0) => {
          return {
            a: item.goods_cover,
            b: common_vendor.t(item.goods_name),
            c: "148e7851-1-" + i0,
            d: common_vendor.p({
              value: item.price
            }),
            e: "148e7851-2-" + i0,
            f: common_vendor.o(($event) => item.star = $event, item.id || index),
            g: common_vendor.p({
              activeIcon: "star-cheack",
              inactiveIcon: "star",
              iconSize: "40rpx",
              showScore: false,
              modelValue: item.star
            }),
            h: item.id || index
          };
        })
      } : {}, {
        f: maxWordCount,
        g: common_vendor.o([($event) => ratingText.value = $event.detail.value, handleInput]),
        h: ratingText.value,
        i: common_vendor.t(wordCount.value),
        j: common_vendor.t(maxWordCount),
        k: common_vendor.f(evaTags.value, (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: item.id || index,
            c: item.selected ? 1 : "",
            d: common_vendor.o(($event) => handleTagClick(item), item.id || index)
          };
        }),
        l: common_vendor.o(handleSubmit)
      }));
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-148e7851"]]);
wx.createPage(MiniProgramPage);
