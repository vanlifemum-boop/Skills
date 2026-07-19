# CLAUDE.md

Guidance for AI assistants (Claude Code and others) working in this repository.

## What this repository is

This is a **Claude Code Skills** repository. A Skill is a self-contained,
model-invoked capability: a `SKILL.md` file with YAML frontmatter (`name` +
`description`) that Claude reads and follows when a user's request matches the
skill's trigger. Skills may ship supporting `scripts/` and `templates/`
alongside the `SKILL.md`.

At present the repository contains **one skill**, defined at the root:

- `SKILL.md` — **`scroll-cinematic`**: builds an "award-winning 3D scroll"
  website from a single prompt. It generates a cinematic hero image and clips
  via the **Higgsfield MCP**, slices the clips into a numbered JPG sequence with
  **ffmpeg**, and assembles a scroll-scrubbed, Lenis-smooth static site
  (plain HTML/CSS/JS, zero build) served on localhost.

> **Note:** `SKILL.md` references `templates/` (`index.html`, `styles.css`,
> `scroll-cinematic.js`, `CinematicReveal.tsx`, `Launch Demo.command`) and
> `scripts/` (`ensure-ffmpeg.sh`, `extract-frames.sh`, `compress-frames.sh`).
> Those directories are **not currently committed** to this repo. The skill
> expects to run from an installed location (`~/.claude/skills/scroll-cinematic/`)
> where those files are present. If you add or edit the skill, keep `SKILL.md`
> and its referenced files in sync.

## Repository layout

```
.
├── SKILL.md      # the scroll-cinematic skill definition
└── CLAUDE.md     # this file
```

As more skills are added, the conventional layout is one directory per skill:

```
<skill-name>/
├── SKILL.md      # frontmatter + instructions (required)
├── scripts/      # helper scripts the skill shells out to (optional)
└── templates/    # files the skill copies into the user's project (optional)
```

## SKILL.md conventions

A `SKILL.md` has two parts:

1. **YAML frontmatter** (between `---` fences) with:
   - `name` — kebab-case identifier (e.g. `scroll-cinematic`).
   - `description` — a dense, trigger-rich paragraph. This is what the model
     matches against a user request, so it must state *what the skill does*,
     *when to use it*, and include concrete **trigger words/phrases**. Write it
     for retrieval, not marketing.

2. **Markdown body** — the actual playbook the model follows: prerequisites, an
   ordered pipeline, engine/implementation rules, known gotchas, and a file
   manifest. Keep steps imperative and runnable; call out external
   dependencies (MCP servers, CLI tools) and how to satisfy them without
   asking the user to do manual setup where avoidable.

When authoring or editing a skill, the `skill-creator` skill is the canonical
tool for scaffolding, refining, and evaluating skills — prefer it over
hand-rolling structure.

## Conventions observed in this repo

- **Zero-build output.** The scroll-cinematic skill produces plain
  HTML/CSS/JS + Lenis that runs from any static server — no bundler, no npm
  build step. Preserve this when editing the templates.
- **Don't make the user install tooling.** ffmpeg is bootstrapped by
  `scripts/ensure-ffmpeg.sh` (system binary if present, otherwise a static
  download to `/tmp/ffmpeg-bin/ffmpeg`) rather than asking the user to install
  it. Follow the same "make it work without manual setup" principle.
- **Be honest about generation results.** For MCP-driven media generation,
  poll job status, handle `nsfw`/`failed` (refunded → retry, reword, or switch
  models), and never claim an asset rendered when it didn't.
- **Cost awareness.** Higgsfield generation costs real credits (~$1–2 per
  site). Preflight with `get_cost:true` and confirm with the user when they're
  low on credits.

## External dependencies

- **Higgsfield MCP** — image/video/audio generation. Tools include
  `generate_image`, `generate_video`, `job_display`, `models_explore`. The user
  must have it connected with credits.
- **ffmpeg** — frame extraction/compression. Bootstrapped by the skill, not a
  hard user prerequisite.

## Development workflow

There is no build, test, or lint tooling in this repository — it is a
Markdown-and-assets skill repo. "Correctness" means:

- `SKILL.md` frontmatter parses (valid YAML, `name` + `description` present).
- The body's instructions are internally consistent and every file it
  references in its **Files** section actually exists (or is clearly marked as
  installed elsewhere).
- Any shell scripts are executable and portable (macOS + Linux) with sensible
  fallbacks.

### Git

- **Work on the branch you were assigned**; create it from the latest default
  branch if it doesn't exist. Do not push to other branches without explicit
  permission.
- Write clear, descriptive commit messages.
- Do **not** open a pull request unless explicitly asked.

## Adding a new skill

1. Create `<skill-name>/SKILL.md` with valid frontmatter (kebab-case `name`, a
   trigger-rich `description`).
2. Put helper scripts in `<skill-name>/scripts/` and copy-in assets in
   `<skill-name>/templates/`.
3. Keep the body's **Files** manifest accurate.
4. Use the `skill-creator` skill to scaffold and validate.
