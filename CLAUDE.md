# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## What this repository is

This is a **Claude Code Skill** repository. It packages a single skill,
**`scroll-cinematic`**, which builds an award-winning "3D scroll" website from one
prompt. It is **not** a conventional application codebase — there is no build system,
no test suite, no dependency manifest, and no source tree to compile. The deliverable
*is* the skill definition: a set of instructions and (when fully assembled) supporting
templates and scripts that Claude follows at runtime to generate a website for the user.

Do not treat this repo like an app. There is nothing here to `npm install`, `build`,
or `run`. Changes are almost always edits to prose instructions in `SKILL.md` (or to
the template/script assets described below).

## Current repository layout

```
.
└── SKILL.md        # The entire skill: front-matter metadata + runtime instructions
```

That is the complete tracked contents today. `SKILL.md` is the source of truth.

### Referenced-but-not-yet-tracked assets

`SKILL.md` documents a `templates/` and a `scripts/` directory that are **not currently
present** in this repository:

- `templates/index.html`, `templates/styles.css`, `templates/scroll-cinematic.js` — the
  multi-section canvas image-sequence scrub site.
- `templates/CinematicReveal.tsx` — optional React/Next drop-in.
- `templates/Launch Demo.command` — double-click localhost launcher.
- `scripts/ensure-ffmpeg.sh` — installs a static ffmpeg binary if none is present.
- `scripts/extract-frames.sh` — slices a clip into ~180 numbered JPGs.
- `scripts/compress-frames.sh` — downsizes/compresses those frames.

When a skill is *installed* (into `~/.claude/skills/scroll-cinematic/`), these files live
alongside `SKILL.md`. If you are asked to make the skill self-contained, add these assets
here so the paths in `SKILL.md` resolve. Until then, keep `SKILL.md`'s file references
accurate to whatever is actually shipped.

## How the skill works (the pipeline)

`scroll-cinematic` produces the viral "3D scroll" effect, which is a **canvas
image-sequence scrub** — *not* Three.js. A short cinematic clip is exported to ~180
numbered JPGs, all preloaded, and the frame painted to a `<canvas>` is chosen by scroll
progress (via Lenis smooth scroll). The "3D" comes entirely from the source video.

The runtime pipeline encoded in `SKILL.md`:

1. **Decide the brief** — infer site type, hero subject, vibe/palette, brand, and two hero
   motions from the user's prompt.
2. **Generate the hero keyframe** — Higgsfield `generate_image` (`nano_banana_pro`, 16:9).
3. **Generate 1–2 cinematic clips** — Higgsfield `generate_video` (`seedance_2_0`, 1080p),
   run in parallel, poll `job_display`.
4. **Handle render results** — download on success; on `nsfw`/`failed`, reword and retry
   (or fall back to `grok_video_v15`).
5. **Slice + compress frames** — the ffmpeg scripts (`extract-frames.sh`,
   `compress-frames.sh`).
6. **Build the site** — copy the `templates/` files, edit the `SCRUB_SECTIONS` config, write
   brand copy/palette/sections.
7. **Launch on localhost** — via `Launch Demo.command` / `python3 -m http.server`.

## External dependencies (runtime, not repo)

These are needed when the *skill runs*, not to work on this repo:

- **Higgsfield MCP** — image/video generation. The only thing the end user must set up
  (needs credits, ~$1–2 per site). Higgsfield MCP tools are available in this environment
  (`mcp__Higgsfield__generate_image`, `generate_video`, `job_display`, etc.).
- **ffmpeg** — never ask the user to install it; `scripts/ensure-ffmpeg.sh` downloads a
  static binary to `/tmp/ffmpeg-bin/ffmpeg` if the system lacks it.
- The generated site itself is **zero-build**: plain HTML + CSS + JS + Lenis, served from
  any static server.

## Conventions

- **`SKILL.md` is the product.** Its YAML front-matter (`name`, `description`) is how
  Claude Code discovers and triggers the skill — edit the `description` carefully, since its
  trigger words determine when the skill fires. Keep `name: scroll-cinematic` stable.
- **Keep instructions runnable and honest.** The skill emphasizes never claiming a clip
  rendered if it didn't, and always telling the user about retries. Preserve that tone in
  any edits.
- **Match the existing document style** — imperative, numbered pipeline steps, concrete
  tool names and parameters, a "Known gotchas" section. Extend those sections rather than
  restructuring wholesale.
- **File references must stay accurate.** If you add, rename, or remove a template/script,
  update the `## Files` list and every inline path in `SKILL.md` to match.

## Development workflow

- **Branch:** do all work on `claude/claude-md-docs-m8wgx5` (create it from `main` if
  needed). Never push to `main` without explicit permission.
- **Commit** with clear, descriptive messages. **Push** with `git push -u origin <branch>`.
- **Do not open a pull request** unless explicitly asked.
- There are no tests or linters to run. "Verifying" a change means re-reading `SKILL.md`
  for internal consistency (do the pipeline steps, file paths, and tool names still line
  up?) and, where practical, exercising the actual pipeline end-to-end.

## Editing checklist for AI assistants

Before committing changes to this repo, confirm:

- [ ] `SKILL.md` front-matter is valid YAML and `name`/`description` are intact.
- [ ] Every file path mentioned in `SKILL.md` exists in the repo (or is clearly noted as an
      installed-skill asset).
- [ ] Tool names and parameters (Higgsfield models, ffmpeg script args) are still correct.
- [ ] The numbered pipeline remains coherent end to end.
- [ ] This `CLAUDE.md` still reflects the actual layout if you added/removed files.
