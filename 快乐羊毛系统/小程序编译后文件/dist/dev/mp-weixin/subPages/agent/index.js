"use strict";
const common_vendor = require("../../common/vendor.js");
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const { proxy } = common_vendor.getCurrentInstance();
    const bgImg = common_vendor.ref("");
    const qrImg = common_vendor.ref("");
    const mergedImg = common_vendor.ref("");
    const cvsW = common_vendor.ref(375);
    const cvsH = common_vendor.ref(667);
    const getImagePath = (url) => {
      return new Promise((resolve, reject) => {
        if (url.startsWith("/static") || url.startsWith("static")) {
          resolve(url);
          return;
        }
        common_vendor.index.downloadFile({
          url,
          success: (res) => resolve(res.tempFilePath),
          fail: (err) => {
            console.error("下载图片失败:", url, err);
            reject(err);
          }
        });
      });
    };
    const generateImage = async () => {
      if (!bgImg.value || !qrImg.value) {
        common_vendor.index.showToast({ title: "图片加载中...", icon: "none" });
        return;
      }
      common_vendor.index.showLoading({ title: "正在合成...", mask: true });
      try {
        const ctx = common_vendor.index.createCanvasContext("shareCanvas", proxy);
        const w = cvsW.value;
        const h = cvsH.value;
        const localBg = await getImagePath(bgImg.value);
        const localQr = await getImagePath(qrImg.value);
        ctx.drawImage(localBg, 0, 0, w, h);
        const qrSize = w * 0.35;
        const qrX = (w - qrSize) / 2;
        const qrY = h - qrSize - h * 0.25;
        ctx.setFillStyle("#ffffff");
        ctx.fillRect(qrX - 8, qrY - 8, qrSize + 16, qrSize + 16);
        ctx.drawImage(localQr, qrX, qrY, qrSize, qrSize);
        ctx.draw(false, () => {
          setTimeout(() => {
            common_vendor.index.canvasToTempFilePath(
              {
                canvasId: "shareCanvas",
                destWidth: w * 3,
                // 3倍图保证清晰
                destHeight: h * 3,
                success: (res) => {
                  mergedImg.value = res.tempFilePath;
                  common_vendor.index.hideLoading();
                  common_vendor.index.showToast({ title: "合成成功", icon: "success" });
                },
                fail: (err) => {
                  common_vendor.index.hideLoading();
                  common_vendor.index.showToast({ title: "导出失败", icon: "none" });
                }
              },
              proxy
            );
          }, 300);
        });
      } catch (e) {
        common_vendor.index.hideLoading();
        common_vendor.index.showToast({ title: "合成出错", icon: "none" });
        console.error(e);
      }
    };
    common_vendor.onMounted(() => {
      const sysInfo = common_vendor.index.getSystemInfoSync();
      cvsW.value = sysInfo.windowWidth;
      cvsH.value = sysInfo.windowHeight;
      bgImg.value = "/static/image/agent-share.png";
      qrImg.value = "/static/image/code.png";
    });
    return (_ctx, _cache) => {
      return common_vendor.e({
        a: bgImg.value,
        b: qrImg.value
      }, qrImg.value ? {
        c: qrImg.value
      } : {}, {
        d: cvsW.value + "px",
        e: cvsH.value + "px",
        f: mergedImg.value
      }, mergedImg.value ? {
        g: mergedImg.value,
        h: common_vendor.o(($event) => mergedImg.value = "")
      } : {}, {
        i: common_vendor.o(generateImage)
      });
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-9f24eac3"]]);
wx.createPage(MiniProgramPage);
