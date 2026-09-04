# Ascend Growth Partners — Homepage

A pixel-exact recreation of the Ascend Growth Partners homepage
(https://ascendgpartners.com/), homepage only, since evolved with
client-directed changes on top of the faithful base:

- Hero: left-aligned headline/copy/CTA (no logomark), concise SEO-focused
  paragraph, WebGL particle-wave background (from a video reference) recolored
  to a rich blue / deep navy / black system over layered gradient depth with a
  soft left scrim, larger type, arrow-only scroll indicator.
- "AI-powered strategies" section: rebuilt as a split layout (text left, two
  opposing vertical logo-card columns right) from a video layout reference,
  replacing the original centered headline + 6-column logo grid.
- The horizontal logo ticker between the hero and the strategies section was
  removed; the strategies deck now caps the hero directly. Section decks stack
  with rounded caps from the hero down; the scroll indicator rides the hero
  parallax and fades on scroll.
- The services section was rebuilt (from a video layout reference) as a cream
  deck with scroll-stacked cards: four service cards in brand colors pin in
  place, hold, then toss up over each other with a spring tilt while upcoming
  cards fan out as slim peeks below. Note: the body-level overflow-x clip was
  moved to <html> only, since a body clip container disables position: sticky
  page-wide.

Everything else remains verbatim from the live page, including the SVG
stroke-draw loading screen.

Note: `logos/clearstem.png` as served by the live site is a fully transparent
PNG (blank). The logo-card columns render Clearstem as a styled wordmark
instead; the horizontal ticker keeps the original (blank) asset for fidelity.

## Structure

```
index.html                  Homepage markup (verbatim from the live page)
assets/css/styles.css       All page styles (both original style blocks, cascade order preserved)
assets/js/main.js           Preloader, custom cursor, nav, mobile drawer, reveal
                            observers, hero parallax, stats counters, testimonials
assets/js/hero-wave.js      Hero background: WebGL particle-wave field recreated
                            from the client's reference video (no dependencies)
assets/js/services-stack.js  Services: scroll-driven stacked cards (spring
                            follow with tilt, fanned peeks, no dependencies)
favicon.png                 Site favicon (original asset)
logos/                      12 client logos (original assets)
uploads/                    3 case-study images (original assets)
```

### Hero background

The hero renders a real-time particle-wave field (`assets/js/hero-wave.js`,
raw WebGL, zero dependencies, ~60fps): a dotted sheet displaced by layered
simplex noise, drawn with additive blending so perspective-folded rows stack
into glowing cyan caustic strings. All constants were measured from the
reference video (1338×1206, 5.18s): palette ramp rgb(8,25,40) → rgb(40,87,100)
→ rgb(79,173,177) → rgb(86,220,219), ~6.7px dots, ~15px face-on string pitch,
374px fold amplitude, ~1.5%/s lateral drift, static camera. The morph runs at
roughly 45% of the reference's measured rate and slightly darker, per client
direction (smoother, more subtle). Geometry is anchored to reference pixels
(scaled by viewport width ÷ 1338) so the effect reads as a cover-fit of the
video at any viewport. Hover adds only a heavily-eased few-px camera drift.
If WebGL is unavailable the canvas hides and the hero falls back to its plain
black background.

The content deck stacks over the hero with the site's rounded-cap motif (the
strategies section rounds 24px over the wave, as every later section does over
its predecessor), and the hero's scroll indicator rides the content parallax
and fades out as scrolling begins, so nothing collides at any viewport height.

External runtime dependencies:

- Google Fonts — Instrument Sans (400/500/600/700) + Instrument Serif
  (italic 400 only); loaded with preconnect + display=swap
- (GSAP was removed along with the original pinned services animation; the
  page is now fully dependency-free JavaScript)

### Typography system

Instrument Sans is the primary voice (`--font-primary`): body 400, nav and
small labels 500, buttons/headings 600, hero H1 and stat numbers 700, with
tight negative tracking on display sizes. Instrument Serif Italic
(`--font-editorial`) appears only as an editorial accent: the hero word
"Dominate", the orange highlight phrases ("unleash your brand", "$50M in
revenue"), the testimonials heading and rotating quote, and "Ascend." in the
closing CTA.

## Run

Serve the project root over HTTP (paths are root-relative, as on the live site):

```
python3 -m http.server 4173
```

Then open http://localhost:4173/. A preview config is also provided in
`.claude/launch.json` (name: `ascend-homepage`).

## Fidelity notes

- The CSS/JS were split out of the original single-file page for
  maintainability. The split was verified lossless: re-inlining the four
  extracted blocks reconstructs the live HTML byte-for-byte.
- Script order and blocking semantics are unchanged (`main.js` at the end of
  `<body>` before the GSAP CDN tags; `services-scroll.js` after them), so the
  loading screen, reveal timing, and scroll behavior match the live page.
- Verified against the live site with full-page screenshot diffs at
  1440×900, 768×1024, and 375×812: 0 differing pixels at all three sizes,
  identical section offsets/heights, and identical ScrollTrigger pin geometry.
  Interactive states (three nav dropdowns incl. the case-studies mega-menu,
  mobile drawer + Services accordion, and a mid-scrub frame of the pinned
  services animation) also diff at 0 pixels.
- The only thing intentionally not reproduced is the Cloudflare analytics
  beacon the live host injects at the edge; it has no visual or behavioral
  effect on the page.
