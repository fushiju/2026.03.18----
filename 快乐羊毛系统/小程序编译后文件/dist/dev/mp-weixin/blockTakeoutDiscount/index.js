"use strict";
const common_vendor = require("../common/vendor.js");
const api_brand = require("../api/brand.js");
const api_link = require("../api/link.js");
if (!Math) {
  SwiperCategory();
}
const SwiperCategory = () => "../components/SwiperCategory/SwiperCategory.js";
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const curId = common_vendor.ref(0);
    const iconList = common_vendor.ref([]);
    const allGoods = common_vendor.ref([]);
    const leftList = common_vendor.ref([]);
    const rightList = common_vendor.ref([]);
    const page = common_vendor.ref(1);
    const loading = common_vendor.ref(false);
    const isNoMore = common_vendor.ref(false);
    common_vendor.onLoad((e) => {
      curId.value = e.id || 0;
      initTopBanner();
      initPage();
    });
    common_vendor.onPullDownRefresh(async () => {
      page.value = 1;
      isNoMore.value = false;
      leftList.value = [];
      rightList.value = [];
      allGoods.value = [];
      await initPage();
      common_vendor.index.stopPullDownRefresh();
    });
    common_vendor.onReachBottom(() => {
      if (loading.value || isNoMore.value)
        return;
      page.value++;
      initPage();
    });
    const initPage = async () => {
      if (loading.value)
        return;
      loading.value = true;
      try {
        let res = await api_brand.brandList({
          lat: "",
          lng: "",
          serId: null,
          page: page.value,
          limit: 10,
          typeId: 15
        });
        if (!res.data || !res.data.data || res.data.data.length === 0) {
          isNoMore.value = true;
          return;
        }
        const formatted = res.data.data.map((i) => ({
          ...i,
          name: i.coach_name,
          icon: i.work_img,
          text: i.text
        }));
        allGoods.value = [...allGoods.value, ...formatted];
        splitData(formatted);
        if (res.data.length < 10) {
          isNoMore.value = true;
        }
      } catch (err) {
      } finally {
        loading.value = false;
      }
    };
    const initTopBanner = async () => {
      try {
        let res = await api_link.goodsList({
          categoryId: curId.value,
          page: 1,
          limit: 10
        });
        if (res.data && res.data.length > 0) {
          const formatted = res.data.map((i) => ({
            ...i,
            name: i.goods_name,
            icon: i.goods_img
          }));
          iconList.value = formatted;
        }
      } catch (err) {
      }
    };
    const splitData = (newData) => {
      newData.forEach((item) => {
        if (leftList.value.length <= rightList.value.length) {
          leftList.value.push(item);
        } else {
          rightList.value.push(item);
        }
      });
    };
    const onIconClick = async (e) => {
      const info = e.item.link_info;
      if (!info || !info.appid)
        return;
      const autograph = common_vendor.index.getStorageSync("autograph");
      if (!autograph) {
        common_vendor.index.showToast({
          title: "请先登录",
          icon: "none",
          duration: 1500
        });
        setTimeout(() => {
          common_vendor.index.navigateTo({
            url: "/subPages/login"
          });
        }, 1500);
        return;
      }
      common_vendor.index.navigateToMiniProgram({
        appId: info.appid,
        path: info.link_url
      });
    };
    const handleDetail = (item) => {
      const autograph = common_vendor.index.getStorageSync("autograph");
      if (!autograph) {
        common_vendor.index.showToast({
          title: "请先登录",
          icon: "none",
          duration: 1500
        });
        setTimeout(() => {
          common_vendor.index.navigateTo({
            url: "/subPages/login"
          });
        }, 1500);
        return;
      }
      common_vendor.index.navigateTo({
        url: `/blockTakeoutDiscount/discountDetail?id=${item.id}`
      });
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.o(onIconClick),
        b: common_vendor.p({
          rows: 2,
          cols: 4,
          iconList: iconList.value,
          height: "24.5vh"
        }),
        c: allGoods.value.length > 0
      }, allGoods.value.length > 0 ? {
        d: common_vendor.f(leftList.value, (item, k0, i0) => {
          return common_vendor.e({
            a: item.icon,
            b: common_vendor.t(item.name),
            c: item.link_info
          }, item.link_info ? {} : {}, {
            d: item.id + "left",
            e: common_vendor.o(($event) => handleDetail(item), item.id + "left")
          });
        }),
        e: common_vendor.f(rightList.value, (item, k0, i0) => {
          return common_vendor.e({
            a: item.icon,
            b: common_vendor.t(item.name),
            c: common_vendor.t(item.text),
            d: item.link_info
          }, item.link_info ? {} : {}, {
            e: item.id + "right",
            f: common_vendor.o(($event) => handleDetail(item), item.id + "right")
          });
        })
      } : {}, {
        f: allGoods.value.length > 0
      }, allGoods.value.length > 0 ? common_vendor.e({
        g: loading.value
      }, loading.value ? {} : isNoMore.value ? {} : {}, {
        h: isNoMore.value
      }) : {}, {
        i: allGoods.value.length === 0 && !loading.value
      }, allGoods.value.length === 0 && !loading.value ? {} : {});
    };
  }
};
wx.createPage(_sfc_main);
