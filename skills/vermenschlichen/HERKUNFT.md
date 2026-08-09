# Herkunft

Dieser Skill stammt nicht von uns, sondern aus dem Repo
[LOGIN-TB/claude-skills](https://github.com/LOGIN-TB/claude-skills).

- Quelle: `skills/vermenschlichen/SKILL.md`
- Übernommener Stand: `ff74380f1f17ba35bcc785bef74fa881a1c5f155`
- Lizenz: MIT, Copyright (c) 2026 LOGIN — Volltext in [`LIZENZ`](LIZENZ)

Die `SKILL.md` ist unverändert übernommen. Wer sie hier anpasst, sollte das
vermerken, damit beim nächsten Abgleich mit der Quelle klar ist, was von uns
stammt.

## Auf einen neueren Stand bringen

```bash
git clone --depth 1 https://github.com/LOGIN-TB/claude-skills.git /tmp/login-skills
cp /tmp/login-skills/skills/vermenschlichen/SKILL.md skills/vermenschlichen/SKILL.md
```

Alternativ ließe sich der Skill direkt als Plugin beziehen, dann kommen
Aktualisierungen von selbst — er läge aber außerhalb dieses Repos:

```
/plugin marketplace add LOGIN-TB/claude-skills
/plugin install vermenschlichen@login-skills
```
