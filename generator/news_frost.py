"""궤도 너머 특별 노선 「서리의 고리」 (5장)"""
from pathlib import Path
from PIL import Image, ImageDraw
import cardnews_v2 as c
from cardnews_v2 import F, N, W, H, M, PAPER, PANEL, INK, ACCENT, SOFT, LINE, VIVID, tracked, fade, brand_bar

c.TOTAL = 5
OUT = c.ROOT / "out" / "frost"
OUT.mkdir(parents=True, exist_ok=True)
CH = c.ROOT / "assets/characters"
EL = c.ROOT / "assets/icons/element"
SRC = "중국 서버 선행 데이터 종합 · 2026.11"
U = str(c.ROOT / "assets" / "info_cards") + "/"


def art(name, h, crop_frac=None):
    im = Image.open(CH / name).convert("RGBA")
    im = im.crop(im.getbbox())
    if crop_frac:
        im = im.crop((0, 0, im.width, int(im.height * crop_frac)))
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def el_badge(name, size):
    """속성 아이콘을 짙은 원판 위에 얹는다 (빛 아이콘이 밝은 배경에서 안 보이므로)."""
    b = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(b).ellipse((0, 0, size - 1, size - 1), fill=INK + (255,))
    ic = Image.open(EL / f"{name}_icon.png").convert("RGBA")
    s = int(size * 0.78)
    ic = ic.resize((s, s), Image.LANCZOS)
    b.alpha_composite(ic, ((size - s) // 2, (size - s) // 2))
    return b


def cover():
    BG = (16, 30, 56)
    img = Image.new("RGBA", (W, H), BG + (255,))
    kv = Image.open(c.ROOT / "assets/beyond_rails_kv.png").convert("RGBA")
    kv = kv.crop((170, 0, 170 + W, kv.height))  # 원본 해상도 그대로, 가운데 열차 위주
    kh = kv.height
    kv = fade(kv, bottom=240)
    img.alpha_composite(kv, (0, 0))
    d = ImageDraw.Draw(img)
    y = kh - 40
    tracked(d, (M, y), "궤도 너머 · 특별 노선", F("Bold", 30), (150, 190, 235), track=0.04)
    y += 62
    tracked(d, (M - 6, y), "서리의 고리", F("Black", 140), (255, 255, 255), track=-0.05)
    y += 196
    tracked(d, (M - 4, y), "11.19 – 12.3", N("Black", 64), (130, 200, 255), track=-0.02)
    y += 96
    d.text((M, y), "버프 · 약점 · 파티", font=F("Bold", 32), fill=(190, 205, 230))
    yb = H - 66
    f1 = F("Bold", 22)
    d.text((M, yb), "@nte.zip", font=f1, fill=(255, 255, 255))
    x = M + d.textlength("@nte.zip", font=f1) + 16
    fs = F("Medium", 19)
    d.text((x, yb + 2), SRC, font=fs, fill=(150, 170, 205))
    x += d.textlength(SRC, font=fs) + 16
    d.text((x, yb + 1), "01 / 05", font=F("SemiBold", 20), fill=(150, 170, 205))
    img.convert("RGB").save(OUT / "01_cover.png", optimize=True)


def buffs():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150
    y += 52
    tracked(d, (M - 4, y), "이번 버프", F("Black", 96), INK, track=-0.04)
    y += 170
    rows = [
        ("20", "적 방어력 무시", "파티 전원 · 항상"),
        ("20", "적 모든 속성 저항 무시", "궁극기 쓴 캐릭터 · 20초 · 다시 쓰면 갱신"),
    ]
    d.line([M, y, W - M, y], fill=INK, width=3)
    for num, what, who in rows:
        f = N("Black", 150)
        d.text((M - 6, y + 20), num, font=f, fill=VIVID)
        nx = M + d.textlength(num, font=f) + 4
        d.text((nx, y + 92), "%", font=N("Black", 60), fill=VIVID)
        tx = M + 330
        d.text((tx, y + 50), what, font=F("Black", 44), fill=INK)
        d.text((tx, y + 116), who, font=F("Medium", 26), fill=SOFT)
        y += 220
        d.line([M, y, W - M, y], fill=LINE, width=2)
    y += 40
    d.rectangle([M, y, W - M, y + 110], fill=PANEL)
    d.text((M + 36, y + 38), "보상", font=F("Bold", 28), fill=SOFT)
    d.text((M + 150, y + 34), "환석 · 폰즈 · 운행 기록", font=F("Bold", 36), fill=INK)
    el = fade(Image.open(CH / "elyms_chibi_hq.png").convert("RGBA"), bottom=30)
    el = el.crop(el.getbbox())
    eh = 230
    el = el.resize((int(el.width * eh / el.height), eh), Image.LANCZOS)
    img.alpha_composite(el, (W - el.width - 30, H - 74 - eh))
    d = ImageDraw.Draw(img)
    brand_bar(d, 2, SRC)
    img.convert("RGB").save(OUT / "02_buffs.png", optimize=True)


WEAK = [("상", 9), ("혼", 6), ("빛", 4), ("령", 2), ("암", 2), ("주", 1)]


def weakness():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150
    y += 52
    tracked(d, (M - 4, y), "적 약점", F("Black", 96), INK, track=-0.04)
    y += 128
    d.text((M, y), "등장하는 적 12종 기준", font=F("Medium", 26), fill=SOFT)
    y += 70
    d.line([M, y, W - M, y], fill=INK, width=3)
    bx0, bx1 = M + 200, W - M - 90
    rh = 120
    for i, (el, n) in enumerate(WEAK):
        top = i < 2
        badge = el_badge(el, 76)
        img.alpha_composite(badge, (M, y + (rh - 76) // 2))
        d.text((M + 96, y + 34), el, font=F("Black", 44), fill=INK if top else ACCENT)
        bw = (bx1 - bx0) * n / 12
        d.rounded_rectangle([bx0, y + 44, bx0 + bw, y + rh - 44], 10, fill=VIVID if top else SOFT)
        d.text((bx0 + bw + 18, y + 30), str(n), font=N("Black", 52), fill=VIVID if top else ACCENT)
        y += rh
        d.line([M, y, W - M, y], fill=LINE, width=2)
    brand_bar(d, 3, SRC)
    img.convert("RGB").save(OUT / "03_weakness.png", optimize=True)


TEAMS = [
    ("상행선", "몹 무리", [("shinku", "신쿠"), ("akane", "아카네 린"), ("iroi", "일로이"), ("elyms", "엘림")]),
    ("하행선", "보스", [("zankou", "잔홍"), ("blackbird", "레이븐"), ("linko", "링코"), ("daffodill", "다포딜")]),
]


def card(key, w, h):
    im = Image.open(CH / "cards" / f"{key}.webp").convert("RGBA")
    # 얼굴~가슴이 보이게 위쪽을 잘라 같은 비율로
    cw = im.width
    ch = int(cw * h / w)
    if key == "daffodill":
        bb = im.getbbox()
        im = im.crop(bb)
        cw = im.width
        ch = min(im.height, int(cw * h / w))
    im = im.crop((0, 0, cw, ch)).resize((w, h), Image.LANCZOS)
    bg = Image.new("RGBA", (w, h), PANEL + (255,))
    bg.alpha_composite(im)
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 16, fill=255)
    return bg, m


def party():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150
    y += 52
    tracked(d, (M - 4, y), "추천 파티", F("Black", 96), INK, track=-0.04)
    y += 160
    gap = 14
    tw = (W - 2 * M - gap * 3) // 4
    th = int(tw * 1.12)
    for line, kind, mem in TEAMS:
        d.line([M, y, W - M, y], fill=INK, width=3)
        d.text((M, y + 18), line, font=F("Black", 40), fill=INK)
        d.text((M + 150, y + 26), kind, font=F("Bold", 30), fill=VIVID)
        y += 84
        for i, (key, name) in enumerate(mem):
            x = M + i * (tw + gap)
            cimg, m = card(key, tw, th)
            img.paste(cimg, (x, y), m)
            d = ImageDraw.Draw(img)
            d.text((x + 4, y + th + 10), name, font=F("Bold", 26), fill=INK)
        y += th + 60
    d.text((M, y + 4), "캐릭터가 부족하면  아카네 린 + 레이븐 + 일로이 · 사키리 · 엘림 중 둘", font=F("Medium", 24), fill=ACCENT)
    brand_bar(d, 4, SRC)
    img.convert("RGB").save(OUT / "04_party.png", optimize=True)


ORDER = ['nanally', 'hotori', 'lacrimosa', 'chaos', 'shinku', 'iroi',
         'zankou', 'linko', 'raven', 'akane', 'elyms']


def outro():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 110
    d.text((M, y), "서리의 고리 끝", font=F("Bold", 30), fill=ACCENT)
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
    img.save(OUT / "05_outro.png", optimize=True)


cover(); buffs(); weakness(); party(); outro()
print("frost ok")
