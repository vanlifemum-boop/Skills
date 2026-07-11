/* WowMoman — interaktiver Kugel-Hero (vanilla Three.js, lokal gevendort)
   Physik-Kugeln in Markenfarben, die dem Mauszeiger folgen.
   Wird in #hero-media eingehängt; ohne WebGL bleibt der CSS-Verlauf stehen. */
import {
  Clock, PerspectiveCamera, Scene, WebGLRenderer, SRGBColorSpace, ACESFilmicToneMapping,
  MathUtils, Vector2, Vector3, Color, Object3D, InstancedMesh, SphereGeometry,
  MeshStandardMaterial, AmbientLight, PointLight, DirectionalLight, Raycaster, Plane,
} from "./vendor/three.module.min.js";

const HOST = document.getElementById("hero-media");
if (HOST && window.matchMedia("(prefers-reduced-motion: no-preference)").matches) {
  try { init(HOST); } catch (e) { /* WebGL nicht verfügbar → CSS-Fallback bleibt */ }
}

function init(host) {
  const COLORS = ["#e0479a", "#7b3fa0", "#f3eef5", "#c98adf", "#b53d8f"];
  const COUNT = 90;

  const canvas = document.createElement("canvas");
  host.appendChild(canvas);
  host.classList.add("has-ballpit");

  const renderer = new WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: "high-performance" });
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = ACESFilmicToneMapping;

  const camera = new PerspectiveCamera(50, 1, 0.1, 100);
  camera.position.set(0, 0, 20);
  const scene = new Scene();

  // Licht
  scene.add(new AmbientLight(0xffffff, 1.1));
  const dir = new DirectionalLight(0xffffff, 1.6);
  dir.position.set(6, 8, 10);
  scene.add(dir);
  const cursorLight = new PointLight(0xec6fb1, 60, 40, 1.8);
  scene.add(cursorLight);

  // Instanzierte Kugeln
  const geo = new SphereGeometry(1, 28, 28);
  const mat = new MeshStandardMaterial({ metalness: 0.45, roughness: 0.22 });
  const mesh = new InstancedMesh(geo, mat, COUNT);
  const colorObjs = COLORS.map((c) => new Color(c));
  for (let i = 0; i < COUNT; i++) mesh.setColorAt(i, colorObjs[i % colorObjs.length]);
  mesh.instanceColor.needsUpdate = true;
  scene.add(mesh);

  // Physik-Daten
  const pos = new Float32Array(COUNT * 3);
  const vel = new Float32Array(COUNT * 3);
  const size = new Float32Array(COUNT);
  const bounds = { x: 12, y: 6, z: 5 };
  size[0] = 1.6; // Cursor-Kugel
  for (let i = 1; i < COUNT; i++) size[i] = MathUtils.randFloat(0.35, 0.95);
  for (let i = 0; i < COUNT; i++) {
    pos[i * 3] = MathUtils.randFloatSpread(bounds.x * 2);
    pos[i * 3 + 1] = MathUtils.randFloatSpread(bounds.y * 2);
    pos[i * 3 + 2] = MathUtils.randFloatSpread(bounds.z * 2);
  }

  const GRAVITY = 0.35, FRICTION = 0.995, BOUNCE = 0.55, MAXV = 0.14;
  const center = new Vector3();
  const dummy = new Object3D();
  const vA = new Vector3(), vB = new Vector3(), vDiff = new Vector3();

  // Maus → Weltposition (Ebene z=0)
  const pointer = new Vector2(0.3, 0.2);
  const raycaster = new Raycaster();
  const plane = new Plane(new Vector3(0, 0, 1), 0);
  window.addEventListener("pointermove", (e) => {
    const r = host.getBoundingClientRect();
    pointer.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  }, { passive: true });

  function step(dt) {
    // Kugel 0 folgt dem Cursor
    raycaster.setFromCamera(pointer, camera);
    raycaster.ray.intersectPlane(plane, center);
    vA.fromArray(pos, 0).lerp(center, 0.12).toArray(pos, 0);
    cursorLight.position.set(pos[0], pos[1], pos[2] + 2);

    for (let i = 1; i < COUNT; i++) {
      const b = i * 3;
      vA.fromArray(pos, b); vB.fromArray(vel, b);
      vB.y -= dt * GRAVITY * size[i];
      vB.multiplyScalar(FRICTION).clampLength(0, MAXV);
      vA.add(vB);
      // Kollision mit allen anderen (inkl. Cursor-Kugel)
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
      // Wände
      if (Math.abs(vA.x) + size[i] > bounds.x) { vA.x = Math.sign(vA.x) * (bounds.x - size[i]); vB.x *= -BOUNCE; }
      if (vA.y - size[i] < -bounds.y) { vA.y = -bounds.y + size[i]; vB.y *= -BOUNCE; }
      if (vA.y + size[i] > bounds.y) { vA.y = bounds.y - size[i]; vB.y *= -BOUNCE; }
      if (Math.abs(vA.z) + size[i] > bounds.z) { vA.z = Math.sign(vA.z) * (bounds.z - size[i]); vB.z *= -BOUNCE; }
      vA.toArray(pos, b); vB.toArray(vel, b);
    }
    for (let i = 0; i < COUNT; i++) {
      dummy.position.fromArray(pos, i * 3);
      dummy.scale.setScalar(size[i]);
      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    }
    mesh.instanceMatrix.needsUpdate = true;
  }

  function resize() {
    const w = host.offsetWidth || 1, h = host.offsetHeight || 1;
    renderer.setSize(w, h, false);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    const fov = (camera.fov * Math.PI) / 180;
    const wh = 2 * Math.tan(fov / 2) * camera.position.z;
    bounds.y = wh / 2;
    bounds.x = (wh * camera.aspect) / 2;
    bounds.z = bounds.x / 3;
  }
  window.addEventListener("resize", resize);
  resize();

  // Nur animieren, wenn sichtbar (Akku/Perf)
  const clock = new Clock();
  let running = false, raf = 0;
  function loop() {
    raf = requestAnimationFrame(loop);
    const dt = Math.min(clock.getDelta(), 0.05);
    step(dt);
    renderer.render(scene, camera);
  }
  new IntersectionObserver((entries) => {
    const vis = entries[0].isIntersecting && !document.hidden;
    if (vis && !running) { running = true; clock.start(); loop(); }
    else if (!vis && running) { running = false; cancelAnimationFrame(raf); clock.stop(); }
  }, { threshold: 0 }).observe(canvas);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && running) { running = false; cancelAnimationFrame(raf); clock.stop(); }
    else if (!document.hidden && !running) { running = true; clock.start(); loop(); }
  });
}
