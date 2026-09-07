"""GEO — the six 'What You Get' cards.

Same contract as the SEO and Link Building sets: canvas 1080x1500 (ratio 0.720),
safe area x [96, 984] y [120, 1380], nothing under 44px, one shared skeleton,
and one job for the accent — it marks the outcome earned or the gap still open.
An answer engine is always one of four neutral marks, never a brand logo.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from dsl import *

W, H = 1080, 1500
SX, SY = 96, 120
L, R = SX, W - SX
CXC = W / 2
CARD = '#FBFBF9'
OUT = 'outgeo'
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
    o = [rect(cx - w/2, cy - h/2, w, h, fill=fill, r=r, stroke=stroke, sw=sw)]
    if bar:
        bw, bh = w * bar, max(14, h * 0.20)
        o.append(rect(cx - bw/2, cy - bh/2, bw, bh, fill=barcol or stroke, r=bh/2))
    return ''.join(o)

def engine_mark(i, cx, cy, s, col=INK, sw=3.4):
    """Four answer engines, four neutral marks. No logos anywhere in the set."""
    if i == 0:  return circle(cx, cy, s, fill='none', stroke=col, sw=sw)
    if i == 1:  return rect(cx - s, cy - s, s*2, s*2, fill='none', r=s*0.34, stroke=col, sw=sw)
    if i == 2:  return path(f'M{cx:.0f} {cy - s*1.08:.0f} L{cx + s:.0f} {cy + s*0.82:.0f} L{cx - s:.0f} {cy + s*0.82:.0f} Z', fill='none', stroke=col, sw=sw)
    return path(f'M{cx:.0f} {cy - s*1.1:.0f} L{cx + s*1.1:.0f} {cy:.0f} L{cx:.0f} {cy + s*1.1:.0f} L{cx - s*1.1:.0f} {cy:.0f} Z', fill='none', stroke=col, sw=sw)

def arrow_in(x1, y1, x2, y2, stroke, sw, gap=0):
    d = math.hypot(x2-x1, y2-y1) or 1
    ux, uy = (x2-x1)/d, (y2-y1)/d
    ex, ey = x2-ux*gap, y2-uy*gap
    o = [line(x1, y1, ex, ey, stroke, sw)]
    a = sw*3.4; px, py = -uy, ux
    o.append(path(f'M{ex:.1f} {ey:.1f} L{ex-ux*a+px*a*0.62:.1f} {ey-uy*a+py*a*0.62:.1f} '
                  f'L{ex-ux*a-px*a*0.62:.1f} {ey-uy*a-py*a*0.62:.1f} Z', fill=stroke))
    return ''.join(o)

# ── 01 · geo strategy & audit ────────────────────────────────────────────────
def card_audit():
    """What each engine already says about you, and where it says nothing."""
    s = frame('How AI sees you now')
    y0, pitch = 384, 244
    share = [0.72, 0.54, 0.38, 0.08]
    for i in range(4):
        y = y0 + i * pitch
        gap = i == 3
        col = ACCENT if gap else INK
        s.add(engine_mark(i, L + 34, y, 30, col, 3.6))
        bx, bw = L + 108, R - (L + 108)
        s.add(rect(bx, y - 19, bw, 38, fill=HAIR, r=19))
        if gap:
            s.add(rect(bx, y - 19, bw * share[i], 38, fill=ACCENT, r=19))
            s.add(rect(bx + bw * share[i] + 12, y - 19, bw * (1 - share[i]) - 12, 38,
                       fill='none', r=19, stroke=ACCENT, sw=3.4, dash='14 11'))
        else:
            s.add(rect(bx, y - 19, bw * share[i], 38, fill=INK, r=19))
        if i < 3:
            s.add(line(L, y + pitch/2, R, y + pitch/2, HAIR, 1.6))
    return s

# ── 02 · schema & entity engineering ─────────────────────────────────────────
def card_schema():
    """Loose mentions on a page, resolved into one entity a model can hold."""
    s = frame('One entity, resolved')
    px, py, pw, ph = L, 300, R - L, 372
    s.add(rect(px, py, pw, ph, fill=CARD, r=20, stroke=HAIR, sw=3))
    marks = [(0.30, 0.14), (0.62, 0.44), (0.24, 0.74)]
    for i, (wf, yf) in enumerate(marks):
        yy = py + 58 + i * 96
        s.add(rect(px + 46, yy, (pw - 92) * 0.86, 18, fill=HAIR2, r=9))
        cxm = px + 46 + (pw - 92) * (0.10 + i * 0.22)
        s.add(rect(cxm - 12, yy - 26, 210, 46, fill='none', r=10, stroke=INK, sw=3.2))
        s.add(rect(cxm + 4, yy - 9, 170, 16, fill=INK, r=8))
    for i in range(3):
        sx = px + 46 + (pw - 92) * (0.10 + i * 0.22) + 90
        s.add(arrow_in(sx, py + ph - 6, CXC, 892, INK, 3.2, gap=104))
    s.add(rect(CXC - 216, 892 - 84, 432, 168, fill=CARD, r=20, stroke=ACCENT, sw=5))
    s.add(rect(CXC - 150, 892 - 34, 300, 26, fill=ACCENT, r=13))
    s.add(rect(CXC - 150, 892 + 14, 220, 18, fill=INK, r=9))
    for i in range(3):
        yy = 1076 + i * 84
        s.add(rect(L + 150, yy, 190, 22, fill=HAIR2, r=11))
        s.add(rect(L + 372, yy, 320 - i * 44, 22, fill=INK, r=11))
        s.add(line(L + 120, yy + 11, L + 138, yy + 11, HAIR2, 3))
    return s

# ── 03 · ai citation tracking ────────────────────────────────────────────────
def card_tracking():
    """Every answer that named you, and the one that got you wrong."""
    s = frame('Where you surface')
    rows, y0, pitch = 4, 452, 250
    ticks = [0.05, 0.17, 0.28, 0.40, 0.51, 0.62, 0.74, 0.86, 0.96]
    mine = {0: [1, 4, 7], 1: [0, 3, 6, 8], 2: [2, 5], 3: [1, 3, 5, 8]}
    for r_ in range(rows):
        y = y0 + r_ * pitch
        s.add(line(L, y, R, y, HAIR2, 3))
        for i, t in enumerate(ticks):
            x = L + (R - L) * t
            on = i in mine[r_]
            if on:
                s.add(line(x, y - 92, x, y, ACCENT, 8))
                s.add(circle(x, y - 92, 13, fill=ACCENT))
            else:
                s.add(line(x, y - 44, x, y, HAIR2, 5))
        if r_ == 1:
            x = L + (R - L) * ticks[6]
            rr = 46
            s.add(path(f'M{x-rr:.1f} {y-92:.1f} a{rr} {rr} 0 1 0 {2*rr} 0 a{rr} {rr} 0 1 0 {-2*rr} 0',
                       stroke=ACCENT, sw=4, dash='13 10'))
    return s

# ── 04 · authority & source building ─────────────────────────────────────────
def card_authority():
    """The source types models actually pull from, and the one you earned."""
    s = frame('What models pull from')
    widths = [0.96, 0.80, 0.64, 0.48, 0.32]
    y0, bh, gap = 392, 116, 34
    for i, wf in enumerate(widths):
        y = y0 + i * (bh + gap)
        w = (R - L) * wf
        earned = i == 1
        col = ACCENT if earned else INK
        s.add(rect(CXC - w/2, y, w, bh, fill=CARD, r=16, stroke=col, sw=4.2 if earned else 3.4))
        s.add(rect(CXC - w*0.28, y + bh/2 - 11, w*0.56, 22, fill=col, r=11))
    return s

# ── 05 · prompt-intent mapping ───────────────────────────────────────────────
def card_prompts():
    """The prompts customers actually type, sorted into the moments they mean."""
    s = frame('The prompts they ask')
    px, pw = L, 300
    prompts = [0.92, 0.74, 0.86, 0.62, 0.80, 0.68]
    ys = [392, 496, 600, 704, 808, 912]
    moments = [(792, 520), (792, 760), (792, 1000)]
    link = [0, 0, 1, 1, 2, 2]
    for i, (yy, wf) in enumerate(zip(ys, prompts)):
        s.add(rect(px, yy - 18, pw * wf, 36, fill=INK, r=18))
        mx, my = moments[link[i]]
        col = ACCENT if link[i] == 2 else HAIR2
        s.add(path(f'M{px + pw * wf + 14:.0f} {yy:.0f} C{px + pw + 120:.0f} {yy:.0f} '
                   f'{mx - 190:.0f} {my:.0f} {mx - 118:.0f} {my:.0f}', stroke=col, sw=3.2))
    for i, (mx, my) in enumerate(moments):
        best = i == 2
        col = ACCENT if best else INK
        s.add(rect(mx - 116, my - 62, 232, 124, fill=CARD, r=18, stroke=col, sw=4.4 if best else 3.4))
        s.add(rect(mx - 66, my - 11, 132, 22, fill=col, r=11))
    return s

# ── 06 · revenue attribution & reporting ─────────────────────────────────────
def card_revenue():
    """An answer engine session, stitched all the way to revenue."""
    s = frame('Session to revenue')
    for i in range(4):
        x = L + 96 + i * 216
        s.add(engine_mark(i, x, 348, 30, INK, 3.4))
        s.add(arrow_in(x, 388, CXC, 520, INK, 3, gap=64))
    s.add(rect(CXC - 250, 520 - 46, 500, 92, fill=CARD, r=46, stroke=INK, sw=3.6))
    s.add(rect(CXC - 130, 520 - 11, 260, 22, fill=INK, r=11))
    s.add(line(CXC, 566, CXC, 686, ACCENT, 6))
    s.add(rect(L + 116, 686, R - L - 232, 168, fill=CARD, r=20, stroke=INK, sw=3.6))
    for i in range(3):
        x = L + 152 + i * 214
        s.add(rect(x, 730, 176, 80, fill='none', r=14, stroke=HAIR2, sw=3))
        s.add(rect(x + 42, 762, 92, 16, fill=HAIR2, r=8))
    s.add(line(CXC, 854, CXC, 1000, ACCENT, 6))
    s.add(circle(CXC, 1000, 18, fill=ACCENT))
    s.add(rect(L, 1080, R - L, 46, fill=HAIR, r=23))
    s.add(rect(L, 1080, (R - L) * 0.74, 46, fill=ACCENT, r=23))
    s.add(CAP('Attributed', L, 1054, T_SUB, 600, INK3))
    return s

if __name__ == '__main__':
    close(card_audit(),     'geo-card-audit')
    close(card_schema(),    'geo-card-schema')
    close(card_tracking(),  'geo-card-tracking')
    close(card_authority(), 'geo-card-authority')
    close(card_prompts(),   'geo-card-prompts')
    close(card_revenue(),   'geo-card-revenue')
