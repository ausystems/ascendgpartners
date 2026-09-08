"""Content Creation — the six 'What You Get' cards.

Same contract as the SEO, Link Building and GEO sets: canvas 1080x1500
(ratio 0.720), safe area x [96, 984] y [120, 1380], nothing under 44px, one
shared skeleton, and one job for the accent — it marks the outcome earned or
the opportunity to take.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from dsl import *

W, H = 1080, 1500
SX, SY = 96, 120
L, R = SX, W - SX
CXC = W / 2
CARD = '#FBFBF9'
OUT = 'outcc'
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

def article(cx, cy, w, h, stroke=INK, sw=3.4, lines=3, head=0.62, fill=CARD, r=16, headcol=None):
    """A piece of content, always drawn the same way: a headline and body."""
    o = [rect(cx-w/2, cy-h/2, w, h, fill=fill, r=r, stroke=stroke, sw=sw)]
    ix = cx - w/2 + w*0.10
    iw = w*0.80
    o.append(rect(ix, cy-h/2 + h*0.16, iw*head, max(16, h*0.09), fill=headcol or stroke, r=h*0.045))
    for i in range(lines):
        o.append(rect(ix, cy-h/2 + h*0.36 + i*h*0.15, iw*[0.94, 0.82, 0.6, 0.88][i % 4],
                      max(11, h*0.055), fill=HAIR2, r=h*0.028))
    return ''.join(o)

def arrow_in(x1, y1, x2, y2, stroke, sw, gap=0):
    d = math.hypot(x2-x1, y2-y1) or 1
    ux, uy = (x2-x1)/d, (y2-y1)/d
    ex, ey = x2-ux*gap, y2-uy*gap
    o = [line(x1, y1, ex, ey, stroke, sw)]
    a = sw*3.4; px, py = -uy, ux
    o.append(path(f'M{ex:.1f} {ey:.1f} L{ex-ux*a+px*a*0.62:.1f} {ey-uy*a+py*a*0.62:.1f} '
                  f'L{ex-ux*a-px*a*0.62:.1f} {ey-uy*a-py*a*0.62:.1f} Z', fill=stroke))
    return ''.join(o)

# ── 01 · content strategy ────────────────────────────────────────────────────
def card_strategy():
    """Demand mapped and ranked into groups before a word is written."""
    s = frame('Mapped before written')
    groups = [[0.92, 0.74, 0.61], [0.86, 0.55], [0.68, 0.44]]
    y = 348
    top = True
    for gi, g in enumerate(groups):
        if gi:
            s.add(line(L, y - 66, R, y - 66, HAIR, 1.6))
        for vi, v in enumerate(g):
            best = top
            col = ACCENT if best else INK
            s.add(rect(L, y - 15, 30, 30, fill=col, r=7))
            bx = L + 66
            s.add(rect(bx, y - 19, R - bx, 38, fill=HAIR, r=19))
            s.add(rect(bx, y - 19, (R - bx) * v, 38, fill=col, r=19))
            top = False
            y += 132
        y += 42
    return s

# ── 02 · seo writing ─────────────────────────────────────────────────────────
def card_writing():
    """Written to rank, and still written like a brand."""
    s = frame('Ranks and reads')
    rungs = [396, 512, 628, 744, 860, 976]
    for i, ry in enumerate(rungs):
        first = i == 0
        s.add(line(L, ry, L + (252 if first else 196), ry, ACCENT if first else HAIR2, 9 if first else 5))
        if first:
            s.add(circle(L + 8, ry, 17, fill=ACCENT))
    s.add(article(700, 812, 486, 672, INK, 4, 4, 0.66))
    s.add(path(f'M{L + 258:.0f} 396 C{L + 350:.0f} 396 {700 - 330:.0f} 476 {700 - 249:.0f} 512',
               stroke=ACCENT, sw=5))
    return s

# ── 03 · thought leadership ──────────────────────────────────────────────────
def card_leadership():
    """A piece with a person's name on it, and the places that carried it."""
    s = frame('Signed by a person')
    s.add(article(CXC, 500, R - L, 372, INK, 3.6, 3, 0.7))
    by = 760
    s.add(rect(L, by - 62, R - L, 124, fill=CARD, r=20, stroke=ACCENT, sw=4))
    s.add(circle(L + 78, by, 40, fill='none', stroke=ACCENT, sw=4.5))
    s.add(rect(L + 78 - 16, by - 7, 32, 14, fill=ACCENT, r=7))
    s.add(rect(L + 146, by - 26, 286, 26, fill=ACCENT, r=13))
    s.add(rect(L + 146, by + 8, 196, 18, fill=HAIR2, r=9))
    for i in range(3):
        y = 946 + i * 136
        s.add(rect(L, y, R - L, 96, fill=CARD, r=48, stroke=INK, sw=3.2))
        s.add(rect(L + 46, y + 38, 258 - i * 46, 20, fill=INK, r=10))
        s.add(circle(R - 50, y + 48, 22, fill='none', stroke=HAIR2, sw=3))
    return s

# ── 04 · conversion copy ─────────────────────────────────────────────────────
def card_conversion():
    """The path a reader takes from the page to becoming a customer."""
    s = frame('Reader to customer')
    s.add(article(CXC, 424, 470, 268, INK, 3.6, 2, 0.62))
    s.add(line(CXC, 558, CXC, 690, ACCENT, 6))
    s.add(rect(CXC - 190, 690, 380, 96, fill=ACCENT, r=48))
    s.add(rect(CXC - 96, 728, 192, 20, fill='#FFFFFF', r=10))
    s.add(line(CXC, 786, CXC, 906, ACCENT, 6))
    s.add(rect(CXC - 230, 906, 460, 190, fill=CARD, r=20, stroke=INK, sw=3.6))
    for i in range(3):
        s.add(rect(CXC - 180, 942 + i * 48, 360 - i * 70, 26, fill=HAIR2, r=13))
    s.add(line(CXC, 1096, CXC, 1210, ACCENT, 6))
    s.add(circle(CXC, 1264, 54, fill='none', stroke=ACCENT, sw=5))
    s.add(check(CXC, 1266, 24, ACCENT, 7))
    return s

# ── 05 · refreshes ───────────────────────────────────────────────────────────
def card_refresh():
    """Pages that already rank, made to carry more."""
    s = frame('Old pages, doing more')
    rows = [(0.44, 0.30), (0.36, 0.26), (0.52, 0.22), (0.30, 0.34), (0.46, 0.18)]
    y = 400
    for before, gain in rows:
        s.add(rect(L, y - 21, R - L, 42, fill=HAIR, r=21))
        s.add(rect(L, y - 21, (R - L) * before, 42, fill=INK, r=21))
        s.add(rect(L + (R - L) * before, y - 21, (R - L) * gain, 42, fill=ACCENT, r=21))
        y += 176
    return s

# ── 06 · editorial systems ───────────────────────────────────────────────────
def card_systems():
    """A calendar that keeps moving, and a check before anything ships."""
    s = frame('Briefs, calendar, QA')
    cols, rows = 6, 4
    cw, ch, gx, gy = 120, 120, 30, 30
    gw = cols * cw + (cols - 1) * gx
    x0 = L + (R - L - gw) / 2
    y0 = 356
    shipped = {(0,0),(1,0),(2,0),(0,1),(1,1),(3,1),(0,2),(2,2),(1,3)}
    for r_ in range(rows):
        for c in range(cols):
            x = x0 + c * (cw + gx)
            y = y0 + r_ * (ch + gy)
            if c == 4:
                s.add(rect(x, y, cw, ch, fill='none', r=18, stroke=ACCENT, sw=4))
                if r_ < 2:
                    s.add(check(x + cw/2, y + ch/2 + 2, 24, ACCENT, 6))
            elif (c, r_) in shipped:
                s.add(rect(x, y, cw, ch, fill=INK, r=18))
            else:
                s.add(rect(x, y, cw, ch, fill='none', r=18, stroke=HAIR2, sw=3))
    return s

if __name__ == '__main__':
    close(card_strategy(),   'cc-card-strategy')
    close(card_writing(),    'cc-card-writing')
    close(card_leadership(), 'cc-card-leadership')
    close(card_conversion(), 'cc-card-conversion')
    close(card_refresh(),    'cc-card-refresh')
    close(card_systems(),    'cc-card-systems')
