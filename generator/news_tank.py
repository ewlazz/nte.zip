"""탄탄대로 (4인 탱크 대전) 4장"""
from PIL import Image, ImageDraw
import cardnews_v2 as c
from cardnews_v2 import F, N, W, H, M, PAPER, PANEL, INK, ACCENT, SOFT, LINE, VIVID, tracked, fade, brand_bar

c.TOTAL = 3
OUT = c.ROOT / "out" / "tank"
OUT.mkdir(parents=True, exist_ok=True)
A = c.ROOT / "assets"
SRC = "인게임 기준 · 2026.11"
U = str(A / "info_cards") + "/"


def tank(w):
    t = Image.open(A / "tank_ironogre_x2.png").convert("RGBA")
    return t.resize((w, int(t.height * w / t.width)), Image.LANCZOS)


SHOP = c.ROOT / "assets" / "tank_shop"


def coin(h):
    im = Image.open(SHOP / "coin.png").convert("RGBA")
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def cover():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    kv = Image.open(c.ROOT / "assets" / "tank_map.png").convert("RGBA")
    kv = kv.crop((0, 0, int(kv.width * 0.80), kv.height))  # 오른쪽 위 게임 안내 문구 제외
    kv = fade(kv.resize((W, int(kv.height * W / kv.width)), Image.LANCZOS), bottom=240)
    img.alpha_composite(kv, (0, 0))
    t = tank(580)
    img.alpha_composite(t, (W - t.width - 10, H - 90 - t.height))
    d = ImageDraw.Draw(img)
    y = 600
    tracked(d, (M - 6, y), "탄탄대로", F("Black", 150), INK, track=-0.05)
    y += 196
    d.text((M, y), "4명 개인전 · 맞히면 점수", font=F("Bold", 40), fill=ACCENT)
    y += 76
    tracked(d, (M - 4, y), "11.11 – 12.23", N("Black", 64), VIVID, track=-0.02)
    brand_bar(d, 1, SRC)
    img.convert("RGB").save(OUT / "01_cover.png", optimize=True)


RULES = [
    ("4명 개인전", "포탄을 맞히면 점수 · 끝나면 점수대로 보상"),
    ("공중 보급", "강한 포탄"),
    ("중앙 쟁탈 구역", "상대 위치가 보이고, 여기서 격파하면 점수 더"),
]


def rules():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150 + 52
    tracked(d, (M - 4, y), "규칙", F("Black", 96), INK, track=-0.04)
    y += 160
    d.line([M, y, W - M, y], fill=INK, width=3)
    for i, (head, body) in enumerate(RULES):
        d.text((M - 2, y + 30), f"{i + 1}", font=N("Black", 64), fill=VIVID)
        tx = M + 90
        d.text((tx, y + 30), head, font=F("Black", 44), fill=INK)
        d.text((tx, y + 92), body, font=F("Medium", 28), fill=ACCENT)
        y += 160
        d.line([M, y, W - M, y], fill=LINE, width=2)
    t = tank(520)
    img.alpha_composite(t, (W - t.width - 20, H - 84 - t.height))
    d = ImageDraw.Draw(img)
    brand_bar(d, 2, SRC)
    img.convert("RGB").save(OUT / "02_rules.png", optimize=True)


ITEMS = [  # (아이콘, 이름, 총량, 코인 합계)
    ("stone", "환석", "300", 450),
    ("fons", "폰즈", "150,000", 300),
    ("ticket", "유빙 극장 티켓", "2", 200),
    ("guide", "특급 헌터 가이드", "12", 240),
    ("dye", "혼돈 염료", "12", 240),
    ("core", "확장 코어", "30", 225),
    ("unit", "이성질 유닛", "45", 225),
    ("beetle", "비틀 코인", "60,000", 120),
]


def rewards():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150 + 52
    tracked(d, (M - 4, y), "기념 상점", F("Black", 96), INK, track=-0.04)
    y += 150
    d.text((M, y), "전부 사면 받는 양 · 드는 코인", font=F("Medium", 28), fill=SOFT)
    y += 64
    gap = 16
    cols = 4
    cw = (W - 2 * M - gap * (cols - 1)) // cols
    ch = 300
    for i, (key, name, qty, cost) in enumerate(ITEMS):
        r, cc = divmod(i, cols)
        x, yy = M + cc * (cw + gap), y + r * (ch + gap)
        d.rounded_rectangle((x, yy, x + cw - 1, yy + ch - 1), 18, fill=PANEL if key != "stone" else (226, 224, 250))
        ic = Image.open(SHOP / f"{key}.png").convert("RGBA")
        ic.thumbnail((cw - 70, 130), Image.LANCZOS)
        img.alpha_composite(ic, (x + (cw - ic.width) // 2, yy + 24 + (130 - ic.height) // 2))
        d = ImageDraw.Draw(img)
        fq = N("Black", 44)
        tw = d.textlength(qty, font=fq)
        d.text((x + (cw - tw) / 2, yy + 160), qty, font=fq, fill=VIVID if key == "stone" else INK)
        fn = F("Bold", 21)
        nw = d.textlength(name, font=fn)
        d.text((x + (cw - nw) / 2, yy + 214), name, font=fn, fill=ACCENT)
        co = coin(28)
        ct = f"{cost:,}"
        fc = N("Bold", 26)
        tot = co.width + 8 + d.textlength(ct, font=fc)
        cx = x + (cw - tot) / 2
        img.alpha_composite(co, (int(cx), yy + 252))
        d = ImageDraw.Draw(img)
        d.text((cx + co.width + 8, yy + 250), ct, font=fc, fill=INK)
    y += 2 * ch + gap + 40
    d.rectangle([M, y, W - M, y + 110], fill=INK)
    co = coin(56)
    img.alpha_composite(co, (M + 34, y + 27))
    d = ImageDraw.Draw(img)
    d.text((M + 110, y + 30), "전부 사려면 2,000", font=F("Black", 40), fill=(255, 255, 255))
    brand_bar(d, 2, SRC)
    img.convert("RGB").save(OUT / "02_rewards.png", optimize=True)


ORDER = ['nanally', 'hotori', 'lacrimosa', 'chaos', 'shinku', 'iroi',
         'zankou', 'linko', 'raven', 'akane', 'elyms']


def outro():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 110
    d.text((M, y), "탄탄대로 끝", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "팔로우하고", F("Black", 80), INK, track=-0.04)
    y += 98
    tracked(d, (M - 4, y), "이환 소식 받아보기", F("Black", 80), INK, track=-0.04)
    y += 130
    d.text((M, y), "도움이 됐다면 좋아요 한 번 눌러주세요", font=F("Medium", 30), fill=ACCENT)
    y += 70
    tracked(d, (M - 2, y), "@nte.zip", N("Black", 88), VIVID, track=-0.02)
    gap, cols = 14, 4
    tw = (W - 2 * M - gap * (cols - 1)) // cols
    th = int(tw * 0.8)
    top = H - 110 - 3 * th - 2 * gap
    for i in range(12):
        r, cc = divmod(i, cols)
        x, yy = M + cc * (tw + gap), top + r * (th + gap)
        if i < len(ORDER):
            im = Image.open(U + ORDER[i] + ".webp").convert("RGB")
            box = (152, 310, 558, 636) if im.width == 1000 else (137, 279, 502, 572)
            t = im.crop(box).resize((tw, th), Image.LANCZOS)
            m = Image.new("L", (tw, th), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, tw - 1, th - 1), 18, fill=255)
            img.paste(t, (x, yy), m)
        else:
            d.rounded_rectangle((x, yy, x + tw - 1, yy + th - 1), 18, fill=PANEL)
            f = N("Black", 96)
            d.text((x + (tw - d.textlength("?", font=f)) / 2, yy + th / 2 - 62), "?", font=f, fill=SOFT)
    img.save(OUT / "03_outro.png", optimize=True)


if __name__ == "__main__":
    cover(); rewards(); outro()
    print("tank ok")
