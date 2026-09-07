"""The six 'What You Get' cards: one artefact per card, one system.

Canvas 1080x1500 (ratio 0.720) matches the sticky column's mid ratio.
Cover-cropping across the real container band (0.648 .. 0.800) removes at most
54px from each side or 75px from top and bottom, so everything meaningful lives
inside x [96, 984], y [120, 1380].
Smallest render is the 272x340 chapter plate on a 320px phone: scale 0.252,
so no artwork type is smaller than 44px (11px on screen).

ACCENT RULE, one job across the whole set: orange marks the outcome the client
gets, or the opportunity they can take. Never the brand, never decoration.
A site is always drawn as the same neutral page glyph, never as the Ascend mark.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from dsl import *

W, H = 1080, 1500
SX, SY = 96, 120
L, R = SX, W - SX
CXC = W / 2
CARD = '#FBFBF9'
OUT = 'out'

T_EYE  = 46      # eyebrow                       -> 11.6px at the smallest plate
T_MARK = 54      # data values in the artwork    -> 13.6px
T_SUB  = 44      # secondary labels              -> 11.1px

def frame(eyebrow):
    s = SVG(W, H, bg=PAPER)
    s.add(CAP(eyebrow, L, 190, T_EYE, 600, INK3))
    s.add(line(L, 232, R, 232, HAIR, 1.6))
    return s

def close(s, name):
    s.add(line(L, 1380, R, 1380, HAIR, 1.6))
    n = s.save(f'{OUT}/{name}.svg')
    print(f'{n/1024:6.1f}KB  {name}.svg')

def page(cx, cy, w, h, stroke=INK, sw=3.4, bar=0.52, barcol=None, fill=CARD, r=14):
    """A site or page, always drawn the same way: a card with a title bar."""
    o = [rect(cx - w / 2, cy - h / 2, w, h, fill=fill, r=r, stroke=stroke, sw=sw)]
    if bar:
        bw, bh = w * bar, max(14, h * 0.20)
        o.append(rect(cx - bw / 2, cy - bh / 2, bw, bh, fill=barcol or stroke, r=bh / 2))
    return ''.join(o)

def arrow_in(x1, y1, x2, y2, stroke, sw, gap=0):
    """A connector ending in a small arrowhead just short of the target."""
    d = math.hypot(x2 - x1, y2 - y1) or 1
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    ex, ey = x2 - ux * gap, y2 - uy * gap
    o = [line(x1, y1, ex, ey, stroke, sw)]
    a = sw * 3.4
    px, py = -uy, ux
    o.append(path(f'M{ex:.1f} {ey:.1f} L{ex - ux*a + px*a*0.62:.1f} {ey - uy*a + py*a*0.62:.1f} '
                  f'L{ex - ux*a - px*a*0.62:.1f} {ey - uy*a - py*a*0.62:.1f} Z', fill=stroke))
    return ''.join(o)

# ── 01 · keyword intelligence ────────────────────────────────────────────────
def card_keywords():
    """Demand, ranked, sorted by intent — and the two positions still unclaimed."""
    s = frame('Unclaimed demand')
    rows = [(0.94, 0, False), (0.82, 1, True), (0.71, 1, False),
            (0.57, 2, False), (0.45, 3, True), (0.33, 3, False)]
    bx = L + 196
    bw = R - bx
    y = 372
    for vol, lane, gap in rows:
        for i in range(4):                       # intent ladder: four bands, one occupied
            on = i == lane
            s.add(rect(L + i * 44, y - 15, 30, 30, fill=INK if on else HAIR, r=7))
        if gap:
            s.add(rect(bx, y - 19, bw * vol, 38, fill='none', r=19, stroke=ACCENT, sw=4.5, dash='15 11'))
        else:
            s.add(rect(bx, y - 19, bw * vol, 38, fill=INK, r=19))
        y += 172
    return s

# ── 02 · technical seo audits ────────────────────────────────────────────────
def card_technical():
    """Every page reachable: the architecture, with the crawler's route traced."""
    s = frame('Every page reachable')
    home = (CXC, 396)
    cats = [(240, 726), (CXC, 726), (840, 726)]
    pages = [(178, 1036), (302, 1036), (478, 1036), (602, 1036), (778, 1036), (902, 1036)]
    for i, c in enumerate(cats):
        s.add(path(f'M{home[0]:.0f} {home[1] + 48:.0f} C{home[0]:.0f} {home[1] + 168:.0f} '
                   f'{c[0]:.0f} {c[1] - 168:.0f} {c[0]:.0f} {c[1] - 42:.0f}', stroke=INK, sw=3.4))
    for i, p in enumerate(pages):
        c = cats[i // 2]
        s.add(path(f'M{c[0]:.0f} {c[1] + 42:.0f} C{c[0]:.0f} {c[1] + 130:.0f} '
                   f'{p[0]:.0f} {p[1] - 130:.0f} {p[0]:.0f} {p[1] - 34:.0f}', stroke=INK, sw=3))
    # the crawler's traversal, drawn over the structure it walks
    s.add(path(f'M{L - 2:.0f} 396 L{home[0] - 176:.0f} 396', stroke=INK, sw=4.5, dash='17 12'))
    s.add(path(f'M{home[0]:.0f} {home[1] + 48:.0f} C{home[0]:.0f} {home[1] + 168:.0f} '
               f'{cats[0][0]:.0f} {cats[0][1] - 168:.0f} {cats[0][0]:.0f} {cats[0][1] - 42:.0f}', stroke=INK, sw=4.5, dash='17 12'))
    s.add(path(f'M{cats[0][0]:.0f} {cats[0][1] + 42:.0f} C{cats[0][0]:.0f} {cats[0][1] + 130:.0f} '
               f'{pages[0][0]:.0f} {pages[0][1] - 130:.0f} {pages[0][0]:.0f} {pages[0][1] - 34:.0f}', stroke=INK, sw=4.5, dash='17 12'))
    s.add(page(home[0], home[1], 352, 96, INK, 3.8, 0.55))
    for c in cats:
        s.add(page(c[0], c[1], 232, 84, INK, 3.4, 0.55))
    for p in pages:
        s.add(page(p[0], p[1], 118, 68, INK, 3.0, 0.58))
    # the route resolves at the deepest page
    s.add(line(pages[0][0], pages[0][1] + 34, pages[0][0], 1148, INK, 4.5, dash='14 10'))
    s.add(circle(pages[0][0], 1194, 46, fill=ACCENT))
    s.add(check(pages[0][0], 1196, 21, '#FFFFFF', 7))
    return s

# ── 03 · content engineering ─────────────────────────────────────────────────
def card_content():
    """Four clusters of supporting pages feeding one pillar page."""
    s = frame('One pillar, four clusters')
    pillar = (CXC, 404)
    s.add(page(pillar[0], pillar[1], 566, 118, ACCENT, 5, 0.42, barcol=ACCENT))
    cols = [216, 432, 648, 864]
    hub_y, sup_y0, sup_gap = 760, 906, 96
    for x in cols:
        s.add(arrow_in(x, hub_y - 40, x, pillar[1] + 76, INK, 3.6, gap=6))
        for k in range(3):
            yy = sup_y0 + k * sup_gap
            s.add(line(x, yy - 26, x, yy - 46, HAIR2, 2.6))
        s.add(page(x, hub_y, 176, 78, INK, 3.4, 0.5))
        for k in range(3):
            yy = sup_y0 + k * sup_gap
            s.add(page(x, yy, 176, 52, HAIR2, 2.8, 0.46, barcol=INK3))
    return s

# ── 04 · authority & link building ───────────────────────────────────────────
def card_authority():
    """Links earned from outside, arriving at the site, weighted by authority."""
    s = frame('Earned links')
    site = (CXC, 800)
    srcs = [(216, 452, 7.5, True), (CXC, 386, 5.6, False), (864, 452, 4.6, False),
            (216, 1148, 3.8, False), (CXC, 1214, 3.2, False), (864, 1148, 2.6, False)]
    for sx, sy, wt, best in srcs:
        col = ACCENT if best else INK
        d = math.hypot(site[0] - sx, site[1] - sy)
        s.add(arrow_in(sx, sy, site[0], site[1], col, wt, gap=86))
    for sx, sy, wt, best in srcs:
        col = ACCENT if best else INK
        s.add(rect(sx - 104, sy - 40, 208, 80, fill=CARD, r=40, stroke=col, sw=4 if best else 3.2))
        s.add(rect(sx - 46, sy - 9, 92, 18, fill=col, r=9))
    s.add(page(site[0], site[1], 250, 116, INK, 4, 0.5))
    return s

# ── 05 · rank tracking & revenue attribution ─────────────────────────────────
def card_rank():
    """Position tracked, then traced through traffic to revenue: one chain."""
    s = frame('Tracked and traced')
    gx, gy, gw, gh = L + 96, 320, 694, 470          # ends well inside the frame, not on its edge
    for i, p in enumerate([1, 10, 20]):
        yy = gy + (gh - 40) * (i / 2)
        s.add(line(gx, yy, gx + gw, yy, HAIR, 2))
        s.add(T(str(p), gx - 30, yy + 18, T_MARK, 600, INK3, 'end'))
    series = [20, 18, 15, 16, 12, 10, 11, 7, 5, 3]     # tracked movement, not a straight promise
    px = lambda i: gx + 26 + (gw - 52) * (i / (len(series) - 1))
    py = lambda p: gy + (gh - 40) * (min(p, 20) - 1) / 19
    s.add(path('M' + ' L'.join(f'{px(i):.1f} {py(p):.1f}' for i, p in enumerate(series)), stroke=ACCENT, sw=6.5))
    ex, ey = px(len(series) - 1), py(series[-1])
    s.add(circle(ex, ey, 20, fill=ACCENT))
    # the chain: position -> traffic -> revenue, one continuous accent spine
    t_y, r_y = 1010, 1210
    s.add(line(ex, ey + 20, ex, r_y, ACCENT, 6.5))
    for yy, label, frac in ((t_y, 'Traffic', 1.0), (r_y, 'Revenue', 0.66)):
        x0 = ex - (ex - L) * frac
        s.add(circle(ex, yy, 17, fill=ACCENT))
        s.add(rect(x0, yy - 17, ex - x0, 34, fill=INK, r=17))
        s.add(CAP(label, x0, yy - 44, T_SUB, 600, INK3))
    return s

# ── 06 · ai search & geo readiness ───────────────────────────────────────────
def card_geo():
    """A generated answer that cites the site, and where that citation stands."""
    s = frame('Cited as the source')
    ax, ay, aw, ah = L, 300, R - L, 452
    s.add(rect(ax, ay, aw, ah, fill=CARD, r=20, stroke=HAIR, sw=3))
    for i, f in enumerate([0.88, 0.94, 0.66]):
        s.add(rect(ax + 46, ay + 66 + i * 68, (aw - 92) * f, 26, fill=HAIR2, r=13))
    s.add(rect(ax + 46, ay + 274, 92, 46, fill=ACCENT, r=10))
    s.add(T('1', ax + 92, ay + 310, 54, 700, '#FFFFFF', 'middle'))
    s.add(rect(ax + 46, ay + 344, aw - 92, 84, fill=PAPER, r=14, stroke=ACCENT, sw=3.4))
    s.add(page(ax + 116, ay + 386, 92, 52, INK, 3, 0.5))
    s.add(rect(ax + 186, ay + 375, 300, 22, fill=INK, r=11))
    # four answer engines, four different marks, four honest states
    ey, pitch = 906, 116
    states = ['cited', 'cited', 'partial', 'pending']
    for i in range(4):
        yy = ey + i * pitch
        gx0 = L + 26
        if i == 0:   s.add(circle(gx0, yy, 24, fill='none', stroke=INK, sw=3.4))
        elif i == 1: s.add(rect(gx0 - 22, yy - 22, 44, 44, fill='none', r=8, stroke=INK, sw=3.4))
        elif i == 2: s.add(path(f'M{gx0:.0f} {yy - 26:.0f} L{gx0 + 24:.0f} {yy + 20:.0f} L{gx0 - 24:.0f} {yy + 20:.0f} Z', fill='none', stroke=INK, sw=3.4))
        else:        s.add(path(f'M{gx0:.0f} {yy - 26:.0f} L{gx0 + 26:.0f} {yy:.0f} L{gx0:.0f} {yy + 26:.0f} L{gx0 - 26:.0f} {yy:.0f} Z', fill='none', stroke=INK, sw=3.4))
        s.add(rect(L + 76, yy - 11, 330 - i * 24, 22, fill=HAIR2, r=11))
        st = states[i]
        if st == 'cited':
            s.add(circle(R - 30, yy, 24, fill=ACCENT))
            s.add(check(R - 30, yy + 2, 11, '#FFFFFF', 4))
        elif st == 'partial':
            s.add(circle(R - 30, yy, 24, fill='none', stroke=ACCENT, sw=3.4))
            s.add(path(f'M{R - 30:.0f} {yy - 24:.0f} A24 24 0 0 1 {R - 30:.0f} {yy + 24:.0f} Z', fill=ACCENT))
        else:
            s.add(circle(R - 30, yy, 24, fill='none', stroke=HAIR2, sw=3.4))
        if i < 3:
            s.add(line(L, yy + pitch / 2, R, yy + pitch / 2, HAIR, 1.6))
    return s

if __name__ == '__main__':
    close(card_keywords(),  'card-keywords')
    close(card_technical(), 'card-technical')
    close(card_content(),   'card-content')
    close(card_authority(), 'card-authority')
    close(card_rank(),      'card-rank')
    close(card_geo(),       'card-geo')
