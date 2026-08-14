#!/usr/bin/env bash
# Macht alle Skills aus diesem Ordner in ALLEN Projekten verfügbar — und dazu
# die stehenden Vorgaben aus vorgaben.md als ~/.claude/CLAUDE.md.
#
# Für jeden Unterordner mit einer SKILL.md wird ein Symlink unter
# ~/.claude/skills/<name> angelegt. Weil es Symlinks sind, wirkt jedes spätere
# "git pull" sofort — ohne erneutes Installieren.
#
#   bash skills/installieren.sh
#
# Schutzregel: ein bereits vorhandener ECHTER Ordner wird nie gelöscht und nie
# überschrieben, sondern gemeldet und übersprungen. Nur Symlinks werden erneuert.

set -euo pipefail

hier="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ziel="${HOME}/.claude/skills"

mkdir -p "$ziel"

verlinkt=0
uebersprungen=0

for ordner in "$hier"/*/; do
  [ -f "${ordner}SKILL.md" ] || continue

  name="$(basename "$ordner")"
  pfad="${ziel}/${name}"

  if [ -L "$pfad" ]; then
    # Ein Symlink von einem früheren Lauf — der darf erneuert werden.
    if [ "$(readlink "$pfad")" = "${hier}/${name}" ]; then
      echo "  bereits verlinkt   ${name}"
      verlinkt=$((verlinkt + 1))
      continue
    fi
    rm "$pfad"
  elif [ -e "$pfad" ]; then
    # Ein echter Ordner oder eine echte Datei — Finger weg.
    echo "  ÜBERSPRUNGEN       ${name} — dort liegt schon etwas Echtes: ${pfad}"
    echo "                     Bitte selbst ansehen und ggf. von Hand wegräumen."
    uebersprungen=$((uebersprungen + 1))
    continue
  fi

  ln -s "${hier}/${name}" "$pfad"
  echo "  verlinkt           ${name}"
  verlinkt=$((verlinkt + 1))
done

echo
echo "${verlinkt} Skills unter ${ziel} verfügbar, ${uebersprungen} übersprungen."

# Stehende Vorgaben (vorgaben.md) nach ~/.claude/CLAUDE.md verlinken.
# Gleiche Schutzregel: eine echte Datei wird nie überschrieben.
quelle="${hier}/vorgaben.md"
merkdatei="${HOME}/.claude/CLAUDE.md"

if [ -f "$quelle" ]; then
  echo
  if [ -L "$merkdatei" ] && [ "$(readlink "$merkdatei")" = "$quelle" ]; then
    echo "Vorgaben: bereits verlinkt (${merkdatei})."
  elif [ -e "$merkdatei" ] || [ -L "$merkdatei" ]; then
    echo "Vorgaben: ÜBERSPRUNGEN — ${merkdatei} existiert bereits."
    echo "  Um sie trotzdem zu übernehmen, diese Zeile dort einfügen:"
    echo "    @${quelle}"
  else
    ln -s "$quelle" "$merkdatei"
    echo "Vorgaben: verlinkt (${merkdatei} → ${quelle})."
  fi
fi

if [ "$verlinkt" -gt 0 ]; then
  echo "Claude Code neu starten, damit die Skills gefunden werden."
fi

if [ -z "${KIE_API_KEY:-}" ] && [ -f "${hier}/media-skill/SKILL.md" ]; then
  echo
  echo "Hinweis: KIE_API_KEY ist nicht gesetzt — media-skill braucht ihn."
  echo "  export KIE_API_KEY='dein-schluessel'   (dauerhaft in ~/.zshrc bzw. ~/.bashrc)"
fi
