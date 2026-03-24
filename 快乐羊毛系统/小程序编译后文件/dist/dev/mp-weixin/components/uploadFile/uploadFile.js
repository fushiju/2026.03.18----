"use strict";
const common_vendor = require("../../common/vendor.js");
if (!Array) {
  const _component_uni_icons = common_vendor.resolveComponent("uni-icons");
  _component_uni_icons();
}
if (!Math) {
  Icon();
}
const Icon = () => "../Icon/Icon.js";
const _sfc_main = {
  __name: "uploadFile",
  props: {
    // 标题
    title: {
      type: String,
      default: ""
    },
    // 最大上传数量
    maxCount: {
      type: Number,
      default: 9
    },
    // 最大文件大小（MB）
    maxSize: {
      type: Number,
      default: 10
    },
    // 允许的文件类型
    fileType: {
      type: Array,
      default: () => ["png", "jpg", "jpeg", "gif"]
    },
    // 上传地址
    uploadUrl: {
      type: String,
      required: true
    },
    // 请求头
    header: {
      type: Object,
      default: () => ({
        "content-type": "multipart/form-data"
      })
    },
    // 表单字段名称（文件字段）
    name: {
      type: String,
      default: "file"
    },
    // 附加数据
    formData: {
      type: Object,
      default: () => ({
        type: "picture"
        // 默认添加 type 字段
      })
    },
    // 是否自动上传
    autoUpload: {
      type: Boolean,
      default: true
    },
    // 初始图片列表
    initialList: {
      type: Array,
      default: () => []
    }
  },
  emits: [
    "upload-success",
    "upload-fail",
    "upload-complete",
    "delete"
  ],
  setup(__props, { expose: __expose, emit: __emit }) {
    const props = __props;
    const emit = __emit;
    const imageList = common_vendor.ref([]);
    const errorMsg = common_vendor.ref("");
    if (props.initialList.length) {
      imageList.value = props.initialList.map((item) => ({
        url: typeof item === "string" ? item : item.url,
        status: "success",
        progress: 100,
        ...item
      }));
    }
    const chooseImage = () => {
      common_vendor.index.chooseImage({
        count: props.maxCount - imageList.value.length,
        sizeType: ["original", "compressed"],
        sourceType: ["album", "camera"],
        success: (res) => {
          const tempFiles = res.tempFiles || res.tempFilePaths.map((path) => ({
            path,
            size: 0
            // 如果没有size信息，后续可能需要在APP端获取
          }));
          handleChooseSuccess(tempFiles);
        },
        fail: (err) => {
          errorMsg.value = "选择图片失败";
          setTimeout(() => {
            errorMsg.value = "";
          }, 3e3);
        }
      });
    };
    const handleChooseSuccess = (tempFiles) => {
      tempFiles.forEach((file) => {
        const fileType = file.path.split(".").pop().toLowerCase();
        if (!props.fileType.includes(fileType)) {
          errorMsg.value = `不支持的文件类型，请上传 ${props.fileType.join("、")} 格式的图片`;
          setTimeout(() => {
            errorMsg.value = "";
          }, 3e3);
          return;
        }
        const fileSize = file.size / (1024 * 1024);
        if (fileSize > props.maxSize) {
          errorMsg.value = `文件大小不能超过 ${props.maxSize}MB`;
          setTimeout(() => {
            errorMsg.value = "";
          }, 3e3);
          return;
        }
        const newItem = {
          url: file.path,
          status: "pending",
          progress: 0,
          file,
          // 存储文件信息，用于上传
          filePath: file.path,
          fileName: file.path.split("/").pop() || "image.jpg"
        };
        imageList.value.push(newItem);
        if (props.autoUpload) {
          uploadImage(imageList.value.length - 1);
        }
      });
    };
    const uploadImage = (index) => {
      const item = imageList.value[index];
      if (!item)
        return;
      item.status = "uploading";
      const uploadTask = common_vendor.index.uploadFile({
        url: props.uploadUrl,
        filePath: item.filePath,
        name: props.name,
        // 文件字段名，默认为 'file'
        header: {
          ...props.header
        },
        formData: props.formData,
        // 其他表单字段
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            item.status = "success";
            item.progress = 100;
            item.serverResponse = res.data;
            try {
              const responseData = typeof res.data === "string" ? JSON.parse(res.data) : res.data;
              emit("upload-success", {
                index,
                data: responseData,
                originalItem: item,
                response: res
              });
            } catch (e) {
              emit("upload-success", {
                index,
                data: res.data,
                originalItem: item,
                response: res
              });
            }
          } else {
            handleUploadFail(index, new Error(`上传失败: HTTP ${res.statusCode}`));
          }
        },
        fail: (err) => {
          handleUploadFail(index, err);
        },
        complete: () => {
          emit("upload-complete", index);
        }
      });
      uploadTask.onProgressUpdate((res) => {
        if (item.status === "uploading") {
          item.progress = res.progress;
        }
      });
      item.uploadTask = uploadTask;
    };
    const handleUploadFail = (index, error) => {
      const item = imageList.value[index];
      item.status = "error";
      item.progress = 0;
      item.error = error;
      emit("upload-fail", {
        index,
        error,
        item
      });
      errorMsg.value = error.message || "上传失败，点击图片重试";
      setTimeout(() => {
        errorMsg.value = "";
      }, 3e3);
    };
    const deleteImage = (index) => {
      const item = imageList.value[index];
      if (item.uploadTask && item.status === "uploading") {
        item.uploadTask.abort();
      }
      imageList.value.splice(index, 1);
      emit("delete", { index, item });
    };
    const previewImage = (index) => {
      const urls = imageList.value.map((item) => item.url);
      common_vendor.index.previewImage({
        current: index,
        urls
      });
    };
    const retryUpload = (index) => {
      const item = imageList.value[index];
      if (item.status === "error") {
        item.status = "pending";
        uploadImage(index);
      }
    };
    const addImage = (imageInfo) => {
      const newItem = {
        url: imageInfo.url,
        status: imageInfo.status || "success",
        progress: 100,
        filePath: imageInfo.filePath || imageInfo.url,
        ...imageInfo
      };
      imageList.value.push(newItem);
    };
    const getUploadedImages = () => {
      return imageList.value.filter((item) => item.status === "success").map((item) => ({
        url: item.url,
        serverResponse: item.serverResponse,
        filePath: item.filePath
      }));
    };
    const getUploadStatus = () => {
      const uploading = imageList.value.some((item) => item.status === "uploading");
      const hasError = imageList.value.some((item) => item.status === "error");
      const success = imageList.value.every((item) => item.status === "success");
      return {
        uploading,
        hasError,
        success,
        total: imageList.value.length,
        uploaded: imageList.value.filter((item) => item.status === "success").length,
        failed: imageList.value.filter((item) => item.status === "error").length
      };
    };
    const clearImages = () => {
      imageList.value.forEach((item) => {
        if (item.uploadTask && item.status === "uploading") {
          item.uploadTask.abort();
        }
      });
      imageList.value = [];
    };
    const uploadAll = () => {
      imageList.value.forEach((item, index) => {
        if (item.status === "pending" || item.status === "error") {
          uploadImage(index);
        }
      });
    };
    __expose({
      addImage,
      getUploadedImages,
      getUploadStatus,
      clearImages,
      retryUpload,
      uploadAll
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: common_vendor.f(imageList.value, (item, index, i0) => {
          return common_vendor.e({
            a: item.url,
            b: common_vendor.o(($event) => previewImage(index), index),
            c: item.status === "uploading"
          }, item.status === "uploading" ? {
            d: common_vendor.t(item.progress),
            e: item.progress
          } : {}, {
            f: item.status === "error"
          }, item.status === "error" ? {
            g: "d7109c73-0-" + i0,
            h: common_vendor.p({
              type: "closeempty",
              size: "30",
              color: "#FF6B6B"
            }),
            i: common_vendor.o(($event) => retryUpload(index), index)
          } : {}, {
            j: "d7109c73-1-" + i0,
            k: common_vendor.o(($event) => deleteImage(index), index),
            l: index,
            m: item.status === "error" ? 1 : ""
          });
        }),
        b: common_vendor.p({
          name: "close",
          size: "18",
          color: "#FFFFFF"
        }),
        c: imageList.value.length < __props.maxCount
      }, imageList.value.length < __props.maxCount ? common_vendor.e({
        d: common_vendor.p({
          name: "xiangji",
          size: "60rpx",
          color: "#999999"
        }),
        e: __props.title
      }, __props.title ? {
        f: common_vendor.t(__props.title)
      } : {}, {
        g: common_vendor.t(imageList.value.length),
        h: common_vendor.t(__props.maxCount),
        i: common_vendor.o(chooseImage)
      }) : {}, {
        j: errorMsg.value
      }, errorMsg.value ? {
        k: common_vendor.t(errorMsg.value)
      } : {});
    };
  }
};
const Component = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-d7109c73"]]);
wx.createComponent(Component);
