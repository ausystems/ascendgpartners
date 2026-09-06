// SEO page: five small real-time objects, one per idea. Matte, slow, scroll-linked.
// index (points on a sphere) · lattice (structure) · layers (content) · graph (authority) · orbits (AI discovery)
(function () {
  if (typeof THREE === 'undefined') return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var CREAM = 0xf7f8f8, NAVY = 0x0f1535, ORANGE = 0xe8613c;
  var scenes = [];

  function makeRenderer(canvas) {
    var ctx = canvas.getContext('webgl', { alpha: true, antialias: true, premultipliedAlpha: true, powerPreference: 'high-performance' });
    if (!ctx) return null;
    var r = new THREE.WebGLRenderer({ canvas: canvas, context: ctx, alpha: true, antialias: true });
    r.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    r.setClearColor(0x000000, 0);
    return r;
  }
  function lights(scene, dark) {
    scene.add(new THREE.HemisphereLight(0xffffff, dark ? 0x0f1535 : 0xd9d4ca, dark ? 1.1 : 0.9));
    var d = new THREE.DirectionalLight(0xffffff, dark ? 0.9 : 0.7); d.position.set(3, 4, 5); scene.add(d);
  }
  function matte(color) { return new THREE.MeshStandardMaterial({ color: color, roughness: 0.62, metalness: 0.05 }); }
  function lineMat(color, opacity) { return new THREE.LineBasicMaterial({ color: color, transparent: true, opacity: opacity }); }
  function fib(n, r) {
    var pts = [], g = Math.PI * (3 - Math.sqrt(5));
    for (var i = 0; i < n; i++) { var y = 1 - (i / (n - 1)) * 2, rad = Math.sqrt(1 - y * y), t = g * i; pts.push(new THREE.Vector3(Math.cos(t) * rad * r, y * r, Math.sin(t) * rad * r)); }
    return pts;
  }

  var builders = {
    // the index: a sphere of points, a few of them lit orange
    index: function (scene, dark) {
      var pts = fib(1100, 1.55), pos = new Float32Array(pts.length * 3), col = new Float32Array(pts.length * 3);
      var c1 = new THREE.Color(dark ? CREAM : NAVY), c2 = new THREE.Color(ORANGE);
      pts.forEach(function (p, i) { pos.set([p.x, p.y, p.z], i * 3); var c = (i % 37 === 0) ? c2 : c1; col.set([c.r, c.g, c.b], i * 3); });
      var g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.BufferAttribute(col, 3));
      var m = new THREE.PointsMaterial({ size: 0.028, vertexColors: true, transparent: true, opacity: 0.9, sizeAttenuation: true });
      var o = new THREE.Points(g, m); scene.add(o); return o;
    },
    // structure: a lattice of nodes and edges
    lattice: function (scene, dark) {
      var group = new THREE.Group(), n = 4, s = 0.62, off = (n - 1) * s / 2, verts = [];
      var nodeM = matte(dark ? CREAM : NAVY), nodeG = new THREE.SphereGeometry(0.045, 14, 14);
      for (var x = 0; x < n; x++) for (var y = 0; y < n; y++) for (var z = 0; z < n; z++) {
        var p = new THREE.Vector3(x * s - off, y * s - off, z * s - off);
        var node = new THREE.Mesh(nodeG, (x === 1 && y === 2 && z === 1) ? matte(ORANGE) : nodeM); node.position.copy(p); group.add(node);
        if (x < n - 1) verts.push(p.x, p.y, p.z, p.x + s, p.y, p.z);
        if (y < n - 1) verts.push(p.x, p.y, p.z, p.x, p.y + s, p.z);
        if (z < n - 1) verts.push(p.x, p.y, p.z, p.x, p.y, p.z + s);
      }
      var lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
      group.add(new THREE.LineSegments(lg, lineMat(dark ? CREAM : NAVY, 0.22)));
      group.rotation.set(0.5, 0.6, 0); scene.add(group); return group;
    },
    // content: layered planes, one lit
    layers: function (scene, dark) {
      var group = new THREE.Group(), g = new THREE.BoxGeometry(2.2, 0.06, 1.5);
      for (var i = 0; i < 5; i++) {
        var m = new THREE.Mesh(g, i === 3 ? matte(ORANGE) : matte(dark ? CREAM : NAVY));
        m.position.set((i - 2) * 0.08, (i - 2) * 0.34, (i - 2) * -0.1); m.userData.base = m.position.y; group.add(m);
      }
      group.rotation.set(0.42, -0.55, 0.08); scene.add(group); return group;
    },
    // authority: a graph of nodes linked to a center
    graph: function (scene, dark) {
      var group = new THREE.Group(), pts = fib(16, 1.35), verts = [], nodeG = new THREE.SphereGeometry(0.06, 14, 14), nm = matte(dark ? CREAM : NAVY);
      var center = new THREE.Mesh(new THREE.SphereGeometry(0.16, 20, 20), matte(ORANGE)); group.add(center);
      pts.forEach(function (p, i) {
        var nd = new THREE.Mesh(nodeG, nm); nd.position.copy(p); group.add(nd);
        verts.push(0, 0, 0, p.x, p.y, p.z);
        var q = pts[(i + 5) % pts.length]; if (i % 2 === 0) verts.push(p.x, p.y, p.z, q.x, q.y, q.z);
      });
      var lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
      group.add(new THREE.LineSegments(lg, lineMat(dark ? CREAM : NAVY, 0.28)));
      scene.add(group); return group;
    },
    // AI discovery: rings orbiting the index
    orbits: function (scene, dark) {
      var group = new THREE.Group();
      group.add(new THREE.Mesh(new THREE.SphereGeometry(0.34, 32, 32), matte(ORANGE)));
      var rm = matte(dark ? CREAM : NAVY);
      [[1.05, 0.0, 0.0], [1.35, 1.1, 0.4], [1.65, 0.5, 1.2]].forEach(function (cfg, i) {
        var ring = new THREE.Mesh(new THREE.TorusGeometry(cfg[0], 0.012, 12, 140), rm);
        ring.rotation.set(cfg[1], cfg[2], 0); ring.userData.speed = 0.12 + i * 0.05; group.add(ring);
        var sat = new THREE.Mesh(new THREE.SphereGeometry(0.05, 12, 12), rm); sat.userData.r = cfg[0]; sat.userData.ring = ring; sat.userData.phase = i * 2.1; group.add(sat);
      });
      group.rotation.x = 0.35; scene.add(group); return group;
    }
  };

  document.querySelectorAll('canvas[data-object]').forEach(function (canvas) {
    var type = canvas.getAttribute('data-object'), dark = canvas.getAttribute('data-theme') === 'dark';
    var renderer = makeRenderer(canvas); if (!renderer) return;
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50); camera.position.set(0, 0, 6.2);
    lights(scene, dark);
    var obj = builders[type] ? builders[type](scene, dark) : null;
    if (!obj) return;
    var entry = { canvas: canvas, renderer: renderer, scene: scene, camera: camera, obj: obj, type: type, visible: false, t0: performance.now(), needs: true };
    scenes.push(entry);
    function resize() {
      var w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
      renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); entry.needs = true;
    }
    window.addEventListener('resize', resize); resize();
    new IntersectionObserver(function (en) { entry.visible = en[0].isIntersecting; entry.needs = true; }, { rootMargin: '10% 0px' }).observe(canvas);
  });
  if (!scenes.length) return;

  var scrollY = window.scrollY;
  window.addEventListener('scroll', function () { scrollY = window.scrollY; }, { passive: true });

  function frame(now) {
    scenes.forEach(function (s) {
      if (!s.visible) return;
      var t = (now - s.t0) / 1000;
      var r = s.canvas.getBoundingClientRect();
      var p = (r.top + r.height / 2 - window.innerHeight / 2) / window.innerHeight; // -1..1 through the viewport
      if (!reduce) {
        var o = s.obj;
        if (s.type === 'index') { o.rotation.y = t * 0.08 + p * 0.6; o.rotation.x = p * 0.25; }
        else if (s.type === 'lattice') { o.rotation.y = 0.6 + t * 0.1 + p * 0.5; o.rotation.x = 0.5 + p * 0.2; }
        else if (s.type === 'layers') { o.rotation.y = -0.55 + t * 0.06 + p * 0.35; o.children.forEach(function (m, i) { m.position.y = m.userData.base + Math.sin(t * 0.9 + i * 0.7) * 0.03; }); }
        else if (s.type === 'graph') { o.rotation.y = t * 0.12 + p * 0.6; o.rotation.z = p * 0.15; }
        else if (s.type === 'orbits') {
          o.rotation.y = t * 0.05 + p * 0.4;
          o.children.forEach(function (c) {
            if (c.userData.speed) c.rotation.z += 0; 
            if (c.userData.ring) { var a = t * (0.35 + c.userData.r * 0.1) + c.userData.phase; var v = new THREE.Vector3(Math.cos(a) * c.userData.r, Math.sin(a) * c.userData.r, 0); v.applyEuler(c.userData.ring.rotation); c.position.copy(v); }
          });
        }
        s.renderer.render(s.scene, s.camera);
      } else if (s.needs) { s.renderer.render(s.scene, s.camera); s.needs = false; }
    });
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();
