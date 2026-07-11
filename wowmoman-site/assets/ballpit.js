/* WowMoman — schwebende Kugel-Ebene (vanilla Three.js, lokal gevendort)
   Physik-Kugeln in Markenfarben als fixe Ebene über der ganzen Seite:
   sie wandern beim Scrollen mit, reagieren auf Scroll-Impulse und weichen
   dem Mauszeiger aus. Ohne WebGL/Reduced-Motion bleibt der CSS-Verlauf. */
import {
  Clock, PerspectiveCamera, Scene, WebGLRenderer, SRGBColorSpace, ACESFilmicToneMapping,
  MathUtils, Vector2, Vector3, Color, Object3D, InstancedMesh, SphereGeometry,
  MeshStandardMaterial, AmbientLight, PointLight, DirectionalLight, Raycaster, Plane,
} from "./vendor/three.module.min.js";

if (window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
  try { init(); } catch (e) { /* WebGL nicht verfügbar → CSS-Fallback bleibt */ }
}

function init() {
  const COLORS = ["#e0479a", "#7b3fa0", "#f3eef5", "#c98adf", "#b53d8f"];
  const COUNT = 46;          // Kugel 0 = unsichtbarer Cursor-Schieber
  const CURSOR_R = 1.2;

  // Fixe Ebene über der ganzen Seite (unter der Navigation, über dem Inhalt)
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
  const dir = new DirectionalLight(0xffffff, 1.6);
  dir.position.set(6, 8, 10);
  scene.add(dir);
  const cursorLight = new PointLight(0xec6fb1, 40, 30, 1.8);
  scene.add(cursorLight);

  const geo = new SphereGeometry(1, 26, 26);
  const mat = new MeshStandardMaterial({ metalness: 0.45, roughness: 0.22, transparent: true, opacity: 0.92 });
  const mesh = new InstancedMesh(geo, mat, COUNT);
  const colorObjs = COLORS.map((c) => new Color(c));
  for (let i = 0; i < COUNT; i++) mesh.setColorAt(i, colorObjs[i % colorObjs.length]);
  mesh.instanceColor.needsUpdate = true;
  scene.add(mesh);

  // Physik-Daten
  const pos = new Float32Array(COUNT * 3);
  const vel = new Float32Array(COUNT * 3);
  const size = new Float32Array(COUNT);
  const bounds = { x: 12, y: 6, z: 4 };
  size[0] = CURSOR_R;
  for (let i = 1; i < COUNT; i++) size[i] = MathUtils.randFloat(0.18, 0.55);
  for (let i = 0; i < COUNT; i++) {
    pos[i * 3] = MathUtils.randFloatSpread(bounds.x * 2);
    pos[i * 3 + 1] = MathUtils.randFloatSpread(bounds.y * 2);
    pos[i * 3 + 2] = MathUtils.randFloatSpread(bounds.z * 2);
    vel[i * 3] = MathUtils.randFloatSpread(0.02);
    vel[i * 3 + 1] = MathUtils.randFloatSpread(0.02);
  }

  const FRICTION = 0.997, BOUNCE = 0.6, MAXV = 0.16;
  const center = new Vector3();
  const dummy = new Object3D();
  const vA = new Vector3(), vB = new Vector3(), vDiff = new Vector3();

  // Maus → Weltposition (Ebene z=0); pointer-events:none → global lauschen
  const pointer = new Vector2(0.35, 0.25);
  const raycaster = new Raycaster();
  const plane = new Plane(new Vector3(0, 0, 1), 0);
  window.addEventListener("pointermove", (e) => {
    pointer.set((e.clientX / window.innerWidth) * 2 - 1, -(e.clientY / window.innerHeight) * 2 + 1);
  }, { passive: true });

  // Scroll-Impuls: beim Scrollen bekommen die Kugeln einen sanften Schubs
  let scrollKick = 0, lastScrollY = window.scrollY;
  window.addEventListener("scroll", () => {
    const dy = window.scrollY - lastScrollY;
    lastScrollY = window.scrollY;
    scrollKick = MathUtils.clamp(scrollKick + dy * 0.0015, -0.09, 0.09);
  }, { passive: true });

  function step(dt) {
    raycaster.setFromCamera(pointer, camera);
    raycaster.ray.intersectPlane(plane, center);
    vA.fromArray(pos, 0).lerp(center, 0.14).toArray(pos, 0);
    cursorLight.position.set(pos[0], pos[1], pos[2] + 2);

    for (let i = 1; i < COUNT; i++) {
      const b = i * 3;
      vA.fromArray(pos, b); vB.fromArray(vel, b);
      vB.y += scrollKick * size[i];              // Scroll schiebt die Kugeln
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
      // Wände (weiches Zurückfedern am Viewport-Rand)
      if (Math.abs(vA.x) + size[i] > bounds.x) { vA.x = Math.sign(vA.x) * (bounds.x - size[i]); vB.x *= -BOUNCE; }
      if (Math.abs(vA.y) + size[i] > bounds.y) { vA.y = Math.sign(vA.y) * (bounds.y - size[i]); vB.y *= -BOUNCE; }
      if (Math.abs(vA.z) + size[i] > bounds.z) { vA.z = Math.sign(vA.z) * (bounds.z - size[i]); vB.z *= -BOUNCE; }
      vA.toArray(pos, b); vB.toArray(vel, b);
    }
    scrollKick *= 0.9; // Impuls klingt ab

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

  // Nur animieren, wenn der Tab sichtbar ist (Akku/Perf)
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
