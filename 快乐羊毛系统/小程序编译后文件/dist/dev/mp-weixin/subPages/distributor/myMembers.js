"use strict";
const common_vendor = require("../../common/vendor.js");
const api_distributor = require("../../api/distributor.js");
const defaultAvatar = "https://pic.rmb.bdstatic.com/bjh/250325/beautify/d09d80ef2952714b3f1ec5ef2d88f4c3.jpeg?for=bg";
const _sfc_main = {
  __name: "myMembers",
  setup(__props) {
    const members = common_vendor.ref([]);
    const page = common_vendor.ref(1);
    const pageSize = common_vendor.ref(10);
    const status = common_vendor.ref("more");
    const loading = common_vendor.ref(false);
    const formatDate = (time) => {
      if (!time)
        return "";
      const date = new Date(time);
      return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, "0")}-${date.getDate().toString().padStart(2, "0")}`;
    };
    const getMembersList = async (isRefresh = false) => {
      if (loading.value)
        return;
      if (isRefresh) {
        page.value = 1;
        status.value = "more";
      }
      loading.value = true;
      status.value = "loading";
      try {
        const res = await api_distributor.myteamList({
          page: page.value,
          limit: pageSize.value
        });
        if (res.data && res.code === 200) {
          const newList = res.data.data || [];
          const total = res.data.total || 0;
          if (isRefresh) {
            members.value = newList;
            common_vendor.index.stopPullDownRefresh();
          } else {
            members.value = [...members.value, ...newList];
          }
          if (members.value.length >= total || newList.length < pageSize.value) {
            status.value = "noMore";
          } else {
            status.value = "more";
            page.value++;
          }
        } else {
          status.value = "more";
          if (isRefresh)
            common_vendor.index.stopPullDownRefresh();
        }
      } catch (error) {
        status.value = "more";
        if (isRefresh)
          common_vendor.index.stopPullDownRefresh();
      } finally {
        loading.value = false;
      }
    };
    common_vendor.onLoad(() => {
      getMembersList(true);
    });
    common_vendor.onPullDownRefresh(() => {
      getMembersList(true);
    });
    common_vendor.onReachBottom(() => {
      if (status.value === "noMore")
        return;
      getMembersList();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(members.value, (item, k0, i0) => {
          return {
            a: item.avatarUrl || defaultAvatar,
            b: common_vendor.t(item.nickName || "微信用户"),
            c: common_vendor.t(formatDate(item.createTime)),
            d: item.id
          };
        }),
        b: members.value.length === 0 && !loading.value
      }, members.value.length === 0 && !loading.value ? {} : {}, {
        c: members.value.length > 0
      }, members.value.length > 0 ? common_vendor.e({
        d: status.value === "loading"
      }, status.value === "loading" ? {} : {}, {
        e: status.value === "noMore"
      }, status.value === "noMore" ? {} : {}) : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-ea069fbe"]]);
wx.createPage(MiniProgramPage);
