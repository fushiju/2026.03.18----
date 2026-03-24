"use strict";
const common_vendor = require("../../common/vendor.js");
const api_order = require("../../api/order.js");
if (!Array) {
  const _easycom_Icon2 = common_vendor.resolveComponent("Icon");
  const _easycom_Price2 = common_vendor.resolveComponent("Price");
  (_easycom_Icon2 + _easycom_Price2)();
}
const _easycom_Icon = () => "../../components/Icon/Icon.js";
const _easycom_Price = () => "../../components/Price/Price.js";
if (!Math) {
  (_easycom_Icon + _easycom_Price + UploadFile)();
}
const UploadFile = () => "../../components/uploadFile/uploadFile.js";
const maxWordCount = 200;
const _sfc_main = {
  __name: "apply",
  setup(__props) {
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
    const getCurPayType = (pay_type) => {
      const item = status.find((val) => val.value == pay_type);
      return item ? item.label : "";
    };
    const selGoods = (e) => {
      e.ischeck = !e.ischeck;
    };
    const reasonCur = common_vendor.ref(0);
    const refundList = common_vendor.ref([
      {
        value: 1,
        title: "退款原因 1"
      },
      {
        value: 2,
        title: "退款原因 2"
      },
      {
        value: 3,
        title: "其他原因"
      }
    ]);
    const isShowOtherReason = common_vendor.ref(false);
    const selReason = (e) => {
      const selectedIndex = refundList.value.findIndex(
        (item) => item.value == e.detail.value
      );
      reasonCur.value = selectedIndex;
      isShowOtherReason.value = selectedIndex === refundList.value.length - 1;
      otherReason.value = "";
      otherReason.value = isShowOtherReason.value ? otherReason.value : refundList.value[selectedIndex].title;
    };
    const otherReason = common_vendor.ref("");
    const wordCount = common_vendor.ref(0);
    const handleInput = (event) => {
      wordCount.value = event.detail.value.length;
    };
    const selectedGoodsList = common_vendor.computed(() => {
      var _a;
      return ((_a = orderDetail.value.order_goods) == null ? void 0 : _a.filter((item) => item.ischeck)) || [];
    });
    const selectedCount = common_vendor.computed(() => {
      return selectedGoodsList.value.length;
    });
    const selectedTotal = common_vendor.computed(() => {
      return (orderDetail.value.order_goods || []).filter((item) => item.ischeck).reduce((sum, item) => {
        return sum + parseFloat(item.price) * parseInt(item.num);
      }, 0).toFixed(2);
    });
    const isAllSelected = common_vendor.computed(() => {
      const goods = orderDetail.value.order_goods || [];
      return goods.length > 0 && goods.every((item) => item.ischeck);
    });
    const toggleAll = () => {
      var _a;
      const newState = !isAllSelected.value;
      (_a = orderDetail.value.order_goods) == null ? void 0 : _a.forEach((item) => {
        item.ischeck = newState;
      });
    };
    const orderDetail = common_vendor.ref({});
    const config = common_vendor.ref({});
    const initData = async (id) => {
      var _a;
      const params = {
        id,
        apply_refund: 1
      };
      let res = await api_order.orderInfo(params);
      (_a = res.data.order_goods) == null ? void 0 : _a.forEach((i) => {
        i.ischeck = true;
      });
      orderDetail.value = res.data;
    };
    const uploaderRef = common_vendor.ref();
    const uploadApi = common_vendor.ref(`https://red.jinyedaojia.com/customer/20005`);
    const initialImages = common_vendor.ref([]);
    const uploadHeader = {
      "autograph": common_vendor.index.getStorageSync("autograph")
    };
    const handleUploadSuccess = ({ index, data }) => {
      if (data.code == 200) {
        initialImages.value[index] = data.data.attachment_path;
      }
    };
    const handleUploadFail = ({ index, error }) => {
    };
    const handleDelete = ({ index, item }) => {
      initialImages.value.splice(index, 1);
    };
    common_vendor.onLoad((e) => {
      initData(e.id);
      order_id.value = e.id;
      otherReason.value = isShowOtherReason.value ? otherReason.value : refundList.value[reasonCur.value].title;
      config.value = common_vendor.index.getStorageSync("config");
    });
    const subParams = common_vendor.ref({});
    const order_id = common_vendor.ref(0);
    const submit = async () => {
      const checkedGoods = selectedGoodsList.value;
      if (!checkedGoods.length) {
        common_vendor.index.showToast({ title: "请选择要退款的商品", icon: "none" });
        return;
      }
      if (!otherReason.value) {
        common_vendor.index.showToast({ title: "请选择或填写退款原因", icon: "none" });
        return;
      }
      subParams.value = {
        order_id: Number(order_id.value),
        list: checkedGoods.map((item) => ({
          id: item.id,
          num: item.num
        })),
        text: otherReason.value,
        imgs: initialImages.value
      };
      let result = await api_order.refundOrder(subParams.value);
      if (result.code == 200) {
        common_vendor.index.showToast({ title: "提交成功", icon: "none" });
        setTimeout(() => {
          common_vendor.index.navigateBack();
        }, 1e3);
      }
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.t(common_vendor.unref(orderDetail).order_code),
        b: common_vendor.t(getCurPayType(common_vendor.unref(orderDetail).pay_type)),
        c: common_vendor.f(common_vendor.unref(orderDetail).order_goods, (item, index, i0) => {
          return {
            a: "0b0e8c80-0-" + i0,
            b: common_vendor.p({
              name: item.ischeck ? "xuanzhongduigou" : "check_normal",
              size: "40rpx",
              color: item.ischeck ? "#ff471f" : "#ccc"
            }),
            c: item.img,
            d: common_vendor.t(item.goods_name),
            e: common_vendor.t(item.num),
            f: "0b0e8c80-1-" + i0,
            g: common_vendor.p({
              value: item.price
            }),
            h: index,
            i: common_vendor.o(($event) => selGoods(item), index)
          };
        }),
        d: common_vendor.p({
          value: common_vendor.unref(selectedTotal)
        }),
        e: common_vendor.f(common_vendor.unref(refundList), (item, index, i0) => {
          return {
            a: item.value,
            b: index === common_vendor.unref(reasonCur),
            c: common_vendor.t(item.title),
            d: item.value
          };
        }),
        f: common_vendor.o(selReason),
        g: common_vendor.unref(isShowOtherReason)
      }, common_vendor.unref(isShowOtherReason) ? {
        h: maxWordCount,
        i: common_vendor.o([($event) => common_vendor.isRef(otherReason) ? otherReason.value = $event.detail.value : null, handleInput]),
        j: common_vendor.unref(otherReason),
        k: common_vendor.t(common_vendor.unref(wordCount)),
        l: common_vendor.t(maxWordCount)
      } : {}, {
        m: common_vendor.sr(uploaderRef, "0b0e8c80-3", {
          "k": "uploaderRef"
        }),
        n: common_vendor.o(handleUploadSuccess),
        o: common_vendor.o(handleUploadFail),
        p: common_vendor.o(handleDelete),
        q: common_vendor.p({
          ["max-count"]: 9,
          ["max-size"]: 5,
          ["file-type"]: ["png", "jpg", "jpeg"],
          uploadUrl: common_vendor.unref(uploadApi),
          header: uploadHeader,
          name: "file",
          formData: {
            type: "picture"
          },
          ["initial-list"]: common_vendor.unref(initialImages)
        }),
        r: common_vendor.t(common_vendor.unref(config).trading_rules || "加载中"),
        s: common_vendor.p({
          name: common_vendor.unref(isAllSelected) ? "xuanzhongduigou" : "check_normal",
          size: "40rpx",
          color: common_vendor.unref(isAllSelected) ? "#ff471f" : "#ccc"
        }),
        t: common_vendor.o(toggleAll),
        v: common_vendor.t(common_vendor.unref(selectedCount)),
        w: common_vendor.p({
          value: common_vendor.unref(selectedTotal)
        }),
        x: common_vendor.o(submit)
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-0b0e8c80"]]);
wx.createPage(MiniProgramPage);
