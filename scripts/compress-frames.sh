#!/usr/bin/env bash
# Downscale + recompress a frame folder in place so it loads fast on the web.
# Usage: compress-frames.sh <dir> [width] [quality]
#   dir      folder of frame_*.jpg produced by extract-frames.sh
#   width    target width in px (default 1600; height auto, keeps aspect)
#   quality  JPEG quality 2-31 lower=better for ffmpeg qscale; we accept a
#            0-100 "quality" and map it (default 88 -> crisp, small)
set -euo pipefail

DIR="${1:?usage: compress-frames.sh <dir> [width] [quality]}"
WIDTH="${2:-1600}"
QUALITY="${3:-88}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG="ffmpeg"
elif [ -x /tmp/ffmpeg-bin/ffmpeg ]; then
  FFMPEG="/tmp/ffmpeg-bin/ffmpeg"
else
  FFMPEG="$(bash "$SCRIPT_DIR/ensure-ffmpeg.sh" | tail -n1)"
fi

if [ ! -d "$DIR" ]; then echo "[compress-frames] not a dir: $DIR" >&2; exit 1; fi

# Map 0-100 quality to ffmpeg qscale:v (2=best .. 31=worst).
QSCALE="$(awk -v q="$QUALITY" 'BEGIN{v=2+(100-q)*(29/100); if(v<2)v=2; if(v>31)v=31; printf "%d", v}')"

count=0
total_before=0
for f in "$DIR"/frame_*.jpg; do
  [ -e "$f" ] || continue
  total_before=$((total_before + $(wc -c < "$f")))
  "$FFMPEG" -y -loglevel error -i "$f" \
    -vf "scale=${WIDTH}:-2:flags=lanczos" -qscale:v "$QSCALE" "$f.tmp.jpg"
  mv "$f.tmp.jpg" "$f"
  count=$((count+1))
done

total_after=0
for f in "$DIR"/frame_*.jpg; do
  [ -e "$f" ] || continue
  total_after=$((total_after + $(wc -c < "$f")))
done

mb() { awk -v b="$1" 'BEGIN{printf "%.1f", b/1048576}'; }
echo "[compress-frames] $count frames @ ${WIDTH}px q${QUALITY} (qscale ${QSCALE}) -> $DIR"
echo "[compress-frames] size: $(mb $total_before)MB -> $(mb $total_after)MB"
