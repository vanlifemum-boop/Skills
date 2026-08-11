#!/usr/bin/env bash
# vorschau.sh — schneller 480p-Render nur mit Text und Ton, zur Abnahme des Timings.
# Blendet oben links den Zeitcode ein, damit Korrekturstellen benannt werden können.
set -euo pipefail

HIER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FF="$("$HIER/../../scripts/ensure-ffmpeg.sh" 2>/dev/null | tail -1)"

AUDIO="$HIER/material/song.mp3"
POSTER="$HIER/material/poster.jpg"
ASS="$HIER/bauplatz/text_vorschau.ass"
SCHRIFT="$HIER/bauplatz/schrift"
ZIEL="${1:-$HIER/bauplatz/vorschau_sync.mp4}"

# fontsdir zeigt libass auf die aus docs/fonts konvertierte Archivo Black.
"$FF" -y -v warning -stats \
  -loop 1 -framerate 25 -i "$POSTER" \
  -i "$AUDIO" \
  -filter_complex "\
[0:v]scale=854:480:force_original_aspect_ratio=increase,crop=854:480,\
eq=brightness=-0.28:saturation=0.45,\
ass='$ASS':fontsdir='$SCHRIFT'[v]" \
  -map "[v]" -map 1:a \
  -c:v libx264 -preset veryfast -crf 28 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -shortest -movflags +faststart \
  "$ZIEL"

echo "$ZIEL"
