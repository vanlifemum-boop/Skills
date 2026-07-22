#!/usr/bin/env bash
# Slice a clip into N evenly-spaced numbered JPGs for canvas scrubbing.
# Usage: extract-frames.sh <clip.mp4> <out_dir> [count]
#   clip.mp4  source video (continuous motion, no hard cuts)
#   out_dir   destination folder (created; frames named frame_0000.jpg ...)
#   count     number of frames to emit (default 180)
set -euo pipefail

CLIP="${1:?usage: extract-frames.sh <clip.mp4> <out_dir> [count]}"
OUT="${2:?usage: extract-frames.sh <clip.mp4> <out_dir> [count]}"
COUNT="${3:-180}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve ffmpeg (system, cached, or downloaded).
if command -v ffmpeg >/dev/null 2>&1; then
  FFMPEG="ffmpeg"
elif [ -x /tmp/ffmpeg-bin/ffmpeg ]; then
  FFMPEG="/tmp/ffmpeg-bin/ffmpeg"
else
  FFMPEG="$(bash "$SCRIPT_DIR/ensure-ffmpeg.sh" | tail -n1)"
fi

if [ ! -f "$CLIP" ]; then echo "[extract-frames] source not found: $CLIP" >&2; exit 1; fi
mkdir -p "$OUT"
rm -f "$OUT"/frame_*.jpg

# Probe duration so we can spread exactly COUNT frames across the whole clip.
DUR="$("$FFMPEG" -i "$CLIP" 2>&1 | awk -F', ' '/Duration/ {print $1}' | awk '{print $2}' \
  | awk -F: '{printf "%f", ($1*3600)+($2*60)+$3}')"

if [ -z "$DUR" ] || [ "$DUR" = "0.000000" ]; then
  # Fallback: pull frames at source rate then trim/pad to COUNT.
  echo "[extract-frames] could not probe duration; extracting at source fps" >&2
  "$FFMPEG" -y -loglevel error -i "$CLIP" -qscale:v 2 "$OUT/frame_%04d.jpg"
else
  FPS="$(awk -v c="$COUNT" -v d="$DUR" 'BEGIN{printf "%f", c/d}')"
  "$FFMPEG" -y -loglevel error -i "$CLIP" -vf "fps=${FPS}" -qscale:v 2 "$OUT/frame_%04d.jpg"
fi

# Normalize to exactly COUNT frames and 0-based naming (frame_0000.jpg ...).
i=0
for f in $(ls "$OUT"/frame_*.jpg 2>/dev/null | sort); do
  printf -v newname "$OUT/tmp_%04d.jpg" "$i"
  mv "$f" "$newname"
  i=$((i+1))
done
# trim overflow
while [ "$i" -gt "$COUNT" ]; do
  i=$((i-1))
  printf -v extra "$OUT/tmp_%04d.jpg" "$i"
  rm -f "$extra"
done
# rename tmp_ -> frame_
n=0
for f in $(ls "$OUT"/tmp_*.jpg 2>/dev/null | sort); do
  printf -v final "$OUT/frame_%04d.jpg" "$n"
  mv "$f" "$final"
  n=$((n+1))
done

echo "[extract-frames] wrote $n frames to $OUT (requested $COUNT)"
