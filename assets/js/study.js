// Case study pages: reading progress, hero parallax, stat count-ups.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = typeof window.gsap !== 'undefined';

  // reading progress line
  var bar = document.getElementById('bkProgress');
  var fig = document.querySelector('.bk-fig');
  var img = fig ? fig.querySelector('img') : null;
  var ticking = false;
  function onScroll() {
    ticking = false;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ')';
    if (img && !reduce) {
      var r = fig.getBoundingClientRect();
      if (r.bottom > 0 && r.top < window.innerHeight) {
        var p = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight;
        img.style.translate = '0 ' + (p * 6).toFixed(2) + '%';
      }
    }
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  // hero image: clip-wipe reveal on load
  if (fig) {
    if (hasGsap && !reduce) {
      gsap.fromTo(fig, { clipPath: 'inset(6% 0 0 0)', opacity: 0 },
        { clipPath: 'inset(0% 0 0 0)', opacity: 1, duration: 1.3, ease: 'expo.out', delay: 0.35, clearProps: 'clip-path' });
      gsap.fromTo(img, { scale: 1.08 }, { scale: 1, duration: 1.6, ease: 'expo.out', delay: 0.35 });
    } else {
      fig.style.opacity = '1';
    }
  }

  // count-ups: numbers roll to their value the first time the strip is seen
  var counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;
  function run(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var prefix = el.getAttribute('data-prefix') || '';
    var suffix = el.getAttribute('data-suffix') || '';
    var out = el.querySelector('b');
    if (reduce || !hasGsap) { out.textContent = prefix + target + suffix; return; }
    var obj = { v: 0 };
    gsap.to(obj, {
      v: target, duration: 1.6, ease: 'expo.out',
      onUpdate: function () { out.textContent = prefix + Math.round(obj.v) + suffix; }
    });
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      io.unobserve(en.target);
      run(en.target);
    });
  }, { threshold: 0.4 });
  counters.forEach(function (c) { io.observe(c); });
})();
