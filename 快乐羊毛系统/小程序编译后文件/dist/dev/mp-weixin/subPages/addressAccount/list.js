"use strict";
const common_vendor = require("../../common/vendor.js");
const api_common = require("../../api/common.js");
if (!Array) {
  const _easycom_Icon2 = common_vendor.resolveComponent("Icon");
  const _easycom_Checkbox2 = common_vendor.resolveComponent("Checkbox");
  (_easycom_Icon2 + _easycom_Checkbox2)();
}
const _easycom_Icon = () => "../../components/Icon/Icon.js";
const _easycom_Checkbox = () => "../../components/Checkbox/Checkbox.js";
if (!Math) {
  (_easycom_Icon + _easycom_Checkbox)();
}
const _sfc_main = {
  __name: "list",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const list = common_vendor.ref([]);
    const initData = async () => {
      const res = await api_common.addressList();
      list.value = res.data.data;
    };
    common_vendor.onShow(() => {
      initData();
    });
    const del = async (id) => {
      const res = await api_common.addressDelete({ id });
      if (res.code === 200) {
        proxy.$u.toast("删除成功");
        initData();
      }
    };
    const sel = (item) => {
      common_vendor.index.$emit("selCity", item);
      common_vendor.index.navigateBack();
    };
    return (_ctx, _cache) => {
      return {
        a: common_vendor.f(common_vendor.unref(list), (item, index, i0) => {
          return {
            a: common_vendor.o(_ctx.backUrl, index),
            b: "558b34a0-0-" + i0,
            c: common_vendor.t(item.user_name),
            d: common_vendor.t(item.mobile),
            e: common_vendor.t(item.address_info),
            f: "558b34a0-1-" + i0,
            g: common_vendor.o(($event) => item.status = $event, index),
            h: common_vendor.p({
              circle: "circle",
              size: "small",
              checkedColor: "#f9be5f",
              labelSize: "24rpx",
              label: "点击选择",
              modelValue: item.status
            }),
            i: common_vendor.o(($event) => del(item.id), index),
            j: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl(`/subPages/addressAccount/update?id=${item.id}`), index),
            k: index,
            l: common_vendor.o(($event) => sel(item), index)
          };
        }),
        b: common_vendor.p({
          name: "location",
          size: 36,
          color: "#333"
        }),
        c: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/addressAccount/update"))
      };
    };
  }
};
wx.createPage(_sfc_main);
