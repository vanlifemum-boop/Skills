---
name: scroll-cinematic
description: Build an award-winning "3D scroll" website of ANY kind from ONE prompt — product launch, portfolio, agency, contractor/home-services, restaurant, real estate, personal brand, event, app, etc. Generates a high-end cinematic hero visual + clips (360° orbit, fly-through, reveal, explode, parallax) fitting the site's subject with the Higgsfield MCP, slices them into a scroll-scrubbed canvas frame sequence with ffmpeg, builds a branded multi-section site (Lenis smooth scroll + scroll reveals), and launches it on localhost. Use when the user asks for a "3D scroll" site, scroll-driven hero/reveal, a cinematic landing page, a buckssauce/Apple/Awwwards-style scroll site, or "build me a website like X" — for a product OR a service, person, place, or brand. Trigger words: 3D scroll, scroll animation, cinematic hero, fly-through, turntable, scroll site, landing page, portfolio site, agency site, Higgsfield site.
---

# Scroll-Cinematic — one-prompt 3D product sites

## What this actually is (read first)
The viral "3D scroll" effect is **not** Three.js. It's a **canvas image-sequence scrub**:
a short cinematic clip is exported to ~180 numbered JPGs, all preloaded, and the frame
drawn to a `<canvas>` is chosen by scroll progress. Scrolling forward/backward plays the
clip. Add Lenis smooth scroll + scroll-synced overlay copy and it reads as premium 3D.
The "3D" comes entirely from the source video — which we generate with Higgsfield.

Stack: plain **HTML + CSS + JS + Lenis** (zero build, runs from any static server).
**Lenis is vendored** at `templates/vendor/lenis.min.js` — no CDN, works fully offline.

## Prerequisites
- **Higgsfield MCP** connected + credits (~$1–2 / site). This is the only thing the user must set up.
- **ffmpeg** — DO NOT ask the user to install it. Step 0 below installs it automatically (no Homebrew).
- This skill installed at `~/.claude/skills/scroll-cinematic/`.

### Step 0 — Ensure ffmpeg (run first, always)
Run `bash ~/.claude/skills/scroll-cinematic/scripts/ensure-ffmpeg.sh`. It uses system ffmpeg if
present, otherwise downloads a static binary to `/tmp/ffmpeg-bin/ffmpeg` (macOS/Linux, no Homebrew).
The extract/compress scripts already fall back to that path. Never block the build on ffmpeg.

## THE PIPELINE — run all of this from the single prompt

### 1. Decide the brief (works for ANY site — no extra questions unless the subject is unclear)
From the user's prompt pick: **site type**, **hero subject**, **vibe/palette**, **brand/name**
(invent one if not given), and **2 hero motions**. The hero subject is whatever the site is
about — a product, a person/founder, a building/space, a dish, a vehicle, or an abstract visual.
Default motions by site type:
- **Product** (bottle, gadget, shoe, cosmetic) → 360° rotation + explode/pour/reveal.
- **Portfolio / personal brand** → cinematic portrait or abstract liquid/geometry motion + a slow parallax/orbit.
- **Agency / app / SaaS** → abstract 3D shape/logo morph or UI-in-space + light-streak fly-through.
- **Contractor / home services / real estate** → slow orbit or fly-through of a building/home/jobsite + a detail reveal.
- **Restaurant / food** → dish 360° + ingredient/steam motion or interior fly-through.
- **Fitness / events / travel** → motion of the subject (athlete, crowd, landscape) + a sweeping camera move.
If unsure, default to one **hero orbit/fly-through** + one **reveal/parallax** clip.

### 2. Generate the hero keyframe (Higgsfield `generate_image`)
- Model: **`nano_banana_pro`** (top quality / crisp). Prompt the hero subject for the site
  (product, person, place, abstract), strong lighting, intentional background, "ultra sharp,
  photorealistic, 8k, editorial/advertising". 16:9. (For portfolios you can also use a brand-colored
  abstract 3D render so there's no likeness/IP issue.)
- Poll `job_display` until `status:"completed"`; keep the job **id** (used as the video start frame).

### 3. Generate 1–2 cinematic clips (Higgsfield `generate_video`)
- Model: **`seedance_2_0`**, `resolution:"1080p"`, `aspect_ratio:"16:9"`, `duration:6`,
  `medias:[{role:"start_image", value:<keyframe id>}]`. Always pass
  `declined_preset_id:"24bae836-2c4a-48e0-89b6-49fcc0b21612"` if it suggests a preset; if it
  suggests a different preset, retry with that preset's id in `declined_preset_id`.
- Motion prompt patterns (pick what fits the subject):
  - **turntable** — "smooth seamless full 360-degree rotation, one complete revolution, stays centered".
  - **fly-through** — "slow continuous forward camera flight through/around the [building/space/scene], smooth dolly, deep parallax".
  - **reveal/explode** — "the [contents/components/elements] burst or assemble outward and float in slow motion" (keep it object/scene context — moderation-friendly).
  - **abstract** — "elegant slow-morphing liquid-metal / glass / particle form drifting and rotating".
- **Generate both clips in parallel** (two tool calls in one message), then poll `job_display`.
  1080p renders take ~3–8 min; sleep in the background between polls.
- **Cost:** preflight with `get_cost:true` once; ~54 credits per 1080p clip. Confirm if the user is low.

### 4. Handle render results
- `completed` → download `results.rawUrl` with `curl`.
- `nsfw` or `failed` → **refunded, retry**. Moderation false-flags abstract "floating pills/
  dissolving figures"; reword to product-context, or switch that clip to **`grok_video_v15`**
  (`resolution:"720p"`, more lenient). Product turntables/explosions pass at 1080p.
- Tell the user about any retry; never claim a clip rendered if it didn't.

### 5. Slice + compress frames (ffmpeg)
- `scripts/extract-frames.sh <clip.mp4> frames/<name> 180`  → ~179 numbered JPGs.
- `scripts/compress-frames.sh frames/<name> 1600 88`        → 1600px wide, q88 (crisp, <~15MB/section).
- One folder per clip (e.g. `frames/spin`, `frames/explode`).

### 6. Build the site from templates/
- Copy `templates/index.html`, `styles.css`, `scroll-cinematic.js`, `booking.js`, and
  `vendor/lenis.min.js` into the project (keep the `vendor/` path so Lenis loads locally).
- Edit the `SCRUB_SECTIONS` config (bottom of index.html) — one entry per clip:
  `{ section:"#hero", frameCount:179, bg:"#0a0a12", framePath:(i)=>\`frames/spin/frame_${String(i).padStart(4,"0")}.jpg\` }`.
- Write brand copy, palette (CSS vars), benefit/colorway/feature sections, stats, CTA.
- **Booking function** (already wired in the template): the `#booking` section + `booking.js`
  give a self-contained appointment form — validation, an inline confirmation, a downloadable
  `.ics` calendar invite, and a pre-filled `mailto:` fallback (no backend needed). Configure via
  the inline `window.BOOKING_CONFIG` block (business name, email, services, duration). For real
  submissions set `endpoint` to a Formspree/API URL; it POSTs JSON and still falls back gracefully.
- **Hue-shift trick** for product variants/colorways (no extra generation):
  `ffmpeg -i base.png -vf "hue=h=120:s=1.15" variant.png`.

### 7. Launch on localhost
- Copy `templates/Launch Demo.command` into the project, edit PORT + name, `chmod +x` it.
- Start it (`python3 -m http.server <port>`), `curl` the page + a frame to confirm 200, `open` the URL.
- Tell the user the URL + that double-clicking the .command relaunches it for recording.

## Engine rules (already in templates/scroll-cinematic.js)
- Preload every frame; paint frame 0 on first load; redraw only when the frame index changes.
- Sticky stage: outer section `height: 420–600vh`, inner `position:sticky; top:0; height:100vh`.
  Progress = `clamp(-rect.top / (rect.height - innerH), 0, 1)`. Throttle in the rAF loop.
- Cover-fit draw + HiDPI (`devicePixelRatio`, cap 2). Drive updates from the Lenis rAF loop
  (robust to any scroll source). Overlay copy fades over per-line `[in,out]` progress windows.
- Multi-section: `SCRUB_SECTIONS` array; engine **skips** sections whose element is missing.

## Known gotchas
- More/larger frames = slow load → keep 1600px / q88 / ~180 frames.
- Continuous-motion clips only (no hard cuts — ugly when scrubbed backward).
- The headless screenshot tool blanks sticky-canvas sections when scrolled; verify with
  pixel sampling, and view live in a real browser.
- `python http.server` previews die when idle — the `.command` launcher is the durable demo.

## Live demo + GitHub Pages
- `docs/` is a **self-contained live demo** (`docs/index.html`) that renders the scroll-scrub
  effect with **procedural canvas scenes** (`docs/demo-scene.js`) — no generated frames, so it
  works with zero binary assets. It includes the working booking function.
- `.github/workflows/pages.yml` publishes `docs/` to **GitHub Pages** on push. Live URL:
  `https://<owner>.github.io/<repo>/`.
  - **Enable Pages once:** repo **Settings → Pages → Build and deployment → Source: "GitHub
    Actions"**. The Actions token usually can't turn Pages on by itself (`enablement:true` then
    fails with *"Resource not accessible by integration"*), so this one manual flip is required;
    after it, re-run the workflow and every push deploys.
  - **Private repos:** GitHub Pages on a *private* repo needs a paid plan (Pro/Team/Enterprise).
    On a free plan, make the repo public first, or host the demo elsewhere.
- To showcase a *real* build instead of the procedural demo, drop the generated `frames/` into
  `docs/` and swap the `render:` sections for `framePath:` in `docs/index.html`.

## Files
- `templates/index.html`, `styles.css`, `scroll-cinematic.js` — multi-section scrub site.
- `templates/booking.js` — self-contained booking form (validation, `.ics`, mailto, optional POST).
- `templates/vendor/lenis.min.js` — vendored Lenis smooth-scroll (no CDN).
- `templates/demo-scene.js` — procedural canvas scenes for a no-asset preview.
- `templates/CinematicReveal.tsx` — React/Next drop-in (optional).
- `templates/Launch Demo.command` — double-click localhost launcher.
- `scripts/ensure-ffmpeg.sh`, `scripts/extract-frames.sh`, `scripts/compress-frames.sh` — the ffmpeg pipeline.
- `docs/` + `.github/workflows/pages.yml` — the live GitHub Pages demo.
