/* WowMoman — schwebende Kugel-Ebene (vanilla Three.js, lokal gevendort)
   Physik-Kugeln in Markenfarben als fixe Ebene über der ganzen Seite:
   sie folgen der Maus, bekommen beim Scrollen Schub und werden über
   Text durchsichtig, damit alles lesbar bleibt. */
import {
  Clock, PerspectiveCamera, Scene, WebGLRenderer, SRGBColorSpace, ACESFilmicToneMapping,
  MathUtils, Vector2, Vector3, Color, Object3D, InstancedMesh, SphereGeometry,
  MeshStandardMaterial, AmbientLight, PointLight, DirectionalLight, Raycaster, Plane,
  InstancedBufferAttribute,
} from "./vendor/three.module.min.js";

if (window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
  try { init(); } catch (e) { /* WebGL nicht verfügbar → CSS-Fallback bleibt */ }
}

function init() {
  const COLORS = ["#e0479a", "#7b3fa0", "#f3eef5", "#c98adf", "#b53d8f"];
  const COUNT = 90;              // wie Version 1 — volles Bällebad
  const CURSOR_R = 1.4;          // unsichtbarer Cursor-Schieber
  const ALPHA_FULL = 0.95, ALPHA_TEXT = 0.18;

  const host = document.createElement("div");
  host.id = "ballpit-layer";
  host.style.cssText = "position:fixed;inset:0;z-index:30;pointer-events:none;";
  document.body.appendChild(host);
  const heroMedia = document.getElementById("hero-media");
  if (heroMedia) heroMedia.classList.add("has-ballpit");

  const canvas = document.createElement("canvas");
  host.appendChild(canvas);

  const renderer = new WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: "high-performance" });
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = ACESFilmicToneMapping;

  const camera = new PerspectiveCamera(50, 1, 0.1, 100);
  camera.position.set(0, 0, 20);
  const scene = new Scene();

  scene.add(new AmbientLight(0xffffff, 1.1));
  const dirLight = new DirectionalLight(0xffffff, 1.6);
  dirLight.position.set(6, 8, 10);
  scene.add(dirLight);
  const cursorLight = new PointLight(0xec6fb1, 50, 35, 1.8);
  scene.add(cursorLight);

  // Per-Kugel-Transparenz über Instanz-Attribut + Shader-Patch
  const geo = new SphereGeometry(1, 26, 26);
  const alphaAttr = new InstancedBufferAttribute(new Float32Array(COUNT).fill(ALPHA_FULL), 1);
  geo.setAttribute("aAlpha", alphaAttr);
  const mat = new MeshStandardMaterial({ metalness: 0.45, roughness: 0.22, transparent: true });
  mat.onBeforeCompile = (shader) => {
    shader.vertexShader = shader.vertexShader
      .replace("#include <common>", "#include <common>\nattribute float aAlpha;\nvarying float vAlpha;")
      .replace("#include <begin_vertex>", "#include <begin_vertex>\nvAlpha = aAlpha;");
    shader.fragmentShader = shader.fragmentShader
      .replace("#include <common>", "#include <common>\nvarying float vAlpha;")
      .replace("vec4 diffuseColor = vec4( diffuse, opacity );", "vec4 diffuseColor = vec4( diffuse, opacity * vAlpha );");
  };
  const mesh = new InstancedMesh(geo, mat, COUNT);
  const colorObjs = COLORS.map((c) => new Color(c));
  for (let i = 0; i < COUNT; i++) mesh.setColorAt(i, colorObjs[i % colorObjs.length]);
  mesh.instanceColor.needsUpdate = true;
  scene.add(mesh);

  // Physik-Daten
  const pos = new Float32Array(COUNT * 3);
  const vel = new Float32Array(COUNT * 3);
  const size = new Float32Array(COUNT);
  const alpha = new Float32Array(COUNT).fill(ALPHA_FULL);
  const bounds = { x: 12, y: 6, z: 4 };
  size[0] = CURSOR_R;
  for (let i = 1; i < COUNT; i++) size[i] = MathUtils.randFloat(0.3, 0.8);
  for (let i = 0; i < COUNT; i++) {
    pos[i * 3] = MathUtils.randFloatSpread(bounds.x * 2);
    pos[i * 3 + 1] = MathUtils.randFloatSpread(bounds.y * 2);
    pos[i * 3 + 2] = MathUtils.randFloatSpread(bounds.z * 2);
    vel[i * 3] = MathUtils.randFloatSpread(0.02);
    vel[i * 3 + 1] = MathUtils.randFloatSpread(0.02);
  }

  const FRICTION = 0.995, BOUNCE = 0.6, MAXV = 0.2, FOLLOW = 0.4;
  const center = new Vector3();
  const dummy = new Object3D();
  const vA = new Vector3(), vB = new Vector3(), vDiff = new Vector3(), vProj = new Vector3();

  // Maus → Weltposition (Ebene z=0)
  const pointer = new Vector2(0.35, 0.25);
  const raycaster = new Raycaster();
  const plane = new Plane(new Vector3(0, 0, 1), 0);
  window.addEventListener("pointermove", (e) => {
    pointer.set((e.clientX / window.innerWidth) * 2 - 1, -(e.clientY / window.innerHeight) * 2 + 1);
  }, { passive: true });

  // Kraeftiger Scroll-Impuls
  let scrollKick = 0, lastScrollY = window.scrollY;
  window.addEventListener("scroll", () => {
    const dy = window.scrollY - lastScrollY;
    lastScrollY = window.scrollY;
    scrollKick = MathUtils.clamp(scrollKick + dy * 0.005, -0.25, 0.25);
  }, { passive: true });

  // Text-Rechtecke (Dokument-Koordinaten) fuer die Durchsichtig-ueber-Text-Logik
  let textRects = [];
  function collectTextRects() {
    const els = document.querySelectorAll("h1, h2, h3, h4, p, li, blockquote, .btn, .eyebrow, .affirm-text");
    const rects = [];
    els.forEach((el) => {
      if (!el.offsetParent && el.offsetWidth === 0) return;
      const r = el.getBoundingClientRect();
      if (r.width < 8 || r.height < 8) return;
      rects.push({ l: r.left, t: r.top + window.scrollY, r: r.right, b: r.bottom + window.scrollY });
    });
    textRects = rects;
  }
  collectTextRects();
  setInterval(collectTextRects, 2000); // Reveals/Layout-Aenderungen einsammeln
  window.addEventListener("resize", collectTextRects);

  function step(dt) {
    // Cursor-Kugel folgt der Maus
    raycaster.setFromCamera(pointer, camera);
    raycaster.ray.intersectPlane(plane, center);
    vA.fromArray(pos, 0).lerp(center, 0.15).toArray(pos, 0);
    cursorLight.position.set(pos[0], pos[1], pos[2] + 2);

    for (let i = 1; i < COUNT; i++) {
      const b = i * 3;
      vA.fromArray(pos, b); vB.fromArray(vel, b);
      // sanfte Anziehung zur Maus → die Kugeln folgen dem Zeiger
      vDiff.subVectors(center, vA);
      vB.addScaledVector(vDiff.normalize(), FOLLOW * dt);
      vB.y += scrollKick * size[i];          // Scroll-Schub
      vB.multiplyScalar(FRICTION).clampLength(0, MAXV);
      vA.add(vB);
      for (let j = 0; j < COUNT; j++) {
        if (j === i) continue;
        const ob = j * 3;
        vDiff.set(pos[ob] - vA.x, pos[ob + 1] - vA.y, pos[ob + 2] - vA.z);
        const d = vDiff.length(), rSum = size[i] + size[j];
        if (d > 0 && d < rSum) {
          const push = (rSum - d) * 0.5;
          vDiff.normalize();
          vA.addScaledVector(vDiff, -push);
          vB.addScaledVector(vDiff, -push * 0.6);
        }
      }
      if (Math.abs(vA.x) + size[i] > bounds.x) { vA.x = Math.sign(vA.x) * (bounds.x - size[i]); vB.x *= -BOUNCE; }
      if (Math.abs(vA.y) + size[i] > bounds.y) { vA.y = Math.sign(vA.y) * (bounds.y - size[i]); vB.y *= -BOUNCE; }
      if (Math.abs(vA.z) + size[i] > bounds.z) { vA.z = Math.sign(vA.z) * (bounds.z - size[i]); vB.z *= -BOUNCE; }
      vA.toArray(pos, b); vB.toArray(vel, b);
    }
    scrollKick *= 0.88;

    // Projektion + Text-Check + Alpha-Blende
    const w = window.innerWidth, h = window.innerHeight;
    const fov = (camera.fov * Math.PI) / 180;
    const wh = 2 * Math.tan(fov / 2) * camera.position.z;
    const pxPerUnit = h / wh;
    const fade = 1 - Math.exp(-dt * 10);
    for (let i = 1; i < COUNT; i++) {
      vProj.fromArray(pos, i * 3).project(camera);
      const sx = ((vProj.x + 1) / 2) * w;
      const sy = ((1 - vProj.y) / 2) * h + window.scrollY; // Dokument-Koordinate
      const rPx = size[i] * pxPerUnit;
      let overText = false;
      for (let k = 0; k < textRects.length; k++) {
        const t = textRects[k];
        const cx = Math.max(t.l, Math.min(sx, t.r));
        const cy = Math.max(t.t, Math.min(sy, t.b));
        const dx = sx - cx, dy2 = sy - cy;
        if (dx * dx + dy2 * dy2 < rPx * rPx) { overText = true; break; }
      }
      const target = overText ? ALPHA_TEXT : ALPHA_FULL;
      alpha[i] += (target - alpha[i]) * fade;
    }
    alphaAttr.array.set(alpha);
    alphaAttr.needsUpdate = true;

    for (let i = 0; i < COUNT; i++) {
      dummy.position.fromArray(pos, i * 3);
      dummy.scale.setScalar(i === 0 ? 0.0001 : size[i]); // Cursor-Kugel unsichtbar
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
  }

  function resize() {
    const w = window.innerWidth || 1, h = window.innerHeight || 1;
    renderer.setSize(w, h, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const fov = (camera.fov * Math.PI) / 180;
    const wh = 2 * Math.tan(fov / 2) * camera.position.z;
    bounds.y = wh / 2;
    bounds.x = (wh * camera.aspect) / 2;
    bounds.z = bounds.x / 4;
  }
  window.addEventListener("resize", resize);
  resize();

  const clock = new Clock();
  let running = false, raf = 0;
  function loop() {
    raf = requestAnimationFrame(loop);
    const dt = Math.min(clock.getDelta(), 0.05);
    step(dt);
    renderer.render(scene, camera);
  }
  function setRunning(on) {
    if (on && !running) { running = true; clock.start(); loop(); }
    else if (!on && running) { running = false; cancelAnimationFrame(raf); clock.stop(); }
  }
  setRunning(true);
  document.addEventListener("visibilitychange", () => setRunning(!document.hidden));
}
