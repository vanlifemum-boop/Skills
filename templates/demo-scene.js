/* demo-scene.js — procedural canvas scenes for the zero-asset demo.
 *
 * These simulate the "cinematic clip" look without any generated frames, so the
 * scroll-scrub effect is visible on GitHub Pages. In a real build you replace
 * these render functions with `framePath` pointing at Higgsfield-derived JPGs.
 *
 * Each function has the signature render(ctx, progress, { width, height }),
 * where progress is 0..1 for that section's scroll.
 */
window.DemoScenes = (function () {
  "use strict";

  function lerp(a, b, t) { return a + (b - a) * t; }

  // Radial background glow.
  function glow(ctx, w, h, cx, cy, r, color) {
    const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, r);
    g.addColorStop(0, color);
    g.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, w, h);
  }

  /* Scene 1 — a metallic orb on a turntable: rotates one full turn over the
     section, with a moving specular highlight and an orbiting ring. */
  function turntable(ctx, progress, { width: w, height: h }) {
    const cx = w * 0.5;
    const cy = h * 0.52;
    const R = Math.min(w, h) * 0.26;
    const angle = progress * Math.PI * 2; // one revolution

    glow(ctx, w, h, cx, cy - R * 0.4, R * 3.2, "rgba(108,123,255,0.22)");

    // Orbiting ring (behind).
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(angle * 0.5);
    ctx.strokeStyle = "rgba(176,108,255,0.35)";
    ctx.lineWidth = Math.max(2, R * 0.03);
    ctx.beginPath();
    ctx.ellipse(0, 0, R * 1.5, R * 0.5, 0, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();

    // The orb: base sphere gradient with a highlight that moves with rotation.
    const hlx = cx + Math.cos(angle) * R * 0.5;
    const hly = cy - R * 0.4 + Math.sin(angle) * R * 0.2;
    const sphere = ctx.createRadialGradient(hlx, hly, R * 0.05, cx, cy, R * 1.05);
    sphere.addColorStop(0, "#eef0ff");
    sphere.addColorStop(0.25, "#8f9bff");
    sphere.addColorStop(0.7, "#3a3f8f");
    sphere.addColorStop(1, "#0d0e1c");
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.fillStyle = sphere;
    ctx.fill();

    // Rotating banding to read as a spinning surface.
    ctx.save();
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.clip();
    ctx.globalAlpha = 0.12;
    for (let i = 0; i < 10; i++) {
      const bx = cx + Math.cos(angle + i) * R * 2 - R;
      ctx.fillStyle = i % 2 ? "#ffffff" : "#1a1c3a";
      ctx.fillRect(bx, cy - R, R * 0.35, R * 2);
    }
    ctx.restore();

    // Orbiting ring (front).
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(angle * 0.5);
    ctx.strokeStyle = "rgba(108,123,255,0.75)";
    ctx.lineWidth = Math.max(2, R * 0.035);
    ctx.beginPath();
    ctx.ellipse(0, 0, R * 1.5, R * 0.5, 0, Math.PI * 0.02, Math.PI * 0.98);
    ctx.stroke();
    ctx.restore();

    // Floor reflection.
    const refl = ctx.createLinearGradient(0, cy + R, 0, cy + R * 2.2);
    refl.addColorStop(0, "rgba(108,123,255,0.18)");
    refl.addColorStop(1, "rgba(108,123,255,0)");
    ctx.fillStyle = refl;
    ctx.fillRect(cx - R * 1.4, cy + R * 0.9, R * 2.8, R * 1.3);
  }

  /* Scene 2 — assembling shards: particles start scattered and converge into a
     tight ring as you scroll (an "explode/assemble" beat, reversible). */
  const SHARDS = 90;
  const seeds = Array.from({ length: SHARDS }, (_, i) => ({
    a: (i / SHARDS) * Math.PI * 2 + (i * 2.399),
    scatter: 0.6 + ((i * 7) % 40) / 40,
    hue: i % 3,
    size: 0.6 + ((i * 13) % 100) / 100,
  }));

  function assemble(ctx, progress, { width: w, height: h }) {
    const cx = w * 0.5;
    const cy = h * 0.5;
    const R = Math.min(w, h) * 0.3;
    const t = progress; // 0 scattered -> 1 assembled
    const spin = progress * Math.PI;

    glow(ctx, w, h, cx, cy, R * 2.6, "rgba(176,108,255,0.18)");

    const colors = ["#6c7bff", "#b06cff", "#8fa0ff"];
    for (const s of seeds) {
      const ang = s.a + spin;
      const scatterR = R * (2.4 * s.scatter);
      const rr = lerp(scatterR, R, t);
      const x = cx + Math.cos(ang) * rr;
      const y = cy + Math.sin(ang) * rr * 0.72;
      const size = Math.max(1.5, R * 0.035 * s.size) * lerp(1.6, 1, t);
      ctx.globalAlpha = lerp(0.25, 0.95, t);
      ctx.fillStyle = colors[s.hue];
      ctx.beginPath();
      ctx.arc(x, y, size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;

    // Core that brightens as things lock in.
    const core = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 0.6);
    core.addColorStop(0, `rgba(255,255,255,${0.15 + t * 0.5})`);
    core.addColorStop(0.5, `rgba(140,160,255,${0.1 + t * 0.35})`);
    core.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = core;
    ctx.fillRect(0, 0, w, h);
  }

  return { turntable, assemble };
})();
