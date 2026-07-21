/* =========================================================================
   Kleine Füße, große Welt — gemeinsame Skripte (Vanilla JS)
   Läuft auf allen Seiten. Ohne externe Abhängigkeiten.
   ========================================================================= */
(function () {
  "use strict";

  // JS ist aktiv -> erlaubt der CSS, Reveal-Elemente zunächst auszublenden.
  // Passiert sofort (nicht erst bei DOMContentLoaded), um Aufblitzen zu vermeiden.
  document.documentElement.classList.add("js");

  /* ---------- Mobile-Navigation umschalten ---------- */
  function initNavToggle() {
    var toggle = document.querySelector(".nav__toggle");
    var links = document.getElementById("nav-links");
    if (!toggle || !links) return;
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    // Menü schließen, wenn ein Link angeklickt wird (mobil)
    links.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        links.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------- Newsletter- & Download-Formulare (Attrappen) ----------
     Statische Seite ohne Backend: Wir zeigen nur eine Bestätigung an.
     >>> Hier später den Newsletter-Dienst anbinden (z. B. Mailchimp,
         CleverReach, Brevo). Die E-Mail-Adresse steht in `data.email`. <<<
  */
  function initFakeForms() {
    var forms = document.querySelectorAll("form[data-fake]");
    forms.forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var status = form.querySelector(".form-status");
        var email = form.querySelector('input[type="email"]');
        if (email && !email.checkValidity()) {
          if (status) status.textContent = "Bitte gib eine gültige E-Mail-Adresse ein.";
          return;
        }
        // TODO: An dieser Stelle den echten Newsletter-/Download-Dienst aufrufen.
        // Beispiel: fetch("/api/subscribe", { method:"POST", body: ... })
        if (status) {
          status.textContent =
            "Fast geschafft! 🎉 Wir haben dir eine Bestätigungs-Mail geschickt " +
            "(Double-Opt-In). Bitte klicke den Link darin, um die Anmeldung abzuschließen.";
        }
        form.reset();
      });
    });
  }

  /* ---------- Scroll-Reveal (kleine, dezente Einblendung) ----------
     Robust: Elemente im Viewport werden sofort eingeblendet, ein
     Sicherheitsnetz nach dem Laden blendet garantiert alles ein — so bleibt
     nie Inhalt unsichtbar, falls der Observer verzögert oder nicht feuert. */
  function initReveal() {
    var els = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
    if (!els.length) return;
    function revealAll() { els.forEach(function (el) { el.classList.add("is-visible"); }); }
    if (!("IntersectionObserver" in window)) { revealAll(); return; }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });

    // Sofort einblenden, was beim Laden bereits sichtbar ist.
    requestAnimationFrame(function () {
      var vh = window.innerHeight || document.documentElement.clientHeight;
      els.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < vh && r.bottom > 0) el.classList.add("is-visible");
      });
    });

    // Sicherheitsnetz: nach dem Laden nichts verborgen lassen.
    window.addEventListener("load", function () { setTimeout(revealAll, 700); });
  }

  /* ---------- Aktuelles Jahr im Footer ---------- */
  function initYear() {
    var y = document.getElementById("year");
    if (y) y.textContent = String(new Date().getFullYear());
  }

  /* ---------- Expand-Galerie (aufziehende Comic-Panels) ----------
     Auf dem Desktop reicht CSS-:hover. Für Touch/Tastatur schalten wir
     hier zusätzlich eine .is-active-Klasse per Klick um.
  */
  function initExpandGallery() {
    var galleries = document.querySelectorAll(".expand-gallery");
    galleries.forEach(function (gallery) {
      var panels = gallery.querySelectorAll(".expand-panel");
      panels.forEach(function (panel) {
        if (!panel.hasAttribute("tabindex")) panel.setAttribute("tabindex", "0");
        function activate() {
          panels.forEach(function (p) { p.classList.remove("is-active"); });
          panel.classList.add("is-active");
        }
        panel.addEventListener("click", activate);
        panel.addEventListener("focus", activate);
        panel.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); activate(); }
        });
      });
      // erstes Panel als Startzustand hervorheben
      if (panels.length) panels[0].classList.add("is-active");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initNavToggle();
    initFakeForms();
    initReveal();
    initYear();
    initExpandGallery();
  });
})();
