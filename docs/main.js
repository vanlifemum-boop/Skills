/* GutachtenKompass — gemeinsames Seiten-JS.
 * Sanfte Reveals (respektiert prefers-reduced-motion), mobiles Menü,
 * aktiver Navigationslink, Datenschutz-Hinweisleiste, Jahreszahl.
 */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  /* Reveal-Animationen */
  function reveals() {
    const els = document.querySelectorAll("[data-reveal]");
    const reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduziert || !("IntersectionObserver" in window) || !els.length) {
      els.forEach((el) => el.classList.add("sichtbar"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("sichtbar");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    els.forEach((el) => io.observe(el));
  }

  /* Mobiles Menü */
  function menue() {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".nav");
    if (!burger || !nav) return;
    burger.addEventListener("click", () => {
      const offen = nav.classList.toggle("offen");
      burger.setAttribute("aria-expanded", offen ? "true" : "false");
      burger.textContent = offen ? "✕" : "☰";
    });
    nav.addEventListener("click", (e) => {
      if (e.target.closest("a")) {
        nav.classList.remove("offen");
        burger.setAttribute("aria-expanded", "false");
        burger.textContent = "☰";
      }
    });
  }

  /* Aktiven Nav-Link markieren */
  function aktiverLink() {
    const datei = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    document.querySelectorAll(".nav a:not(.btn)").forEach((a) => {
      const ziel = (a.getAttribute("href") || "").split("#")[0].toLowerCase();
      if (ziel && ziel === datei) a.classList.add("aktiv");
    });
  }

  /* Datenschutz-Hinweisleiste (keine Cookies/Tracker auf dieser Seite —
     die Leiste ist rein informativ und merkt sich das Ausblenden lokal). */
  function hinweisleiste() {
    const leiste = document.getElementById("datenschutz-hinweis");
    if (!leiste) return;
    let gesehen = false;
    try { gesehen = localStorage.getItem("gk-hinweis-ok") === "1"; } catch (e) { /* privat-modus */ }
    if (gesehen) { leiste.hidden = true; return; }
    leiste.hidden = false;
    const knopf = leiste.querySelector("button");
    if (knopf) {
      knopf.addEventListener("click", () => {
        leiste.hidden = true;
        try { localStorage.setItem("gk-hinweis-ok", "1"); } catch (e) { /* ok */ }
      });
    }
  }

  /* Lead-Magnet-Formulare: POSTet an data-endpoint (z. B. Formspree).
     Solange der Endpoint noch [PLATZHALTER] ist, wird ehrlich bestätigt,
     dass der Versand erst nach Einrichtung aktiv ist. */
  function leadFormulare() {
    document.querySelectorAll("form.lead-form").forEach((form) => {
      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const email = form.querySelector('input[type="email"]');
        if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
          email.focus();
          return;
        }
        const endpoint = form.getAttribute("data-endpoint") || "";
        const echt = endpoint && !endpoint.includes("PLATZHALTER");
        let ok = false;
        if (echt) {
          try {
            const r = await fetch(endpoint, {
              method: "POST",
              headers: { "Content-Type": "application/json", Accept: "application/json" },
              body: JSON.stringify(Object.fromEntries(new FormData(form))),
            });
            ok = r.ok;
          } catch (err) { ok = false; }
        }
        const p = document.createElement("p");
        p.className = "lead-hinweis";
        p.setAttribute("role", "status");
        p.textContent = ok
          ? "Danke! Der Leitfaden ist unterwegs in dein Postfach."
          : echt
            ? "Das hat leider nicht geklappt. Bitte versuche es später noch einmal."
            : "Danke für dein Interesse! Der automatische Versand wird gerade eingerichtet — trage dich gern trotzdem ein, wir melden uns.";
        form.replaceWith(p);
      });
    });
  }

  /* Jahreszahl im Footer */
  function jahr() {
    document.querySelectorAll("[data-jahr]").forEach((el) => {
      el.textContent = new Date().getFullYear();
    });
  }

  ready(function () {
    reveals();
    menue();
    aktiverLink();
    hinweisleiste();
    leadFormulare();
    jahr();
  });
})();
