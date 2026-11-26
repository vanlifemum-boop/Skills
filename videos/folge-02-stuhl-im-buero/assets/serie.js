/* Systemfehler Familie — gemeinsame Animationshelfer für alle Szenen.
   Alles hängt nur an der Timeline-Zeit, nichts läuft von selbst. */
window.SF = (function () {
  const POSEN = ["ruhig", "erklaert", "denkt", "zeigt"];

  // Posenwechsel: Bild tauschen, kurz "einatmen" (Squash + Settle)
  function pose(tl, fig, name, t) {
    POSEN.forEach((p) => {
      const el = document.querySelector("#" + fig + "-" + p);
      if (el) tl.set(el, { opacity: p === name ? 1 : 0 }, t);
    });
    tl.fromTo(
      "#" + fig + "-hub",
      { scaleY: 0.975, scaleX: 1.015 },
      { scaleY: 1, scaleX: 1, duration: 0.32, ease: "back.out(3)" },
      t,
    );
  }

  // Ruhiges Atmen über die ganze Szene
  function atem(tl, fig, dauer, versatz = 0) {
    const zyklus = 1.7;
    tl.fromTo(
      "#" + fig + "-atem",
      { scaleY: 1 },
      {
        scaleY: 1.012,
        duration: zyklus,
        ease: "sine.inOut",
        yoyo: true,
        repeat: Math.max(0, Math.floor((dauer - versatz) / zyklus) - 1),
      },
      versatz,
    );
  }

  // Beim Sprechen leicht mitgehen (Kopf/Oberkörper-Wippen)
  function sprich(tl, fig, t, dauer) {
    const takt = 0.42;
    const n = Math.max(1, Math.floor(dauer / takt));
    for (let i = 0; i < n; i++) {
      const s = t + i * takt;
      const r = [0.9, -0.6, 0.5, -0.9, 0.7][i % 5];
      tl.to("#" + fig + "-hub", { rotation: r, y: -5, duration: takt / 2, ease: "sine.out" }, s);
      tl.to("#" + fig + "-hub", { rotation: 0, y: 0, duration: takt / 2, ease: "sine.in" }, s + takt / 2);
    }
  }

  // Gehen: gleichmäßig vorwärts, jeder Schritt hebt und kippt leicht
  function gehen(tl, fig, t, von, bis, dauer) {
    tl.fromTo("#" + fig, { x: von }, { x: bis, duration: dauer, ease: "none" }, t);
    const schritt = 0.32;
    const n = Math.max(1, Math.floor(dauer / schritt));
    for (let i = 0; i < n; i++) {
      const s = t + i * schritt;
      const r = i % 2 ? -1.6 : 1.6;
      tl.to("#" + fig + "-hub", { y: -16, rotation: r, duration: schritt / 2, ease: "sine.out" }, s);
      tl.to("#" + fig + "-hub", { y: 0, rotation: 0, duration: schritt / 2, ease: "sine.in" }, s + schritt / 2);
    }
  }

  // Sprechblase oder Infokasten: aufploppen, halten, ausblenden
  function blase(tl, sel, t, dauer) {
    tl.fromTo(
      sel,
      { opacity: 0, scale: 0.72, y: 24 },
      { opacity: 1, scale: 1, y: 0, duration: 0.38, ease: "back.out(2.2)" },
      t,
    );
    tl.to(sel, { opacity: 0, y: -12, duration: 0.26, ease: "power2.in" }, t + dauer - 0.26);
  }

  // Einblenden und stehen lassen
  function rein(tl, sel, t, von = { y: 30 }) {
    tl.fromTo(
      sel,
      Object.assign({ opacity: 0 }, von),
      { opacity: 1, x: 0, y: 0, scale: 1, rotation: 0, duration: 0.5, ease: "power3.out" },
      t,
    );
  }

  return { pose, atem, sprich, gehen, blase, rein };
})();
