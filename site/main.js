/* =====================================================================
   Seifenglück — Scroll-Engine + Rezept-Rendering
   Vanilla JS, keine externen Abhängigkeiten (offline-tauglich).
   ===================================================================== */
(function () {
  "use strict";

  const $  = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const esc = (s) => String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

  /* ---------- Jahr im Footer ---------- */
  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Rezepte rendern ---------- */
  const recipes = window.RECIPES || [];
  const list = $("#recipeList");

  function recipeCard(r) {
    const zutaten = r.zutaten.map((z) => `<li>${esc(z)}</li>`).join("");
    const schritte = r.schritte.map((s) => `<li>${esc(s)}</li>`).join("");
    const hashtags = r.hashtags.map((h) => `<span>${esc(h)}</span>`).join(" ");
    const prompts = r.bildPrompts
      .map((p, i) => `<div class="prompt-box">
          <button class="copy-btn" data-copy="${esc(p)}">Kopieren</button>
          <b>Prompt ${i + 1}</b>
          <p>${esc(p)}</p>
        </div>`).join("");

    return `
    <article class="card reveal" data-cat="${esc(r.category)}" id="rezept-${esc(r.id)}">
      <div class="card__top">
        <span class="card__cat">${esc(r.category)}</span>
        <div class="card__emoji">${r.emoji}</div>
        <h3 class="card__title">${esc(r.title)}</h3>
        <p class="card__subtitle">${esc(r.subtitle)}</p>
        <div class="card__meta">
          <span class="tag tag--time">${esc(r.schwierigkeit)}</span>
          <span class="tag tag--keep">${esc(r.haltbarkeit)}</span>
        </div>
      </div>
      <div class="card__body">
        <p class="card__hook">${esc(r.hook)}</p>
        <p>${esc(r.intro)}</p>

        <div class="recipe-block">
          <h4>Zutaten</h4>
          <ul class="zutaten">${zutaten}</ul>
        </div>

        <div class="recipe-block">
          <h4>So geht's</h4>
          <ol class="schritte">${schritte}</ol>
        </div>

        <div class="callout"><b>Warum es wirkt:</b> ${esc(r.nutzen)}</div>
        <div class="callout callout--tip"><b>Mein Tipp:</b> ${esc(r.tipp)}</div>

        <a class="btn btn--primary card__affiliate" href="${esc(r.affiliate.href)}" rel="sponsored nofollow" target="_blank">${r.affiliate.label}</a>

        <div class="extras">
          <details>
            <summary>Für Social Media & deine Bilder ✨</summary>
            <div class="extras__inner">
              <div class="caption-box">
                <button class="copy-btn" data-copy="${esc(r.caption + "\n\n" + r.hashtags.join(" "))}">Kopieren</button>
                <b>Caption</b>
                <p>${esc(r.caption)}</p>
                <div class="hashtags">${hashtags}</div>
              </div>
              <div>
                <b style="font-size:.86rem;color:var(--sage-deep)">Bild-Prompts (EN, Clean Girl Aesthetic)</b>
                ${prompts}
              </div>
            </div>
          </details>
        </div>
      </div>
    </article>`;
  }

  if (list && recipes.length) {
    list.innerHTML = recipes.map(recipeCard).join("");
  }

  /* ---------- Filter-Chips ---------- */
  const filterBar = $("#filterBar");
  if (filterBar && recipes.length) {
    const cats = ["Alle", ...Array.from(new Set(recipes.map((r) => r.category)))];
    filterBar.innerHTML = cats
      .map((c, i) => `<button class="chip${i === 0 ? " active" : ""}" data-filter="${esc(c)}">${esc(c)}</button>`)
      .join("");

    filterBar.addEventListener("click", (e) => {
      const chip = e.target.closest(".chip");
      if (!chip) return;
      $$(".chip", filterBar).forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
      const f = chip.dataset.filter;
      $$(".card", list).forEach((card) => {
        const show = f === "Alle" || card.dataset.cat === f;
        card.style.display = show ? "" : "none";
      });
    });
  }

  /* ---------- Copy-to-Clipboard ---------- */
  const toast = $("#toast");
  let toastTimer;
  function showToast(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2200);
  }
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".copy-btn");
    if (!btn) return;
    const text = btn.getAttribute("data-copy") || "";
    const done = () => showToast("In die Zwischenablage kopiert ✓");
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
    } else {
      fallbackCopy(text, done);
    }
  });
  function fallbackCopy(text, cb) {
    const ta = document.createElement("textarea");
    ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); cb(); } catch (_) {}
    document.body.removeChild(ta);
  }

  /* ---------- Scroll Reveal (IntersectionObserver) ---------- */
  const revealEls = $$(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }

  /* ---------- Nav Hintergrund beim Scrollen ---------- */
  const nav = $("#nav");
  const onScrollNav = () => {
    if (!nav) return;
    nav.classList.toggle("scrolled", window.scrollY > 40);
  };

  /* ---------- Parallax Hero ---------- */
  const parallaxEls = $$("[data-parallax]");
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      onScrollNav();
      if (!prefersReduced) {
        const y = window.scrollY;
        parallaxEls.forEach((el) => {
          const speed = parseFloat(el.dataset.parallax) || 0.2;
          el.style.transform = `translate3d(0, ${y * speed}px, 0)`;
        });
      }
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Smooth-Scroll für Anker (mit Nav-Offset) ---------- */
  $$('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 70;
      window.scrollTo({ top, behavior: prefersReduced ? "auto" : "smooth" });
    });
  });

  console.log("Seifenglück geladen ·", recipes.length, "Rezepte");
})();
