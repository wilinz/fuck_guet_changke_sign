import os
import uuid

import cv2
from urllib.parse import urlparse, parse_qs
import json
import requests
from parse_sign_qr_code import parse_sign_qr_code

session = requests.Session()
base_url = "https://courses.guet.edu.cn"

def scan_url_analysis(e: str):
    print(f"scanUrlAnalysis url: {e}")

    # 如果 URL 包含 "/j?p=" 且不是以 "http" 开头，拼接基础 URL
    if "/j?p=" in e and not e.startswith("http"):
        e = base_url + e

    # 如果仍然不是 HTTP 链接，直接返回
    if not e.startswith("http"):
        return e

    try:
        n = urlparse(e)
    except Exception:
        return e

    # 处理特定路径
    if n.path in ["/j", "/scanner-jumper"]:
        o = parse_qs(n.query)
        r = None
        try:
            a = o.get("_p", [None])[0]
            if a:
                r = json.loads(a)
        except Exception:
            pass

        if not r:
            p_value = o.get("p", [""])[0]
            r = parse_sign_qr_code(p_value)

        return json.dumps(r) if r and isinstance(r, dict) and r else e

    return e

def sign(data):
    url = f"{base_url}/api/rollcall/{data['rollcallId']}/answer_qr_rollcall"
    body = {
        "data": data['data'],
        "deviceId": str(uuid.uuid4()),
    }
    print("request body:", body)
    resp = session.put(url, data=json.dumps(body))
    print(resp.status_code)
    print(resp.text)

if __name__ == '__main__':
    # 读取图像
    image = cv2.imread("qrcode.png")
    # 初始化二维码检测器
    detector = cv2.QRCodeDetector()
    # 识别二维码
    codeText, bbox, _ = detector.detectAndDecode(image)
    if codeText:
        data = scan_url_analysis(codeText)
        print("二维码内容:", codeText)
        print("二维码解析内容:", data)
        print("正在签到...")
        sign(json.loads(data))
    else:
        print("未检测到二维码")