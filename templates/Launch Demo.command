#!/usr/bin/env bash
# Double-click to (re)launch the local demo. Edit PORT + SITE_NAME per project.
# Works on macOS (double-click) and Linux (bash "Launch Demo.command").
PORT=8777
SITE_NAME="BRAND — cinematic scroll"

# cd to the folder this script lives in (so it serves the site files).
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR" || exit 1

URL="http://localhost:${PORT}/"

# If something is already serving this port, just open it.
if command -v curl >/dev/null 2>&1 && curl -s -o /dev/null "$URL"; then
  echo "[$SITE_NAME] already running at $URL"
else
  echo "[$SITE_NAME] starting static server on port $PORT ..."
  # Prefer python3; fall back to python.
  if command -v python3 >/dev/null 2>&1; then
    python3 -m http.server "$PORT" >/tmp/scroll-cinematic-server.log 2>&1 &
  else
    python -m http.server "$PORT" >/tmp/scroll-cinematic-server.log 2>&1 &
  fi
  SERVER_PID=$!
  echo "[$SITE_NAME] server pid $SERVER_PID (log: /tmp/scroll-cinematic-server.log)"
  # give it a moment to bind
  for _ in 1 2 3 4 5; do
    if curl -s -o /dev/null "$URL" 2>/dev/null; then break; fi
    sleep 0.4
  done
fi

# Open in the default browser.
if command -v open >/dev/null 2>&1; then
  open "$URL"            # macOS
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL"        # Linux
else
  echo "[$SITE_NAME] open $URL in your browser."
fi

echo "[$SITE_NAME] serving $DIR at $URL"
echo "Leave this window open while recording; close it to stop the server."
# Keep the window alive so the server keeps running on macOS double-click.
wait
