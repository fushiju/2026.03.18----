"""
HTTP 请求客户端 - 封装 requests，支持 AES 加解密
"""
import base64
import json
import logging
from urllib.parse import quote_plus

import allure
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from config import config

logger = logging.getLogger(__name__)


class ApiClient:
    """统一 API 请求客户端"""

    def __init__(self, base_url=None):
        self.base_url = base_url or config["base_url"]
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._aes_key = config["aes"]["key"]
        self._aes_iv = config["aes"]["iv"]

    # ---- 基础请求 ----

    @allure.step("POST {path}")
    def post(self, path, data=None, json_data=None, headers=None, **kwargs):
        url = f"{self.base_url}{path}"
        resp = self.session.post(url, data=data, json=json_data, headers=headers, **kwargs)
        logger.info(f"POST {url} => {resp.status_code}")
        return resp

    @allure.step("GET {path}")
    def get(self, path, params=None, headers=None, **kwargs):
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params, headers=headers, **kwargs)
        logger.info(f"GET {url} => {resp.status_code}")
        return resp

    # ---- AES 加解密 ----

    def aes_encrypt(self, plaintext):
        cipher = AES.new(self._aes_key.encode(), AES.MODE_CBC, self._aes_iv.encode())
        padded = pad(str(plaintext).encode(), AES.block_size)
        encrypted = base64.b64encode(cipher.encrypt(padded)).decode()
        return quote_plus(encrypted)

    def aes_decrypt(self, ciphertext):
        raw = base64.b64decode(ciphertext)
        cipher = AES.new(self._aes_key.encode(), AES.MODE_CBC, self._aes_iv.encode())
        decrypted = unpad(cipher.decrypt(raw), AES.block_size)
        return decrypted.decode()

    @allure.step("POST(AES) {path}")
    def post_encrypted(self, path, data, headers=None):
        encrypted = self.aes_encrypt(json.dumps(data))
        return self.post(path, json_data={"data": encrypted}, headers=headers)

    @allure.step("GET(AES) {path}")
    def get_encrypted(self, path, data, headers=None):
        encrypted = self.aes_encrypt(json.dumps(data))
        url_path = f"{path}?data={encrypted}"
        return self.get(url_path, headers=headers)

    # ---- 便捷方法 ----

    def set_token(self, token):
        self.session.headers.update({"token": token})

    def json(self, resp):
        return resp.json()
