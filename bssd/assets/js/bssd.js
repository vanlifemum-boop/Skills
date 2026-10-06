// BSSD — kleine Helfer: Mobilmenü, Scroll-Einblendung, Kontaktformular, Jahreszahl.
(function () {
  // Mobilmenü
  var burger = document.querySelector(".burger");
  var nav = document.querySelector(".nav");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      var offen = nav.classList.toggle("ist-offen");
      burger.setAttribute("aria-expanded", String(offen));
      burger.textContent = offen ? "✕" : "☰";
    });
  }

  // Scroll-Einblendung (bewegt nur, blendet nie aus — Inhalt bleibt immer lesbar)
  var ziele = document.querySelectorAll("[data-zeigen]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("ist-sichtbar"); io.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    ziele.forEach(function (el) { io.observe(el); });
  } else {
    ziele.forEach(function (el) { el.classList.add("ist-sichtbar"); });
  }

  // Kontaktformular: Bereich aus ?bereich=… vorwählen, beim Absenden E-Mail vorbereiten
  var form = document.getElementById("anfrage");
  if (form) {
    var bereich = new URLSearchParams(location.search).get("bereich");
    if (bereich && form.bereich) {
      var opt = form.bereich.querySelector('option[value="' + bereich + '"]');
      if (opt) opt.selected = true;
    }
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (!form.reportValidity()) return;
      var f = form.elements;
      var betreff = "Anfrage: " + f.bereich.options[f.bereich.selectedIndex].text;
      var text =
        "Name: " + f.name.value + "\n" +
        "E-Mail: " + f.email.value + "\n" +
        (f.telefon.value ? "Telefon: " + f.telefon.value + "\n" : "") +
        "Bereich: " + f.bereich.options[f.bereich.selectedIndex].text + "\n\n" +
        f.nachricht.value;
      location.href = "mailto:" + form.dataset.empfaenger +
        "?subject=" + encodeURIComponent(betreff) + "&body=" + encodeURIComponent(text);
    });
  }

  var jahr = document.getElementById("jahr");
  if (jahr) jahr.textContent = new Date().getFullYear();
})();
