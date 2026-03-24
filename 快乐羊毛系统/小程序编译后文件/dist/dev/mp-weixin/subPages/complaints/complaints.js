"use strict";
const common_vendor = require("../../common/vendor.js");
const api_common = require("../../api/common.js");
if (!Math) {
  UploadFile();
}
const UploadFile = () => "../../components/uploadFile/uploadFile.js";
const maxWordCount = 200;
const _sfc_main = {
  __name: "complaints",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const typeCur = common_vendor.ref(-1);
    const feedbackList = common_vendor.ref([
      {
        id: 1,
        title: "订单问题"
      },
      {
        id: 2,
        title: "功能问题"
      },
      {
        id: 3,
        title: "账号问题"
      },
      {
        id: 4,
        title: "操作问题"
      },
      {
        id: 5,
        title: "bug反馈"
      },
      {
        id: 6,
        title: "其他"
      }
    ]);
    const selType = (index) => {
      typeCur.value = index;
    };
    const orderNo = common_vendor.ref("");
    const wordCount = common_vendor.ref(0);
    const complaintsText = common_vendor.ref("");
    const handleInput = (event) => {
      wordCount.value = event.detail.value.length;
    };
    const uploaderRef = common_vendor.ref();
    const uploadApi = common_vendor.ref(`https://red.jinyedaojia.com/customer/20005`);
    const picList = common_vendor.ref([]);
    const uploadHeader = {
      "autograph": common_vendor.index.getStorageSync("autograph")
    };
    const picHandleUploadSuccess = ({ index, data }) => {
      if (data.code == 200) {
        picList.value[index] = data.data.attachment_path;
      }
    };
    const picHandleUploadFail = ({ index, error }) => {
    };
    const picHandleDelete = ({ index, item }) => {
      picList.value.splice(index, 1);
    };
    const videoList = common_vendor.ref([]);
    const videoHandleUploadSuccess = ({ index, data }) => {
      if (data.code == 200) {
        videoList.value[index] = data.data.attachment_path;
      }
    };
    const videoHandleUploadFail = ({ index, error }) => {
    };
    const videoHandleDelete = ({ index, item }) => {
      videoList.value.splice(index, 1);
    };
    const submit = async () => {
      const params = {
        content: complaintsText.value,
        order_code: orderNo.value,
        images: picList.value,
        video_url: videoList.value,
        type_name: feedbackList.value[typeCur.value].title
      };
      const result = await api_common.feedback(params);
      if (result.code === 200) {
        common_vendor.index.showToast({
          title: "提交成功",
          icon: "none",
          duration: 1500,
          complete: () => {
            proxy.$u.goUrl("subPages/complaints/list");
          }
        });
      }
    };
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(common_vendor.unref(feedbackList), (item, index, i0) => {
          return {
            a: common_vendor.t(item.title),
            b: common_vendor.o(($event) => selType(index), index),
            c: index,
            d: common_vendor.unref(typeCur) === index ? 1 : ""
          };
        }),
        b: common_vendor.unref(typeCur) === 0
      }, common_vendor.unref(typeCur) === 0 ? {
        c: common_vendor.unref(orderNo),
        d: common_vendor.o(($event) => common_vendor.isRef(orderNo) ? orderNo.value = $event.detail.value : null)
      } : {}, {
        e: maxWordCount,
        f: common_vendor.o([($event) => common_vendor.isRef(complaintsText) ? complaintsText.value = $event.detail.value : null, handleInput]),
        g: common_vendor.unref(complaintsText),
        h: common_vendor.t(common_vendor.unref(wordCount)),
        i: common_vendor.t(maxWordCount),
        j: common_vendor.sr(uploaderRef, "5710efb1-0", {
          "k": "uploaderRef"
        }),
        k: common_vendor.o(picHandleUploadSuccess),
        l: common_vendor.o(picHandleUploadFail),
        m: common_vendor.o(picHandleDelete),
        n: common_vendor.p({
          title: "上传图片",
          ["max-count"]: 3,
          ["max-size"]: 5,
          ["file-type"]: ["png", "jpg", "jpeg"],
          uploadUrl: common_vendor.unref(uploadApi),
          header: uploadHeader,
          name: "file",
          formData: {
            type: "picture"
          },
          ["initial-list"]: common_vendor.unref(picList)
        }),
        o: common_vendor.sr(uploaderRef, "5710efb1-1", {
          "k": "uploaderRef"
        }),
        p: common_vendor.o(videoHandleUploadSuccess),
        q: common_vendor.o(videoHandleUploadFail),
        r: common_vendor.o(videoHandleDelete),
        s: common_vendor.p({
          title: "上传视频",
          ["max-count"]: 3,
          ["max-size"]: 5,
          ["file-type"]: ["mp4", "avi", "mov"],
          uploadUrl: common_vendor.unref(uploadApi),
          header: uploadHeader,
          name: "file",
          formData: {
            type: "video"
          },
          ["initial-list"]: common_vendor.unref(videoList)
        }),
        t: common_vendor.o(($event) => common_vendor.unref(proxy).$u.goUrl("/subPages/complaints/list")),
        v: common_vendor.o(submit)
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-5710efb1"]]);
wx.createPage(MiniProgramPage);
