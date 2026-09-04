(function () {
  if (typeof window === "undefined") return;

  var scriptVersion = "20260609-formscroll2";
  if (window.__agpSmoothScrollLoaded === scriptVersion) return;
  window.__agpSmoothScrollLoaded = scriptVersion;

  function initSmoothScroll() {
    if (!document.body) return;

    var root = document.documentElement;
    var body = document.body;
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function isAdminPath() {
      return window.location.pathname.indexOf("/admin") === 0;
    }

    if (reduceMotion || isAdminPath()) return;

    if (!document.getElementById("agp-smooth-scroll-css")) {
      var style = document.createElement("style");
      style.id = "agp-smooth-scroll-css";
      style.textContent = [
        "html.agp-smooth-scroll{scroll-behavior:auto!important;}",
        "html.agp-smooth-scroll body{overscroll-behavior-y:none;}",
        "[data-smooth-parallax]{will-change:translate;}",
        "@media (prefers-reduced-motion: reduce){[data-smooth-parallax]{will-change:auto!important;translate:none!important;}}",
        "@media (max-width:767px){[data-smooth-parallax]{will-change:auto;}}"
      ].join("");
      document.head.appendChild(style);
    }

    root.classList.add("agp-smooth-scroll");

    var pointerFine = window.matchMedia("(pointer: fine)").matches;
    var ease = pointerFine ? 0.115 : 0.18;
    var wheelMultiplier = pointerFine ? 0.92 : 1;
    var current = window.scrollY || window.pageYOffset || 0;
    var target = current;
    var last = current;
    var maxScroll = 0;
    var frame = 0;
    var refreshFrame = 0;
    var ignoreScroll = false;
    var parallaxItems = [];

    var parallaxSelectors = [
      ".hero-bg-glow",
      ".hero-bg-glow-2",
      ".headline-section h2",
      ".cases-header",
      ".stats-bar",
      ".case-stats-card",
      ".case-card",
      ".case-related-card",
      ".case-client-card",
      ".blog-card",
      ".service-card",
      ".diff-card",
      ".client-cell"
    ].join(",");

    function clamp(value, min, max) {
      return Math.max(min, Math.min(max, value));
    }

    function getMaxScroll() {
      return Math.max(0, root.scrollHeight - window.innerHeight);
    }

    function getDelta(event) {
      var delta = event.deltaY;
      if (event.deltaMode === 1) delta *= 18;
      if (event.deltaMode === 2) delta *= window.innerHeight;
      return delta * wheelMultiplier;
    }

    function canUseParallax() {
      return window.innerWidth >= 768 && !isAdminPath();
    }

    function getElement(node) {
      if (!node || node === window || node === document) return null;
      return node.nodeType === 1 ? node : node.parentElement;
    }

    function isContactFormControl(element) {
      if (!element) return false;
      return Boolean(element.closest("input, textarea, select, button, label, .ag-lead-form, .ag-form-field, .ag-form-control, .ag-check-option, .ag-check-panel, .ag-submit-button"));
    }

    function shouldSkipElement(node) {
      var element = getElement(node);
      if (!element) return false;
      if (element.closest("[contenteditable='true'], [data-native-scroll], .admin-shell")) return true;

      if (isContactFormControl(element)) return false;

      while (element && element !== body) {
        var styles = window.getComputedStyle(element);
        var overflowY = styles.overflowY;
        var canScroll = (overflowY === "auto" || overflowY === "scroll" || overflowY === "overlay") && element.scrollHeight > element.clientHeight + 2;
        if (canScroll) return true;
        element = element.parentElement;
      }

      return false;
    }

    function shouldSkipKeyElement(node) {
      var element = getElement(node);
      if (!element) return false;
      if (element.closest("[contenteditable='true'], [data-native-scroll], .admin-shell")) return true;
      if (element.closest("input, textarea, select, button, [role='button']")) return true;
      return shouldSkipElement(element);
    }

    function collectParallax() {
      maxScroll = getMaxScroll();

      if (!canUseParallax()) {
        parallaxItems.forEach(function (item) {
          item.el.style.removeProperty("translate");
        });
        parallaxItems = [];
        return;
      }

      var nodes = document.querySelectorAll("[data-smooth-parallax], " + parallaxSelectors);
      var items = [];
      var count = 0;

      nodes.forEach(function (node) {
        if (count > 140) return;
        if (!(node instanceof HTMLElement)) return;
        if (node.closest("nav, header [role='navigation'], footer, .footer, .nav-dropdown, .admin-shell")) return;

        var rect = node.getBoundingClientRect();
        if (rect.width < 16 || rect.height < 16) return;

        var attrDepth = Number(node.getAttribute("data-smooth-depth"));
        var depth = Number.isFinite(attrDepth) && attrDepth !== 0 ? attrDepth : 0.018 + (count % 4) * 0.004;
        if (node.matches(".hero-bg-glow, .hero-bg-glow-2")) depth = 0.055;
        if (node.matches(".stats-bar, .case-stats-card")) depth = 0.012;

        if (!node.hasAttribute("data-smooth-parallax")) node.setAttribute("data-smooth-parallax", "auto");
        items.push({
          el: node,
          top: rect.top + (window.scrollY || window.pageYOffset || 0),
          height: rect.height,
          depth: depth
        });
        count += 1;
      });

      parallaxItems = items;
    }

    function updateParallax(scroll) {
      if (!canUseParallax()) return;

      var viewport = window.innerHeight;
      var center = scroll + viewport / 2;

      parallaxItems.forEach(function (item) {
        if (scroll > item.top + item.height + viewport || scroll + viewport < item.top - viewport) return;
        var itemCenter = item.top + item.height / 2;
        var y = clamp((center - itemCenter) * -item.depth, -70, 70);
        item.el.style.setProperty("translate", "0 " + y.toFixed(2) + "px");
      });
    }

    function emit(scroll, velocity) {
      try {
        window.dispatchEvent(new CustomEvent("agp:smooth-scroll", {
          detail: {
            scroll: scroll,
            target: target,
            velocity: velocity,
            progress: maxScroll ? scroll / maxScroll : 0
          }
        }));
      } catch (error) {}
    }

    function animate() {
      frame = 0;
      maxScroll = getMaxScroll();
      target = clamp(target, 0, maxScroll);

      var distance = target - current;
      current += distance * ease;
      if (Math.abs(distance) < 0.08) current = target;

      var velocity = current - last;
      last = current;

      ignoreScroll = true;
      window.scrollTo(0, current);
      window.requestAnimationFrame(function () {
        ignoreScroll = false;
      });

      updateParallax(current);
      emit(current, velocity);

      if (current !== target) {
        frame = window.requestAnimationFrame(animate);
      }
    }

    function start() {
      if (!frame) frame = window.requestAnimationFrame(animate);
    }

    function setTarget(value) {
      if (isAdminPath()) return;
      maxScroll = getMaxScroll();
      target = clamp(value, 0, maxScroll);
      start();
    }

    function onWheel(event) {
      if (event.__agpSmoothWheelHandled) return;
      if (isAdminPath() || event.ctrlKey || event.metaKey || event.shiftKey || shouldSkipElement(event.target)) return;
      event.__agpSmoothWheelHandled = true;
      event.preventDefault();
      if (typeof event.stopImmediatePropagation === "function") event.stopImmediatePropagation();
      setTarget(target + getDelta(event));
    }

    function onKeyDown(event) {
      if (event.defaultPrevented || isAdminPath() || event.altKey || event.ctrlKey || event.metaKey) return;
      if (shouldSkipKeyElement(document.activeElement)) return;

      var amount = 0;
      if (event.key === "ArrowDown") amount = 90;
      if (event.key === "ArrowUp") amount = -90;
      if (event.key === "PageDown") amount = window.innerHeight * 0.86;
      if (event.key === "PageUp") amount = -window.innerHeight * 0.86;
      if (event.key === " ") amount = event.shiftKey ? -window.innerHeight * 0.86 : window.innerHeight * 0.86;
      if (event.key === "Home") {
        event.preventDefault();
        setTarget(0);
        return;
      }
      if (event.key === "End") {
        event.preventDefault();
        setTarget(getMaxScroll());
        return;
      }
      if (!amount) return;

      event.preventDefault();
      setTarget(target + amount);
    }

    function getHeaderOffset() {
      var header = document.querySelector("header, .nav, .site-nav");
      if (!(header instanceof HTMLElement)) return 20;
      var styles = window.getComputedStyle(header);
      if (styles.position !== "fixed" && styles.position !== "sticky") return 20;
      return header.getBoundingClientRect().height + 20;
    }

    function onAnchorClick(event) {
      if (isAdminPath()) return;
      var targetNode = event.target instanceof Element ? event.target : null;
      if (!targetNode) return;
      var anchor = targetNode.closest("a[href^='#']");
      if (!(anchor instanceof HTMLAnchorElement)) return;
      var href = anchor.getAttribute("href") || "";
      if (href.length <= 1) return;
      var id = decodeURIComponent(href.slice(1));
      var destination = document.getElementById(id);
      if (!destination) return;

      event.preventDefault();
      setTarget(destination.getBoundingClientRect().top + (window.scrollY || window.pageYOffset || 0) - getHeaderOffset());
      try {
        history.pushState(null, "", href);
      } catch (error) {}
    }

    function onScroll() {
      if (ignoreScroll) return;
      current = window.scrollY || window.pageYOffset || 0;
      target = current;
      last = current;
      updateParallax(current);
    }

    function requestRefresh() {
      if (refreshFrame) return;
      refreshFrame = window.requestAnimationFrame(function () {
        refreshFrame = 0;
        collectParallax();
        updateParallax(window.scrollY || window.pageYOffset || 0);
      });
    }

    function onResize() {
      current = window.scrollY || window.pageYOffset || 0;
      target = current;
      requestRefresh();
    }

    collectParallax();
    updateParallax(current);

    window.addEventListener("wheel", onWheel, { passive: false, capture: true });
    window.addEventListener("keydown", onKeyDown);
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onResize, { passive: true });
    window.addEventListener("load", requestRefresh, { once: true });
    document.addEventListener("click", onAnchorClick);

    if ("MutationObserver" in window) {
      var observer = new MutationObserver(requestRefresh);
      observer.observe(body, { childList: true, subtree: true, attributes: true, attributeFilter: ["class", "style", "data-smooth-depth", "data-smooth-parallax"] });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initSmoothScroll, { once: true });
  } else {
    initSmoothScroll();
  }
})();
