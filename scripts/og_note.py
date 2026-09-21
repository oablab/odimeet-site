#!/usr/bin/env python3
"""OG cards (1200x630) for a dev note: headline + kicker on the left, two mini iPhones
(host teal / guest amber level bars) on the right. Usage: og_note.py <slug> ; edits TEXT below."""
import sys, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
TEXTS = {}
TEXTS["rode-wireless-micro"] = {
  "en": dict(kicker="OdiMeet · development notes",
             title=["The RØDE", "Wireless Micro", "passes too"],
             sub="Second certified wireless mic set, hours after the DJI.\nOne setting: Channel Routing set to Split in RØDE Central.",
             font="/System/Library/Fonts/HelveticaNeue.ttc", bold_index=1, kfont_index=0, a="TX1", b="TX2"),
  # Hiragino Sans (JP) W6: Hiragino Sans GB has no Ø glyph (renders tofu).
  "zh": dict(kicker="OdiMeet 開發筆記",
             title=["RØDE Wireless", "Micro 也通過了"],
             sub="DJI 之後幾小時，第二套認證的迷你無線麥克風。\n唯一的設定：RØDE Central 裡把 Channel Routing 選 Split。",
             font="/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", bold_index=0, kfont_index=0, a="TX1", b="TX2"),
}
TEXTS["dji-mic-mini"] = {
  "en": dict(kicker="OdiMeet · development notes",
             title=["Tonight OdiMeet", "learned to use", "a DJI Mic Mini"],
             sub="One receiver, two clip-on transmitters, one iPhone.\nOne speaker per channel — 19.6 dB apart, zero alignment.",
             font="/System/Library/Fonts/HelveticaNeue.ttc", bold_index=1, kfont_index=0, a="TX1", b="TX2"),
  "zh": dict(kicker="OdiMeet 開發筆記",
             title=["今晚，OdiMeet", "正式支援", "DJI Mic Mini"],
             sub="一個接收器、兩個領夾發射器、一支 iPhone。\n一人一聲道——相差 19.6 dB，不用對齊。",
             font="/System/Library/Fonts/Hiragino Sans GB.ttc", bold_index=2, kfont_index=0, a="TX1", b="TX2"),
}
TEXTS["iphone-array"] = TEXT = {
  "en": dict(kicker="OdiMeet · development notes",
             title=["How the iPhone", "recording array", "works"],
             sub="A phone per speaker. The loudest track is the one talking —\nmeasured, not guessed.",
             font="/System/Library/Fonts/HelveticaNeue.ttc", bold_index=1, kfont_index=0,
             a="Alice", b="Ben"),
  "zh": dict(kicker="OdiMeet 開發筆記",
             title=["iPhone 錄音陣列", "怎麼做到的"],
             sub="每個人面前一支手機，哪支最大聲就是誰在講——\n量出來的，不是猜的。",
             font="/System/Library/Fonts/Hiragino Sans GB.ttc", bold_index=2, kfont_index=0,
             a="小美", b="阿明"),
}

def font(path, size, index=None, bold=False):
    return ImageFont.truetype(path, size, index=index or 0)

def gradient(draw):
    top, bot = (15, 23, 32), (21, 48, 46)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (W, y)], fill=c)

def phone(im, x, y, w, h, name, color, loud, bars):
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(w * 0.19), fill=(28, 30, 34))
    pad = int(w * 0.06)
    d.rounded_rectangle([x + pad, y + pad, x + w - pad, y + h - pad], radius=int(w * 0.14), fill=(6, 8, 11))
    # island
    iw = int(w * 0.34); d.rounded_rectangle([x + (w - iw) // 2, y + pad + 12, x + (w + iw) // 2, y + pad + 24], radius=6, fill=(28, 30, 34))
    f = ImageFont.truetype("/System/Library/Fonts/Hiragino Sans GB.ttc", int(w * 0.13), index=2)
    tw = d.textlength(name, font=f); d.text((x + (w - tw) / 2, y + pad + 44), name, font=f, fill=color if loud else (154, 167, 181))
    # level bars
    bw = int(w * 0.075); gap = int(w * 0.045); total = 4 * bw + 3 * gap
    bx = x + (w - total) // 2; base = y + h * 0.62; maxh = h * 0.24
    for i, lvl in enumerate(bars):
        bh = maxh * lvl
        d.rounded_rectangle([bx + i * (bw + gap), base - bh, bx + i * (bw + gap) + bw, base], radius=bw // 2,
                            fill=color if loud else (255, 255, 255, 60) if False else ((60, 66, 74) if not loud else color))
    # dB
    f2 = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", int(w * 0.11))
    db = "−24 dB" if loud else "−39 dB"
    tw = d.textlength(db, font=f2); d.text((x + (w - tw) / 2, base + 16), db, font=f2, fill=(232, 238, 245) if loud else (111, 126, 140))

def card(lang, out, TEXT):
    t = TEXT[lang]
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im); gradient(d)
    teal, amber = (79, 179, 169), (231, 183, 95)
    # kicker
    kf = font(t["font"], 26, t["kfont_index"], bold=False)
    d.text((72, 78), t["kicker"], font=kf, fill=teal)
    # title
    tf = font(t["font"], 66 if lang == "en" else 78, t["bold_index"], bold=True)
    y = 120 if lang == "en" else 128
    for line in t["title"]:
        assert 72 + d.textlength(line, font=tf) <= 824, ("headline crosses artwork", line)
        d.text((72, y), line, font=tf, fill=(232, 238, 245)); y += (76 if lang == "en" else 100)
    # sub
    sf = font(t["font"], 28 if lang == "zh" else 26, t["kfont_index"], bold=False)
    y += 14
    for line in t["sub"].split("\n"):
        assert 72 + d.textlength(line, font=sf) <= 824, ("subline crosses artwork", line)
        d.text((72, y), line, font=sf, fill=(154, 167, 181)); y += 42
    # footer brand
    bf = font(t["font"], 24, t["kfont_index"], bold=False)
    d.text((72, H - 84), "odimeet.app", font=bf, fill=(154, 167, 181))
    # artwork right: two phones, host loud
    pw, ph = 150, 302
    phone(im, 862, 160, pw, ph, t["a"], teal, True, [0.7, 1.0, 0.85, 0.95])
    phone(im, 1038, 160, pw, ph, t["b"], amber, False, [0.3, 0.42, 0.26, 0.36])
    # link label between phones
    d = ImageDraw.Draw(im)
    lf = ImageFont.truetype("/System/Library/Fonts/HelveticaNeue.ttc", 20)
    d.text((1012, 300), "⇄", font=ImageFont.truetype("/System/Library/Fonts/Apple Symbols.ttf", 26) if os.path.exists("/System/Library/Fonts/Apple Symbols.ttf") else lf, fill=teal)
    im.save(out, optimize=True); print(out, im.size, os.path.getsize(out))

if __name__ == "__main__":
    slug = sys.argv[1]
    TEXT = TEXTS[slug]
    for lang in ("en", "zh"):
        card(lang, f"notes/{slug}/og-{lang}.png", TEXT)
