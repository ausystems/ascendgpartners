// THE ASCEND INDEX — motion engine. Scroll is a camera moving through an information machine.
// Every movement stands for indexing, ranking, alignment, organization, connection, or measurement.
(function () {
  if (typeof gsap === 'undefined') return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobile = window.matchMedia('(max-width: 600px)').matches;
  var hasST = typeof ScrollTrigger !== 'undefined';
  if (hasST) gsap.registerPlugin(ScrollTrigger);
  var EASE = 'expo.out';

  // words behind masks, for typography that reveals by narrative rather than fade
  function splitWords(el) {
    var out = [];
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var frag = document.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            var w = document.createElement('span'); w.className = 'ix-w'; w.style.cssText = 'display:inline-block;overflow:hidden;vertical-align:bottom;padding:0.12em 0.06em;margin:-0.12em -0.06em';
            var i = document.createElement('span'); i.className = 'ix-wi'; i.style.display = 'inline-block'; i.textContent = p;
            w.appendChild(i); frag.appendChild(w); out.push(i);
          });
          node.replaceChild(frag, c);
        } else if (c.nodeType === 1 && c.tagName !== 'BR') walk(c);
      });
    })(el);
    return out;
  }

  // ---------- 01 HERO ----------
  var hero = document.querySelector('.ix-hero');
  if (hero) {
    var label = hero.querySelector('.ix-label'), l1 = hero.querySelector('.l1'), l2 = hero.querySelector('.l2');
    var mono = hero.querySelector('.ix-hero-monolith'), copy = hero.querySelector('.ix-hero-copy'), cta = hero.querySelector('.ix-hero-cta');
    var monoImgs = mono ? Array.prototype.slice.call(mono.querySelectorAll('img')) : [];
    var w1 = splitWords(l1), w2 = splitWords(l2);
    if (reduce) {
      [label, copy, cta].forEach(function (e) { if (e) e.style.opacity = 1; });
      if (mono) { mono.style.opacity = 1; mono.style.filter = 'none'; mono.style.transform = 'none'; }
      if (monoImgs[2]) monoImgs[2].style.opacity = 1;
    } else {
      gsap.set(w1, { yPercent: 110 }); gsap.set(w2, { xPercent: 40, opacity: 0 });
      var tl = gsap.timeline({ delay: 0.05 });
      tl.to(label, { opacity: 1, duration: 0.8, ease: 'power2.out' }, 0.15)
        .to(w1, { yPercent: 0, duration: 1.2, ease: EASE, stagger: 0.06 }, 0.35)
        .to(w2, { xPercent: 0, opacity: 1, duration: 1.2, ease: EASE, stagger: 0.06 }, 0.58)
        .to(mono, { opacity: 1, filter: 'blur(0px)', scale: 1, duration: 1.6, ease: EASE }, 0.78)
        .to(monoImgs[1] || {}, { opacity: 1, duration: 1.4, ease: 'power2.inOut' }, 0.95)
        .to(copy, { opacity: 1, duration: 0.9, ease: 'power2.out' }, 1.10)
        .to(cta, { opacity: 1, duration: 0.9, ease: 'power2.out' }, 1.20);
      if (hasST && !mobile && monoImgs[2]) {
        ScrollTrigger.create({ trigger: hero, start: 'top top', end: 'bottom top', scrub: 0.6, onUpdate: function (st) {
          monoImgs[2].style.opacity = Math.min(1, st.progress * 1.6);
          gsap.set(mono, { y: st.progress * -60 });
        } });
      }
    }
  }

  // ---------- 02 SEO ENGINE ----------
  var engine = document.querySelector('.ix-engine');
  if (engine) {
    var stats = Array.prototype.slice.call(engine.querySelectorAll('.ix-stat'));
    var plates = Array.prototype.slice.call(engine.querySelectorAll('.ix-engine-plate img'));
    var idx = Array.prototype.slice.call(engine.querySelectorAll('.ix-engine-index span'));
    function setEngine(p) {
      var step = Math.min(2, Math.floor(p * 3));
      stats.forEach(function (s, i) { var on = i === step; s.style.opacity = on ? 1 : 0; s.style.transform = on ? 'translateY(0)' : 'translateY(' + (i < step ? -14 : 14) + 'px)'; });
      idx.forEach(function (s, i) { s.classList.toggle('on', i === step); });
      var x = p * 2; plates.forEach(function (img, i) { img.style.opacity = Math.max(0, 1 - Math.abs(x - i)); });
    }
    stats.forEach(function (s) { s.style.transition = 'opacity 0.5s, transform 0.7s cubic-bezier(0.16,1,0.3,1)'; });
    if (reduce || mobile || !hasST) {
      // at rest: all three readings stacked, the first plate held
      stats.forEach(function (s) { s.style.opacity = 1; s.style.transform = 'none'; });
      plates.forEach(function (img, i) { img.style.opacity = i === 0 ? 1 : 0; });
    } else {
      setEngine(0);
      ScrollTrigger.create({ trigger: engine.querySelector('.ix-engine-track'), start: 'top top', end: 'bottom bottom', scrub: 0.4, onUpdate: function (st) { setEngine(st.progress); } });
    }
  }
  // measurement tracks
  document.querySelectorAll('.ix-track').forEach(function (t) {
    var v = parseFloat(t.getAttribute('data-v')) / 100, b = t.querySelector('.rail b'), i = t.querySelector('.rail i');
    function run() { gsap.to(b, { scaleX: v, duration: 1.6, ease: EASE }); gsap.to(i, { left: (v * 100) + '%', duration: 1.6, ease: EASE }); }
    if (reduce || !hasST) { b.style.transform = 'scaleX(' + v + ')'; i.style.left = (v * 100) + '%'; }
    else ScrollTrigger.create({ trigger: t, start: 'top 80%', once: true, onEnter: run });
  });
  // editorial statistics + section headlines: mask in once
  document.querySelectorAll('[data-mask]').forEach(function (el) {
    if (reduce || !hasST) return;
    var words = splitWords(el); gsap.set(words, { yPercent: 110 });
    ScrollTrigger.create({ trigger: el, start: 'top 85%', once: true, onEnter: function () { gsap.to(words, { yPercent: 0, duration: 1.1, ease: EASE, stagger: 0.05 }); } });
  });

  // ---------- transition: entering the machine ----------
  var enter = document.querySelector('.ix-enter');
  if (enter && hasST && !reduce && !mobile) {
    var plate = enter.querySelector('.ix-plate'), veil = enter.querySelector('.veil');
    ScrollTrigger.create({ trigger: enter, start: 'top top', end: 'bottom bottom', scrub: 0.5, onUpdate: function (st) {
      var p = st.progress; gsap.set(plate, { scale: 1 + p * 0.9 }); veil.style.opacity = Math.max(0, (p - 0.55) / 0.45);
    } });
  }

  // ---------- 03 TECHNICAL SEO ----------
  var tech = document.querySelector('.ix-tech');
  if (tech) {
    var timgs = Array.prototype.slice.call(tech.querySelectorAll('.ix-tech-visual .ix-plate img'));
    var notes = Array.prototype.slice.call(tech.querySelectorAll('.ix-tech-notes span'));
    if (reduce || !hasST) { if (timgs[1]) timgs[1].style.opacity = 1; notes.forEach(function (n) { n.classList.add('on'); }); }
    else ScrollTrigger.create({ trigger: tech.querySelector('.ix-tech-visual'), start: 'top 75%', end: 'bottom 45%', scrub: 0.5, onUpdate: function (st) {
      var p = st.progress; if (timgs[1]) timgs[1].style.opacity = Math.max(0, Math.min(1, (p - 0.35) / 0.4));
      notes.forEach(function (n, i) { n.classList.toggle('on', p > 0.08 + i * 0.1); n.classList.toggle('hot', n.getAttribute('data-hot') === '1' && p > 0.2 && p < 0.72); });
    } });
  }

  // ---------- 04 CONTENT STRATEGY ----------
  var content = document.querySelector('.ix-content');
  if (content) {
    var cimgs = Array.prototype.slice.call(content.querySelectorAll('.ix-content-stage .ix-plate img'));
    var stateB = content.querySelector('.ix-content-state b');
    // each page supplies its own stage labels; the SEO page's remain the default
    var states = ((stateB && stateB.parentNode.getAttribute('data-states')) ||
      'Hundreds of unrelated pages|Clusters emerge|One topic, fully supported').split('|');
    function setContent(p) { var x = p * 2; cimgs.forEach(function (img, i) { img.style.opacity = i === 0 ? 1 : Math.max(0, 1 - Math.abs(x - i)); }); if (stateB) stateB.textContent = states[Math.min(2, Math.floor(p * 3))]; }
    if (reduce || mobile || !hasST) { if (cimgs[2]) { cimgs[2].style.opacity = 1; } if (stateB) stateB.textContent = states[2]; }
    else ScrollTrigger.create({ trigger: content.querySelector('.ix-content-track'), start: 'top top', end: 'bottom bottom', scrub: 0.5, onUpdate: function (st) { setContent(st.progress); } });
  }

  // ---------- plane flips to its graphite side ----------
  var flip = document.querySelector('.ix-flip');
  if (flip) {
    var card = flip.querySelector('.card');
    if (reduce || mobile || !hasST) gsap.set(card, { rotateY: 180 });
    else ScrollTrigger.create({ trigger: flip, start: 'top top', end: 'bottom bottom', scrub: 0.4, onUpdate: function (st) { gsap.set(card, { rotateY: st.progress * 180 }); } });
  }

  // ---------- 05 AUTHORITY ----------
  var auth = document.querySelector('.ix-auth');
  if (auth) {
    var word = auth.querySelector('.word'), aimgs = Array.prototype.slice.call(auth.querySelectorAll('.ix-auth-visual .ix-plate img'));
    var drift = ((word && word.getAttribute('data-drift')) || '-6,-20').split(',').map(parseFloat);
    var dFrom = drift[0], dTo = drift[1];
    if (reduce || !hasST) { if (aimgs[1]) aimgs[1].style.opacity = 1; }
    else {
      ScrollTrigger.create({ trigger: auth, start: 'top bottom', end: 'bottom top', scrub: 0.6, onUpdate: function (st) { gsap.set(word, { xPercent: dFrom + st.progress * (dTo - dFrom) }); } });
      ScrollTrigger.create({ trigger: auth.querySelector('.ix-auth-visual'), start: 'top 80%', end: 'bottom 40%', scrub: 0.5, onUpdate: function (st) {
        if (aimgs[1]) aimgs[1].style.opacity = Math.max(0, Math.min(1, (st.progress - 0.2) / 0.5));
      } });
    }
  }

  // ---------- 06 THE INSTRUMENT ----------
  var inst = document.querySelector('.ix-inst');
  if (inst) {
    var nums = Array.prototype.slice.call(inst.querySelectorAll('.ix-inst-num span'));
    var items = Array.prototype.slice.call(inst.querySelectorAll('.ix-inst-copy .item'));
    var vis = Array.prototype.slice.call(inst.querySelectorAll('.ix-inst-visual .ix-plate img'));
    var marks = Array.prototype.slice.call(inst.querySelectorAll('.ix-inst-rail i'));
    var cur = -1;
    function setStep(s) {
      if (s === cur) return; cur = s;
      nums.forEach(function (n, i) { gsap.to(n, { opacity: i === s ? 1 : 0, y: i === s ? 0 : (i < s ? -30 : 30), duration: 0.6, ease: EASE }); });
      items.forEach(function (n, i) { gsap.to(n, { opacity: i === s ? 1 : 0, y: i === s ? 0 : (i < s ? -12 : 12), duration: 0.55, ease: EASE }); });
      vis.forEach(function (img, i) { gsap.to(img, { opacity: i === s ? 1 : 0, duration: 0.7, ease: 'power2.inOut' }); });
      marks.forEach(function (m, i) { m.classList.toggle('on', i === s); });
    }
    if (hasST && !reduce && !window.matchMedia('(max-width: 1024px)').matches) {
      ScrollTrigger.create({ trigger: inst.querySelector('.ix-inst-track'), start: 'top top', end: 'bottom bottom', scrub: true, onUpdate: function (st) { setStep(Math.min(5, Math.floor(st.progress * 6))); } });
    }
    setStep(0);
  }

  // ---------- 07 FAQ ----------
  document.querySelectorAll('.ix-q button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement, open = item.classList.contains('open');
      document.querySelectorAll('.ix-q.open').forEach(function (o) { o.classList.remove('open'); o.querySelector('button').setAttribute('aria-expanded', 'false'); });
      if (!open) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  // ---------- 08 FINAL ----------
  var fin = document.querySelector('.ix-final');
  if (fin) {
    var fplate = fin.querySelector('.ix-plate'), fcta = fin.querySelector('.ix-btn');
    if (fcta && fplate && !reduce) {
      fcta.addEventListener('mouseenter', function () { gsap.to(fplate, { y: -5, duration: 0.8, ease: EASE }); });
      fcta.addEventListener('mouseleave', function () { gsap.to(fplate, { y: 0, duration: 0.8, ease: EASE }); });
    }
    if (hasST && !reduce && !mobile) ScrollTrigger.create({ trigger: fin, start: 'top bottom', end: 'bottom top', scrub: 0.6, onUpdate: function (st) { gsap.set(fplate, { scale: 1.06 - st.progress * 0.06 }); } });
  }
})();
