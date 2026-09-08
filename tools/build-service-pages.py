"""Build the five Ascend service pages on the quiet system.

One image per chapter, one reveal, one turn from paper to graphite.
Copy is passed in verbatim; this file only lays it out.
Run:  python3 tools/build-service-pages.py
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY = json.load(open(os.environ.get('COPY_JSON', os.path.join(ROOT, 'tools/service-copy.json')), encoding='utf-8'))

# slug -> (image folder, hero image, [chapter images], index of the dark chapter)
ART = {
 'seo':              ('index',   'hero-active',  ['tech-aligned', 'content-organized', 'authority-connected'], 2),
 'link-building':    ('link',    'lb-hero-3',    ['lb-gap-2', 'lb-field-3', 'lb-earned-2'], 2),
 'geo':              ('geo',     'geo-hero-3',   ['geo-vis-2', 'geo-field-3', 'geo-attrib-2'], 2),
 'content-creation': ('content', 'cc-hero-3',    ['cc-demand-2', 'cc-field-3', 'cc-pipe-2'], 2),
 'email-marketing':  ('email',   'em-hero-3',    ['em-rev-2', 'em-field-3', 'em-sms', 'em-creators'], 2),
}
ALT = {
 'hero-active': 'The index complete: every layer aligned and the strongest at the top',
 'tech-aligned': 'A site’s infrastructure layers in alignment, every route open',
 'content-organized': 'Four clusters of supporting pages feeding one pillar page',
 'authority-connected': 'Links earned from outside publications arriving at one site',
 'lb-hero-3': 'A site connected to the publications that have linked to it',
 'lb-gap-2': 'A backlink profile measured against the authority the same rankings demand',
 'lb-field-3': 'Research resolved into one asset a publication would want to cite',
 'lb-earned-2': 'Pitches going out, and the links that came back',
 'geo-hero-3': 'A generated answer citing the brand as its first source',
 'geo-vis-2': 'A page a model reads as one resolved entity',
 'geo-field-3': 'The finite set of sources a model trusts, with the brand inside it',
 'geo-attrib-2': 'Answer engine sessions stitched through to revenue',
 'cc-hero-3': 'Published pieces whose value keeps compounding',
 'cc-demand-2': 'Demand measured and ranked before a word is written',
 'cc-field-3': 'Pieces organised into lanes across the buyer journey around one pillar',
 'cc-pipe-2': 'Five pieces, each with a job, feeding one pipeline',
 'em-hero-3': 'A message composed, sent, and landing at the top of the inbox',
 'em-rev-2': 'Sends measured by the revenue each one produced',
 'em-field-3': 'One list resolved into segments, each receiving its own message',
 'em-sms': 'A month of email, and the two moments that earned a text',
 'em-creators': 'An issue landing on the same day, and the list it builds',
}
NAV_SELF = {
 'seo': 'SEO', 'link-building': 'Link Building', 'geo': 'GEO',
 'content-creation': 'Content Creation', 'email-marketing': 'Email &amp; SMS',
}
SIBLING_HREF = {
 'SEO': '../seo/', 'GEO': '../geo/', 'Link Building': '../link-building/',
 'Content Creation': '../content-creation/', 'Email &amp; SMS': '../email-marketing/',
}
E = lambda s: html.escape(s, quote=False).replace('&amp;#', '&#')

_CHROME = None
def shared_chrome():
    """Nav, cursor and footer are lifted once from a built page and never edited."""
    global _CHROME
    if _CHROME is None:
        src = open(os.path.join(ROOT, 'services/seo/index.html'), encoding='utf-8').read()
        a = src.index('<!-- CUSTOM CURSOR -->')
        b = src.index('<main')
        nav = src[a:b]
        foot = src[src.index('</main>') + len('</main>'):src.index('<script src="https://cdnjs')]
        _CHROME = (nav, foot)
    return _CHROME

def nav_for(slug, nav):
    """Point every service link at its sibling, and the current page at itself."""
    out = nav
    for label, href in SIBLING_HREF.items():
        out = out.replace('<a href="../../services/%s/">%s</a>' % (href.strip('./'), label),
                          '<a href="%s">%s</a>' % (href, label))
    out = out.replace('<a href="./">SEO</a>', '<a href="../seo/">SEO</a>')
    me = NAV_SELF[slug]
    out = out.replace('<a href="%s">%s</a>' % (SIBLING_HREF[me], me), '<a href="./">%s</a>' % me)
    return out

def art_size(folder, name):
    """Intrinsic size from the artwork itself, so the layout never shifts."""
    src = open(os.path.join(ROOT, 'uploads', folder, name + '.svg'), encoding='utf-8').read()
    m = re.search(r'viewBox="[\d.-]+ [\d.-]+ ([\d.]+) ([\d.]+)"', src)
    return (round(float(m.group(1))), round(float(m.group(2)))) if m else (1600, 1000)

def stage(folder, name, eager=False):
    w, h = art_size(folder, name)
    return ('<div class="sv-stage rv" data-rv="120">'
            '<img src="../../uploads/%s/%s.svg" alt="%s" width="%d" height="%d" '
            '%s decoding="async">'
            '</div>') % (folder, name, E(ALT.get(name, '')), w, h,
                         'fetchpriority="high"' if eager else 'loading="lazy"')

def chapter(c, folder, img, dark=False):
    return ('<section class="sv-chapter">\n'
            '  <div class="sv-in">\n'
            '    <div class="sv-mid rv">\n'
            '      <span class="sv-label">%s</span>\n'
            '      <h2 class="sv-h">%s</h2>\n'
            '      <p class="sv-body">%s</p>\n'
            '    </div>\n'
            '    %s\n'
            '  </div>\n'
            '</section>') % (E(c['label']), E(c['h2']), E(c['body']), stage(folder, img))

def build(slug, d):
    folder, hero_img, chap_imgs, dark_at = ART[slug]
    nav, foot = shared_chrome()
    faq = d.get('faq') or []

    graph = [{"@type": "Service", "name": d['label'],
              "provider": {"@type": "Organization", "name": "Ascend Growth Partners", "url": "https://ascendgpartners.com/"},
              "areaServed": "North America", "url": d['canonical'], "description": d['lede']},
             {"@type": "BreadcrumbList", "itemListElement": [
               {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://ascendgpartners.com/"},
               {"@type": "ListItem", "position": 2, "name": "Services", "item": "https://ascendgpartners.com/services"},
               {"@type": "ListItem", "position": 3, "name": d['label'], "item": d['canonical']}]}]
    if faq:
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q['q'], "acceptedAnswer": {"@type": "Answer", "text": q['a']}} for q in faq]})

    head = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n'
      '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
      '<title>%s</title>\n<meta name="description" content="%s">\n'
      '<link rel="canonical" href="%s">\n'
      '<link rel="icon" href="../../favicon.png">\n<link rel="apple-touch-icon" href="../../favicon.png">\n'
      '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
      '<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">\n'
      '<link rel="stylesheet" href="../../assets/css/styles.css">\n'
      '<link rel="stylesheet" href="../../assets/css/case-studies.css">\n'
      '<link rel="stylesheet" href="../../assets/css/service-page.css">\n'
      '<link rel="preload" as="image" href="../../uploads/%s/%s.svg" fetchpriority="high">\n'
      '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
      '<meta property="og:type" content="website">\n<meta property="og:url" content="%s">\n'
      '<script type="application/ld+json">%s</script>\n'
      '</head>\n<body class="cs-page">\n') % (
        E(d['title']), d['desc'], d['canonical'], folder, hero_img,
        E(d['title']), E(d['lede'][:180]), d['canonical'],
        json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False))

    hero = ('\n<main class="sv">\n\n'
      '<section class="sv-hero" id="top">\n  <div class="sv-in">\n'
      '    <div class="rv">\n'
      '      <span class="sv-label is-accent">%s</span>\n'
      '      <h1 class="sv-h">%s</h1>\n'
      '      <p class="sv-lede">%s</p>\n'
      '      <a class="sv-btn" href="../../contact/">%s <span aria-hidden="true">&#8594;</span></a>\n'
      '    </div>\n'
      '  </div>\n  %s\n</section>\n') % (
        E(d['label']), E(d['h1']), E(d['lede']), E(d['cta']),
        stage(folder, hero_img, eager=True))

    figs = ''.join('<div class="sv-fig"><strong>%s</strong><span>%s</span></div>' % (E(f['value']), E(f['cap']))
                   for f in d['figures'])
    figures = ('\n<section class="sv-figures">\n  <div class="sv-in">\n'
               '    <div class="sv-figrow rv">%s</div>\n  </div>\n</section>\n') % figs

    chaps = d['chapters']
    before = ''.join('\n' + chapter(c, folder, chap_imgs[i]) + '\n' for i, c in enumerate(chaps[:dark_at]))
    dark_block = chapter(chaps[dark_at], folder, chap_imgs[dark_at], dark=True)
    turn = '\n<div class="sv-turn">\n%s\n</div>\n' % dark_block
    after = ''.join('\n' + chapter(c, folder, chap_imgs[dark_at + 1 + i]) + '\n'
                    for i, c in enumerate(chaps[dark_at + 1:]))

    rows = ''.join(
      '<div class="sv-row rv" data-rv="%d"><b>%02d</b><h3>%s</h3><p>%s</p></div>' % (i * 60, i + 1, E(x['title']), E(x['desc']))
      for i, x in enumerate(d['list']))
    lst = ('\n<section class="sv-list" id="deliverables" aria-labelledby="svList">\n  <div class="sv-in">\n'
           '    <div class="sv-list-head rv">\n'
           '      <span class="sv-label is-accent">What You Get</span>\n'
           '      <h2 class="sv-h" id="svList">The pieces needed to scale cleanly.</h2>\n'
           '    </div>\n    %s\n  </div>\n</section>\n') % rows

    faq_html = ''
    if faq:
        qs = ''.join(
          '<div class="sv-q"><button type="button" aria-expanded="false" aria-controls="q%d">'
          '<span class="t">%s</span><span class="pm" aria-hidden="true"></span></button>'
          '<div class="sv-a" id="q%d"><div><p>%s</p></div></div></div>' % (i + 1, E(x['q']), i + 1, E(x['a']))
          for i, x in enumerate(faq))
        faq_html = ('\n<section class="sv-faq" id="faq" aria-labelledby="svFaq">\n  <div class="sv-in">\n'
                    '    <div class="sv-faq-head rv">\n'
                    '      <span class="sv-label is-accent">FAQ</span>\n'
                    '      <h2 class="sv-h" id="svFaq">Common questions.</h2>\n'
                    '    </div>\n    <div class="rv">%s</div>\n  </div>\n</section>\n') % qs

    final = ('\n<section class="sv-final" id="ready" aria-labelledby="svReady">\n  <div class="sv-in">\n'
             '    <div class="sv-mid rv">\n'
             '      <span class="sv-label is-accent">Ready?</span>\n'
             '      <h2 class="sv-h" id="svReady">Let’s build the system that grows with you.</h2>\n'
             '      <a class="sv-btn" href="../../contact/">%s <span aria-hidden="true">&#8594;</span></a>\n'
             '    </div>\n  </div>\n</section>\n\n</main>\n') % E(d['final_cta'])

    scripts = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>\n'
               '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>\n'
               '<script src="../../assets/js/case-studies.js"></script>\n'
               '<script src="../../assets/js/service-page.js"></script>\n</body>\n</html>\n')

    doc = head + nav_for(slug, nav) + hero + figures + before + turn + after + lst + faq_html + final + foot + scripts
    out = os.path.join(ROOT, 'services', slug, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(doc)
    return len(doc)

if __name__ == '__main__':
    shared_chrome()          # cache before the first page overwrites its source
    for slug, d in COPY.items():
        n = build(slug, d)
        print('%-18s %6d chars  %d chapters  %d list  %d questions' % (slug, n, len(d['chapters']), len(d['list']), len(d.get('faq') or [])))
