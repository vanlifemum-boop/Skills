/* ============ Tussy Van — Site JS ============ */
(function () {
  "use strict";

  /* ---------- Konfiguration (hier anpassen!) ---------- */
  var CONFIG = {
    youtubeHandle: "tussyvan",
    // Kanal-ID (beginnt mit "UC...") eintragen, dann laedt die Video-Sektion
    // automatisch die neuesten Videos als Playlist. Zu finden unter:
    // YouTube Studio -> Einstellungen -> Kanal -> Erweiterte Einstellungen.
    youtubeChannelId: "UCcUM-tEcaUAKm8ki0Q2qRxw",
    // Newsletter: Form-Action deines Anbieters (Mailchimp, Brevo, ...) eintragen.
    // Leer = Hinweis-Modus (Formular zeigt freundliche Meldung statt zu senden).
    newsletterAction: ""
  };
  window.TV_CONFIG = CONFIG;

  /* ---------- kleiner Bulli als SVG (Seitenansicht, faehrt nach rechts) ---------- */
  var BULLI_SVG =
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 62" class="bulli-svg">' +
    '<path d="M8 13 L90 13 L104 22 L114 30 L114 44 L8 44 Z" fill="#1b49c8" stroke="#26251f" stroke-width="3" stroke-linejoin="round"/>' +
    '<path d="M8 35 L114 35 L114 44 L8 44 Z" fill="#10307e" stroke="#26251f" stroke-width="2" stroke-linejoin="round"/>' +
    '<rect x="14" y="17" width="40" height="12" fill="#cfe6ff" stroke="#26251f" stroke-width="2.5"/>' +
    '<path d="M60 17 L92 17 L103 26 L60 26 Z" fill="#cfe6ff" stroke="#26251f" stroke-width="2.5" stroke-linejoin="round"/>' +
    '<circle cx="34" cy="46" r="9" fill="#26251f"/><circle cx="34" cy="46" r="4" fill="#c9c4b2"/>' +
    '<circle cx="92" cy="46" r="9" fill="#26251f"/><circle cx="92" cy="46" r="4" fill="#c9c4b2"/>' +
    '<circle cx="72" cy="32" r="3" fill="#ffff00"/><circle cx="46" cy="33" r="2.4" fill="#ffff00"/>' +
    '<circle cx="58" cy="40" r="2.6" fill="#ffff00"/><circle cx="24" cy="32" r="2" fill="#ffff00"/>' +
    '<rect x="109" y="31" width="5" height="5" fill="#ffd76a" stroke="#26251f" stroke-width="1.5"/>' +
    '</svg>';
  window.TV_BULLI_SVG = BULLI_SVG;

  /* ---------- Smooth Scroll ---------- */
  var lenis = null;
  if (window.Lenis && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    lenis = new window.Lenis({ lerp: 0.1 });
    function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
  }

  /* ---------- Nav (mobil) ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () { nav.classList.toggle("open"); });
  }

  /* ---------- Reveals ---------- */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add("visible"); io.unobserve(en.target); }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll(".reveal").forEach(function (el) { io.observe(el); });

  /* ---------- Bulli am Seitenrand faehrt mit ---------- */
  var roadBulli = document.querySelector(".road-bulli");
  if (roadBulli) {
    roadBulli.innerHTML = BULLI_SVG;
    var ticking = false;
    function updateRoad() {
      var max = document.documentElement.scrollHeight - innerHeight;
      var p = max > 0 ? Math.min(1, scrollY / max) : 0;
      roadBulli.style.top = (6 + p * (innerHeight - 70)) + "px";
      ticking = false;
    }
    addEventListener("scroll", function () {
      if (!ticking) { requestAnimationFrame(updateRoad); ticking = true; }
    }, { passive: true });
    updateRoad();
  }

  /* ---------- Parallax-Deko im Hero ---------- */
  var heroDecos = document.querySelectorAll(".hero [data-parallax]");
  if (heroDecos.length) {
    addEventListener("scroll", function () {
      var y = scrollY;
      heroDecos.forEach(function (el) {
        el.style.translate = "0 " + (y * parseFloat(el.getAttribute("data-parallax"))).toFixed(1) + "px";
      });
    }, { passive: true });
  }

  /* ---------- Cookie-Consent ---------- */
  var CONSENT_KEY = "tv-consent"; // "all" | "essential"
  function getConsent() { try { return localStorage.getItem(CONSENT_KEY); } catch (e) { return null; } }
  function setConsent(v) {
    try { localStorage.setItem(CONSENT_KEY, v); } catch (e) {}
    var b = document.querySelector(".cookie-banner");
    if (b) b.classList.remove("show");
    if (v === "all") loadYouTube();
  }
  window.TV_setConsent = setConsent;
  var banner = document.querySelector(".cookie-banner");
  if (banner && !getConsent()) banner.classList.add("show");
  document.querySelectorAll("[data-consent]").forEach(function (btn) {
    btn.addEventListener("click", function () { setConsent(btn.getAttribute("data-consent")); });
  });

  /* ---------- YouTube (DSGVO: laedt erst nach Klick/Consent) ---------- */
  function loadYouTube() {
    var player = document.querySelector(".yt-player");
    if (!player || player.querySelector("iframe")) return;
    var src;
    if (CONFIG.youtubeChannelId && CONFIG.youtubeChannelId.indexOf("UC") === 0) {
      // Uploads-Playlist des Kanals: neueste Videos automatisch
      src = "https://www.youtube-nocookie.com/embed/videoseries?list=UU" + CONFIG.youtubeChannelId.slice(2);
    } else if (CONFIG.youtubeVideoId) {
      src = "https://www.youtube-nocookie.com/embed/" + CONFIG.youtubeVideoId;
    } else {
      window.open("https://www.youtube.com/@" + CONFIG.youtubeHandle, "_blank", "noopener");
      return;
    }
    var iframe = document.createElement("iframe");
    iframe.src = src;
    iframe.title = "Tussy Van auf YouTube";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;
    var consent = player.querySelector(".yt-consent");
    if (consent) consent.remove();
    player.appendChild(iframe);
  }
  document.querySelectorAll("[data-load-youtube]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!getConsent()) setConsent("all"); else loadYouTube();
    });
  });
  if (getConsent() === "all") loadYouTube();

  /* ---------- Newsletter ---------- */
  var nlForm = document.querySelector(".newsletter form");
  if (nlForm) {
    if (CONFIG.newsletterAction) nlForm.action = CONFIG.newsletterAction;
    nlForm.addEventListener("submit", function (e) {
      if (!CONFIG.newsletterAction) {
        e.preventDefault();
        var out = nlForm.querySelector(".note");
        if (out) out.textContent = "Danke! Der Newsletter startet bald — die Anmeldung wird freigeschaltet, sobald ein Anbieter (z. B. Brevo/Mailchimp) in js/site.js eingetragen ist.";
      }
    });
  }

  /* ---------- Europakarte mit Route ---------- */
  var mapStage = document.querySelector(".map-stage");
  if (mapStage) buildMap(mapStage);

  function buildMap(stage) {
    Promise.all([
      fetch(stage.getAttribute("data-map")).then(function (r) { return r.text(); }),
      fetch(stage.getAttribute("data-points")).then(function (r) { return r.json(); })
    ]).then(function (res) {
      var holder = document.createElement("div");
      holder.innerHTML = res[0];
      var svg = holder.querySelector("svg");
      stage.insertBefore(svg, stage.firstChild);
      var pts = res[1];
      var visited = ["PL", "DE", "NL", "FR", "ES", "PT", "IT", "HR", "AT", "CH", "BE"];
      visited.forEach(function (cc) {
        var p = svg.querySelector("#c-" + cc);
        if (p) p.classList.add("visited");
      });

      var NS = "http://www.w3.org/2000/svg";
      // Route als sanfte Kurve durch die Stationen
      var d = "M" + pts[0].x + "," + pts[0].y;
      for (var i = 1; i < pts.length; i++) {
        var mx = (pts[i - 1].x + pts[i].x) / 2, my = (pts[i - 1].y + pts[i].y) / 2;
        d += " Q" + pts[i - 1].x + "," + pts[i - 1].y + " " + mx + "," + my;
      }
      d += " L" + pts[pts.length - 1].x + "," + pts[pts.length - 1].y;
      var route = document.createElementNS(NS, "path");
      route.setAttribute("d", d);
      route.setAttribute("class", "route");
      svg.appendChild(route);

      // Stationen
      var card = stage.querySelector(".map-card");
      var destBase = stage.getAttribute("data-dest-base") || "reiseziele.html";
      var dests = window.TV_DESTINATIONS || [];
      pts.forEach(function (p) {
        var g = document.createElementNS(NS, "g");
        g.setAttribute("class", "stop");
        g.setAttribute("transform", "translate(" + p.x + "," + p.y + ")");
        var c = document.createElementNS(NS, "circle");
        c.setAttribute("r", "9");
        g.appendChild(c);
        var t = document.createElementNS(NS, "title");
        t.textContent = p.name;
        g.appendChild(t);
        g.addEventListener("click", function () {
          svg.querySelectorAll(".stop.active").forEach(function (s) { s.classList.remove("active"); });
          g.classList.add("active");
          var dest = dests.find(function (x) { return x.id === p.id; });
          if (card) {
            card.querySelector("h3").textContent = p.name;
            card.querySelector("p").textContent = dest ? dest.blurb : "";
            var link = card.querySelector("a");
            link.href = destBase + "#" + p.id;
            card.classList.add("show");
          }
        });
        svg.appendChild(g);
      });

      // Bulli faehrt beim Scrollen die Route entlang
      var bulli = document.createElementNS(NS, "g");
      bulli.setAttribute("class", "map-bulli");
      bulli.innerHTML = BULLI_SVG.replace("<svg ", "<svg width='72' height='37' x='-36' y='-30' ");
      svg.appendChild(bulli);
      var len = route.getTotalLength();
      function drive() {
        var r = stage.getBoundingClientRect();
        var total = r.height + innerHeight;
        var p = Math.min(1, Math.max(0, (innerHeight - r.top) / total));
        var eased = Math.min(1, Math.max(0, (p - 0.15) / 0.7));
        var pt = route.getPointAtLength(eased * len);
        var ahead = route.getPointAtLength(Math.min(len, eased * len + 2));
        var flip = ahead.x < pt.x ? " scale(-1,1)" : "";
        bulli.setAttribute("transform", "translate(" + pt.x + "," + pt.y + ")" + flip);
      }
      addEventListener("scroll", function () { requestAnimationFrame(drive); }, { passive: true });
      drive();
    }).catch(function (err) {
      console.error("Karte konnte nicht geladen werden:", err);
    });
  }

  /* ---------- Reiseziele: Filter ---------- */
  var destGrid = document.querySelector("[data-dest-grid]");
  if (destGrid && window.TV_DESTINATIONS) {
    renderDests("alle");
    document.querySelectorAll(".dest-filter .chip").forEach(function (chip) {
      chip.addEventListener("click", function () {
        document.querySelectorAll(".dest-filter .chip").forEach(function (c) { c.classList.remove("active"); });
        chip.classList.add("active");
        renderDests(chip.getAttribute("data-filter"));
      });
    });
  }
  function renderDests(filter) {
    var list = window.TV_DESTINATIONS.filter(function (x) {
      return filter === "alle" || x.country === filter;
    });
    destGrid.innerHTML = list.map(function (x) {
      return '<article class="dest-card" id="' + x.id + '">' +
        '<div class="head ' + x.color + '">' +
        '<span class="flag">' + x.flag + '</span>' +
        '<h3>' + x.name + '</h3>' +
        '<span class="region">' + x.region + '</span>' +
        '</div><div class="body">' +
        '<p>' + x.blurb + '</p>' +
        '<ul class="dest-tips">' +
        '<li><b>🅿️ Stellplatz:</b><span>' + x.stellplatz + '</span></li>' +
        '<li><b>📅 Beste Zeit:</b><span>' + x.zeit + '</span></li>' +
        '<li><b>💛 Mein Tipp:</b><span>' + x.tipp + '</span></li>' +
        '</ul></div></article>';
    }).join("");
    if (location.hash) {
      var target = document.querySelector(location.hash);
      if (target) target.scrollIntoView({ block: "center" });
    }
  }
})();
