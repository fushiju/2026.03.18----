"""验证码识别 - 优先使用万能验证码绕过，降级使用 ddddocr OCR"""
from config.settings import CAPTCHA_BYPASS


def _ensure_png(image_bytes: bytes) -> bytes:
    """确保图片是标准 PNG 格式（Playwright canvas 截图可能需要重编码）"""
    from PIL import Image
    import io
    try:
        img = Image.open(io.BytesIO(image_bytes))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return image_bytes


def solve_captcha(image_bytes: bytes) -> str:
    """识别验证码图片，返回识别结果字符串"""
    if CAPTCHA_BYPASS:
        return CAPTCHA_BYPASS
    if not image_bytes:
        return "0000"
    # 重编码为标准 PNG，确保 ddddocr 能识别
    png_bytes = _ensure_png(image_bytes)
    import ddddocr
    ocr = ddddocr.DdddOcr(show_ad=False)
    result = ocr.classification(png_bytes)
    cleaned = "".join(c for c in result.lower() if c.isalnum())
    return cleaned[:4] if cleaned else "0000"
