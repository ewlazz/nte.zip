"""탄탄대로 (4인 탱크 대전) 4장"""
from PIL import Image, ImageDraw
import cardnews_v2 as c
from cardnews_v2 import F, N, W, H, M, PAPER, PANEL, INK, ACCENT, SOFT, LINE, VIVID, tracked, fade, brand_bar

c.TOTAL = 4
OUT = c.ROOT / "out" / "tank"
OUT.mkdir(parents=True, exist_ok=True)
A = c.ROOT / "assets"
SRC = "공식 공지 · 2026.11"
U = str(A / "info_cards") + "/"


def tank(w):
    t = Image.open(A / "tank_ironogre_x2.png").convert("RGBA")
    return t.resize((w, int(t.height * w / t.width)), Image.LANCZOS)


def cover():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    t = tank(1000)
    img.alpha_composite(t, (W - t.width - 20, H - 96 - t.height - 20))
    d = ImageDraw.Draw(img)
    y = 150
    tracked(d, (M, y), "1.5 신규 콘텐츠", F("Bold", 28), SOFT, track=0.04)
    y += 60
    tracked(d, (M - 6, y), "탄탄대로", F("Black", 150), INK, track=-0.05)
    y += 196
    d.text((M, y), "4인 탱크 대전", font=F("Bold", 40), fill=ACCENT)
    y += 76
    tracked(d, (M - 4, y), "11.11 – 12.23", N("Black", 64), VIVID, track=-0.02)
    brand_bar(d, 1, SRC)
    img.convert("RGB").save(OUT / "01_cover.png", optimize=True)


RULES = [
    ("4명 개인전", "포탄을 맞히면 점수"),
    ("시간이 끝나면", "최종 점수대로 보상"),
    ("공중 보급", "강한 포탄을 얻는다"),
    ("중앙 쟁탈 구역", "보급품을 먹으면 상대 위치가 보이고\n여기서 격파하면 점수를 더 받는다"),
]


def rules():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150 + 52
    tracked(d, (M - 4, y), "규칙", F("Black", 96), INK, track=-0.04)
    y += 160
    d.line([M, y, W - M, y], fill=INK, width=3)
    for i, (head, body) in enumerate(RULES):
        rh = 170 if "\n" in body else 140
        d.text((M - 2, y + 26), f"{i + 1}", font=N("Black", 64), fill=VIVID)
        tx = M + 90
        d.text((tx, y + 28), head, font=F("Black", 40), fill=INK)
        d.multiline_text((tx, y + 84), body, font=F("Medium", 28), fill=ACCENT, spacing=10)
        y += rh
        d.line([M, y, W - M, y], fill=LINE, width=2)
    t = tank(420)
    img.alpha_composite(t, (W - t.width - 30, H - 84 - t.height))
    d = ImageDraw.Draw(img)
    brand_bar(d, 2, SRC)
    img.convert("RGB").save(OUT / "02_rules.png", optimize=True)


def rewards():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150 + 52
    tracked(d, (M - 4, y), "보상", F("Black", 96), INK, track=-0.04)
    y += 150
    d.text((M, y), "참여하면 이벤트 코인 → 이벤트 상점에서 교환", font=F("Medium", 28), fill=SOFT)
    y += 70
    d.line([M, y, W - M, y], fill=INK, width=3)
    st = Image.open(A / "icons" / "stone.png").convert("RGBA")
    sh = 150
    st = st.resize((int(st.width * sh / st.height), sh), Image.LANCZOS)
    img.alpha_composite(st, (M - 6, y + 34))
    d.text((M + st.width + 24, y + 62), "환석", font=F("Black", 72), fill=INK)
    y += 220
    d.line([M, y, W - M, y], fill=LINE, width=2)
    for name in ["폰즈", "영화 티켓", "특급 헌터 가이드", "혼돈 염료"]:
        d.text((M, y + 26), name, font=F("Bold", 40), fill=INK)
        y += 100
        d.line([M, y, W - M, y], fill=LINE, width=2)
    brand_bar(d, 3, SRC)
    img.convert("RGB").save(OUT / "03_rewards.png", optimize=True)


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
    img.save(OUT / "04_outro.png", optimize=True)


if __name__ == "__main__":
    cover(); rules(); rewards(); outro()
    print("tank ok")
