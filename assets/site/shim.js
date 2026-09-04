// Vanilla runtime for the statically captured pages: nav scroll state,
// mobile drawer + accordion toggles (recorded style pairs), form submits.
(function () {
  // --- nav scroll background (matches the live site's scrolled style) ---
  var navs = document.querySelectorAll('nav');
  var initial = [];
  navs.forEach(function (n, i) {
    initial[i] = {
      background: n.style.background,
      backdropFilter: n.style.backdropFilter,
      webkitBackdropFilter: n.style.webkitBackdropFilter,
      borderBottom: n.style.borderBottom,
    };
  });
  function onScroll() {
    var sc = window.scrollY > 24;
    navs.forEach(function (n, i) {
      if (sc) {
        n.style.background = 'rgba(10, 15, 40, 0.97)';
        n.style.backdropFilter = 'blur(20px)';
        n.style.webkitBackdropFilter = 'blur(20px)';
        n.style.borderBottom = '1px solid rgba(255, 255, 255, 0.06)';
      } else {
        n.style.background = initial[i].background;
        n.style.backdropFilter = initial[i].backdropFilter;
        n.style.webkitBackdropFilter = initial[i].webkitBackdropFilter;
        n.style.borderBottom = initial[i].borderBottom;
      }
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // --- recorded toggles (hamburger drawer, drawer accordions) ---
  var data = document.getElementById('agp-toggles');
  if (data) {
    var toggles;
    try { toggles = JSON.parse(data.textContent); } catch (e) { toggles = []; }
    toggles.forEach(function (tg) {
      var btn = document.querySelector('[data-agp-btn="' + tg.btn + '"]');
      if (!btn || !tg.targets.length) return;
      var open = false;
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        open = !open;
        tg.targets.forEach(function (t) {
          var el = document.querySelector('[data-agp-t="' + t.t + '"]');
          if (!el) return;
          el.setAttribute('style', open ? t.openStyle : t.closedStyle);
          var cls = open ? t.openClass : t.closedClass;
          if (cls !== null && cls !== undefined) el.setAttribute('class', cls);
        });
      });
    });
  }

  // --- desktop dropdown hovers (recorded open/closed style pairs) ---
  var hdata = document.getElementById('agp-hovers');
  if (hdata) {
    var hovers;
    try { hovers = JSON.parse(hdata.textContent); } catch (e) { hovers = []; }
    hovers.forEach(function (hv) {
      var trig = document.querySelector('[data-agp-hbtn="' + hv.btn + '"]');
      if (!trig || !hv.targets.length) return;
      var item = trig.parentElement || trig;
      var closeTimer = null;
      function setState(open) {
        hv.targets.forEach(function (t) {
          var el = document.querySelector('[data-agp-h="' + t.t + '"]');
          if (el) el.setAttribute('style', open ? t.open : t.closed);
        });
      }
      item.addEventListener('mouseenter', function () {
        if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
        setState(true);
      });
      item.addEventListener('mouseleave', function () {
        closeTimer = setTimeout(function () { setState(false); }, 140);
      });
    });
  }

  // --- close drawer when a drawer link is clicked (navigation happens anyway) ---

  // --- forms: post to the live API endpoint ---
  document.querySelectorAll('form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var btn = form.querySelector('button[type="submit"], button:not([type])');
      if (btn) { btn.disabled = true; btn.style.opacity = '0.6'; }
      fetch('https://ascendgpartners.com/api/forms/submit', { method: 'POST', body: fd, mode: 'no-cors' })
        .then(function () { done(true); })
        .catch(function () { done(false); });
      function done(ok) {
        var msg = document.createElement('p');
        msg.style.cssText = 'margin-top:1rem;font-size:0.95rem;font-weight:600;color:' + (ok ? '#7fd18f' : '#e8613c');
        msg.textContent = ok ? "Thank you! Your message has been sent. We'll be in touch shortly."
                             : 'Something went wrong. Please email us directly.';
        form.appendChild(msg);
        if (btn && !ok) { btn.disabled = false; btn.style.opacity = ''; }
      }
    });
  });
})();
