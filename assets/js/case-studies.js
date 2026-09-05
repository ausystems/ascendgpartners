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
