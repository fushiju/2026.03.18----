"use strict";
const common_vendor = require("./vendor.js");
const config = {
  baseURL: "https://red.jinyedaojia.com/",
  // 生产环境
  timeout: 15e3,
  header: {
    "Content-Type": "application/json",
    "isapp": 2
  }
};
function beforeRequest(options) {
  var _a;
  const token = common_vendor.index.getStorageSync("autograph");
  if (token) {
    options.header = options.header || {};
    options.header["autograph"] = `${token}`;
  }
  if (((_a = options.method) == null ? void 0 : _a.toUpperCase()) === "GET") {
    options.data = {
      ...options.data
    };
  }
  if (options.showLoading) {
    common_vendor.index.showLoading({
      title: options.loadingText || "加载中...",
      mask: true
    });
  }
  return options;
}
function afterResponse(response, options) {
  if (options.showLoading) {
    common_vendor.index.hideLoading();
  }
  const { statusCode, data } = response;
  if (statusCode === 200) {
    if (data.code === 200 || data.code === 0) {
      return data;
    } else {
      handleBusinessError(data, options);
      throw new Error(data.error || data.message || data.msg || "请求失败");
    }
  } else {
    handleHttpError(statusCode, data, options);
    throw new Error(`HTTP错误：${statusCode}`);
  }
}
function handleBusinessError(data, options) {
  if (options.showError === false)
    return;
  const message = data.error || data.message || data.msg || "请求失败";
  switch (data.code) {
    case 400:
      common_vendor.index.showToast({
        title: message,
        icon: "none"
      });
      break;
    case 401:
      common_vendor.index.removeStorageSync("autograph");
      common_vendor.index.removeStorageSync("userInfo");
      common_vendor.index.removeStorageSync("openId");
      common_vendor.index.removeStorageSync("loginCode");
      common_vendor.index.showToast({
        title: "登录已过期，请重新登录",
        icon: "none"
      });
      setTimeout(() => {
        common_vendor.index.reLaunch({
          url: "/subPages/login"
        });
      }, 1500);
      break;
    case 403:
      common_vendor.index.showToast({
        title: "没有权限访问",
        icon: "none"
      });
      break;
    default:
      common_vendor.index.showToast({
        title: message,
        icon: "none"
      });
  }
}
function handleHttpError(status, data, options) {
  if (options.showError === false)
    return;
  let message = "";
  switch (status) {
    case 400:
      message = "请求参数错误";
      break;
    case 401:
      message = "未授权，请登录";
      break;
    case 403:
      message = "拒绝访问";
      break;
    case 404:
      message = "请求地址不存在";
      break;
    case 500:
      message = "服务器内部错误";
      break;
    case 502:
      message = "网关错误";
      break;
    case 503:
      message = "服务不可用";
      break;
    default:
      message = `网络错误：${status}`;
  }
  common_vendor.index.showToast({
    title: message,
    icon: "none"
  });
}
function request$1(options) {
  options = {
    url: "",
    method: "GET",
    data: {},
    header: {},
    timeout: config.timeout,
    showLoading: false,
    showError: true,
    loadingText: "加载中...",
    retry: 0,
    // 重试次数
    ...options
  };
  options = beforeRequest(options);
  let url = options.url.startsWith("http") ? options.url : config.baseURL + (options.url.startsWith("/") ? options.url : "/" + options.url);
  let retryCount = 0;
  return new Promise((resolve, reject) => {
    function doRequest() {
      common_vendor.index.request({
        url,
        method: options.method,
        data: options.data,
        header: {
          ...config.header,
          ...options.header
        },
        timeout: options.timeout,
        dataType: options.dataType || "json",
        responseType: options.responseType || "text",
        success: (response) => {
          try {
            const result = afterResponse(response, options);
            resolve(result);
          } catch (error) {
            reject(error);
          }
        },
        fail: (error) => {
          if (retryCount < options.retry) {
            retryCount++;
            setTimeout(doRequest, 1e3);
          } else {
            if (options.showLoading) {
              common_vendor.index.hideLoading();
            }
            if (options.showError) {
              common_vendor.index.showToast({
                title: "网络连接失败，请检查网络",
                icon: "none"
              });
            }
            reject(error);
          }
        }
      });
    }
    doRequest();
  });
}
const request = {
  get(url, data = {}, options = {}) {
    return request$1({
      url,
      method: "GET",
      data,
      ...options
    });
  },
  post(url, data = {}, options = {}) {
    return request$1({
      url,
      method: "POST",
      data,
      ...options
    });
  },
  put(url, data = {}, options = {}) {
    return request$1({
      url,
      method: "PUT",
      data,
      ...options
    });
  },
  delete(url, data = {}, options = {}) {
    return request$1({
      url,
      method: "DELETE",
      data,
      ...options
    });
  },
  upload(url, filePath, name = "file", data = {}, options = {}) {
    return new Promise((resolve, reject) => {
      common_vendor.index.getStorageSync("autograph");
      if (options.showLoading) {
        common_vendor.index.showLoading({
          title: options.loadingText || "上传中...",
          mask: true
        });
      }
      common_vendor.index.uploadFile({
        url: url.startsWith("http") ? url : config.baseURL + url,
        filePath,
        name,
        formData: data,
        header: {
          "autograph": autograph ? `${autograph}` : "",
          ...options.header
        },
        success: (res) => {
          if (options.showLoading) {
            common_vendor.index.hideLoading();
          }
          if (res.statusCode === 200) {
            const data2 = JSON.parse(res.data);
            if (data2.code === 200 || data2.code === 0) {
              resolve(data2.data || data2);
            } else {
              if (options.showError !== false) {
                common_vendor.index.showToast({
                  title: data2.message || "上传失败",
                  icon: "none"
                });
              }
              reject(data2);
            }
          } else {
            if (options.showError !== false) {
              common_vendor.index.showToast({
                title: "上传失败",
                icon: "none"
              });
            }
            reject(res);
          }
        },
        fail: (error) => {
          if (options.showLoading) {
            common_vendor.index.hideLoading();
          }
          if (options.showError !== false) {
            common_vendor.index.showToast({
              title: "上传失败",
              icon: "none"
            });
          }
          reject(error);
        }
      });
    });
  }
};
exports.request = request;
