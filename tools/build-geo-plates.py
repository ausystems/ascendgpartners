"""GEO — the wide plates: hero, engine, the three sections, the close."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from dsl import *

OUT = 'outgeo'
CARD = '#FBFBF9'

def save(s, name):
    n = s.save(f'{OUT}/{name}.svg')
    print(f'{n/1024:6.1f}KB  {name}.svg')

def page(cx, cy, w, h, stroke=INK, sw=3.4, bar=0.52, barcol=None, fill=CARD, r=14):
    o = [rect(cx-w/2, cy-h/2, w, h, fill=fill, r=r, stroke=stroke, sw=sw)]
    if bar:
        bw, bh = w*bar, max(12, h*0.19)
        o.append(rect(cx-bw/2, cy-bh/2, bw, bh, fill=barcol or stroke, r=bh/2))
    return ''.join(o)

def pill(cx, cy, w, h, stroke, sw=3, barw=0.42, barcol=None, fill=CARD):
    return (rect(cx-w/2, cy-h/2, w, h, fill=fill, r=h/2, stroke=stroke, sw=sw) +
            rect(cx-w*barw/2, cy-8, w*barw, 16, fill=barcol or stroke, r=8))

def emark(i, cx, cy, s, col=INK, sw=3.4):
    if i == 0: return circle(cx, cy, s, fill='none', stroke=col, sw=sw)
    if i == 1: return rect(cx-s, cy-s, s*2, s*2, fill='none', r=s*0.34, stroke=col, sw=sw)
    if i == 2: return path(f'M{cx:.0f} {cy-s*1.08:.0f} L{cx+s:.0f} {cy+s*0.82:.0f} L{cx-s:.0f} {cy+s*0.82:.0f} Z', fill='none', stroke=col, sw=sw)
    return path(f'M{cx:.0f} {cy-s*1.1:.0f} L{cx+s*1.1:.0f} {cy:.0f} L{cx:.0f} {cy+s*1.1:.0f} L{cx-s*1.1:.0f} {cy:.0f} Z', fill='none', stroke=col, sw=sw)

def chip(cx, cy, w, h, col, label_col='#FFFFFF'):
    return rect(cx-w/2, cy-h/2, w, h, fill=col, r=10) + T('1', cx, cy+h*0.30, h*0.66, 700, label_col, 'middle')

# ── hero · the generated answer, and who it names ────────────────────────────
def hero(level):
    """0 you are not in it · 1 you are one of the sources · 2 you are the source it cites."""
    W, H = 1200, 800
    s = SVG(W, H, bg=None)
    ax, ay, aw, ah = 90, 58, 1020, 424
    s.add(rect(ax, ay, aw, ah, fill=CARD, r=24, stroke=HAIR if level == 0 else HAIR2, sw=3.4))
    for i, f in enumerate([0.90, 0.96, 0.82, 0.58]):
        s.add(rect(ax+52, ay+58+i*68, (aw-104)*f, 26, fill=HAIR2, r=13))
    if level >= 1:
        s.add(chip(ax+92, ay+360, 84, 52, INK if level == 1 else ACCENT))
        s.add(rect(ax+152, ay+348, 420, 24, fill=INK, r=12))
    rows = [(556, 0), (636, 1), (716, 2)]
    for yy, i in rows:
        top = (level == 2 and i == 0)
        col = ACCENT if top else (INK if level >= 1 else HAIR2)
        s.add(rect(ax, yy-31, aw, 62, fill=CARD, r=31, stroke=col, sw=3.8 if top else 3))
        s.add(rect(ax+40, yy-9, 300 - i*54, 18, fill=col, r=9))
    if level == 2:
        s.add(path(f'M{ax+92:.0f} {ay+388:.0f} C{ax+92:.0f} {ay+450:.0f} {ax+40:.0f} 496 {ax+40:.0f} 524',
                   stroke=ACCENT, sw=4.5, dash='14 10'))
    return s

# ── engine · mentions across three answer engines ────────────────────────────
def engine(active):
    """The three columns never change. Only the accent marker moves, so the
    crossfade between states stays clean instead of blending two fills."""
    W, H = 1200, 800
    s = SVG(W, H, bg=PAPER)
    cols = [(300, 0.92, 0), (600, 0.62, 3), (900, 0.50, 2)]
    top, base, cw = 176, 646, 132
    for i, (cx, f, mk) in enumerate(cols):
        s.add(emark(mk, cx, 116, 30, INK, 3.6))
        s.add(rect(cx-cw/2, top, cw, base-top, fill=HAIR, r=cw/2))
        hgt = (base-top) * f
        s.add(rect(cx-cw/2, base-hgt, cw, hgt, fill=INK, r=cw/2))
    s.add(line(96, base+30, 1104, base+30, INK, 3.4))
    cx, f, _ = cols[active]
    hgt = (base-top) * f
    s.add(circle(cx, base-hgt+cw/2, 21, fill=ACCENT))
    s.add(rect(cx-cw/2, base+46, cw, 14, fill=ACCENT, r=7))
    return s

# ── the transition · one citation, seen close ────────────────────────────────
def macro():
    W, H = 1600, 1000
    s = SVG(W, H, bg=PAPER)
    for i in range(6):
        s.add(rect(200, 168+i*132, 1200 - (i % 3)*180, 34, fill=HAIR, r=17))
    s.add(rect(700, 400, 320, 190, fill=ACCENT, r=34))
    s.add(T('1', 860, 528, 132, 700, '#FFFFFF', 'middle'))
    return s

# ── section 01 · parsed correctly, or not at all ─────────────────────────────
def vis(parsed):
    W, H = 1200, 800
    s = SVG(W, H, bg=PAPER)
    px, py, pw, ph = 96, 132, 470, 536
    s.add(rect(px, py, pw, ph, fill=CARD, r=20, stroke=INK, sw=3.4))
    for i, f in enumerate([0.86, 0.94, 0.72, 0.9, 0.64]):
        s.add(rect(px+40, py+52+i*84, (pw-80)*f, 22, fill=HAIR2, r=11))
    if parsed:
        for i in (1, 3):
            s.add(rect(px+34, py+42+i*84, (pw-68), 42, fill='none', r=10, stroke=INK, sw=3))
    frag = [(820, 210), (1000, 330), (790, 470)]
    if not parsed:
        for fx, fy in frag:
            s.add(path(f'M{px+pw+18:.0f} {py+ph/2:.0f} C{px+pw+150:.0f} {py+ph/2:.0f} {fx-150:.0f} {fy:.0f} {fx-96:.0f} {fy:.0f}',
                       stroke=HAIR2, sw=3, dash='14 11'))
            s.add(pill(fx, fy, 190, 62, HAIR2, 3, 0.42))
    else:
        ex, ey = 900, 400
        for fx, fy in frag:
            s.add(path(f'M{px+pw+18:.0f} {py+ph/2:.0f} C{px+pw+150:.0f} {py+ph/2:.0f} {ex-230:.0f} {ey:.0f} {ex-176:.0f} {ey:.0f}',
                       stroke=INK, sw=3.2))
        s.add(rect(ex-176, ey-98, 352, 196, fill=CARD, r=22, stroke=ACCENT, sw=5))
        s.add(rect(ex-120, ey-40, 240, 26, fill=ACCENT, r=13))
        s.add(rect(ex-120, ey+8, 176, 20, fill=INK, r=10))
        s.add(rect(ex-120, ey+46, 132, 20, fill=HAIR2, r=10))
    return s

# ── section 02 · the finite set of sources a model trusts ────────────────────
def field(stage):
    W, H = 1600, 900
    s = SVG(W, H, bg=PAPER)
    seed = 20260909
    def rnd():
        nonlocal seed
        seed = (1103515245*seed + 12345) % 2147483648
        return seed/2147483648
    pts = [(60 + rnd()*1480, 60 + rnd()*780) for _ in range(46)]
    ring = [(800 + math.cos(a*math.pi/6)*318, 450 + math.sin(a*math.pi/6)*236) for a in range(12)]
    for i, (x, y) in enumerate(pts):
        if stage == 0:
            s.add(pill(x-60, y-20, 120, 40, HAIR2, 2.4, 0.4))
        elif i < 12:
            rx, ry = ring[i]
            s.add(pill(rx-60, ry-20, 120, 40, INK, 3, 0.42))
        else:
            s.add(pill(x-60, y-20, 120, 40, HAIR, 2.2, 0.4))
    if stage == 2:
        for rx, ry in ring:
            s.add(line(rx, ry, 800, 450, HAIR2, 2.4))
        s.add(page(800, 450, 260, 132, ACCENT, 5, 0.44, barcol=ACCENT))
    elif stage == 1:
        s.add(rect(800-146, 450-76, 292, 152, fill='none', r=20, stroke=HAIR2, sw=3, dash='15 12'))
    return s

# ── section 03 · sessions stitched to revenue (dark) ─────────────────────────
def attrib(done):
    W, H = 1600, 900
    s = SVG(W, H, bg=GRAPH)
    for i in range(4):
        y = 200 + i*168
        s.add(emark(i, 250, y, 30, ONDARK, 3.4))
        if done:
            s.add(path(f'M290 {y} C420 {y} 560 450 660 450', stroke=ONDARK, sw=3.4))
        else:
            s.add(path(f'M290 {y} C400 {y} 470 {y} 540 {y}', stroke='#3A3A38', sw=3, dash='15 12'))
    s.add(rect(660, 350, 300, 200, fill=DPANEL, r=22, stroke=ONDARK if done else '#4A4A48', sw=3.6))
    for i in range(3):
        s.add(rect(700, 386 + i*54, 220, 32, fill='none', r=8,
                   stroke=ONDARK if done else '#4A4A48', sw=2.6))
    if done:
        s.add(path('M960 450 C1060 450 1080 450 1160 450', stroke=ACCENT, sw=6))
    s.add(rect(1160, 402, 280, 96, fill='none', r=48, stroke=ACCENT if done else '#4A4A48', sw=4))
    if done:
        s.add(rect(1188, 434, 224, 32, fill=ACCENT, r=16))
    return s

# ── the close · the answer, and you inside it ────────────────────────────────
def final():
    """Narrow and tall, weighted right: it clears the CTA scrim and the phone crop."""
    W, H = 1600, 1200
    s = SVG(W, H, bg=PAPER)
    ax, ay, aw, ah = 830, 250, 530, 452
    s.add(rect(ax, ay, aw, ah, fill=CARD, r=22, stroke=HAIR2, sw=3))
    for i, f in enumerate([0.88, 0.94, 0.76, 0.56]):
        s.add(rect(ax+44, ay+62+i*72, (aw-88)*f, 24, fill=HAIR, r=12))
    s.add(chip(ax+84, ay+382, 76, 48, ACCENT))
    s.add(rect(ax+140, ay+370, 250, 22, fill=HAIR2, r=11))
    for i, yy in enumerate([772, 858, 944]):
        top = i == 0
        col = ACCENT if top else HAIR2
        s.add(rect(ax, yy-30, aw, 60, fill=CARD, r=30, stroke=col, sw=3.6 if top else 2.8))
        s.add(rect(ax+38, yy-9, 220 - i*44, 18, fill=col, r=9))
    return s

if __name__ == '__main__':
    for i in range(3): save(hero(i),   f'geo-hero-{i+1}')
    for i in range(3): save(engine(i), f'geo-engine-{i+1}')
    save(macro(), 'geo-macro')
    save(vis(False), 'geo-vis-1'); save(vis(True), 'geo-vis-2')
    for i in range(3): save(field(i), f'geo-field-{i+1}')
    save(attrib(False), 'geo-attrib-1'); save(attrib(True), 'geo-attrib-2')
    save(final(), 'geo-final')
