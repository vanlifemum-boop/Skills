/* WowMoman — Interaktivität (selbst-enthalten, keine externen Abhängigkeiten)
   - Mobile-Navigation
   - Scroll-Reveals (IntersectionObserver)
   - Affirmationen-Rotator
   - Hero-Video-Andockstelle (Platzhalter für spätere Higgsfield-Frame-Sequenz)
*/
(function () {
  "use strict";

  /* ---- Mobile-Nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  /* ---- Scroll-Reveals ---- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Affirmationen-Rotator ---- */
  var affirmText = document.querySelector(".affirm-text");
  var dotsWrap = document.querySelector(".affirm-dots");
  if (affirmText) {
    var affirmations = [
      "Ich bin die Architektin meines Erfolgs. Ich diskutiere nicht mit meinen Zielen.",
      "Meine Angst ist kleiner als meine Vision. Ich handle sofort.",
      "Geld fließt zu mir, weil ich Werte schaffe und mutig verkaufe.",
      "Jeder Tag ist ein guter Tag, um neu anzufangen.",
      "Ich stehe wie der Phönix aus der Asche auf: stärker, besser, phänomenal.",
      "Ich brauche keine Erlaubnis, um mein Leben zu leben. Ich gehe jetzt leben.",
      "Ich bin eine Gewinnerin, denn ich treffe Entscheidungen rasch und bleibe lange dabei.",
      "Ich bin tatkräftig und umsetzungsstark. Lieber beginne ich unvollkommen, als perfekt zu zögern.",
      "Ich werde immer stärker; ich bin voller Stärke und Kraft. Ich gebe niemals auf.",
      "Ich bin eine Schöpferin und erschaffe mir das Leben, das ich haben will.",
      "Ich bin mutig und gehe trotz Angst vorwärts.",
      "Ich bin Reichtum, ich bin Wohlstand, ich bin Überfluss. Ich bin ein Geldmagnet.",
      "Ich bin auf dem Weg, Millionärin zu sein. Alles Große braucht Zeit.",
      "Ich akzeptiere keine Ausreden; ich suche Lösungen.",
      "Ich bin die Gestalterin meines Lebens."
    ];
    var idx = 0;
    var dots = [];
    if (dotsWrap) {
      affirmations.forEach(function (_, i) {
        var b = document.createElement("button");
        b.setAttribute("aria-label", "Affirmation " + (i + 1));
        b.addEventListener("click", function () { show(i); });
        dotsWrap.appendChild(b);
        dots.push(b);
      });
    }
    function render() {
      affirmText.textContent = "„" + affirmations[idx] + "“";
      dots.forEach(function (d, i) { d.classList.toggle("active", i === idx); });
    }
    function show(i) {
      idx = (i + affirmations.length) % affirmations.length;
      affirmText.classList.add("fade");
      setTimeout(function () { render(); affirmText.classList.remove("fade"); }, 320);
    }
    render();
    setInterval(function () { show(idx + 1); }, 5000);
  }

  /* ---- Hero-Video-Andockstelle ----
     Später: hier wird die Higgsfield-Frame-Sequenz per Canvas-Scrub eingehängt
     (siehe scroll-cinematic Skill). Aktuell nur Platzhalter-Gradient im CSS. */
  window.WOWMOMAN_HERO_READY = true;

  /* ---- Newsletter-Platzhalter ---- */
  var forms = document.querySelectorAll("form[data-newsletter]");
  forms.forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      f.innerHTML = '<p style="color:var(--gold-400);font-weight:700;margin:0;">Danke! Du bist dabei. Check dein Postfach. 💛</p>';
    });
  });
})();
