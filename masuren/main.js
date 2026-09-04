/* Neues Leben Masuren — gemeinsames Seiten-JS.
 * Sanfte Reveals (respektiert prefers-reduced-motion), mobiles Menü,
 * aktiver Navigationslink, Anfrageformular mit ehrlichem Fallback, Jahreszahl.
 *
 * Kein Tracking, keine Cookies, keine externen Requests.
 */
(function () {
  "use strict";

  /* Wohin Anfragen gehen. Solange hier [PLATZHALTER] steht, wird nichts
     verschickt — das Formular sagt das dem Besucher offen und bietet den
     vorausgefüllten E-Mail-Link an. */
  var KONTAKT_EMAIL = "[PLATZHALTER: deine@email.de]";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function jedes(liste, fn) { Array.prototype.forEach.call(liste, fn); }

  /* ---------------------------------------------------------- Reveals -- */
  function reveals() {
    var els = document.querySelectorAll("[data-reveal]");
    var reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduziert || !("IntersectionObserver" in window) || !els.length) {
      jedes(els, function (el) { el.classList.add("sichtbar"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("sichtbar");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12 });
    jedes(els, function (el) { io.observe(el); });
  }

  /* ----------------------------------------------------- Mobiles Menü -- */
  function menue() {
    var burger = document.querySelector(".burger");
    var nav = document.querySelector(".nav");
    if (!burger || !nav) return;

    function schliessen() {
      nav.classList.remove("offen");
      burger.setAttribute("aria-expanded", "false");
      burger.setAttribute("aria-label", "Menü öffnen");
      burger.textContent = "☰";
    }

    burger.addEventListener("click", function () {
      var offen = nav.classList.toggle("offen");
      burger.setAttribute("aria-expanded", offen ? "true" : "false");
      burger.setAttribute("aria-label", offen ? "Menü schließen" : "Menü öffnen");
      burger.textContent = offen ? "✕" : "☰";
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) schliessen();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("offen")) {
        schliessen();
        burger.focus();
      }
    });
  }

  /* ------------------------------------------------ Aktiver Nav-Link --- */
  function aktiverLink() {
    var datei = (location.pathname.split("/").pop() || "index.html").toLowerCase();
    if (!datei) datei = "index.html";
    jedes(document.querySelectorAll(".nav a:not(.btn)"), function (a) {
      var ziel = (a.getAttribute("href") || "").split("#")[0].toLowerCase();
      if (ziel && ziel === datei) {
        a.classList.add("aktiv");
        a.setAttribute("aria-current", "page");
      }
    });
  }

  /* ------------------------------------------------- Anfrageformular --- */
  /* POSTet an data-endpoint (z. B. Formspree). Solange der Endpoint noch
     [PLATZHALTER] ist, wird ehrlich gesagt, dass der Versand nicht aktiv ist,
     und ein vorausgefüllter mailto:-Link angeboten. */
  function anfrageFormular() {
    jedes(document.querySelectorAll("form.anfrage-form"), function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!form.checkValidity()) { form.reportValidity(); return; }

        var daten = {};
        new FormData(form).forEach(function (wert, schluessel) { daten[schluessel] = wert; });

        var endpoint = form.getAttribute("data-endpoint") || "";
        var endpointEcht = endpoint && endpoint.indexOf("PLATZHALTER") === -1;
        var emailEcht = KONTAKT_EMAIL.indexOf("PLATZHALTER") === -1;

        var betreff = "Anfrage über die Website: " + (daten.anliegen || "Grundstück in Masuren");
        var koerper = Object.keys(daten).map(function (k) {
          return k + ": " + daten[k];
        }).join("\n");
        var mailto = "mailto:" + (emailEcht ? KONTAKT_EMAIL : "") +
          "?subject=" + encodeURIComponent(betreff) +
          "&body=" + encodeURIComponent(koerper);

        function antworten(html) {
          var box = document.createElement("div");
          box.className = "form-antwort";
          box.setAttribute("role", "status");
          box.setAttribute("tabindex", "-1");
          box.innerHTML = html;
          form.replaceWith(box);
          box.focus();
        }

        if (!endpointEcht) {
          antworten(
            "<p><strong>Danke für deine Nachricht.</strong></p>" +
            "<p>Der automatische Versand dieses Formulars ist noch nicht eingerichtet — " +
            "deine Eingaben wurden also <em>nicht</em> verschickt. Damit nichts verloren geht, " +
            "haben wir dir eine fertige E-Mail vorbereitet:</p>" +
            '<p><a class="btn" href="' + mailto + '">E-Mail mit deinen Angaben öffnen</a></p>' +
            (emailEcht ? "" :
              '<p class="klein">Hinweis für den Seitenbetreiber: In <code>main.js</code> die ' +
              "E-Mail-Adresse eintragen und am Formular ein echtes " +
              "<code>data-endpoint</code> hinterlegen.</p>")
          );
          return;
        }

        var knopf = form.querySelector('button[type="submit"]');
        if (knopf) { knopf.disabled = true; knopf.textContent = "Wird gesendet …"; }

        fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(daten)
        }).then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          antworten(
            "<p><strong>Danke! Deine Anfrage ist angekommen.</strong></p>" +
            "<p>Wir melden uns so schnell wie möglich bei dir zurück.</p>"
          );
        }).catch(function () {
          antworten(
            "<p><strong>Das hat leider nicht geklappt.</strong></p>" +
            "<p>Der Versand ist fehlgeschlagen. Schick uns deine Anfrage bitte direkt per " +
            "E-Mail — deine Angaben sind schon eingetragen:</p>" +
            '<p><a class="btn" href="' + mailto + '">E-Mail mit deinen Angaben öffnen</a></p>'
          );
        });
      });
    });
  }

  /* -------------------------------------------------------- Jahreszahl - */
  function jahr() {
    jedes(document.querySelectorAll("[data-jahr]"), function (el) {
      el.textContent = new Date().getFullYear();
    });
  }

  ready(function () {
    reveals();
    menue();
    aktiverLink();
    anfrageFormular();
    jahr();
  });
})();
