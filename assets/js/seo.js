// SEO service page: progress line, query typing, engine meters, FAQ, index rail.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = typeof window.gsap !== 'undefined';

  // progress line
  var bar = document.getElementById('sxProgress');
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, window.scrollY / max) : 0) + ')';
    });
  }, { passive: true });

  // query line: the names on this page, typed as searches, each resolving to "found"
  var q = document.getElementById('sxQuery');
  var res = document.getElementById('sxResult');
  if (q) {
    var names = ['Mel Robbins', 'Gymshark', 'BKFC', 'Ed Mylett', 'Tim Grover'];
    if (reduce) { q.textContent = names[0]; }
    else {
      var ni = 0, ci = 0, deleting = false;
      var tick = function () {
        var name = names[ni];
        if (!deleting) {
          ci++;
          q.textContent = name.slice(0, ci);
          if (res) res.style.opacity = ci === name.length ? '1' : '0';
          if (ci === name.length) { deleting = true; setTimeout(tick, 1700); return; }
          setTimeout(tick, 70 + Math.random() * 60);
        } else {
          ci--;
          q.textContent = name.slice(0, ci);
          if (res) res.style.opacity = '0';
          if (ci === 0) { deleting = false; ni = (ni + 1) % names.length; setTimeout(tick, 420); return; }
          setTimeout(tick, 34);
        }
      };
      setTimeout(tick, 900);
    }
  }

  // engine meters: track draws to value, numeral counts up, once
  var meters = document.querySelectorAll('.sx-meter');
  if (meters.length) {
    var mio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        mio.unobserve(en.target);
        var m = en.target;
        m.classList.add('on');
        var out = m.querySelector('.val b');
        var target = parseInt(m.getAttribute('data-v'), 10);
        if (reduce || !hasGsap) { out.textContent = target + '%'; return; }
        var o = { v: 0 };
        gsap.to(o, { v: target, duration: 1.5, ease: 'expo.out', onUpdate: function () { out.textContent = Math.round(o.v) + '%'; } });
      });
    }, { threshold: 0.5 });
    meters.forEach(function (m) { mio.observe(m); });
  }

  // faq accordion (one open at a time)
  document.querySelectorAll('.sx-q button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement;
      var open = item.classList.contains('open');
      document.querySelectorAll('.sx-q.open').forEach(function (o) { o.classList.remove('open'); o.querySelector('button').setAttribute('aria-expanded', 'false'); });
      if (!open) { item.classList.add('open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });

  // index rail: visible after the cover, tracks the current section
  var rail = document.getElementById('sxRail');
  if (rail) {
    var links = Array.prototype.slice.call(rail.querySelectorAll('a')).concat(Array.prototype.slice.call(document.querySelectorAll('#sxForces a')));
    var targets = []; links.forEach(function (a) { var t = document.querySelector(a.getAttribute('href')); if (t && targets.indexOf(t) === -1) targets.push(t); });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = '#' + en.target.id;
        links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === id); });
      });
    }, { rootMargin: '-40% 0px -50% 0px' });
    targets.forEach(function (t) { spy.observe(t); });
    var cover = document.querySelector('.sx-cover');
    var showIo = new IntersectionObserver(function (entries) {
      rail.classList.toggle('show', !entries[0].isIntersecting);
    }, { threshold: 0.2 });
    if (cover) showIo.observe(cover);
  }
})();
