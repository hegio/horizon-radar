#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""horizon-wechat login with the QR rendered as a PNG file (console ASCII QR
is not scannable by WeChat). Monkey-patches _render_qr, keeps the whole
login/session flow intact."""
import sys

sys.path.insert(0, r"D:\AI\Horizon")
sys.argv = ["horizon-wechat", "login"]

import qrcode  # noqa: E402

PNG_PATH = r"D:\AI\Horizon\wechat_login_qr.png"

import src.services.wechat_cli as wcli  # noqa: E402


def render_png(content: str) -> None:
    qr = qrcode.QRCode(border=2)
    qr.add_data(content)
    qr.make(fit=True)
    qr.make_image().save(PNG_PATH)
    print(f"QR_SAVED {PNG_PATH}")


wcli._render_qr = render_png

if __name__ == "__main__":
    wcli.main()
