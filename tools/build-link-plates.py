"""Link Building — the wide plates: hero, engine, the three steps, the close.

Every plate is drawn for the exact container it lands in, so cover-cropping
never removes anything that carries meaning.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from dsl import *

OUT = 'outlb'
CARD = '#FBFBF9'

def save(s, name):
    n = s.save(f'{OUT}/{name}.svg')
    print(f'{n/1024:6.1f}KB  {name}.svg')

def page(cx, cy, w, h, stroke=INK, sw=3.4, bar=0.52, barcol=None, fill=CARD, r=14):
    o = [rect(cx - w/2, cy - h/2, w, h, fill=fill, r=r, stroke=stroke, sw=sw)]
    if bar:
        bw, bh = w * bar, max(12, h * 0.19)
        o.append(rect(cx - bw/2, cy - bh/2, bw, bh, fill=barcol or stroke, r=bh/2))
    return ''.join(o)

def pill(cx, cy, w, h, stroke, sw=3, barw=0.42, barcol=None, fill=CARD):
    return (rect(cx - w/2, cy - h/2, w, h, fill=fill, r=h/2, stroke=stroke, sw=sw) +
            rect(cx - w*barw/2, cy - 8, w*barw, 16, fill=barcol or stroke, r=8))

# ── hero · the authority a site has earned, in three states ──────────────────
def hero(level):
    """level 0 dormant · 1 building · 2 earned. Transparent ground: it floats on the page."""
    W, H = 1200, 800
    s = SVG(W, H, bg=None)
    site = (872, 400)
    pubs = [(196, 124), (196, 216), (196, 308), (196, 400), (196, 492), (196, 584), (196, 676)]
    live = [[3, 5], [1, 3, 5, 6], [0, 1, 2, 3, 4, 5, 6]][level]
    weight = {0: 7.5, 1: 5.4, 2: 3.4, 3: 4.6, 4: 3.0, 5: 5.0, 6: 2.6}
    best = 0
    for i, (pxx, pyy) in enumerate(pubs):
        if i not in live: continue
        on_best = (level == 2 and i == best)
        col = ACCENT if on_best else INK
        w = weight[i] if level == 2 else min(weight[i], 4.2)
        s.add(curve(pxx + 122, pyy, site[0] - 168, site[1], bow=0.09 if pyy < 400 else -0.09, stroke=col, sw=w))
    for i, (pxx, pyy) in enumerate(pubs):
        on = i in live
        col = ACCENT if (level == 2 and i == best) else (INK if on else HAIR2)
        s.add(pill(pxx, pyy, 244, 66, col, 3.4 if on else 2.8, 0.4))
    s.add(page(site[0], site[1], 336, 176, INK, 5, 0.44))
    return s

# ── engine · coverage becoming reach, then demand, then revenue ──────────────
def engine(stage):
    """One bench, three states, matching the +42% / 3.1x / +118% readouts."""
    W, H = 1200, 800
    M = 96
    s = SVG(W, H, bg=PAPER)
    tiles, chips = 16, 6
    tw = (W - 2*M - (tiles - 1) * 14) / tiles
    tops = []
    for i in range(tiles):
        x = M + i * (tw + 14)
        s.add(rect(x, 150, tw, 92, fill=CARD, r=10, stroke=INK, sw=2.8))
        s.add(rect(x + tw*0.22, 188, tw*0.56, 14, fill=INK, r=7))
        tops.append(x + tw/2)
    cw = (W - 2*M - (chips - 1) * 26) / chips
    mids = []
    for i in range(chips):
        x = M + i * (cw + 26)
        on = stage >= 1
        s.add(rect(x, 424, cw, 84, fill=CARD, r=42, stroke=INK if on else HAIR2, sw=3.4 if on else 2.8))
        s.add(rect(x + cw*0.26, 458, cw*0.48, 16, fill=INK if on else HAIR2, r=8))
        mids.append(x + cw/2)
    for i, tx in enumerate(tops):
        mx = mids[min(i * chips // tiles, chips - 1)]
        s.add(path(f'M{tx:.1f} 242 C{tx:.1f} 320 {mx:.1f} 346 {mx:.1f} 424',
                   stroke=INK if stage >= 1 else HAIR, sw=2.6 if stage >= 1 else 2))
    for mx in mids:
        s.add(path(f'M{mx:.1f} 508 C{mx:.1f} 570 600 588 600 630',
                   stroke=INK if stage >= 2 else HAIR, sw=2.6 if stage >= 2 else 2))
    s.add(rect(M, 630, W - 2*M, 68, fill=HAIR, r=34))
    if stage >= 2:
        s.add(rect(M, 630, (W - 2*M) * 0.78, 68, fill=ACCENT, r=34))
    return s

# ── the transition · one link, seen close ────────────────────────────────────
def macro():
    W, H = 1600, 1000
    s = SVG(W, H, bg=PAPER)
    cx, cy = 860, 480
    for i in range(7):
        s.add(line(140, 150 + i*118, 1460, 150 + i*118, HAIR, 2))
    s.add(circle(cx - 118, cy, 168, fill=PAPER, stroke=ACCENT, sw=30))
    s.add(circle(cx + 118, cy, 168, fill='none', stroke=ACCENT, sw=30))
    s.add(rect(cx - 44, cy - 15, 88, 30, fill=ACCENT, r=15))
    return s

# ── step 01 · the authority gap, found then measured ─────────────────────────
def gap(found):
    W, H = 1200, 800
    M = 96
    s = SVG(W, H, bg=PAPER)
    rows = [0.74, 0.52, 0.40, 0.63, 0.28, 0.46]
    bench = [0.86, 0.70, 0.78, 0.72, 0.66, 0.58]
    y = 132
    barw = W - 2*M - 150
    for i, (v, b) in enumerate(zip(rows, bench)):
        s.add(rect(M, y - 17, barw, 34, fill=HAIR, r=17))
        s.add(rect(M, y - 17, barw * v, 34, fill=INK, r=17))
        if found:
            bx = M + barw * b
            s.add(line(bx, y - 34, bx, y + 34, INK, 3.4))
            big = (b - v) > 0.3
            s.add(rect(M + barw * v + 8, y - 17, barw * (b - v) - 16, 34,
                       fill='none', r=17, stroke=ACCENT if big else HAIR2,
                       sw=3.4 if big else 2.6, dash='13 10'))
        y += 108
    return s

# ── step 02 · a field of raw material becoming one asset worth citing ────────
def field(stage):
    """Full-bleed and cropped hard on phones, so the asset stays in the centre band."""
    W, H = 1600, 900
    s = SVG(W, H, bg=PAPER)
    seed = 20260908
    def rnd():
        nonlocal seed
        seed = (1103515245 * seed + 12345) % 2147483648
        return seed / 2147483648
    marks = [(40 + rnd() * 1500, 40 + rnd() * 810) for _ in range(78)]
    for i, (x, yv) in enumerate(marks):
        if stage == 0:
            s.add(rect(x, yv, 26, 8, fill=HAIR2, r=4))
        elif stage == 1:
            tx = 120 + (i % 16) * 92
            ty = 700 - ((i * 37) % 9) * 34
            s.add(rect(tx, ty, 26, 8, fill=HAIR2, r=4, opacity=0.9))
        else:
            tx = 120 + (i % 16) * 92
            s.add(rect(tx, 742, 26, 8, fill=HAIR, r=4, opacity=0.7))
    ax, aw, ah = 800, 500, 350
    ay = 176
    if stage == 0:
        s.add(rect(ax - aw/2, ay, aw, ah, fill='none', r=20, stroke=HAIR2, sw=3, dash='16 12'))
    else:
        s.add(rect(ax - aw/2, ay, aw, ah, fill=CARD, r=20, stroke=ACCENT if stage == 2 else INK, sw=5 if stage == 2 else 3.6))
        s.add(rect(ax - aw/2 + 44, ay + 46, aw*0.62, 26, fill=INK, r=13))
        s.add(rect(ax - aw/2 + 44, ay + 90, aw*0.42, 26, fill=HAIR2, r=13))
        for k, hgt in enumerate([56, 96, 74, 128, 104]):
            s.add(rect(ax - aw/2 + 46 + k*88, ay + ah - 60 - hgt, 56, hgt, r=8,
                       fill=(ACCENT if (stage == 2 and k == 3) else INK)))
        s.add(line(ax - aw/2 + 40, ay + ah - 56, ax + aw/2 - 40, ay + ah - 56, INK, 3))
    return s

# ── step 03 · pitches sent, then links earned (dark section) ─────────────────
def earned(done):
    W, H = 1600, 900
    s = SVG(W, H, bg=GRAPH)
    cx, cy = 800, 450
    nodes = [(1.0, 300), (1.62, 330), (2.28, 300), (2.85, 320), (3.75, 330), (4.35, 300), (5.05, 325), (5.75, 300)]
    pts = [(cx + math.cos(a) * r * 1.55, cy + math.sin(a) * r) for a, r in nodes]
    for i, (px_, py_) in enumerate(pts):
        if done:
            w = [6.5, 3.0, 4.4, 2.6, 5.2, 2.8, 3.6, 2.4][i]
            col = ACCENT if i == 0 else ONDARK
            s.add(curve(px_, py_, cx, cy, bow=0.06, stroke=col, sw=w))
        else:
            s.add(curve(px_, py_, cx, cy, bow=0.06, stroke='#3A3A38', sw=2.6, dash='16 13'))
    for i, (px_, py_) in enumerate(pts):
        col = ACCENT if (done and i == 0) else (ONDARK if done else '#6E6E6A')
        s.add(pill(px_, py_, 210, 62, col, 3.2, 0.4, fill=DPANEL))
    s.add(page(cx, cy, 300, 152, ONDARK, 4.5, 0.44, fill=DPANEL))
    return s

# ── the close · the network, complete ────────────────────────────────────────
def final():
    """Narrow and tall: it clears the CTA scrim on desktop and survives the phone crop."""
    W, H = 1600, 1200
    s = SVG(W, H, bg=PAPER)
    cx, cy = 1090, 600
    RX, RY = 196, 344
    ring = [0.50, 1.16, 1.86, 2.55, 3.30, 3.98, 4.68, 5.42]
    pts = [(cx + math.cos(a) * RX, cy + math.sin(a) * RY) for a in ring]
    for i, (px_, py_) in enumerate(pts):
        w = [5.0, 2.6, 3.6, 2.4, 4.2, 2.4, 3.0, 2.2][i]
        s.add(curve(px_, py_, cx, cy, bow=0.05, stroke=ACCENT if i == 0 else HAIR2, sw=w))
    for i, (px_, py_) in enumerate(pts):
        best = i == 0
        s.add(pill(px_, py_, 178, 58, ACCENT if best else HAIR2, 3.0, 0.4,
                   barcol=ACCENT if best else HAIR2))
    s.add(page(cx, cy, 268, 140, INK3, 4, 0.44, barcol=INK3))
    return s

if __name__ == '__main__':
    for i in range(3): save(hero(i),   f'lb-hero-{i+1}')
    for i in range(3): save(engine(i), f'lb-engine-{i+1}')
    save(macro(), 'lb-macro')
    save(gap(False), 'lb-gap-1'); save(gap(True), 'lb-gap-2')
    for i in range(3): save(field(i), f'lb-field-{i+1}')
    save(earned(False), 'lb-earned-1'); save(earned(True), 'lb-earned-2')
    save(final(), 'lb-final')
