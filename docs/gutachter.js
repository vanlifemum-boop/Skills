(function () {
  "use strict";

  var daten = window.GUTACHTER_DATEN || [];
  var suche = document.getElementById("gs-suche");
  var liste = document.getElementById("gs-liste");
  var anzahl = document.getElementById("gs-anzahl");
  var leer = document.getElementById("gs-leer");
  if (!suche || !liste || !anzahl) return;

  function normalisieren(text) {
    return (text || "").toLocaleLowerCase("de-DE");
  }

  function eintragText(e) {
    return normalisieren([e.name, e.ort].concat(e.details || []).join(" "));
  }

  function escapeHtml(text) {
    var div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  function renderEintrag(e) {
    var el = document.createElement("article");
    el.className = "gs-eintrag";

    var name = document.createElement("h3");
    name.textContent = e.name;
    el.appendChild(name);

    if (e.ort) {
      var ort = document.createElement("p");
      ort.className = "gs-ort";
      ort.textContent = e.ort;
      el.appendChild(ort);
    }

    if (e.details && e.details.length) {
      var details = document.createElement("p");
      details.className = "gs-details";
      details.innerHTML = e.details.map(escapeHtml).join("<br />");
      el.appendChild(details);
    }

    if (e.profil) {
      var link = document.createElement("a");
      link.className = "gs-profil";
      link.href = e.profil;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = "Profil auf vaterlos.eu ansehen";
      el.appendChild(link);
    }

    return el;
  }

  var alleEintraege = daten.map(function (e) {
    return { daten: e, text: eintragText(e), el: renderEintrag(e) };
  });

  var frag0 = document.createDocumentFragment();
  alleEintraege.forEach(function (item) { frag0.appendChild(item.el); });
  liste.appendChild(frag0);

  function render() {
    var q = normalisieren(suche.value.trim());
    var treffer = 0;
    alleEintraege.forEach(function (item) {
      var passt = !q || item.text.indexOf(q) !== -1;
      item.el.hidden = !passt;
      if (passt) treffer++;
    });
    anzahl.textContent = treffer === alleEintraege.length
      ? treffer + " Einträge insgesamt"
      : treffer + " von " + alleEintraege.length + " Einträgen";
    if (leer) leer.hidden = treffer !== 0;
  }

  suche.addEventListener("input", render);
  render();
})();
