// PRELOADER
window.addEventListener('load', () => {
  setTimeout(() => {
    document.getElementById('preloader').classList.add('done');
    animateHero();
  }, 3000);
});

// HERO ANIMATION
function animateHero() {
  const wordmark = document.querySelector('.hero-wordmark');
  const sub = document.querySelector('.hero-sub');
  const ctaRow = document.querySelector('.hero-cta-row');

  setTimeout(() => {
    wordmark.style.transition = 'opacity 1s var(--ease-out-expo), transform 1s var(--ease-out-expo)';
    wordmark.style.opacity = '1';
    wordmark.style.transform = 'translateY(0)';
  }, 200);

  if (sub) setTimeout(() => {
    sub.style.transition = 'opacity 1s var(--ease-out-expo), transform 1s var(--ease-out-expo)';
    sub.style.opacity = '1';
    sub.style.transform = 'translateY(0)';
  }, 500);

  if (ctaRow) setTimeout(() => {
    ctaRow.style.transition = 'opacity 1s var(--ease-out-expo), transform 1s var(--ease-out-expo)';
    ctaRow.style.opacity = '1';
    ctaRow.style.transform = 'translateY(0)';
  }, 750);
}

// CUSTOM CURSOR
const cursor = document.getElementById('cursor');
let cursorX = 0, cursorY = 0, clientX = 0, clientY = 0;
document.addEventListener('mousemove', e => { clientX = e.clientX; clientY = e.clientY; });
function updateCursor() {
  cursorX += (clientX - cursorX) * 0.15;
  cursorY += (clientY - cursorY) * 0.15;
  cursor.style.left = cursorX + 'px';
  cursor.style.top = cursorY + 'px';
  requestAnimationFrame(updateCursor);
}
updateCursor();
document.querySelectorAll('a, button, .service-card, .testimonial-dot, .case-card, .client-cell, .btn-accent').forEach(el => {
  el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
});

// NAV SCROLL
window.addEventListener('scroll', () => {
  document.getElementById('nav').classList.toggle('scrolled', window.scrollY > 20);
});

// MOBILE HAMBURGER
const navEl = document.getElementById('nav');
const hamburger = document.getElementById('navHamburger');
if (hamburger) {
  hamburger.addEventListener('click', () => {
    navEl.classList.toggle('menu-open');
  });
}
// Accordion sections
document.querySelectorAll('.nav-mb-section-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const section = btn.getAttribute('data-section');
    const list = document.querySelector(`[data-section-list="${section}"]`);
    const isOpen = btn.classList.contains('open');
    // close all
    document.querySelectorAll('.nav-mb-section-btn').forEach(b => b.classList.remove('open'));
    document.querySelectorAll('.nav-mb-sublist').forEach(l => l.classList.remove('open'));
    // open clicked
    if (!isOpen) { btn.classList.add('open'); if (list) list.classList.add('open'); }
  });
});
// Close menu on link click
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

// PARALLAX ON HERO
window.addEventListener('scroll', () => {
  const s = window.scrollY;
  const hero = document.querySelector('.hero-content');
  if (s < window.innerHeight) {
    hero.style.transform = `translateY(${s * 0.25}px)`;
    hero.style.opacity = 1 - (s / window.innerHeight) * 0.7;
  }
});

// SCROLL INDICATOR
// The hero scroll control is a hash anchor. /smooth-scroll.js intercepts it for animated scrolling.

// STATS COUNTER
const statsObs = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.querySelectorAll('.stat-val').forEach(el => {
        const target = parseInt(el.dataset.target);
        animateNum(el, target);
      });
      statsObs.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('.stats-bar').forEach(el => statsObs.observe(el));

function animateNum(el, end) {
  let start = null;
  function step(ts) {
    if (!start) start = ts;
    const p = Math.min((ts - start) / 1800, 1);
    const eased = 1 - Math.pow(1 - p, 4);
    el.textContent = Math.floor(eased * end) + '%';
    if (p < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

