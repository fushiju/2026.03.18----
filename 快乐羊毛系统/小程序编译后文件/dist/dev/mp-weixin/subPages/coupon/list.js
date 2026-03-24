"use strict";
const common_vendor = require("../../common/vendor.js");
const api_common = require("../../api/common.js");
if (!Math) {
  (Price + Icon)();
}
const Icon = () => "../../components/Icon/Icon.js";
const Price = () => "../../components/Price/Price.js";
const _sfc_main = {
  __name: "list",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const activeIndex = common_vendor.ref(0);
    const couponType = common_vendor.ref([
      {
        title: "待使用",
        value: 0
      },
      {
        title: "已使用",
        value: 1
      },
      {
        title: "已过期",
        value: 2
      }
    ]);
    const statusType = {
      1: "去使用",
      2: "已使用",
      3: "删除"
    };
    const onTabClick = (index) => {
      activeIndex.value = index;
      initData();
    };
    const couponList = common_vendor.ref([]);
    const initData = async () => {
      const params = {
        page: 1,
        pageSize: 10
      };
      id.value ? params.coach_id = id.value : params.status = activeIndex.value + 1;
      let list = id.value ? await api_common.getUserCouponList(params) : await api_common.getCouponList(params);
      couponList.value = list.data.data;
      couponList.value.map((i) => {
        i.isOpen = false;
      });
    };
    const id = common_vendor.ref(0);
    const type = common_vendor.ref("");
    common_vendor.onLoad((e) => {
      id.value = e.coach_id;
      type.value = e.type;
      initData();
    });
    const use = async (i, status) => {
      if (status === 1) {
        if (type.value === "use") {
          common_vendor.index.$emit("coupon", couponList.value[i]);
          common_vendor.index.navigateBack();
        } else {
          common_vendor.index.redirectTo({
            url: "/pages/index"
          });
        }
      } else if (status === 2) {
        common_vendor.index.showToast({
          title: "优惠券已使用",
          icon: "none"
        });
      } else {
        let p = {
          coupon_id: couponList.value[i].id
        };
        let res = await api_common.couponDel(p);
        if (res.code === 200) {
          common_vendor.index.showToast({
            title: "优惠券已使用",
            icon: "none"
          });
          initData();
        }
        return;
      }
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: !common_vendor.unref(type)
      }, !common_vendor.unref(type) ? {
        b: common_vendor.f(common_vendor.unref(couponType), (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.unref(activeIndex) === index ? 1 : "",
            c: index,
            d: common_vendor.o(($event) => onTabClick(index), index)
          };
        })
      } : {}, {
        c: !common_vendor.unref(type)
      }, !common_vendor.unref(type) ? {} : {}, {
        d: common_vendor.unref(couponList).length > 0
      }, common_vendor.unref(couponList).length > 0 ? {
        e: common_vendor.f(common_vendor.unref(couponList), (item, index, i0) => {
          return common_vendor.e({
            a: "fb116824-0-" + i0,
            b: common_vendor.p({
              value: item.discount,
              color: item.status === 1 ? "#ff3b30" : "#999999"
            }),
            c: common_vendor.t(item.type == 0 ? `满${item.full}元可用` : "无门槛"),
            d: common_vendor.t(item.num),
            e: item.status !== 2
          }, item.status !== 2 ? {
            f: common_vendor.t(statusType[item.status]),
            g: item.status === 1 ? "#f9be5f" : "#999999",
            h: item.status === 1 ? "1rpx solid #f9be5f" : "1rpx solid #999999",
            i: item.status == 3 ? "absolute" : "",
            j: item.status == 3 ? "170rpx" : "",
            k: common_vendor.o(($event) => use(index, item.status), index)
          } : {}, {
            l: common_vendor.t(common_vendor.unref(type) === "use" ? item.end_time : item.start_time),
            m: "fb116824-1-" + i0,
            n: common_vendor.p({
              name: item.isOpen ? "up" : "down",
              size: "24rpx",
              color: "#999"
            }),
            o: common_vendor.o(($event) => item.isOpen = !item.isOpen, index),
            p: item.isOpen
          }, item.isOpen ? common_vendor.e({
            q: common_vendor.t(item.rule),
            r: common_vendor.t(item.text),
            s: item.send_type == 3
          }, item.send_type == 3 ? {} : common_vendor.e({
            t: common_vendor.f(item.service, (aitem, aindex, i1) => {
              return {
                a: common_vendor.t(aitem.title),
                b: aindex
              };
            }),
            v: item.service.length == 0
          }, item.service.length == 0 ? {} : {}), {
            w: common_vendor.t(item.admin_id ? "仅限部分城市可使用" : "通用券")
          }) : {}, {
            x: common_vendor.t(item.title),
            y: item.status === 1 ? "#ffefd6" : "#dcdcdc",
            z: item.status === 1 ? "#f1af45" : "#969696",
            A: item.status !== 1
          }, item.status !== 1 ? common_vendor.e({
            B: item.status == 2
          }, item.status == 2 ? {
            C: "fb116824-2-" + i0,
            D: common_vendor.p({
              name: "expired",
              size: "160rpx",
              color: "#999"
            })
          } : {}, {
            E: item.status == 3
          }, item.status == 3 ? {
            F: "fb116824-3-" + i0,
            G: common_vendor.p({
              name: "used",
              size: "160rpx",
              color: "#999"
            })
          } : {}) : {}, {
            H: index
          });
        })
      } : {});
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-fb116824"]]);
wx.createPage(MiniProgramPage);
