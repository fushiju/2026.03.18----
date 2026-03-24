"use strict";
const common_vendor = require("../common/vendor.js");
const api_brand = require("../api/brand.js");
if (!Math) {
  Icon();
}
const Icon = () => "../components/Icon/Icon.js";
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const list = common_vendor.ref([
      "https://img1.baidu.com/it/u=4093640845,1838172949&fm=253&app=138&f=JPEG?w=1200&h=800",
      "https://img1.baidu.com/it/u=2732661436,2109210554&fm=253&app=138&f=JPEG?w=889&h=500"
    ]);
    const vip = common_vendor.ref([]);
    let anchor = common_vendor.ref(0);
    let intoView = common_vendor.ref("");
    const instance = common_vendor.getCurrentInstance();
    const sectionTops = common_vendor.ref([]);
    const isAutoScrolling = common_vendor.ref(false);
    let autoScrollTimer = null;
    const tabIntoView = common_vendor.computed(() => `tab-${anchor.value}`);
    const calcSectionTops = () => {
      return new Promise((resolve) => {
        common_vendor.nextTick$1(() => {
          const query = common_vendor.index.createSelectorQuery().in(instance);
          query.select("#vip-scroll").boundingClientRect();
          vip.value.forEach((v) => {
            query.select(`#anchor-${v.id}`).boundingClientRect();
          });
          query.exec((res) => {
            const scrollRect = res == null ? void 0 : res[0];
            if (!scrollRect) {
              sectionTops.value = [];
              resolve([]);
              return;
            }
            const tops = [];
            for (let i = 0; i < vip.value.length; i++) {
              const rect = res == null ? void 0 : res[i + 1];
              if (!rect)
                continue;
              tops.push({
                id: vip.value[i].id,
                top: rect.top - scrollRect.top
              });
            }
            tops.sort((a, b) => a.top - b.top);
            sectionTops.value = tops;
            resolve(tops);
          });
        });
      });
    };
    const selVip = (e, id) => {
      anchor.value = e;
      isAutoScrolling.value = true;
      if (autoScrollTimer)
        clearTimeout(autoScrollTimer);
      intoView.value = `anchor-${id}`;
      autoScrollTimer = setTimeout(() => {
        isAutoScrolling.value = false;
      }, 450);
      if (showMore.value)
        showMore.value = false;
    };
    let showMore = common_vendor.ref(false);
    const openMore = () => {
      showMore.value = !showMore.value;
    };
    const onScroll = (e) => {
      var _a;
      if (isAutoScrolling.value)
        return;
      const scrollTop = ((_a = e == null ? void 0 : e.detail) == null ? void 0 : _a.scrollTop) ?? 0;
      const tops = sectionTops.value;
      if (!tops.length)
        return;
      const threshold = 20;
      let currentId = tops[0].id;
      for (let i = 0; i < tops.length; i++) {
        if (scrollTop + threshold >= tops[i].top)
          currentId = tops[i].id;
        else
          break;
      }
      const idx = vip.value.findIndex((v) => v.id === currentId);
      if (idx !== -1 && anchor.value !== idx)
        anchor.value = idx;
    };
    let params = common_vendor.ref({
      lat: "",
      lng: "",
      ser_id: 0,
      city_id: 1,
      type: 10,
      freeFare: 0
    });
    const transformVipData = (sourceData) => {
      const result = [];
      const recommendList = [];
      const categoryMap = /* @__PURE__ */ new Map();
      sourceData.forEach((item) => {
        const listItem = {
          id: item.id,
          title: item.coach_name,
          desc: item.text,
          icon: item.work_img,
          isSellOut: item.is_work,
          isLimitedTime: item.recommend_icon
        };
        if (item.recommend === "1") {
          recommendList.push(listItem);
        }
        const categoryId = item.type_id;
        if (!categoryMap.has(categoryId)) {
          categoryMap.set(categoryId, {
            id: categoryId,
            name: item.type_title,
            list: []
          });
        }
        categoryMap.get(categoryId).list.push(listItem);
      });
      if (recommendList.length > 0) {
        result.push({
          id: 1,
          name: "热门推荐",
          list: recommendList
        });
      }
      categoryMap.forEach((category) => {
        result.push(category);
      });
      return result;
    };
    const initData = async () => {
      let res = await api_brand.brandList(params.value);
      vip.value = transformVipData(res.data.data);
    };
    const handleRecharge = (item) => {
      if (!item.isSellOut)
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
      proxy.$u.goUrl(`/blockMemberRecharge/recharge?id=${item.id}&title=${item.title}`);
    };
    common_vendor.onLoad(async () => {
      initData();
      await calcSectionTops();
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(common_vendor.unref(list), (item, k0, i0) => {
          return {
            a: item,
            b: item
          };
        }),
        b: common_vendor.f(common_vendor.unref(vip), (item, index, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: common_vendor.unref(anchor) === index ? 1 : "",
            c: index,
            d: "tab-" + index,
            e: common_vendor.o(($event) => selVip(index, item.id), index)
          };
        }),
        c: common_vendor.unref(tabIntoView),
        d: common_vendor.p({
          name: "down",
          size: "24rpx",
          color: "#e1a038"
        }),
        e: common_vendor.o(openMore),
        f: common_vendor.f(common_vendor.unref(vip), (item, index, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: common_vendor.f(item.list, (i, k, i1) => {
              return common_vendor.e({
                a: common_vendor.t(i.title),
                b: common_vendor.t(i.desc),
                c: i.isSellOut
              }, i.isSellOut ? {} : {}, {
                d: i.icon,
                e: !i.isSellOut
              }, !i.isSellOut ? {
                f: "43a59898-1-" + i0 + "-" + i1,
                g: common_vendor.p({
                  name: "shouqing",
                  size: "150rpx"
                })
              } : {}, {
                h: i.isLimitedTime
              }, i.isLimitedTime ? {} : {}, {
                i: k,
                j: common_vendor.o(($event) => handleRecharge(i), k),
                k: !i.isSellOut ? "#a0a0a0" : "#545454"
              });
            }),
            c: index,
            d: "anchor-" + item.id
          };
        }),
        g: common_vendor.unref(intoView),
        h: common_vendor.o(onScroll),
        i: common_vendor.unref(showMore)
      }, common_vendor.unref(showMore) ? {} : {}, {
        j: common_vendor.unref(showMore)
      }, common_vendor.unref(showMore) ? {
        k: common_vendor.p({
          name: "up",
          size: "24rpx",
          ["custom-color"]: "#e1a038"
        }),
        l: common_vendor.o(openMore),
        m: common_vendor.f(common_vendor.unref(vip), (item, index, i0) => {
          return {
            a: common_vendor.t(item.name),
            b: common_vendor.unref(anchor) === index ? 1 : "",
            c: index,
            d: common_vendor.o(($event) => selVip(index, item.id), index)
          };
        })
      } : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-43a59898"]]);
wx.createPage(MiniProgramPage);
