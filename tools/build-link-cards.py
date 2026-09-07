"""Link Building — the six 'What You Get' cards.

Same contract as the SEO page's set: canvas 1080x1500 (ratio 0.720), safe area
x [96, 984] y [120, 1380], nothing under 44px, one shared skeleton, and one job
for the accent — it marks the outcome earned or the opportunity to take.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from dsl import *

W, H = 1080, 1500
SX, SY = 96, 120
L, R = SX, W - SX
CXC = W / 2
CARD = '#FBFBF9'
OUT = 'outlb'

T_EYE, T_MARK, T_SUB = 46, 54, 44

def frame(eyebrow):
    w = text_width(eyebrow.upper(), T_EYE, 600, T_EYE * 0.16)
    assert w <= R - L, f'eyebrow "{eyebrow}" is {w:.0f}px wide, safe width is {R - L}px'
    s = SVG(W, H, bg=PAPER)
    s.add(CAP(eyebrow, L, 190, T_EYE, 600, INK3))
    s.add(line(L, 232, R, 232, HAIR, 1.6))
    return s

def close(s, name):
    s.add(line(L, 1380, R, 1380, HAIR, 1.6))
    n = s.save(f'{OUT}/{name}.svg')
    print(f'{n/1024:6.1f}KB  {name}.svg')

def page(cx, cy, w, h, stroke=INK, sw=3.4, bar=0.52, barcol=None, fill=CARD, r=14):
    o = [rect(cx - w / 2, cy - h / 2, w, h, fill=fill, r=r, stroke=stroke, sw=sw)]
    if bar:
        bw, bh = w * bar, max(14, h * 0.20)
        o.append(rect(cx - bw / 2, cy - bh / 2, bw, bh, fill=barcol or stroke, r=bh / 2))
    return ''.join(o)

def arrow_in(x1, y1, x2, y2, stroke, sw, gap=0):
    d = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    ex, ey = x2 - ux * gap, y2 - uy * gap
    o = [line(x1, y1, ex, ey, stroke, sw)]
    a = sw * 3.4
    px, py = -uy, ux
    o.append(path(f'M{ex:.1f} {ey:.1f} L{ex-ux*a+px*a*0.62:.1f} {ey-uy*a+py*a*0.62:.1f} '
                  f'L{ex-ux*a-px*a*0.62:.1f} {ey-uy*a-py*a*0.62:.1f} Z', fill=stroke))
    return ''.join(o)

def link_chip(cx, cy, w=190, h=60, col=ACCENT):
    """A link, drawn as two joined rings inside a pill."""
    o = [rect(cx - w/2, cy - h/2, w, h, fill=col, r=h/2)]
    r = h * 0.24
    o.append(circle(cx - r*0.85, cy, r, fill='none', stroke='#FFFFFF', sw=6))
    o.append(circle(cx + r*0.85, cy, r, fill='none', stroke='#FFFFFF', sw=6))
    return ''.join(o)

# ── 01 · digital pr ──────────────────────────────────────────────────────────
def card_pr():
    """A story published, and the link it sends back."""
    s = frame('Story to coverage')
    px, py, pw, ph = L, 292, R - L, 520
    s.add(rect(px, py, pw, ph, fill=CARD, r=20, stroke=HAIR, sw=3))
    s.add(rect(px + 46, py + 46, 176, 24, fill=HAIR2, r=12))          # masthead
    s.add(line(px + 46, py + 100, px + pw - 46, py + 100, HAIR, 2))
    s.add(rect(px + 46, py + 138, (pw - 92) * 0.78, 34, fill=INK, r=17))   # headline
    s.add(rect(px + 46, py + 190, (pw - 92) * 0.52, 34, fill=INK, r=17))
    for i, f in enumerate([0.92, 0.86, 0.74, 0.6]):
        s.add(rect(px + 46, py + 272 + i * 50, (pw - 92) * f, 20, fill=HAIR2, r=10))
    s.add(line(CXC, py + ph, CXC, 906, ACCENT, 6))
    s.add(link_chip(CXC, 940))
    s.add(arrow_in(CXC, 974, CXC, 1156, ACCENT, 6, gap=6))
    s.add(page(CXC, 1218, 280, 122, INK, 4, 0.5))
    return s

# ── 02 · linkable assets ─────────────────────────────────────────────────────
def card_assets():
    """One asset worth citing, and the citations it attracts."""
    s = frame('Built to be cited')
    ax, ay = CXC, 838
    pubs = [(214, 420), (866, 420), (214, 1218), (866, 1218)]
    for pxx, pyy in pubs:
        s.add(arrow_in(pxx, pyy, ax, ay, INK, 3.6, gap=178))
    for pxx, pyy in pubs:
        s.add(page(pxx, pyy, 196, 92, INK, 3.2, 0.5))
    s.add(rect(ax - 186, ay - 148, 372, 296, fill=CARD, r=22, stroke=ACCENT, sw=5))
    for i, hgt in enumerate([70, 122, 96, 158]):
        s.add(rect(ax - 132 + i * 76, ay + 96 - hgt, 48, hgt, fill=ACCENT if i == 3 else INK, r=10))
    s.add(line(ax - 140, ay + 100, ax + 140, ay + 100, INK, 3.4))
    return s

# ── 03 · competitor gaps ─────────────────────────────────────────────────────
def card_gaps():
    """What competitors have earned, what you have, and the distance between."""
    s = frame('Where they out-link you')
    base, bw, blk, gap = 1258, 176, 52, 16
    cols = [(216, 8, False), (432, 6, False), (648, 7, False), (864, 3, True)]
    tallest = 8
    for cx, n, mine in cols:
        for i in range(n):
            y = base - (i + 1) * (blk + gap) + gap
            s.add(rect(cx - bw / 2, y, bw, blk, fill=INK, r=10))
        if mine:
            for i in range(n, tallest):
                y = base - (i + 1) * (blk + gap) + gap
                s.add(rect(cx - bw / 2, y, bw, blk, fill='none', r=10, stroke=ACCENT, sw=3.4, dash='13 10'))
    s.add(line(L, base + 6, R, base + 6, INK, 3.4))
    return s

# ── 04 · publisher outreach ──────────────────────────────────────────────────
def card_outreach():
    """A short list of the right publishers, and the ones that answered."""
    s = frame('Targeted, not sprayed')
    y0, pitch = 336, 152
    rows = [(0.62, 3, True), (0.48, 3, False), (0.70, 2, True), (0.40, 2, False), (0.56, 1, False), (0.34, 1, False)]
    for i, (wf, rel, replied) in enumerate(rows):
        y = y0 + i * pitch
        col = ACCENT if replied else INK
        s.add(rect(L, y - 26, 52, 52, fill='none', r=12, stroke=col, sw=3.4))
        s.add(rect(L + 22, y - 6, 8, 12, fill=col, r=4))
        s.add(rect(L + 82, y - 11, (R - L - 300) * wf, 22, fill=HAIR2 if not replied else INK, r=11))
        for k in range(3):                                  # relevance, three bands
            s.add(rect(R - 188 + k * 34, y - 11, 22, 22, fill=INK if k < rel else HAIR, r=6))
        if replied:
            s.add(circle(R - 26, y, 24, fill=ACCENT))
            s.add(check(R - 26, y + 2, 11, '#FFFFFF', 4))
        else:
            s.add(circle(R - 26, y, 24, fill='none', stroke=HAIR2, sw=3.2))
        if i < len(rows) - 1:
            s.add(line(L, y + pitch / 2, R, y + pitch / 2, HAIR, 1.6))
    return s

# ── 05 · authority tracking ──────────────────────────────────────────────────
def card_tracking():
    """Links accumulating, and the authority that accumulates with them."""
    s = frame('Month by month')
    base, n = 1252, 8
    cw, cg = 88, 26
    total = n * cw + (n - 1) * cg
    x0 = L + (R - L - total) / 2
    hs = [124, 186, 244, 322, 396, 492, 588, 700]
    tops = []
    for i, hgt in enumerate(hs):
        x = x0 + i * (cw + cg)
        s.add(rect(x, base - hgt, cw, hgt, fill=INK, r=10))
        tops.append((x + cw / 2, base - hgt))
    s.add(path('M' + ' L'.join(f'{a:.1f} {b - 34:.1f}' for a, b in tops), stroke=ACCENT, sw=6))
    s.add(circle(tops[-1][0], tops[-1][1] - 34, 20, fill=ACCENT))
    s.add(line(L, base + 6, R, base + 6, INK, 3.4))
    return s

# ── 06 · quality control ─────────────────────────────────────────────────────
def card_quality():
    """Everything offered goes through the screen; only the sound links pass."""
    s = frame('What we refuse')
    # candidates arriving
    cand = [(224, 350, True), (540, 350, True), (856, 350, False),
            (224, 486, False), (540, 486, True), (856, 486, True)]
    for cx, cy, ok in cand:
        col = INK if ok else HAIR2
        s.add(rect(cx - 128, cy - 40, 256, 80, fill='none', r=40, stroke=col, sw=3.4))
        s.add(rect(cx - 62, cy - 9, 124, 18, fill=col, r=9))
        if not ok:
            s.add(cross(cx + 92, cy, 17, HAIR2, 4))
    # the screen
    sy = 720
    s.add(rect(L, sy, R - L, 132, fill=CARD, r=22, stroke=INK, sw=4.5))
    for k in range(9):
        x = L + 62 + k * 86
        blocked = k in (2, 6)
        s.add(rect(x, sy + 30, 46, 72, fill=INK if blocked else PAPER, r=10, stroke=INK if not blocked else None, sw=2.6))
    # what passes
    for i, cx in enumerate([300, 780]):
        for j, cy in enumerate([1010, 1160]):
            s.add(rect(cx - 168, cy - 42, 336, 84, fill=CARD, r=42, stroke=ACCENT, sw=3.8))
            s.add(rect(cx - 92, cy - 9, 150, 18, fill=INK, r=9))
            s.add(circle(cx + 108, cy, 24, fill=ACCENT))
            s.add(check(cx + 108, cy + 2, 11, '#FFFFFF', 4))
    return s

if __name__ == '__main__':
    close(card_pr(),       'lb-card-pr')
    close(card_assets(),   'lb-card-assets')
    close(card_gaps(),     'lb-card-gaps')
    close(card_outreach(), 'lb-card-outreach')
    close(card_tracking(), 'lb-card-tracking')
    close(card_quality(),  'lb-card-quality')
