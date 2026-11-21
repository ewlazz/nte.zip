"""이환 1.5 일정 한 장 정리 (4장)"""
from datetime import date
from pathlib import Path
from PIL import Image, ImageDraw
import cardnews_v2 as c
from cardnews_v2 import F, N, W, H, M, PAPER, PANEL, INK, ACCENT, SOFT, LINE, VIVID, tracked, fade, brand_bar

c.TOTAL = 4
OUT = c.ROOT / "out" / "15cal"
OUT.mkdir(parents=True, exist_ok=True)
CH = c.ROOT / "assets/characters"
SRC = "공식 공지 · 2026.11"
U = str(c.ROOT / "assets" / "info_cards") + "/"
TILE = {"elyms": "elyms", "shinku": "shinku", "chaos": "chaos"}


def tile(key, tw, th):
    im = Image.open(U + TILE[key] + ".webp").convert("RGB")
    box = (152, 310, 558, 636) if im.width == 1000 else (137, 279, 502, 572)
    t = im.crop(box).resize((tw, th), Image.LANCZOS)
    m = Image.new("L", (tw, th), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, tw - 1, th - 1), 16, fill=255)
    return t, m


def cover():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    e = Image.open(CH / "elyms_x2.png").convert("RGBA")
    e = e.crop(e.getbbox())
    eh = 1060
    e = e.resize((int(e.width * eh / e.height), eh), Image.LANCZOS)
    e = e.crop((0, 0, e.width, H - 96 - 330))
    e = fade(e, bottom=200)
    img.alpha_composite(e, (W - e.width + 60, 330))
    d = ImageDraw.Draw(img)
    y = 150
    tracked(d, (M, y), "VERSION 1.5", F("Bold", 26), SOFT, track=0.18)
    y += 56
    tracked(d, (M - 6, y), "1.5 일정", F("Black", 150), INK, track=-0.05)
    y += 172
    tracked(d, (M - 6, y), "한 장 정리", F("Black", 150), INK, track=-0.05)
    y += 210
    tracked(d, (M - 4, y), "11.11 – 12.23", N("Black", 64), VIVID, track=-0.02)
    y += 90
    d.text((M, y), "픽업 · 이벤트 기간", font=F("Bold", 32), fill=ACCENT)
    brand_bar(d, 1, SRC)
    img.convert("RGB").save(OUT / "01_cover.png", optimize=True)


def pickups():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 150
    d.text((M, y), "한정 보드", font=F("Bold", 30), fill=ACCENT)
    y += 52
    tracked(d, (M - 4, y), "누가 언제 나오나", F("Black", 96), INK, track=-0.04)
    y += 170
    ts, th = 190, 152
    halves = [
        ("전반", "11.11 – 12.2", [("elyms", "엘림", "디지털 드림", "신규"), ("shinku", "신쿠", "동틀 녘", "복각")]),
        ("후반", "12.2 – 12.23", [(None, "Exe", "오프라인 알고리즘", "신규"), ("chaos", "카오스", "돌아올 수 없는 길", "복각")]),
    ]
    for label, period, items in halves:
        d.line([M, y, W - M, y], fill=INK, width=3)
        d.text((M, y + 20), label, font=F("Black", 40), fill=INK)
        d.text((M + 100, y + 26), period, font=N("Bold", 34), fill=VIVID)
        y += 88
        for key, name, board, tag in items:
            if key:
                t, m = tile(key, ts, th)
                img.paste(t, (M, y), m)
            else:
                d.rounded_rectangle((M, y, M + ts - 1, y + th - 1), 16, fill=PANEL)
                f = N("Black", 48)
                d.text((M + (ts - d.textlength("Exe", font=f)) / 2, y + 44), "Exe", font=f, fill=SOFT)
            nx = M + ts + 32
            d.text((nx, y + 14), tag, font=F("Bold", 26), fill=VIVID if tag == "신규" else SOFT)
            d.text((nx, y + 48), name, font=(N if name.isascii() else F)("Black", 54), fill=INK)
            d.text((nx, y + 116), board, font=F("Medium", 26), fill=SOFT)
            y += th + 20
        y += 10
    brand_bar(d, 2, SRC)
    img.save(OUT / "02_pickups.png", optimize=True)


EVENTS = [
    ("시즌 패스", (11, 11), (12, 23)),
    ("시티 익스프레스", (11, 11), (12, 23)),
    ("탄탄대로", (11, 11), (12, 23)),
    ("시련의 연회", (11, 11), (12, 23)),
    ("픽셀 대방출", (11, 16), (11, 23)),
    ("궤도 너머 서리의 고리", (11, 19), (12, 3)),
    ("어획 대작전", (11, 23), (12, 23)),
    ("골드러시 대작전", (11, 23), (12, 7)),
    ("시티 오너", (12, 2), (12, 23)),
    ("폰즈 러시", (12, 7), (12, 14)),
    ("기상천외 카드 뒤집기", (12, 10), (12, 23)),
]


SHORT = [  # 기간이 짧아 놓치기 쉬운 이벤트만
    ("픽셀 대방출", "11.16", "11.23"),
    ("궤도 너머 서리의 고리", "11.19", "12.3"),
    ("골드러시 대작전", "11.23", "12.7"),
    ("폰즈 러시", "12.7", "12.14"),
]


def gantt():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150
    d.text((M, y), "기간 짧은 이벤트", font=F("Bold", 30), fill=ACCENT)
    y += 52
    tracked(d, (M - 4, y), "이것만 챙기기", F("Black", 96), INK, track=-0.04)
    y += 170
    d.line([M, y, W - M, y], fill=INK, width=3)
    rh = 150
    for name, s0, e0 in SHORT:
        x = tracked(d, (M - 2, y + 26), s0, N("Black", 60), VIVID, track=-0.03)
        d.text((x + 10, y + 26), "–", font=N("Black", 60), fill=VIVID)
        tracked(d, (x + 56, y + 26), e0, N("Black", 60), VIVID, track=-0.03)
        d.text((M, y + 98), name, font=F("Bold", 32), fill=INK)
        y += rh
        d.line([M, y, W - M, y], fill=LINE, width=2)
    y += 34
    d.rectangle([M, y, W - M, y + 96], fill=PANEL)
    d.text((M + 36, y + 28), "나머지 이벤트는 12.23까지", font=F("Bold", 34), fill=INK)
    la = fade(Image.open(CH / "lacrimosa_chibi.png").convert("RGBA"), bottom=0)
    la = la.crop(la.getbbox())
    lh = 300
    la = la.resize((int(la.width * lh / la.height), lh), Image.LANCZOS)
    img.alpha_composite(la, (W - la.width - 30, H - 84 - la.height))
    d = ImageDraw.Draw(img)
    brand_bar(d, 3, SRC)
    img.convert("RGB").save(OUT / "03_events.png", optimize=True)


ORDER = ['nanally', 'hotori', 'lacrimosa', 'chaos', 'shinku', 'iroi',
         'zankou', 'linko', 'raven', 'akane', 'elyms']


def outro():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 110
    d.text((M, y), "1.5 일정 끝", font=F("Bold", 30), fill=ACCENT)
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
    img.save(OUT / "04_outro.png", optimize=True)


cover(); pickups(); gantt(); outro()
print("cal ok")
