#!/usr/bin/env python3
"""Render a Facebook post image (1080x1350) for one of 3 pages.
Usage: python3 render.py spec.json out.png
spec.json examples:
 {"page":"thaison","title":"3 Dấu Hiệu Một Bộ Vest Vừa Vặn","bullets":["Vai áo ôm khít","Tay áo lộ 1–1,5 cm sơ mi"]}
 {"page":"sonleo","tag":"MẸO AI","title":"Hook 3 giây quyết định","highlight":"người xem ở lại","body":"Mở video bằng câu hỏi..."}
 {"page":"giadinh","line1":"Bố ơi, sao bố về muộn thế?","line2":"Con để phần bố cái bánh to nhất.","by":"Bé Bơ"}
"""
import json, sys, os, html, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
e = lambda s: html.escape(str(s or ""))

def fit(text, big, small, long_at):
    n = len(text or "")
    if n <= long_at: return big
    return max(small, int(big * long_at / n))

def thaison(s):
    t = s.get("title", "")
    fs = fit(t, 84, 54, 34)
    bullets = s.get("bullets") or []
    marks = "①②③④"
    bl = "<br>".join(f"{marks[i]} {e(b)}" for i, b in enumerate(bullets[:4]))
    sub = e(s.get("subtitle", ""))
    return f"""<body style="margin:0;width:1080px;height:1350px;background:radial-gradient(circle at 50% 30%,#1c2f55 0%,#0b1630 70%);font-family:'DejaVu Serif',serif;color:#f3e9d2;display:flex;flex-direction:column;align-items:center;justify-content:center;box-sizing:border-box;border:28px solid #0b1630;outline:2px solid #c9a55a;outline-offset:-48px;position:relative">
<div style="letter-spacing:12px;font-size:30px;color:#c9a55a;margin-bottom:40px">VESTON THÁI SƠN</div>
<div style="width:140px;height:2px;background:#c9a55a;margin-bottom:60px"></div>
<div style="font-size:{fs}px;line-height:1.2;text-align:center;font-weight:bold;padding:0 110px">{e(t)}</div>
{f'<div style="font-family:Montserrat;font-size:38px;margin-top:40px;text-align:center;padding:0 120px;color:#e8dcc0;line-height:1.5">{sub}</div>' if sub else ''}
{f'<div style="font-family:Montserrat;font-size:36px;margin-top:60px;line-height:1.9;color:#e8dcc0;padding:0 130px">{bl}</div>' if bl else ''}
<div style="position:absolute;bottom:110px;font-family:Montserrat;font-size:28px;color:#c9a55a;letter-spacing:2px">May đo 20+ năm • 239 Lệ Tảo, Hải Phòng • 0362 836 769</div></body>"""

def sonleo(s):
    t, h = s.get("title", ""), s.get("highlight", "")
    fs = fit(t + h, 92, 60, 40)
    qr = os.path.join(HERE, "assets", "qr_zalo.png")
    return f"""<body style="margin:0;width:1080px;height:1350px;background:linear-gradient(160deg,#0a2a8a,#1f6ff0);font-family:Montserrat;color:#fff;position:relative;overflow:hidden">
<div style="position:absolute;right:-200px;top:-200px;width:600px;height:600px;border-radius:50%;background:rgba(255,255,255,.08)"></div>
<div style="padding:110px 90px 0">
<div style="display:inline-block;background:#ffd23f;color:#0a2a8a;font-weight:800;font-size:30px;padding:12px 26px;border-radius:40px">{e(s.get('tag','MẸO AI'))}</div>
<div style="font-size:{fs}px;font-weight:800;line-height:1.12;margin-top:50px">{e(t)}<br><span style="color:#ffd23f">{e(h)}</span></div>
<div style="font-size:38px;line-height:1.6;margin-top:50px;font-weight:500;opacity:.95;max-width:880px">{e(s.get('body',''))}</div></div>
<div style="position:absolute;bottom:90px;left:90px;right:90px;display:flex;align-items:center;gap:30px;background:#fff;color:#0a2a8a;border-radius:30px;padding:28px 34px">
<img src="file://{qr}" style="width:200px;height:200px">
<div style="font-size:32px;font-weight:700;line-height:1.4">Vào group Zalo<br><span style="font-size:40px;font-weight:800">Sơn Leo AI Ads</span><br><span style="font-weight:500;font-size:28px">Quét QR • Zalo 0362 836 769</span></div></div></body>"""

def giadinh(s):
    l1, l2 = s.get("line1", ""), s.get("line2", "")
    fs = fit(l1 + l2, 66, 44, 75)
    by = s.get("by", "")
    return f"""<body style="margin:0;width:1080px;height:1350px;background:#fff4e6;font-family:Montserrat;color:#4a2c1a;display:flex;flex-direction:column;justify-content:center;padding:0 100px;box-sizing:border-box;position:relative">
<div style="font-size:200px;color:#f08a5d;line-height:.6;font-family:'DejaVu Serif'">“</div>
<div style="font-size:{fs}px;font-weight:700;line-height:1.35">{e(l1)}<br><span style="color:#f08a5d">{e(l2)}</span></div>
{f'<div style="font-size:36px;margin-top:50px;font-weight:500">— {e(by)}</div>' if by else ''}
<div style="position:absolute;bottom:90px;left:100px;font-size:32px;font-weight:800;letter-spacing:3px;color:#f08a5d">CHUYỆN GIA ĐÌNH 🧡</div></body>"""

def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    out = os.path.abspath(sys.argv[2])
    body = {"thaison": thaison, "sonleo": sonleo, "giadinh": giadinh}[spec["page"]](spec)
    d = tempfile.mkdtemp()
    p = os.path.join(d, "p.html")
    open(p, "w", encoding="utf-8").write(f"<html><head><meta charset='utf-8'></head>{body}</html>")
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if chrome:
        subprocess.run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1080,1350", f"--screenshot={out}", f"file://{p}"],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
            pg.goto(f"file://{p}"); pg.screenshot(path=out); b.close()
    print(out)

if __name__ == "__main__":
    main()
