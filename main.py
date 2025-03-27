import os
import uuid

import cv2
from urllib.parse import urlparse, parse_qs
import json
import requests
from requests import Response

from parse_sign_qr_code import parse_sign_qr_code

x_session_id = "V2-1-170eb92a-af81-4cb5-98f0-c3585b6c3d72.ODM1MzQ.1743185592841.PE_rwwEs-obuWYDB51sg7B-cfD4"

session = requests.Session()
session.headers.update({
    "origin": "https://mobile.guet.edu.cn",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "sec-fetch-mode": "cors",
    "x-session-id": x_session_id,
})

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
    resp0 = session.options(url)
    print(resp0.text)
    resp = session.put(url, data=json.dumps(body), headers={"Content-Type": "application/json"})
    print(resp.status_code)
    print(resp.text)

def sign_number(data):
    url = f"{base_url}/api/rollcall/{data['rollcallId']}/answer_number_rollcall"
    # todo
    pass

def get_access_token(code):
    url = "https://identity.guet.edu.cn/auth/realms/guet/protocol/openid-connect/token"
    params = {
        "client_id": "TronClassH5",
        "redirect_uri": "https://mobile.guet.edu.cn/cas-callback?_h5=true",
        "code": code,
        "grant_type": "authorization_code",
        "scope": "openid"
    }
    response = session.post(url, data=params, headers={"Content-Type": "application/x-www-form-urlencoded"})
    return response.json()["access_token"]

def login_and_get_access_token_code():
    url = "https://identity.guet.edu.cn/auth/realms/guet/protocol/openid-connect/auth"
    params = {
        "scope": "openid",
        "response_type": "code",
        "redirect_uri": "https://mobile.guet.edu.cn/cas-callback?_h5=true",
        "client_id": "TronClassH5",
        "autologin": "true"
    }
    response = requests.get(url, params=params)
    # 303 to cas.guet.egu.cn
    cas_url = response.url
    response = login_cas(cas_url)
    # 302 to https://mobile.guet.edu.cn/cas-callback?_h5=true?code=***
    mobile_url = response.url
    mobileUri = urlparse(mobile_url)
    code = parse_qs(mobileUri.query)["code"][0]
    return code

def login_cas(url) -> Response:
    # todo, use username, password to login
    pass

def login_course_guet_edu_cn(access_token):
    url = "https://courses.guet.edu.cn/api/login?login=access_token"
    data = {
        "access_token": access_token,
        "org_id": 1
    }
    resp = session.post(url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    x_session_id = resp.headers.get("x-session-id")
    return x_session_id

def login():
    global x_session_id
    code = login_and_get_access_token_code()
    access_token = get_access_token(code)
    x_session_id = login_course_guet_edu_cn(access_token)


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
