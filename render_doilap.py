#!/usr/bin/env python3
"""Render a Veston Thái Sơn "đối lập" (contrast) image, 1080x1350, PIL only.
Usage: python3 render_doilap.py spec.json out.png
spec.json: {"tag":"CÔNG SỞ","top":"Đồ may sẵn: vai chật, tay dài, cố mặc cho xong","bottom":"Đồ may đo: đo từng vai, từng tay, mặc là vừa","cta":"Bạn từng gặp tình huống nào?"}
 - tag: ≤ 20 ký tự, viết hoa (CÔNG SỞ, ĐÁM CƯỚI, PHỎNG VẤN, TỰ TIN, TỦ ĐỒ, GIA ĐÌNH...)
 - top / bottom: mỗi vế ≤ 60 ký tự, đời thường, không nêu giá/khuyến mãi/cam kết, không nhắm vào hãng hay người cụ thể.
 - cta: tùy chọn, mặc định "Bạn từng gặp tình huống nào?"
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

G = "/usr/share/fonts/truetype/google-fonts/ofl/"
DJ = "/usr/share/fonts/truetype/dejavu/"
W, H = 1080, 1350
NAVY, GOLD, CREAM = (18, 30, 56), (212, 175, 96), (250, 244, 230)


def font(paths, size, wght=None):
    for p in paths:
        if os.path.exists(p):
            f = ImageFont.truetype(p, size)
            if wght:
                try: f.set_variation_by_axes([wght])
                except Exception: pass
            return f
    return ImageFont.load_default()


SERIF = [G + "gelasio/Gelasio[wght].ttf", DJ + "DejaVuSerif-Bold.ttf"]
SANS_M = [G + "firasans/FiraSans-Medium.ttf", DJ + "DejaVuSans.ttf"]
SANS_B = [G + "firasans/FiraSans-SemiBold.ttf", DJ + "DejaVuSans-Bold.ttf"]
SANS_X = [G + "firasans/FiraSans-ExtraBold.ttf", DJ + "DejaVuSans-Bold.ttf"]


def wrap(d, t, f, mw):
    out, cur = [], ""
    for w in t.split():
        x = (cur + " " + w).strip()
        if d.textlength(x, font=f) <= mw: cur = x
        else: out.append(cur); cur = w
    out.append(cur)
    return out


def ctr(d, t, y, f, fill):
    b = d.textbbox((0, 0), t, font=f)
    d.text((W / 2 - (b[2] - b[0]) / 2 - b[0], y), t, font=f, fill=fill)


def block(d, text, top, bot, size, fill):
    while True:
        f = font(SERIF, size, 600)
        ls = wrap(d, text, f, 820)
        lh = int(size * 1.3)
        if len(ls) * lh <= bot - top - 20 or size <= 34: break
        size -= 2
    y = top + (bot - top - len(ls) * lh) / 2
    for l in ls:
        ctr(d, l, y, f, fill); y += lh


def main(spec_path, out):
    s = json.load(open(spec_path, encoding="utf-8"))
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H // 2], fill=CREAM); d.rectangle([0, H // 2, W, H], fill=NAVY)
    ctr(d, "VESTON THÁI SƠN", 62, font(SANS_B, 30), (150, 115, 50))
    tag = s.get("tag", "")
    f = font(SANS_X, 34); tw = d.textlength(tag, font=f)
    d.rounded_rectangle([W / 2 - tw / 2 - 30, 115, W / 2 + tw / 2 + 30, 175], radius=30, fill=NAVY)
    ctr(d, tag, 123, f, GOLD)
    block(d, s["top"], 200, H // 2 - 30, 66, NAVY)
    block(d, s["bottom"], H // 2 + 40, H - 290, 66, CREAM)
    d.ellipse([W / 2 - 60, H // 2 - 60, W / 2 + 60, H // 2 + 60], fill=GOLD, outline=CREAM, width=8)
    ctr(d, "VS", H // 2 - 32, font(SANS_X, 56), NAVY)
    d.line([140, H - 250, W - 140, H - 250], fill=GOLD, width=3)
    ctr(d, s.get("cta", "Bạn từng gặp tình huống nào?"), H - 215, font(SANS_X, 50), CREAM)
    ctr(d, "May đo cao cấp  •  Hải Phòng", H - 130, font(SANS_M, 30), GOLD)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    im.save(out)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
