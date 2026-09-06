// SEO page visuals: each engineered object arrives with a clip-wipe, then its
// assembly clip plays exactly once and holds on the assembled frame.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasGsap = typeof window.gsap !== 'undefined';
  var figs = Array.prototype.slice.call(document.querySelectorAll('.sx-visual'));
  if (!figs.length) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      io.unobserve(en.target);
      var fig = en.target, video = fig.querySelector('video');
      if (hasGsap && !reduce) {
        gsap.fromTo(fig, { clipPath: 'inset(6% 0 0 0)', opacity: 0 }, { clipPath: 'inset(0% 0 0 0)', opacity: 1, duration: 1.2, ease: 'expo.out', clearProps: 'clip-path' });
      } else { fig.style.opacity = '1'; }
      if (video && !reduce) {
        var play = function () { var p = video.play(); if (p && p.catch) p.catch(function () {}); };
        if (video.readyState >= 2) setTimeout(play, 350); else video.addEventListener('loadeddata', function () { setTimeout(play, 350); }, { once: true });
      }
    });
  }, { threshold: 0.45 });
  figs.forEach(function (f) { io.observe(f); });
})();
