/* =====================================================================
   Seifenglück — Rendering + Scroll-Engine („Botanical Noir")
   Vanilla JS, keine externen Abhängigkeiten.
   ===================================================================== */
(function () {
  "use strict";

  const $  = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const esc = (s) => String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
  const pad = (n) => String(n).padStart(2, "0");

  const yearEl = $("#year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Rezepte als Editorial-Reihen rendern ---------- */
  const recipes = window.RECIPES || [];
  const list = $("#recipeList");

  function recipeRow(r, i) {
    const zutaten  = r.zutaten.map((z) => `<li>${esc(z)}</li>`).join("");
    const schritte = r.schritte.map((s) => `<li>${esc(s)}</li>`).join("");
    const hashtags = r.hashtags.map((h) => `<span>${esc(h)}</span>`).join(" ");
    const prompts  = r.bildPrompts.map((p, n) => `
      <div class="box box--prompt">
        <button class="copy-btn" data-copy="${esc(p)}">Kopieren</button>
        <b>Prompt ${n + 1}</b>
        <p>${esc(p)}</p>
      </div>`).join("");

    return `
    <article class="rx reveal" data-cat="${esc(r.category)}" id="rezept-${esc(r.id)}">
      <div class="rx__aside">
        <span class="rx__num">${pad(i + 1)}</span>
        <div class="rx__emoji">${r.emoji}</div>
        <span class="rx__cat">${esc(r.category)}</span>
        <h3 class="rx__title">${esc(r.title)}</h3>
        <p class="rx__subtitle">${esc(r.subtitle)}</p>
        <div class="rx__meta">
          <span class="tag tag--time">${esc(r.schwierigkeit)}</span>
          <span class="tag tag--keep">${esc(r.haltbarkeit)}</span>
        </div>
        <a class="btn btn--primary rx__cta" href="${esc(r.affiliate.href)}"
           rel="sponsored nofollow" target="_blank">${r.affiliate.label}</a>
      </div>

      <div class="rx__main">
        <p class="rx__hook">${esc(r.hook)}</p>
        <p class="rx__intro">${esc(r.intro)}</p>

        <div class="block">
          <h4>Zutaten</h4>
          <ul class="zutaten">${zutaten}</ul>
        </div>

        <div class="block">
          <h4>So geht's</h4>
          <ol class="schritte">${schritte}</ol>
        </div>

        <div class="note"><b>Warum es wirkt:</b> ${esc(r.nutzen)}</div>
        <div class="note note--tip"><b>Mein Tipp:</b> ${esc(r.tipp)}</div>

        <div class="extras">
          <details>
            <summary>Für Social Media &amp; deine Bilder</summary>
            <div class="extras__inner">
              <div class="box">
                <button class="copy-btn" data-copy="${esc(r.caption + "\n\n" + r.hashtags.join(" "))}">Kopieren</button>
                <b>Caption</b>
                <p>${esc(r.caption)}</p>
                <div class="hashtags">${hashtags}</div>
              </div>
              ${prompts}
            </div>
          </details>
        </div>
      </div>
    </article>`;
  }

  if (list && recipes.length) {
    list.innerHTML = recipes.map(recipeRow).join("");
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
      $$(".rx", list).forEach((row) => {
        row.style.display = (f === "Alle" || row.dataset.cat === f) ? "" : "none";
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
  function fallbackCopy(text, cb) {
    const ta = document.createElement("textarea");
    ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta); ta.select();
    try { document.execCommand("copy"); cb(); } catch (_) {}
    document.body.removeChild(ta);
  }
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".copy-btn");
    if (!btn) return;
    const text = btn.getAttribute("data-copy") || "";
    const done = () => showToast("Kopiert ✓");
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
    } else {
      fallbackCopy(text, done);
    }
  });

  /* ---------- Zeilen-Masken im Hero staffeln ---------- */
  $$(".hero__title .line i").forEach((el, i) => el.style.setProperty("--i", i));

  /* ---------- Scroll Reveal ---------- */
  const revealEls = $$(".reveal");
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in");
        io.unobserve(entry.target);
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }

  /* ---------- Scroll: Fortschritt, Nav, Parallax ---------- */
  const nav = $("#nav");
  const bar = $("#progress");
  const parallaxEls = $$("[data-parallax]");
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const y = window.scrollY;

      if (nav) nav.classList.toggle("scrolled", y > 40);

      if (bar) {
        const max = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (max > 0 ? (y / max) * 100 : 0) + "%";
      }

      if (!prefersReduced) {
        parallaxEls.forEach((el) => {
          const speed = parseFloat(el.dataset.parallax) || 0.2;
          el.style.transform = `translate3d(0, ${y * speed}px, 0)`;
        });
      }
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });
  onScroll();

  /* ---------- Anker mit Nav-Offset ---------- */
  $$('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      window.scrollTo({
        top: target.getBoundingClientRect().top + window.scrollY - 72,
        behavior: prefersReduced ? "auto" : "smooth"
      });
    });
  });

  console.log("Seifenglück · Botanical Noir ·", recipes.length, "Rezepte");
})();
