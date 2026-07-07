/* Tussy Van — cinematic scroll engine
   Canvas image-sequence scrub + Lenis smooth scroll + progress-window overlays. */
(function () {
  "use strict";

  var DPR = Math.min(window.devicePixelRatio || 1, 2);
  var sections = [];

  function buildSection(cfg) {
    var el = document.querySelector(cfg.section);
    if (!el) return null;
    var canvas = el.querySelector("canvas");
    var ctx = canvas.getContext("2d");
    var s = {
      el: el,
      canvas: canvas,
      ctx: ctx,
      bg: cfg.bg || "#07100b",
      frameCount: cfg.frameCount,
      framePath: cfg.framePath,
      images: new Array(cfg.frameCount),
      loaded: 0,
      current: -1,
      overlays: Array.prototype.slice.call(el.querySelectorAll("[data-in]")).map(function (node) {
        return {
          node: node,
          in: parseFloat(node.getAttribute("data-in")),
          out: parseFloat(node.getAttribute("data-out"))
        };
      })
    };
    for (var i = 0; i < s.frameCount; i++) {
      (function (idx) {
        var img = new Image();
        img.decoding = "async";
        img.onload = function () {
          s.loaded++;
          if (idx === 0) drawFrame(s, 0);
        };
        img.src = s.framePath(idx + 1);
        s.images[idx] = img;
      })(i);
    }
    return s;
  }

  function sizeCanvas(s) {
    var w = s.canvas.clientWidth, h = s.canvas.clientHeight;
    if (!w || !h) return;
    var pw = Math.round(w * DPR), ph = Math.round(h * DPR);
    if (s.canvas.width !== pw || s.canvas.height !== ph) {
      s.canvas.width = pw;
      s.canvas.height = ph;
      s.current = -1; // force redraw
    }
  }

  function drawFrame(s, idx) {
    var img = s.images[idx];
    if (!img || !img.complete || !img.naturalWidth) return;
    sizeCanvas(s);
    var cw = s.canvas.width, ch = s.canvas.height;
    var scale = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);
    var dw = img.naturalWidth * scale, dh = img.naturalHeight * scale;
    s.ctx.fillStyle = s.bg;
    s.ctx.fillRect(0, 0, cw, ch);
    s.ctx.drawImage(img, (cw - dw) / 2, (ch - dh) / 2, dw, dh);
    s.current = idx;
  }

  function progressOf(el) {
    var rect = el.getBoundingClientRect();
    var innerH = window.innerHeight;
    var total = rect.height - innerH;
    if (total <= 0) return 0;
    return Math.min(1, Math.max(0, -rect.top / total));
  }

  function updateSection(s) {
    var rect = s.el.getBoundingClientRect();
    if (rect.bottom < -200 || rect.top > window.innerHeight + 200) return;
    var p = progressOf(s.el);
    var idx = Math.min(s.frameCount - 1, Math.floor(p * (s.frameCount - 1)));
    if (idx !== s.current) drawFrame(s, idx);
    for (var i = 0; i < s.overlays.length; i++) {
      var o = s.overlays[i];
      var span = o.out - o.in;
      var fadeZone = Math.min(0.12, span / 3);
      var op = 0, shift = 24;
      if (p >= o.in && p <= o.out) {
        var head = o.in <= 0 ? 1 : (p - o.in) / fadeZone;
        var tail = (o.out - p) / fadeZone;
        op = Math.min(1, head, tail);
        shift = (1 - Math.min(1, head)) * 24;
      } else if (p < o.in) {
        shift = 24;
      } else {
        shift = -12;
      }
      o.node.style.opacity = op.toFixed(3);
      o.node.style.transform = "translateY(" + shift.toFixed(1) + "px)";
      o.node.style.pointerEvents = op > 0.5 ? "auto" : "none";
    }
  }

  // --- boot ---
  var cfgs = window.SCRUB_SECTIONS || [];
  for (var i = 0; i < cfgs.length; i++) {
    var s = buildSection(cfgs[i]);
    if (s) sections.push(s);
  }

  var lenis = null;
  if (window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.09, wheelMultiplier: 1, smoothWheel: true });
  }

  var header = document.querySelector(".site-header");
  var progressBar = document.querySelector(".scroll-progress span");
  var docH = 0;

  function onFrame(time) {
    if (lenis) lenis.raf(time);
    for (var i = 0; i < sections.length; i++) updateSection(sections[i]);
    var y = window.scrollY || 0;
    if (header) header.classList.toggle("scrolled", y > 40);
    if (progressBar) {
      if (!docH) docH = document.documentElement.scrollHeight - window.innerHeight;
      progressBar.style.transform = "scaleX(" + Math.min(1, y / docH).toFixed(4) + ")";
    }
    requestAnimationFrame(onFrame);
  }
  requestAnimationFrame(onFrame);

  window.addEventListener("resize", function () {
    docH = 0;
    for (var i = 0; i < sections.length; i++) {
      sections[i].current = -1;
      updateSection(sections[i]);
    }
  });

  // Anchor links through Lenis
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var target = document.querySelector(a.getAttribute("href"));
      if (!target) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(target, { offset: 0, duration: 1.4 });
      else target.scrollIntoView({ behavior: "smooth" });
    });
  });

  // Scroll reveals
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) {
        en.target.classList.add("visible");
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.18 });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  // 3D tilt on product cards
  document.querySelectorAll("[data-tilt]").forEach(function (card) {
    card.addEventListener("mousemove", function (e) {
      var r = card.getBoundingClientRect();
      var rx = ((e.clientY - r.top) / r.height - 0.5) * -7;
      var ry = ((e.clientX - r.left) / r.width - 0.5) * 9;
      card.style.transform = "perspective(900px) rotateX(" + rx.toFixed(2) + "deg) rotateY(" + ry.toFixed(2) + "deg) translateY(-6px)";
    });
    card.addEventListener("mouseleave", function () {
      card.style.transform = "";
    });
  });
})();
