#!/bin/bash
# Rendert einen Tag und komprimiert das Ergebnis: ./rendern.sh 5
set -e
T=$(printf "%02d" $1)
cd "$(dirname "$0")/../tag-$T"
node /root/.claude/skills/hyperframes/scripts/plugin-cli.mjs render --output ../videos/roh-$T.mp4 > ../videos/log-$T.txt 2>&1
ffmpeg -y -loglevel error -i ../videos/roh-$T.mp4 -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart ../videos/tag-$T.mp4
rm -f ../videos/roh-$T.mp4
echo "Tag $T fertig"
