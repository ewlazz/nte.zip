"""신캐 요약 카드뉴스 v2 — 표지 + 성능 (엘림 시안)

- 색: 캐릭터 원화에서 추출 / 글꼴: Pretendard
- 인게임 아이콘: assets/icons/ 에 있으면 사용, 없으면 '아이콘 자리' 표시
  skill/<id>_basic.png, _ex.png, _ultimate.png, _support.png
  element/빛.png, rarity/S.png, arctype/고체.png, role/서포터.png
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
ICONS = ROOT / "assets" / "icons"
OUT = ROOT / "out" / "elyms"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1350
M = 76
FD = str(ROOT / "fonts" / "Pretendard-{}.otf")
_fc = {}


NUMD = str(ROOT / "fonts" / "InterDisplay-{}.ttf")


def N(w, s):
    """숫자 전용 글꼴 (Inter Display)"""
    if ("N", w, s) not in _fc:
        _fc[("N", w, s)] = ImageFont.truetype(NUMD.format(w), s)
    return _fc[("N", w, s)]


def F(w, s):
    if (w, s) not in _fc:
        _fc[(w, s)] = ImageFont.truetype(FD.format(w), s)
    return _fc[(w, s)]


PAPER = (239, 240, 246)
PANEL = (213, 217, 232)
INK = (36, 41, 66)
ACCENT = (80, 90, 130)
SOFT = (106, 128, 180)
LINE = (196, 201, 220)
VIVID = (92, 84, 214)

HANDLE = "@nte.zip"
TOTAL = 9


def tracked(d, xy, text, font, fill, track=0.0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + font.size * track
    return x


def icon(path_rel, size, label, disc=None):
    """인게임 아이콘을 불러온다. disc 색을 주면 게임 버튼처럼 원판 위에 얹는다(흰 실루엣 스킬 아이콘용)."""
    p = ICONS / path_rel
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    if p.exists():
        im = Image.open(p).convert("RGBA")
        inner = int(size * 0.8) if disc else size
        im = im.resize((inner, inner), Image.LANCZOS)
        if disc:
            d.ellipse([0, 0, size - 1, size - 1], fill=disc)
            d.ellipse([4, 4, size - 5, size - 5], outline=(255, 255, 255, 70), width=2)
        out.paste(im, ((size - inner) // 2, (size - inner) // 2), im)
        return out
    d.ellipse([0, 0, size - 1, size - 1], fill=ACCENT)
    f = F("Black", int(size * (0.42 if len(label) == 1 else 0.3)))
    tw = d.textlength(label, font=f)
    d.text(((size - tw) / 2, size * 0.5 - f.size * 0.62), label, font=f, fill=(255, 255, 255))
    return out


def glow_icon(path_rel, size):
    """강화 스킬 버튼: 게임 HUD처럼 보라빛 발광 원 + 반짝이 위에 실제 아이콘을 얹는다."""
    pad = int(size * 0.28)
    S = size + pad * 2
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([pad - size * 0.1, pad - size * 0.1, pad + size * 1.1, pad + size * 1.1], fill=200)
    halo = Image.new("RGBA", (S, S), (150, 110, 255, 0))
    halo.putalpha(mask.filter(ImageFilter.GaussianBlur(size * 0.12)))
    out.alpha_composite(halo)
    d = ImageDraw.Draw(out)
    # 원판: 가운데가 밝은 남보라 → 가장자리 진한 보라
    disc = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    dd = ImageDraw.Draw(disc)
    for r in range(size // 2, 0, -1):
        t = r / (size / 2)
        c = (int(70 + (40 - 70) * t), int(70 + (36 - 70) * t), int(190 + (120 - 190) * t), 255)
        dd.ellipse([size / 2 - r, size / 2 - r, size / 2 + r, size / 2 + r], fill=c)
    out.alpha_composite(disc, (pad, pad))
    d.ellipse([pad + 3, pad + 3, pad + size - 4, pad + size - 4], outline=(235, 230, 255, 235), width=max(2, size // 40))
    p = ICONS / path_rel
    if p.exists():
        im = Image.open(p).convert("RGBA")
        inner = int(size * 0.8)
        im = im.resize((inner, inner), Image.LANCZOS)
        out.alpha_composite(im, (pad + (size - inner) // 2, pad + (size - inner) // 2))
    # 반짝이
    import math
    for ang, dist, rr in [(35, 0.62, 0.055), (160, 0.6, 0.04), (250, 0.64, 0.05), (305, 0.58, 0.035), (95, 0.66, 0.03)]:
        cx = S / 2 + math.cos(math.radians(ang)) * size * dist
        cy = S / 2 + math.sin(math.radians(ang)) * size * dist
        r = size * rr
        d.polygon([(cx, cy - r * 2), (cx + r * 0.45, cy - r * 0.45), (cx + r * 2, cy), (cx + r * 0.45, cy + r * 0.45),
                   (cx, cy + r * 2), (cx - r * 0.45, cy + r * 0.45), (cx - r * 2, cy), (cx - r * 0.45, cy - r * 0.45)], fill=(250, 245, 255, 240))
    return out, pad


def portrait_circle(cid, size):
    card = Image.open(ROOT / "assets/characters/cards" / f"{cid}.webp").convert("RGBA")
    # 정규화 카드: 눈 = (50%, 25%). 얼굴이 원 안에 오도록 확대
    pw = int(size * 1.9)
    ph = int(pw * card.height / card.width)
    r = card.resize((pw, ph), Image.LANCZOS)
    tile = Image.new("RGBA", (size, size), PANEL + (255,))
    tile.paste(r, (size // 2 - pw // 2, int(size * 0.44 - ph * 0.25)), r)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    tile.putalpha(mask)
    return tile



def silhouette(img, x, y, h, color=(228, 231, 242)):
    """엘림 원화의 윤곽만 따서 배경에 옅게 깐다"""
    art = Image.open(ROOT / "assets/characters/elyms.webp").convert("RGBA")
    art = art.crop(art.getbbox())
    w = int(art.width * h / art.height)
    a = art.resize((w, h), Image.LANCZOS).getchannel("A")
    layer = Image.new("RGB", (w, h), color)
    img.paste(layer, (x, y), a)



def fade(im, left=0, right=0, top=0, bottom=0):
    """잘린 가장자리를 부드럽게 사라지게"""
    import numpy as np
    a = np.array(im.getchannel("A")).astype(float)
    h, w = a.shape
    for n, sl in [(left, lambda k: (slice(None), k)), (right, lambda k: (slice(None), w - 1 - k)),
                  (top, lambda k: (k, slice(None))), (bottom, lambda k: (h - 1 - k, slice(None)))]:
        for k in range(n):
            a[sl(k)] *= k / n
    im.putalpha(Image.fromarray(a.astype("uint8")))
    return im


def char_img(name, h=None, w=None):
    im = Image.open(ROOT / "assets/characters" / name).convert("RGBA")
    im = im.crop(im.getbbox())
    if h:
        im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
    elif w:
        im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    return im



def brand_bar(d, page, src):
    """머리띠 대신 하단 한 줄 (왼쪽 정렬): 브랜드 · 출처 · 쪽수"""
    yb = H - 66
    f1 = F("Bold", 22)
    d.text((M, yb), HANDLE, font=f1, fill=INK)
    x = M + d.textlength(HANDLE, font=f1) + 16
    fs = F("Medium", 19)
    if src:
        d.text((x, yb + 2), src, font=fs, fill=SOFT)
        x += d.textlength(src, font=fs) + 16
    d.text((x, yb + 1), f"{page:02d} / {TOTAL:02d}", font=F("SemiBold", 20), fill=SOFT)


def masthead(d, page):
    d.text((M, 64), "이환 신캐 요약", font=F("Bold", 28), fill=INK)
    d.text((M, 100), "NEVERNESS TO EVERNESS", font=F("SemiBold", 18), fill=SOFT)
    pg = f"{page:02d} / {TOTAL:02d}"
    f = F("SemiBold", 24)
    d.text((W - M - d.textlength(pg, font=f), 70), pg, font=f, fill=SOFT)


def footer(d, text, x1=W - M):
    f = F("Medium", 20)
    d.text((M, H - 62), text, font=f, fill=SOFT)
    if HANDLE:
        d.text((x1 - d.textlength(HANDLE, font=F("SemiBold", 24)), H - 66), HANDLE, font=F("SemiBold", 24), fill=SOFT)


# ───────────────── 1. 표지 ─────────────────
def cover():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    PX = 560
    d.rectangle([PX, 0, W, H], fill=PANEL)
    art = Image.open(ROOT / "assets/characters/elyms.webp").convert("RGBA")
    s = 1.92
    art = art.resize((int(art.width * s), int(art.height * s)), Image.LANCZOS)
    img.paste(art, (250, 150 - int(50 * s)), art)
    d = ImageDraw.Draw(img)

    y = 236
    d.text((M, y), "1.5 업데이트", font=F("SemiBold", 30), fill=ACCENT)
    y += 54
    tracked(d, (M - 6, y), "엘림", F("Black", 196), INK, track=-0.05)
    y += 228
    tracked(d, (M, y), "ELYMS", F("Bold", 26), SOFT, track=0.32)
    y += 66
    d.line([M, y, M + 300, y], fill=INK, width=3)
    y += 30
    # 등급·속성·아크 타입·역할 → 인게임 아이콘 + 짧은 글자
    d.text((M, y + 4), "S급", font=F("Black", 32), fill=INK)
    x = M + int(d.textlength("S급", font=F("Black", 32))) + 26
    for rel, ph, label in [("element/빛.png", "빛", "빛"), ("arctype/고체.png", "고", "고체"), ("role/버프형.png", "버", "버프형")]:
        ic = icon(rel, 42, ph)
        img.paste(ic, (int(x), y + 2), ic)
        x += 50
        d.text((x, y + 6), label, font=F("Bold", 29), fill=INK)
        x += int(d.textlength(label, font=F("Bold", 29))) + 22
    y += 76
    for line in ["출전 캐릭터가", "울트 에너지를 얻으면", "파티 전체 빛속성 피해 증가"]:
        d.text((M, y), line, font=F("Medium", 31), fill=ACCENT)
        y += 46
    brand_bar(d, 1, "NEVERNESS TO EVERNESS")
    img.save(OUT / "01_cover.png", optimize=True)


# ───────────────── 2. 성능 ─────────────────
def chain(img, d, x, y, items, size, gap, color):
    """작은 아이콘을 화살표로 이어 붙인다. items: (아이콘 경로, 자리표시 글자, 아래 글자)"""
    for i, (rel, ph, cap) in enumerate(items):
        if rel == "TEXT":
            f = F("Bold", int(size * 0.34))
            w = int(d.textlength(ph, font=f)) + 24
            d.rounded_rectangle([x, y + size * 0.18, x + w, y + size * 0.82], radius=int(size * 0.32), outline=color, width=2)
            d.text((x + 12, y + size * 0.5 - f.size * 0.62), ph, font=f, fill=color)
            cx, x = x + w / 2, x + w
        elif rel.startswith("GLOW:"):
            g, pad = glow_icon(rel[5:], size)
            img.paste(g, (int(x) - pad, y - pad), g)
            cx, x = x + size / 2, x + size
        else:
            ic = icon(rel, size, ph, disc=INK)
            img.paste(ic, (int(x), y), ic)
            cx, x = x + size / 2, x + size
        if cap:
            f = F("SemiBold", 20)
            d.text((cx - d.textlength(cap, font=f) / 2, y + size + 8), cap, font=f, fill=ACCENT)
        if i < len(items) - 1:
            ay = y + size / 2
            d.line([x + 8, ay, x + gap - 12, ay], fill=SOFT, width=3)
            d.polygon([(x + gap - 12, ay - 6), (x + gap - 2, ay), (x + gap - 12, ay + 6)], fill=SOFT)
            x += gap
    return x


def performance():
    """02 운영 — 흐름만 크게"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    sk = fade(char_img("elyms_skin2_top_rgba.png", h=350), left=110, right=30)
    img.paste(sk, (W - sk.width + 20, 472 - sk.height + 8), sk)

    y = 170
    d.text((M, y), "운영", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "E, E, Q 누르고", F("Black", 84), INK, track=-0.04)
    y += 104
    tracked(d, (M - 4, y), "바로 교대", F("Black", 84), INK, track=-0.04)
    y += 150

    # ── 기본 흐름 (세로 대신 가로, 크게) ──
    PH = 360
    d.rectangle([0, y, W, y + PH], fill=PANEL)
    S = 150
    steps = [("skill/elyms_ex.png", "E", "사이클 즉시 최대"),
             ("GLOW:skill/elyms_ex2.png", "강화 E", "E가 빛나면 한 번 더"),
             ("skill/elyms_ultimate.png", "Q", "파티 버프"),
             ("PORTRAIT:shinku", "교대", "필드 밖 협동 공격")]
    col = (W - 2 * M) // 4
    for i, (rel, key, cap) in enumerate(steps):
        cx = M + col * i + col // 2
        top = y + 42
        if rel.startswith("GLOW:"):
            g, pad = glow_icon(rel[5:], S)
            img.paste(g, (cx - S // 2 - pad, top - pad), g)
        elif rel.startswith("PORTRAIT:"):
            pc = portrait_circle(rel[9:], S)
            img.paste(pc, (cx - S // 2, top), pc)
        else:
            ic = icon(rel, S, key, disc=INK)
            img.paste(ic, (cx - S // 2, top), ic)
        if i < 3:
            ax = M + col * (i + 1)
            d.line([ax - 14, top + S / 2, ax + 6, top + S / 2], fill=ACCENT, width=4)
            d.polygon([(ax + 6, top + S / 2 - 9), (ax + 20, top + S / 2), (ax + 6, top + S / 2 + 9)], fill=ACCENT)
        f1 = F("Black", 34)
        d.text((cx - d.textlength(key, font=f1) / 2, top + S + 40), key, font=f1, fill=INK)
        f2 = F("Medium", 21)
        d.text((cx - d.textlength(cap, font=f2) / 2, top + S + 90), cap, font=f2, fill=ACCENT)
    y += PH + 70

    # ── 딜까지 챙길 때 ──
    d.text((M, y), "딜까지 챙길 때", font=F("Black", 36), fill=INK)
    y += 70
    chain(img, d, M, y, [
        ("skill/elyms_ex.png", "E", "E"), ("GLOW:skill/elyms_ex2.png", "E", "강화 E"),
        ("TEXT", "평타 3", ""), ("GLOW:skill/elyms_ex3.png", "E", "강화 E"), ("skill/elyms_ultimate.png", "Q", "Q"),
    ], 92, 46, INK)
    y += 160
    d.text((M, y), "신호를 끝까지 올린 뒤 Q를 쓰면 Q·협동 공격이 더 강해져요", font=F("Medium", 24), fill=ACCENT)
    y += 40
    d.text((M, y), "3돌부터는 E E E Q로 짧아져요", font=F("Medium", 24), fill=SOFT)

    brand_bar(d, 2, "한·중 커뮤니티 공략 종합 · 2026.11")
    img.save(OUT / "02_rotation.png", optimize=True)


def big_number(img, d, x, y, prefix, num, unit, color):
    """'최대' + '30' + '%' 를 숫자 글꼴로 크게. 반환: 오른쪽 끝 x"""
    f = N("Black", 132)
    fu = N("Bold", 70)
    top = y + 30
    # 숫자 실제 윗선/아랫선 기준으로 접두어와 % 위치를 맞춘다
    bx0, by0, bx1, by1 = d.textbbox((x, top), num, font=f)
    if prefix:
        d.text((x + 4, by0 - 40), prefix, font=F("Bold", 26), fill=SOFT)
    d.text((x, top), num, font=f, fill=color)
    ux0, uy0, ux1, uy1 = d.textbbox((0, 0), unit, font=fu)
    d.text((bx1 + 8 - ux0, by1 - uy1), unit, font=fu, fill=color)
    return bx1 + 8 + (ux1 - ux0)


def buffs():
    """03 파티 버프 + 스킬 육성"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    art = Image.open(ROOT / "assets/characters/elyms.webp").convert("RGBA")
    art = art.crop(art.getbbox())
    art = art.crop((0, 0, art.width, int(art.height * 0.42)))
    art = fade(art.resize((int(art.width * 300 / art.height), 300), Image.LANCZOS), bottom=70)
    img.paste(art, (W - art.width + 40, 108), art)

    y = 170
    d.text((M, y), "파티 버프", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "엘림이 들어가면", F("Black", 84), INK, track=-0.04)
    y += 150

    rows = [
        ("약", "+35", "%", "신쿠 파티 딜", "제로 자리에 엘림을 넣었을 때"),
        ("최대", "+30", "%", "빛속성 피해", "패시브 · 차지 파티 전원"),
        ("1돌", "+20", "%", "치명 피해", "파티 전원 · 생존 중 상시"),
    ]
    RH = 196
    for i, (pre, num, unit, what, how) in enumerate(rows):
        if i:
            d.line([M, y - 18, W - M, y - 18], fill=LINE, width=2)
        big_number(img, d, M, y, pre, num, unit, VIVID)
        tx = M + 470
        d.text((tx, y + 66), what, font=F("Black", 40), fill=INK)
        d.text((tx, y + 122), how, font=F("Medium", 24), fill=SOFT)
        y += RH

    # ── 스킬 육성 순서 (한 줄로) ──
    y += 24
    d.rectangle([0, y, W, H], fill=PANEL)
    y += 56
    d.text((M, y), "스킬 육성", font=F("Black", 34), fill=INK)
    d.text((M + 190, y + 8), "Q · E 먼저, 패시브는 모두 개방", font=F("Medium", 24), fill=ACCENT)
    y += 84
    items = [("skill/elyms_ultimate.png", "Q", "Q", INK), ("skill/elyms_ex.png", "E", "E", INK),
             ("skill/elyms_basic.png", "평", "평타", ACCENT), ("skill/elyms_support.png", "서", "서포트", ACCENT)]
    x = M
    for i, (rel, ph, lab, col) in enumerate(items):
        sz = 96 if i < 2 else 80
        ic = icon(rel, sz, ph, disc=col)
        img.paste(ic, (int(x), y + (0 if i < 2 else 8)), ic)
        f = F("Black", 30) if i < 2 else F("Bold", 26)
        cy = y + (0 if i < 2 else 8) + sz / 2
        lb = d.textbbox((0, 0), lab, font=f)
        d.text((x + sz + 14, cy - (lb[1] + lb[3]) / 2), lab, font=f, fill=INK if i < 2 else ACCENT)
        x += sz + 14 + d.textlength(lab, font=f) + 26
        if i < 3:
            ab = d.textbbox((0, 0), "›", font=F("Bold", 44))
            d.text((x - 8, y + 48 - (ab[1] + ab[3]) / 2), "›", font=F("Bold", 44), fill=SOFT)
            x += 34

    brand_bar(d, 3, "한·중 커뮤니티 공략 종합 · 2026.11")
    img.save(OUT / "03_buffs.png", optimize=True)


def arc_img(rel, size):
    im = Image.open(ROOT / "assets" / rel).convert("RGBA")
    return im.resize((size, size), Image.LANCZOS)


def right_number(d, xr, ybase, num, unit, color, fn=84, fu=44):
    """오른쪽 끝(xr)에 맞춰 숫자+% 를 같은 밑선으로"""
    f, g = N("Black", fn), N("Bold", fu)
    ub = d.textbbox((0, 0), unit, font=g)
    nb = d.textbbox((0, 0), num, font=f)
    uw = ub[2] - ub[0]
    nx = xr - uw - 6 - (nb[2] - nb[0]) - nb[0]
    d.text((nx, ybase - nb[3]), num, font=f, fill=color)
    d.text((xr - uw - ub[0], ybase - ub[3]), unit, font=g, fill=color)


def arcs():
    """04 아크 — 신쿠 파티 1사이클 딜 기대값 (엘림 전무 = 100)"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = 170
    d.text((M, y), "아크", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "전무 없으면?", F("Black", 84), INK, track=-0.04)
    y += 128
    d.text((M, y), "신쿠 파티 1사이클 딜 기대값 · 엘림 전무를 100으로 놓고 비교", font=F("Medium", 24), fill=SOFT)
    y += 66

    rows = [
        ("arcs/echoes_on_hold.webp", "연결음이 흐르는 동안", "엘림 전용", "100", VIVID, True),
        ("arcs/marching_beyond_time_5_fork_time.png", "시간 밖으로의 행진", "호토리 전용 · 엘림 딜↑ 신쿠 딜↓, 손이 많이 감", "86.0", INK, False),
        ("arcs/blow_up_the_crowd_5_fork_bitgame.png", "폭발 현장", "전무가 없을 때 가장 많이 추천", "84.5", INK, True),
        ("arcs/fluff_of_fearlessness_5_fork_blastcandy.png", "용맹의 솜뭉치", "배틀패스 아크", "82.2", ACCENT, False),
        ("icons/arc/worldrain.png", "세상을 뒤흔든 비", "제로 전용", "81.8", ACCENT, False),
    ]
    RH, S = 132, 116
    for i, (rel, name, note, num, col, pick) in enumerate(rows):
        if i:
            d.line([M, y - 8, W - M, y - 8], fill=LINE, width=2)
        a = arc_img(rel, S)
        img.paste(a, (M - 6, y + (RH - S) // 2 - 6), a)
        tx = M + S + 22
        d.text((tx, y + 22), name, font=F("Black", 34), fill=INK)
        if pick:
            nw = d.textlength(name, font=F("Black", 34))
            d.text((tx + nw + 14, y + 32), "추천", font=F("Bold", 22), fill=VIVID)
        fn = F("Medium", 21)
        # 노트가 길면 두 줄
        maxw = W - M - 230 - tx
        if d.textlength(note, font=fn) > maxw and " · " in note:
            a1, a2 = note.split(" · ", 1)
            d.text((tx, y + 70), a1, font=fn, fill=SOFT)
            d.text((tx, y + 98), a2, font=fn, fill=SOFT)
        else:
            d.text((tx, y + 72), note, font=fn, fill=SOFT)
        right_number(d, W - M, y + 92, num, "%", col)
        y += RH

    # ── 결론 ──
    y += 14
    d.rectangle([0, y, W, H], fill=PANEL)
    y += 44
    d.text((M, y), "보상만 받을 거면", font=F("Medium", 26), fill=ACCENT)
    d.text((M + 230, y - 4), "전무 없어도 충분", font=F("Black", 32), fill=INK)
    y += 52
    d.text((M, y), "점수를 노린다면", font=F("Medium", 26), fill=ACCENT)
    d.text((M + 230, y - 4), "전무 추천", font=F("Black", 32), fill=INK)

    ch = char_img("elyms_chibi_hq.png", h=270)
    img.paste(ch, (W - ch.width + 4, H - ch.height), ch)
    brand_bar(d, 4, "한·중 커뮤니티 공략 종합 · 2026.11")
    img.save(OUT / "04_arcs.png", optimize=True)


def cart_row(img, d, y, rel, name, pick, lines, S=150):
    a = Image.open(ROOT / "assets/cartridges" / rel).convert("RGBA").resize((S, S), Image.LANCZOS)
    img.paste(a, (M - 14, y - 6), a)
    tx = M + S + 14
    d.text((tx, y + 6), name, font=F("Black", 42), fill=INK)
    if pick:
        nw = d.textlength(name, font=F("Black", 42))
        d.text((tx + nw + 16, y + 20), pick, font=F("Bold", 24), fill=VIVID)
    yy = y + 76
    for k, v in lines:
        d.text((tx, yy), k, font=F("Bold", 24), fill=SOFT)
        d.text((tx + 82, yy), v, font=F("Medium", 26), fill=INK)
        yy += 42
    return yy


def cartridges():
    """05 카트리지 + 드라이브"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    sk = fade(char_img("elyms_skin3_top_rgba.png", h=380), bottom=80, left=120)
    img.paste(sk, (W - sk.width + 40, 150), sk)

    y = 170
    d.text((M, y), "카트리지 · 드라이브", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "잃어버린 빛 4세트", F("Black", 84), INK, track=-0.04)
    y += 160

    cart_row(img, d, y, "lost_radiance_5_cosmos_orange.png", "잃어버린 빛", "",
             [("2세트", "빛속성 피해 +10%"), ("4세트", "Q 후 20초간 방어력 25% 무시")])
    y += 200
    d.line([M, y, W - M, y], fill=LINE, width=2)
    y += 40

    # ── 치명 확률: 이미 61% ──
    d.text((M, y), "Ⅲ형 드라이브 4개면", font=F("Black", 36), fill=INK)
    y += 40
    f = N("Black", 150); fu = N("Bold", 76)
    top = y
    bb = d.textbbox((M, top), "61", font=f)
    d.text((M - 4, top), "61", font=f, fill=VIVID)
    ub = d.textbbox((0, 0), "%", font=fu)
    d.text((bb[2] + 6 - ub[0], bb[3] - ub[3]), "%", font=fu, fill=VIVID)
    tx = M + 400
    d.text((tx, bb[1] + 14), "치명 확률 기본 확보", font=F("Black", 40), fill=INK)
    d.text((tx, bb[1] + 72), "전무 기준 · 부옵션 없이도", font=F("Medium", 24), fill=SOFT)
    y = bb[3] + 40

    # 막대: 기본 5 + 전무 24 + Ⅲ형 32 (100% 기준)
    BW = W - 2 * M
    segs = [(5, "기본", (150, 160, 200)), (24, "전무", SOFT), (32, "Ⅲ형 ×4", VIVID)]
    x = M
    BH = 26
    d.rectangle([M, y, M + BW, y + BH], fill=PANEL)
    for v, lab, col in segs:
        w = BW * v / 100
        d.rectangle([x, y, x + w - 3, y + BH], fill=col)
        fl = F("Bold", 22)
        t = f"{lab} {v}"
        tw = d.textlength(t, font=fl)
        lx = x + w / 2 - tw / 2 if w > tw else x
        d.text((max(M, lx), y + BH + 12), t, font=fl, fill=col if col != (150, 160, 200) else ACCENT)
        x += w
    d.text((M + BW - d.textlength("100", font=F("Medium", 20)), y + BH + 14), "100", font=F("Medium", 20), fill=SOFT)
    y += BH + 70

    # ── 옵션 ──
    d.rectangle([0, y, W, H], fill=PANEL)
    y += 46
    d.text((M, y + 4), "메인 옵션", font=F("Medium", 26), fill=ACCENT)
    d.text((M + 170, y), "치명 피해 · 빛속성 피해", font=F("Black", 34), fill=INK)
    d.text((M + 170, y + 50), "치명 확률 메인은 넘쳐서 비추천", font=F("Medium", 22), fill=SOFT)
    y += 110
    d.text((M, y + 4), "부옵션", font=F("Medium", 26), fill=ACCENT)
    d.text((M + 170, y), "치명 확률 · 치명 피해 › 피해% › 공격력%", font=F("Black", 30), fill=INK)

    brand_bar(d, 5, "한·중 커뮤니티 공략 종합 · 2026.11")
    img.save(OUT / "05_cartridges.png", optimize=True)


def awaken():
    """06 각성 순서"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    art = Image.open(ROOT / "assets/characters/elyms.webp").convert("RGBA")
    art = art.crop(art.getbbox())
    ah = 960
    art = art.resize((int(art.width * ah / art.height), ah), Image.LANCZOS)
    img.paste(art, (W - art.width + 70, 150), art)

    y = 170
    d.text((M, y), "각성", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "1돌이면 4번부터", F("Black", 84), INK, track=-0.04)
    y += 150

    rows = [
        ("1돌", "4", "파티 치명 피해 +20%", "엘림이 살아 있으면 항상"),
        ("2돌", "1", "파티 치명 피해 +10%씩", "Q 전에 강화 E로 환각을 쓸 때마다"),
        ("3돌", "3", "환각 3개 추가 획득", "1번과 합쳐 최대 +40%"),
        ("4돌", "6", "엘림 협동 공격 +25%씩", "쓴 환각 1개마다"),
        ("5돌", "2", "Q 피해 +30%", "Q 배율 증가"),
        ("6돌", "5", "기본 E 피해 +100%", "전투 시작부터 사이클 100"),
    ]
    RH, S = 116, 88
    for i, (st, num, what, how) in enumerate(rows):
        if i:
            d.line([M, y - 10, M + 560, y - 10], fill=LINE, width=2)
        first = i == 0
        ic = icon(f"awaken/{num}.png", S, num, disc=VIVID if first else INK)
        img.paste(ic, (M, y + 2), ic)
        tx = M + S + 30
        tag = f"{st}  ·  {num}번"
        d.text((tx, y + 2), tag, font=F("Bold", 21), fill=VIVID if first else SOFT)
        d.text((tx, y + 30), what, font=F("Black", 34), fill=INK)
        d.text((tx, y + 74), how, font=F("Medium", 21), fill=SOFT)
        y += RH

    # ── 누적 공명 ──
    y += 4
    d.rectangle([0, y, W, H], fill=PANEL)
    y += 40
    for lab, txt in [("3돌 공명", "스킬 레벨 +1 · E 한 번에 강한 신호 → E E E Q"),
                     ("6돌 공명", "파티 전체 모든 속성 저항 12% 무시")]:
        d.text((M, y + 3), lab, font=F("Bold", 24), fill=ACCENT)
        d.text((M + 140, y), txt, font=F("Black", 27), fill=INK)
        y += 48
    ch = Image.open(ROOT / "assets/characters/elyms_chibi_hq.png").convert("RGBA")
    chh = 300
    ch = ch.resize((int(ch.width * chh / ch.height), chh), Image.LANCZOS)
    img.paste(ch, (W - ch.width + 4, H - chh), ch)

    brand_bar(d, 6, "한·중 커뮤니티 공략 종합 · 2026.11")
    img.save(OUT / "06_awaken.png", optimize=True)


def ring_portrait(img, cid, size, x, y, hi=False):
    pc = portrait_circle(cid, size)
    img.paste(pc, (int(x), int(y)), pc)
    if hi:
        ImageDraw.Draw(img).ellipse([x - 5, y - 5, x + size + 4, y + size + 4], outline=VIVID, width=5)


NAMES = {"shinku": "신쿠", "akane": "아카네 린", "elyms": "엘림", "iroi": "일로이",
         "hathor": "하토르", "blackbird": "레이븐"}


def party():
    """07 파티"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    sk = fade(char_img("elyms_skin2_top_rgba.png", h=250), left=100, bottom=70)
    img.paste(sk, (W - sk.width + 30, 112), sk)

    y = 170
    d.text((M, y), "파티", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "엘림은 신쿠 파티로", F("Black", 84), INK, track=-0.04)
    y += 162

    # ── 기본 조합 ──
    S = 164
    col = (W - 2 * M) // 4
    main = [("shinku", "주력 딜러"), ("akane", "레모라"), ("elyms", "빛 버프"), ("iroi", "블라썸")]
    for i, (cid, role) in enumerate(main):
        cx = M + col * i + col // 2
        ring_portrait(img, cid, S, cx - S // 2, y, hi=cid == "elyms")
        nm = NAMES[cid]
        f1 = F("Black", 32)
        d.text((cx - d.textlength(nm, font=f1) / 2, y + S + 18), nm, font=f1, fill=INK)
        f2 = F("Medium", 22)
        d.text((cx - d.textlength(role, font=f2) / 2, y + S + 62), role, font=f2, fill=VIVID if cid == "elyms" else SOFT)
    y += S + 140

    # ── 운영 순서 ──
    d.text((M, y), "운영", font=F("Bold", 24), fill=ACCENT)
    x = M + 82
    steps = [("akane", "E Q"), ("elyms", "E E Q"), ("iroi", "E Q"), ("shinku", "Q 후 딜")]
    s2 = 56
    for i, (cid, key) in enumerate(steps):
        ring_portrait(img, cid, s2, x, y - 14, hi=cid == "elyms")
        x += s2 + 16
        fk = F("Black", 26)
        d.text((x, y - 2), key, font=fk, fill=INK)
        x += d.textlength(key, font=fk) + 14
        if i < 3:
            d.text((x, y - 4), "›", font=F("Bold", 32), fill=SOFT)
            x += 30
    y += 70
    d.line([M, y, W - M, y], fill=LINE, width=2)
    y += 34

    # ── 대체 조합 ──
    alts = [("린이 없다면", ["shinku", "hathor", "elyms", "iroi"], "하토르로 레모라 준비"),
            ("린이 주력이라면", ["akane", "blackbird", "elyms", "iroi"], "사키리 자리에 엘림")]
    s3 = 84
    for lab, ids, note in alts:
        d.text((M, y + 6), lab, font=F("Black", 30), fill=INK)
        d.text((M, y + 52), note, font=F("Medium", 21), fill=SOFT)
        x = M + 330
        for cid in ids:
            ring_portrait(img, cid, s3, x, y, hi=cid == "elyms")
            nm = NAMES[cid]
            fn = F("Bold", 19)
            d.text((x + s3 / 2 - d.textlength(nm, font=fn) / 2, y + s3 + 8), nm, font=fn, fill=ACCENT)
            x += s3 + 66
        y += s3 + 58

    # ── 팁 ──
    y += 6
    d.rectangle([0, y, W, H], fill=PANEL)
    y += 40
    d.text((M, y), "엘림 사이클 강도를 일로이보다 높게", font=F("Black", 30), fill=INK)
    d.text((M, y + 48), "그래야 블라썸 반응이 엘림 기준으로 터져요", font=F("Medium", 23), fill=ACCENT)

    brand_bar(d, 7, "한·중 커뮤니티 공략 종합 · 2026.11")
    img.save(OUT / "07_party.png", optimize=True)


def materials():
    """08 육성 재료"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    art = fade(char_img("elyms.webp", h=900), bottom=160)
    img.paste(art, (W - art.width + 70, 210), art)

    y = 170
    d.text((M, y), "육성 재료", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "Lv.80까지", F("Black", 84), INK, track=-0.04)
    y += 128
    d.text((M, y), "돌파 + 스킬 4종 Lv.10 + 패시브 개방 합계", font=F("Medium", 23), fill=SOFT)
    y += 70

    sections = [
        ("보스 재료", "", [("sea_tear", "86", "바다의 눈물", "", "이상 추적"), ("hollow_seed", "35", "속 빈 꽃씨", "", "이상 순례")]),
        ("실루엣", "이상 드롭 · 돌파와 스킬 공용",
         [("sil1", "57", "빛바랜", " 실루엣", ""), ("sil2", "58", "초점 잃은", " 실루엣", ""), ("sil3", "79", "어두운", " 실루엣", "")]),
        ("스킬 재료", "후디니의 계략 무대",
         [("skill1", "40", "어린새의 희망", "", ""), ("skill2", "42", "비둘기의 날갯짓", "", ""), ("skill3", "65", "올리브 가지", "", "")]),
    ]
    XR = 572          # 숫자 오른쪽 끝 (엘림과 겹치지 않게)
    RH, S = 74, 60
    fN = N("Black", 50)
    for lab, sub, items in sections:
        d.text((M, y), lab, font=F("Black", 30), fill=INK)
        if sub:
            lw = d.textlength(lab, font=F("Black", 30))
            d.text((M + lw + 16, y + 8), sub, font=F("Medium", 21), fill=SOFT)
        y += 50
        for i, (ic, num, name, tail, src) in enumerate(items):
            im = Image.open(ICONS / "mat" / f"{ic}.png").convert("RGBA").resize((S, S), Image.LANCZOS)
            img.paste(im, (M - 2, y + (RH - S) // 2 - 4), im)
            tx = M + S + 20
            cy = y + RH / 2 - 4
            fn = F("Bold", 29)
            bb = d.textbbox((0, 0), name, font=fn)
            d.text((tx, cy - (bb[1] + bb[3]) / 2), name, font=fn, fill=INK)
            tx2 = tx + d.textlength(name, font=fn)
            if tail:
                d.text((tx2, cy - (bb[1] + bb[3]) / 2 + 1), tail, font=F("Medium", 27), fill=SOFT)
            if src:
                fs = F("Medium", 20)
                sb = d.textbbox((0, 0), src, font=fs)
                d.text((tx2 + 14, cy - (sb[1] + sb[3]) / 2 + 2), src, font=fs, fill=SOFT)
            nb = d.textbbox((0, 0), num, font=fN)
            d.text((XR - nb[2], cy - (nb[1] + nb[3]) / 2), num, font=fN, fill=INK)
            if i < len(items) - 1:
                d.line([M, y + RH - 2, XR, y + RH - 2], fill=LINE, width=1)
            y += RH
        y += 26

    brand_bar(d, 8, "인게임 수치 기준 · 2026.11")
    img.save(OUT / "08_materials.png", optimize=True)


def outro():
    """09 마무리: 팔로우 · 좋아요"""
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 150
    d.text((M, y), "엘림 요약 끝", font=F("Bold", 30), fill=ACCENT)
    y += 48
    tracked(d, (M - 4, y), "팔로우하고", F("Black", 84), INK, track=-0.04)
    y += 104
    tracked(d, (M - 4, y), "다음 신캐도 받아보기", F("Black", 84), INK, track=-0.04)
    y += 150
    d.text((M, y), "도움이 됐다면 좋아요 한 번 눌러주세요", font=F("Medium", 30), fill=ACCENT)
    y += 90
    tracked(d, (M - 2, y), "@nte.zip", N("Black", 96), VIVID, track=-0.02)

    el = fade(char_img("elyms_chibi_hq.png", h=500), bottom=60, right=45)
    img.paste(el, (40, H - el.height), el)
    la = fade(char_img("lacrimosa_chibi.png", h=470), bottom=60)
    img.paste(la, (W - la.width + 20, H - la.height), la)
    img.save(OUT / "09_outro.png", optimize=True)



if __name__ == "__main__":
    cover()
    performance()
    buffs()
    arcs()
    cartridges()
    awaken()
    party()
    materials()
    outro()
    print("ok")
