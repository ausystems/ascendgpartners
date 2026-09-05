// Case Studies page: shares the homepage's nav/footer behaviors, adds filters.

// CUSTOM CURSOR
const cursor = document.getElementById('cursor');
let cursorX = 0, cursorY = 0, clientX = 0, clientY = 0;
document.addEventListener('mousemove', e => { clientX = e.clientX; clientY = e.clientY; });
(function updateCursor() {
  cursorX += (clientX - cursorX) * 0.15;
  cursorY += (clientY - cursorY) * 0.15;
  cursor.style.left = cursorX + 'px';
  cursor.style.top = cursorY + 'px';
  requestAnimationFrame(updateCursor);
})();
document.querySelectorAll('a, button').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
});

// NAV SCROLL
window.addEventListener('scroll', () => {
  document.getElementById('nav').classList.toggle('scrolled', window.scrollY > 20);
});

// MOBILE HAMBURGER + DRAWER
const navEl = document.getElementById('nav');
const hamburger = document.getElementById('navHamburger');
if (hamburger) {
  hamburger.addEventListener('click', () => navEl.classList.toggle('menu-open'));
}
document.querySelectorAll('.nav-mb-section-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const section = btn.getAttribute('data-section');
    const list = document.querySelector(`[data-section-list="${section}"]`);
    const isOpen = btn.classList.contains('open');
    document.querySelectorAll('.nav-mb-section-btn').forEach(b => b.classList.remove('open'));
    document.querySelectorAll('.nav-mb-sublist').forEach(l => l.classList.remove('open'));
    if (!isOpen) { btn.classList.add('open'); if (list) list.classList.add('open'); }
  });
});
document.querySelectorAll('.nav-mobile-drawer a').forEach(a => {
  a.addEventListener('click', () => navEl.classList.remove('menu-open'));
});

// SCROLL REVEAL
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add('visible');
  });
}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal, .reveal-stagger').forEach(el => observer.observe(el));

// WORD-MASK REVEALS — section headings use the homepage entrance
var rvReduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
(function () {
  var els = document.querySelectorAll('.rv-words');
  if (!els.length || rvReduce) return;
  els.forEach(function (el) {
    var idx = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var parts = child.textContent.split(/(\s+)/);
          var frag = document.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            var w = document.createElement('span'); w.className = 'rv-w';
            var wi = document.createElement('span'); wi.className = 'rv-wi';
            wi.textContent = p;
            wi.style.transitionDelay = (idx++ * 0.055) + 's';
            w.appendChild(wi); frag.appendChild(w);
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1 && child.tagName !== 'BR') walk(child);
      });
    })(el);
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add('rv-on');
        setTimeout(function () { en.target.classList.add('rv-done'); }, 2100);
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.25, rootMargin: '0px 0px -8% 0px' });
  els.forEach(function (el) { io.observe(el); });
})();

// FEATURED SLIDER — split-panel hero cycles the three studies (GSAP)
(function () {
  var STUDIES = [
    {
      title: 'How Ascend Growth Partners Built David Feldman and BKFC Into a Globally Recognized Combat Sports Authority',
      date: 'Jun 6, 2026',
      desc: 'Relentless press and PR that turned David Feldman and BKFC into a globally recognized combat sports authority.',
      img: '../uploads/bkfc-feldman-stage.webp',
      alt: 'David Feldman, founder of BKFC, at ringside under arena lights',
      href: 'https://ascendgpartners.com/case-studies/bare-knuckle-fc'
    },
    {
      title: "How Ascend Built Dr. Harrison Lee's Media Authority Across Beauty, Lifestyle, and Mainstream Press",
      date: 'May 4, 2026',
      desc: 'Beauty, lifestyle, and mainstream press coverage that established Dr. Harrison Lee as a household media authority.',
      img: '../uploads/dr-harrison-lee-1.webp',
      alt: 'Dr. Harrison Lee in a blue suit beside a red Ferrari',
      href: 'https://ascendgpartners.com/case-studies/dr-harrison-lee'
    },
    {
      title: 'How Ascend Growth Partners Helped Jason Wojo Build Media Authority and Automate $856K in Pipeline',
      date: 'Feb 26, 2026',
      desc: 'Media authority paired with AI-automated outreach that generated $856K in qualified pipeline for Jason Wojo.',
      img: '../uploads/dr-harrison-lee-2.webp',
      alt: 'Jason Wojo presenting at a whiteboard',
      href: 'https://ascendgpartners.com/case-studies/jason-wojo'
    }
  ];
  var title = document.getElementById('csxTitle');
  var date = document.getElementById('csxDate');
  var desc = document.getElementById('csxDesc');
  var read = document.getElementById('csxRead');
  var img = document.getElementById('csxImg');
  var thumbs = Array.prototype.slice.call(document.querySelectorAll('.csx-thumb'));
  if (!title || !img) return;

  STUDIES.forEach(function (s) { var i = new Image(); i.src = s.img; });

  var hasGsap = typeof window.gsap !== 'undefined' && !rvReduce;
  var current = 0;
  var animating = false;

  function split(el) {
    var text = el.textContent;
    el.textContent = '';
    text.split(/(\s+)/).forEach(function (p) {
      if (!p) return;
      if (/^\s+$/.test(p)) { el.appendChild(document.createTextNode(p)); return; }
      var w = document.createElement('span'); w.className = 'csx-w';
      var wi = document.createElement('span'); wi.className = 'csx-wi';
      wi.textContent = p;
      w.appendChild(wi); el.appendChild(w);
    });
    return el.querySelectorAll('.csx-wi');
  }

  // second stacked image layer for seamless crossfades
  var imgB = img.cloneNode();
  imgB.removeAttribute('id');
  imgB.style.opacity = '0';
  imgB.alt = '';
  img.parentElement.appendChild(imgB);

  function setText(i) {
    var s = STUDIES[i];
    title.textContent = s.title;
    date.textContent = s.date;
    desc.textContent = s.desc;
    read.href = s.href;
  }

  function markActive(i) {
    thumbs.forEach(function (t, k) { t.classList.toggle('active', k === i); });
  }

  function goTo(i) {
    if (animating || i === current) return;
    current = i;
    markActive(i);
    if (!hasGsap) {
      setText(i);
      img.src = STUDIES[i].img; img.alt = STUDIES[i].alt;
      return;
    }
    animating = true;
    var s = STUDIES[i];
    // image: true crossfade on the stacked layer, never a blank frame
    imgB.src = s.img;
    gsap.fromTo(imgB, { opacity: 0, scale: 1.06 }, {
      opacity: 1, scale: 1, duration: 0.75, ease: 'expo.out',
      onComplete: function () {
        img.src = s.img; img.alt = s.alt;
        gsap.set(imgB, { opacity: 0, scale: 1 });
      }
    });
    // text: quick exit, immediate re-entrance in the homepage word-mask style
    var oldWords = title.querySelectorAll('.csx-wi');
    var tl = gsap.timeline({ onComplete: function () { animating = false; } });
    tl.to(oldWords, { yPercent: 135, duration: 0.26, stagger: 0.01, ease: 'power2.in' }, 0);
    tl.to([date, desc, read], { opacity: 0, y: 10, duration: 0.22, ease: 'power2.in' }, 0);
    tl.add(function () {
      setText(i);
      var words = split(title);
      gsap.set(words, { yPercent: 140, rotate: 3 });
      gsap.set([date, desc, read], { opacity: 0, y: 12 });
      gsap.to(words, { yPercent: 0, rotate: 0, duration: 0.7, stagger: 0.045, ease: 'expo.out' });
      gsap.to([date, desc, read], { opacity: 1, y: 0, duration: 0.55, stagger: 0.06, ease: 'expo.out', delay: 0.05 });
    }, 0.27);
    tl.to({}, { duration: 0.62 }); // release once the entrance has landed
  }

  document.getElementById('csxPrev').addEventListener('click', function () {
    goTo((current + STUDIES.length - 1) % STUDIES.length);
  });
  document.getElementById('csxNext').addEventListener('click', function () {
    goTo((current + 1) % STUDIES.length);
  });
  thumbs.forEach(function (t) {
    t.addEventListener('click', function () { goTo(parseInt(t.getAttribute('data-i'), 10)); });
  });

  // entrance: same word-mask rise as the homepage headings
  if (hasGsap) {
    var words = split(title);
    gsap.set(words, { yPercent: 140, rotate: 3 });
    gsap.set([date, desc, read], { opacity: 0, y: 12 });
    gsap.to(words, { yPercent: 0, rotate: 0, duration: 0.85, stagger: 0.05, ease: 'expo.out', delay: 0.25 });
    gsap.to([date, desc, read], { opacity: 1, y: 0, duration: 0.7, stagger: 0.08, ease: 'expo.out', delay: 0.4 });
    gsap.fromTo(img, { opacity: 0, scale: 1.06 }, { opacity: 1, scale: 1, duration: 0.9, ease: 'expo.out', delay: 0.2 });
  }
})();

// CASE STUDY FILTERS
(function () {
  const pills = document.querySelectorAll('.cs-filter');
  const cards = document.querySelectorAll('[data-tags]');
  const featured = document.getElementById('csFeatured');
  pills.forEach(pill => {
    pill.addEventListener('click', () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      const f = pill.getAttribute('data-filter');
      let featVisible = 0;
      cards.forEach(card => {
        const show = f === 'all' || card.getAttribute('data-tags').split(' ').indexOf(f) !== -1;
        card.classList.toggle('cs-hidden', !show);
        if (show && card.classList.contains('cs-mini')) featVisible++;
      });
      if (featured) featured.classList.toggle('cs-hidden', featVisible === 0);
    });
  });
})();

// FOOTER TYPEWRITER — same one-shot reveal as the homepage
(function () {
  var giant = document.querySelector('.footer-giant');
  if (!giant) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var span = giant.querySelector('span');
  var text = span.textContent;
  span.textContent = '';
  var letters = [];
  for (var i = 0; i < text.length; i++) {
    var l = document.createElement('i');
    l.className = 'ft-letter';
    l.textContent = text[i] === ' ' ? ' ' : text[i];
    span.appendChild(l);
    letters.push(l);
  }
  giant.classList.add('type-ready');
  var played = false;
  var io = new IntersectionObserver(function (entries) {
    if (played || !entries[0].isIntersecting) return;
    played = true;
    io.disconnect();
    letters.forEach(function (el, idx) {
      setTimeout(function () { el.classList.add('on'); }, 100 + idx * 26);
    });
  }, { threshold: 0.35 });
  io.observe(giant);
})();

// SMOOTH WHEEL SCROLL (desktop pointers; touch keeps native momentum)
if (window.matchMedia('(pointer: fine)').matches) {
  let smoothTarget = 0;
  let smoothCurrent = 0;
  let smoothActive = false;
  const maxScroll = () => document.documentElement.scrollHeight - window.innerHeight;
  window.addEventListener('wheel', (e) => {
    if (e.ctrlKey || e.metaKey) return;
    e.preventDefault();
    const delta = e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY;
    if (!smoothActive) { smoothTarget = window.scrollY; smoothCurrent = window.scrollY; }
    smoothTarget = Math.max(0, Math.min(smoothTarget + delta, maxScroll()));
    if (!smoothActive) { smoothActive = true; requestAnimationFrame(smoothStep); }
  }, { passive: false });
  function smoothStep() {
    smoothCurrent += (smoothTarget - smoothCurrent) * 0.11;
    if (Math.abs(smoothTarget - smoothCurrent) < 0.6) {
      window.scrollTo({ top: smoothTarget, behavior: 'instant' });
      smoothActive = false;
      return;
    }
    window.scrollTo({ top: smoothCurrent, behavior: 'instant' });
    requestAnimationFrame(smoothStep);
  }
}
