"""소식 카드뉴스: 이환 TGA 2026 최고의 모바일 게임 후보 + 환석 1,000개 (4장)"""
from pathlib import Path
from PIL import Image, ImageDraw
import cardnews_v2 as c
from cardnews_v2 import F, N, W, H, M, PAPER, PANEL, INK, ACCENT, SOFT, LINE, VIVID, tracked, fade, brand_bar

c.TOTAL = 5
OUT = c.ROOT / "out" / "tga"
OUT.mkdir(parents=True, exist_ok=True)
CH = c.ROOT / "assets/characters"
SRC = "공식 공지 · 2026.11"


def art(name, h):
    im = Image.open(CH / name).convert("RGBA")
    im = im.crop(im.getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)


def cover():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    # 캐스트: 얼굴 크기(눈~턱)와 눈높이를 맞춰 배치. 가운데(엘림)는 조금 크게, 양옆은 살짝 아래
    # (이름, 눈 y비율, 턱 y비율, 얼굴 x비율 — 이미지 bbox 기준)
    base = H - 96

    def place(name, ey, cy, fx, face, eye_y, face_x, xcrop=None, side_fade=0):
        im = Image.open(CH / name).convert("RGBA")
        im = im.crop(im.getbbox())
        s = face / ((cy - ey) * im.height)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        left, top = int(face_x - fx * im.width), int(eye_y - ey * im.height)
        if xcrop:
            x0, x1 = int(xcrop[0] * im.width), int(xcrop[1] * im.width)
            im = im.crop((x0, 0, x1, im.height)); left += x0
        im = im.crop((0, 0, im.width, max(1, base - top)))
        im = fade(im, bottom=220, left=side_fade, right=side_fade)
        img.alpha_composite(im, (left, top))

    place("nanally_x2.png", 0.30, 0.387, 0.56, 62, 820, 215)
    place("lacrimosa_x2.png", 0.308, 0.40, 0.41, 62, 820, 865)
    place("elyms_x2.png", 0.167, 0.212, 0.67, 68, 790, 540, xcrop=(0.30, 0.95), side_fade=60)
    d = ImageDraw.Draw(img)
    y = 128
    tracked(d, (M, y), "THE GAME AWARDS 2026", F("Bold", 26), SOFT, track=0.18)
    y += 56
    tracked(d, (M - 6, y), "이환,", F("Black", 150), INK, track=-0.05)
    y += 172
    tracked(d, (M - 6, y), "TGA 후보", F("Black", 150), INK, track=-0.05)
    y += 196
    d.text((M, y), "최고의 모바일 게임 부문", font=F("Bold", 34), fill=ACCENT)
    brand_bar(d, 1, SRC)
    img.convert("RGB").save(OUT / "01_cover.png", optimize=True)


def stones():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150
    d.text((M, y), "노미네이트 기념", font=F("Bold", 30), fill=ACCENT)
    y += 52
    tracked(d, (M - 4, y), "모두에게", F("Black", 84), INK, track=-0.04)
    y += 120
    st = Image.open(c.ICONS / "stone.png").convert("RGBA")
    sh = 190
    st = st.resize((int(st.width * sh / st.height), sh), Image.LANCZOS)
    img.alpha_composite(st, (M - 10, y + 40))
    x = tracked(d, (M + st.width + 10, y), "1,000", N("Black", 220), VIVID, track=-0.04)
    d.text((x + 16, y + 128), "환석", font=F("Black", 64), fill=INK)
    y += 300
    d.line([M, y, W - M, y], fill=INK, width=3)
    rows = [("지급", "11월 18일 16:00 이후"), ("수령", "게임 내 우편"), ("조건", "1.5 버전 종료 전까지"), ("", "캐릭터 생성 + 우편 기능 활성화")]
    y += 34
    for k, v in rows:
        if k:
            d.text((M, y + 4), k, font=F("Bold", 30), fill=SOFT)
        d.text((M + 130, y), v, font=F("Bold", 38), fill=INK)
        y += 64 if k != "조건" else 54
        if k and k != "조건":
            d.line([M, y - 14, W - M, y - 14], fill=LINE, width=2)
    la = fade(art("lacrimosa_chibi.png", 360), bottom=50)
    img.alpha_composite(la, (W - la.width + 30, H - 90 - la.height))
    d = ImageDraw.Draw(img)
    brand_bar(d, 2, SRC)
    img.convert("RGB").save(OUT / "02_stones.png", optimize=True)


def rivals():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150
    d.text((M, y), "최고의 모바일 게임", font=F("Bold", 30), fill=ACCENT)
    y += 52
    tracked(d, (M - 4, y), "후보 5개", F("Black", 96), INK, track=-0.04)
    y += 160
    games = [("명일방주: 엔드필드", "Hypergryph"), ("몬스터헌터 아웃랜더스", "티미 스튜디오"),
             ("이환", "Hotta Studio"), ("Pokémon Champions", "The Pokémon Works"),
             ("연운", "Everstone Studio")]
    rh = 112
    d.line([M, y, W - M, y], fill=INK, width=3)
    for g, dev in games:
        me = g == "이환"
        if me:
            d.rectangle([M, y + 2, W - M, y + rh - 1], fill=PANEL)
            d.rectangle([M, y + 2, M + 8, y + rh - 1], fill=VIVID)
        tx = M + (34 if me else 0)
        tf = N("Bold", 38) if g.isascii() else F("Bold", 38)
        d.text((tx, y + 20), g, font=tf, fill=VIVID if me else INK)
        d.text((tx, y + 70), dev, font=F("Medium", 24), fill=SOFT)
        y += rh
        d.line([M, y, W - M, y], fill=LINE, width=2)
    y += 60
    d.rectangle([M, y, W - M, y + 110], fill=PANEL)
    d.text((M + 36, y + 38), "시상식", font=F("Bold", 28), fill=SOFT)
    d.text((M + 180, y + 34), "12월 11일 오전 (한국 시간)", font=F("Bold", 36), fill=INK)
    brand_bar(d, 3, "공식 발표 · 2026.11")
    img.convert("RGB").save(OUT / "03_rivals.png", optimize=True)


def vote():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)
    y = 150
    d.text((M, y), "팬 투표", font=F("Bold", 30), fill=ACCENT)
    y += 52
    tracked(d, (M - 4, y), "투표는 여기서", F("Black", 96), INK, track=-0.04)
    y += 150
    tracked(d, (M - 2, y), "thegameawards.com", N("Black", 78), VIVID, track=-0.02)
    y += 140
    d.line([M, y, W - M, y], fill=INK, width=3)
    steps = [("사이트 접속 후 로그인", None), ("Best Mobile Game", "최고의 모바일 게임"), ("Neverness to Everness", "이환 선택")]
    for i, (t, sub) in enumerate(steps):
        rh = 112
        d.text((M, y + 26), str(i + 1), font=N("Black", 48), fill=SOFT)
        tf = N("Bold", 38) if t[0].isascii() else F("Bold", 38)
        d.text((M + 70, y + (22 if sub else 34)), t, font=tf, fill=INK)
        if sub:
            d.text((M + 70, y + 70), sub, font=F("Medium", 24), fill=SOFT)
        y += rh
        d.line([M, y, W - M, y], fill=LINE, width=2)
    y += 56
    d.rectangle([M, y, W - M, y + 182], fill=PANEL)
    for i, (k, v) in enumerate([("마감", "12월 10일 오전 11시 (한국 시간)"), ("반영", "팬 투표 10% + 심사단 90%")]):
        yy = y + 34 + i * 72
        d.text((M + 36, yy + 4), k, font=F("Bold", 28), fill=SOFT)
        d.text((M + 150, yy), v, font=F("Bold", 36), fill=INK)
    el = fade(art("elyms_chibi_hq.png", 205), bottom=40)
    img.alpha_composite(el, (W - el.width - 30, H - 70 - el.height))
    d = ImageDraw.Draw(img)
    brand_bar(d, 4, "공식 발표 · 2026.11")
    img.convert("RGB").save(OUT / "04_vote.png", optimize=True)


U = str(c.ROOT / "assets" / "info_cards") + "/"
ORDER = ['nanally', 'hotori', 'lacrimosa', 'chaos', 'shinku', 'iroi',
         'zankou', 'linko', 'raven', 'akane', 'elyms']


def tile(fid):
    im = Image.open(U + fid + '.webp').convert('RGB')
    box = (152, 310, 558, 636) if im.width == 1000 else (137, 279, 502, 572)
    return im.crop(box)


def outro():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 110
    d.text((M, y), "이환 소식 끝", font=F("Bold", 30), fill=ACCENT)
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
            t = tile(ORDER[i]).resize((tw, th), Image.LANCZOS)
            m = Image.new('L', (tw, th), 0)
            ImageDraw.Draw(m).rounded_rectangle((0, 0, tw - 1, th - 1), 18, fill=255)
            img.paste(t, (x, yy), m)
        else:
            d.rounded_rectangle((x, yy, x + tw - 1, yy + th - 1), 18, fill=PANEL)
            f = N("Black", 96)
            d.text((x + (tw - d.textlength("?", font=f)) / 2, yy + th / 2 - 62), "?", font=f, fill=SOFT)
    img.save(OUT / "05_outro.png", optimize=True)


cover(); stones(); rivals(); vote(); outro()
print("news ok")
