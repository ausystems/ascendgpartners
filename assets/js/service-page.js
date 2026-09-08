// Ascend service pages: three animations, and nothing else.
//   1 · a single reveal as each block arrives
//   2 · the turn, where the page moves from paper to graphite and back
//   3 · a slow settle on the image inside the dark stretch
// All of it stops under prefers-reduced-motion, which leaves the finished state.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── 1 · reveal ────────────────────────────────────────────────────────────
  var targets = [].slice.call(document.querySelectorAll('.rv'));
  if (reduce || !('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var d = parseFloat(en.target.getAttribute('data-rv')) || 0;
        setTimeout(function () { en.target.classList.add('is-in'); }, d);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
  }

  // ── 2 · the turn ──────────────────────────────────────────────────────────
  // Graphite arrives as an inset, rounded panel and opens to full bleed. The
  // type on it is light throughout, so contrast is never in question; what the
  // eye reads as "the page going dark" is the panel opening.
  var turn = document.querySelector('.sv-turn');
  if (turn) {
    var INSET = 46, RADIUS = 30;
    var setPanel = function (open) {
      var k = 1 - open;
      turn.style.setProperty('--turn-x', (INSET * k).toFixed(1) + 'px');
      turn.style.setProperty('--turn-r', (RADIUS * k).toFixed(1) + 'px');
    };

    if (reduce || typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
      setPanel(1);
    } else {
      gsap.registerPlugin(ScrollTrigger);
      setPanel(0);
      ScrollTrigger.create({
        trigger: turn, start: 'top 94%', end: 'top 52%', scrub: 0.7,
        onUpdate: function (st) { setPanel(st.progress); }
      });
      ScrollTrigger.create({
        trigger: turn, start: 'bottom 56%', end: 'bottom 10%', scrub: 0.7,
        onUpdate: function (st) { setPanel(1 - st.progress); }
      });

      // ── 3 · the settle ──────────────────────────────────────────────────
      var art = turn.querySelector('.sv-stage img');
      if (art) {
        gsap.fromTo(art, { scale: 1.04 }, {
          scale: 1, ease: 'none',
          scrollTrigger: { trigger: art, start: 'top 92%', end: 'bottom 45%', scrub: 0.8 }
        });
      }
    }
  }

  // ── questions ─────────────────────────────────────────────────────────────
  [].slice.call(document.querySelectorAll('.sv-q button')).forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.parentElement, open = item.classList.contains('is-open');
      [].slice.call(document.querySelectorAll('.sv-q.is-open')).forEach(function (o) {
        o.classList.remove('is-open');
        o.querySelector('button').setAttribute('aria-expanded', 'false');
      });
      if (!open) { item.classList.add('is-open'); btn.setAttribute('aria-expanded', 'true'); }
    });
  });
})();
