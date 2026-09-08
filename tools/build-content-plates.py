"""Content Creation — the wide plates: hero, engine, the three steps, the close."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from dsl import *

OUT = 'outcc'
CARD = '#FBFBF9'

def save(s, name):
    n = s.save(f'{OUT}/{name}.svg')
    print(f'{n/1024:6.1f}KB  {name}.svg')

def article(cx, cy, w, h, stroke=INK, sw=3.4, lines=3, head=0.62, fill=CARD, r=14, headcol=None):
    o = [rect(cx-w/2, cy-h/2, w, h, fill=fill, r=r, stroke=stroke, sw=sw)]
    ix, iw = cx - w/2 + w*0.11, w*0.78
    o.append(rect(ix, cy-h/2 + h*0.15, iw*head, max(13, h*0.085), fill=headcol or stroke, r=h*0.042))
    for i in range(lines):
        o.append(rect(ix, cy-h/2 + h*0.36 + i*h*0.155, iw*[0.94, 0.78, 0.58][i % 3],
                      max(9, h*0.052), fill=HAIR2, r=h*0.026))
    return ''.join(o)

# ── hero · content that accumulates ──────────────────────────────────────────
def hero(level):
    """0 published · 1 earning · 2 compounding. The staircase never moves; it lights up."""
    W, H = 1200, 800
    s = SVG(W, H, bg=None)
    xs = [170, 390, 610, 830, 1050]
    hs = [94, 132, 158, 196, 240]
    base = 700
    for i, x in enumerate(xs):
        lit = level >= 1
        s.add(article(x, 218, 186, 236, INK if lit else HAIR2, 3.4 if lit else 2.8, 2, 0.6))
    for i, (x, hgt) in enumerate(zip(xs, hs)):
        last = i == len(xs) - 1
        col = HAIR if level == 0 else (ACCENT if (level == 2 and last) else INK)
        s.add(rect(x-52, base-hgt, 104, hgt, fill=col, r=16))
    if level == 2:
        pts = [(x, base-hgt-30) for x, hgt in zip(xs, hs)]
        s.add(path('M' + ' L'.join(f'{a:.0f} {b:.0f}' for a, b in pts), stroke=ACCENT, sw=6))
        s.add(circle(pts[-1][0], pts[-1][1], 19, fill=ACCENT))
    s.add(line(96, base + 26, 1104, base + 26, INK, 3.4))
    return s

# ── engine · reach becoming demand becoming revenue ──────────────────────────
def engine(active):
    """Three bands, constant. Only the accent marker moves, so states crossfade clean."""
    W, H = 1200, 800
    s = SVG(W, H, bg=PAPER)
    bands = [(96, 1104, 12), (270, 930, 7), (410, 790, 3)]
    ys = [172, 348, 524]
    bh = 132
    for bi, ((x0, x1, n), y) in enumerate(zip(bands, ys)):
        if bi:
            px0, px1, _ = bands[bi-1]
            s.add(path(f'M{px0:.0f} {ys[bi-1]+bh:.0f} L{x0:.0f} {y:.0f}', stroke=HAIR, sw=2.6))
            s.add(path(f'M{px1:.0f} {ys[bi-1]+bh:.0f} L{x1:.0f} {y:.0f}', stroke=HAIR, sw=2.6))
        s.add(rect(x0, y, x1-x0, bh, fill=CARD, r=20, stroke=INK, sw=3.4))
        tw = 52
        span = (x1-x0) - 56
        step = span / n
        for k in range(n):
            s.add(rect(x0 + 28 + k*step + (step-tw)/2, y + bh/2 - 26, tw, 52, fill=INK, r=10))
    x0, x1, _ = bands[active]
    y = ys[active]
    s.add(rect(x0, y, x1-x0, bh, fill='none', r=20, stroke=ACCENT, sw=6))
    s.add(rect(x0 + (x1-x0)/2 - 78, y + bh + 22, 156, 14, fill=ACCENT, r=7))
    return s

# ── the transition · a headline being set, seen close ────────────────────────
def macro():
    W, H = 1600, 1000
    s = SVG(W, H, bg=PAPER)
    for y, w, col in [(250, 1180, HAIR), (430, 1010, ACCENT), (610, 1120, HAIR), (790, 720, HAIR)]:
        s.add(rect(240, y, w, 96, fill=col, r=48))
    return s

# ── step 01 · demand mapped before a word is written ─────────────────────────
def demand(found):
    W, H = 1200, 800
    s = SVG(W, H, bg=PAPER)
    s.add(article(286, 400, 340, 452, INK, 3.6, 3, 0.6))
    rows = [0.94, 0.80, 0.66, 0.55, 0.42, 0.30]
    x0, x1 = 560, 1104
    y = 176
    for i, v in enumerate(rows):
        if found:
            col = ACCENT if i == 0 else INK
            s.add(rect(x0, y - 20, x1-x0, 40, fill=HAIR, r=20))
            s.add(rect(x0, y - 20, (x1-x0)*v, 40, fill=col, r=20))
        else:
            s.add(rect(x0, y - 20, (x1-x0)*0.62, 40, fill='none', r=20, stroke=HAIR2, sw=3, dash='14 11'))
        y += 92
    return s

# ── step 02 · clusters across the whole buyer journey ────────────────────────
def field(stage):
    """Full-bleed and cropped hard on phones, so the pillar stays in the centre band.
    Cards run past both edges on purpose: the field continues beyond the frame."""
    W, H = 1600, 900
    s = SVG(W, H, bg=PAPER)
    lanes = [248, 450, 652]
    seed = 20260910
    def rnd():
        nonlocal seed
        seed = (1103515245*seed + 12345) % 2147483648
        return seed/2147483648
    for ly in lanes:
        s.add(line(-20, ly, 1620, ly, HAIR, 2.4))
    slots = [(x, li) for li in range(3) for x in range(-30, 1690, 172)]
    if stage == 0:
        for i, (x, li) in enumerate(slots):
            if i % 5 in (2, 4):
                continue
            s.add(article(x + (rnd()-0.5)*250, lanes[li] + (rnd()-0.5)*168,
                          142, 96, HAIR2, 2.8, 1, 0.6))
    else:
        for i, (x, li) in enumerate(slots):
            if stage == 2 and li == 1 and abs(x - 800) < 250:
                continue
            s.add(article(x, lanes[li], 142, 96, INK, 3, 1, 0.6))
    if stage == 2:
        for x, li in slots:
            if li == 1 and abs(x - 800) < 250: continue
            if abs(x - 800) < 560:
                s.add(line(x, lanes[li], 800, 450, HAIR2, 2.2))
        s.add(article(800, 450, 404, 218, ACCENT, 5, 2, 0.6, headcol=ACCENT))
    return s

# ── step 03 · every piece has a job (dark) ───────────────────────────────────
def pipeline(done):
    W, H = 1600, 900
    s = SVG(W, H, bg=GRAPH)
    ys = [176, 312, 448, 584, 720]
    for i, y in enumerate(ys):
        s.add(article(320, y, 320, 108, ONDARK if done else '#5C5C58', 3.2, 1, 0.62, fill=DPANEL))
        if done:
            s.add(path(f'M480 {y} C640 {y} 700 450 860 450', stroke=ONDARK, sw=3.4))
        else:
            s.add(path(f'M480 {y} C560 {y} 600 {y} 660 {y}', stroke='#3A3A38', sw=3, dash='15 12'))
    s.add(rect(880, 396, 520, 108, fill='none', r=54, stroke=ACCENT if done else '#4A4A48', sw=4.5))
    if done:
        s.add(rect(906, 424, 468*0.78, 52, fill=ACCENT, r=26))
    return s

# ── the close · the library, compounding ─────────────────────────────────────
def final():
    """Narrow and tall, weighted right: it clears the CTA scrim and the phone crop."""
    W, H = 1600, 1200
    s = SVG(W, H, bg=PAPER)
    for cx in (952, 1238):
        for cy in (368, 596):
            s.add(article(cx, cy, 262, 196, HAIR2, 3, 2, 0.6))
    xs = [846, 942, 1038, 1134, 1230, 1326]
    hs = [82, 112, 138, 170, 206, 248]
    base = 1006
    for i, (x, hgt) in enumerate(zip(xs, hs)):
        last = i == len(xs) - 1
        s.add(rect(x-38, base-hgt, 76, hgt, fill=ACCENT if last else HAIR2, r=14))
    s.add(line(806, base + 22, 1370, base + 22, HAIR2, 3))
    return s

if __name__ == '__main__':
    for i in range(3): save(hero(i),   f'cc-hero-{i+1}')
    for i in range(3): save(engine(i), f'cc-engine-{i+1}')
    save(macro(), 'cc-macro')
    save(demand(False), 'cc-demand-1'); save(demand(True), 'cc-demand-2')
    for i in range(3): save(field(i), f'cc-field-{i+1}')
    save(pipeline(False), 'cc-pipe-1'); save(pipeline(True), 'cc-pipe-2')
    save(final(), 'cc-final')
