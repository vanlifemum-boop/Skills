#!/usr/bin/env bash
# Ensure an ffmpeg binary is available without Homebrew.
# Prints the path to a usable ffmpeg on stdout (last line) and exits 0 on success.
# Order of preference:
#   1. system ffmpeg on PATH
#   2. previously downloaded static binary at /tmp/ffmpeg-bin/ffmpeg
#   3. the static build shipped by the imageio-ffmpeg wheel (PyPI)
#   4. download a static build for this OS/arch into /tmp/ffmpeg-bin/ffmpeg
set -euo pipefail

BIN_DIR="/tmp/ffmpeg-bin"
BIN="$BIN_DIR/ffmpeg"

log() { printf '[ensure-ffmpeg] %s\n' "$*" >&2; }

# 1. system ffmpeg
if command -v ffmpeg >/dev/null 2>&1; then
  log "using system ffmpeg: $(command -v ffmpeg)"
  command -v ffmpeg
  exit 0
fi

# 2. cached static binary
if [ -x "$BIN" ]; then
  log "using cached static ffmpeg: $BIN"
  echo "$BIN"
  exit 0
fi

# 3. imageio-ffmpeg from PyPI. Sandboxes commonly allow pypi.org while blocking the
#    download hosts used below, so this is the more reliable route there. Its wheel
#    carries a full static build (libass, libfreetype, zoompan, xfade, libx264).
if command -v python3 >/dev/null 2>&1; then
  IIO_FF="$(python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null || true)"
  if [ -z "$IIO_FF" ] && python3 -m pip install --quiet imageio-ffmpeg >/dev/null 2>&1; then
    IIO_FF="$(python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())' 2>/dev/null || true)"
  fi
  if [ -n "$IIO_FF" ] && [ -x "$IIO_FF" ]; then
    log "using imageio-ffmpeg build: $IIO_FF"
    echo "$IIO_FF"
    exit 0
  fi
fi

mkdir -p "$BIN_DIR"

OS="$(uname -s)"
ARCH="$(uname -m)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

fetch() {
  # fetch <url> <out>
  if command -v curl >/dev/null 2>&1; then
    curl -fL --retry 4 --retry-delay 2 -o "$2" "$1"
  elif command -v wget >/dev/null 2>&1; then
    wget -O "$2" "$1"
  else
    log "neither curl nor wget available"; return 1
  fi
}

case "$OS" in
  Darwin)
    # evermeet static builds (universal-ish). zip contains a single 'ffmpeg' binary.
    URL="https://evermeet.cx/ffmpeg/getrelease/ffmpeg/zip"
    log "downloading macOS static ffmpeg..."
    fetch "$URL" "$TMP/ffmpeg.zip"
    unzip -o -q "$TMP/ffmpeg.zip" -d "$TMP"
    mv "$TMP/ffmpeg" "$BIN"
    ;;
  Linux)
    case "$ARCH" in
      x86_64|amd64) FF_ARCH="amd64" ;;
      aarch64|arm64) FF_ARCH="arm64" ;;
      armv7l) FF_ARCH="armhf" ;;
      i686|i386) FF_ARCH="i686" ;;
      *) log "unsupported Linux arch: $ARCH"; exit 1 ;;
    esac
    URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-${FF_ARCH}-static.tar.xz"
    log "downloading Linux static ffmpeg ($FF_ARCH)..."
    fetch "$URL" "$TMP/ffmpeg.tar.xz"
    tar -xJf "$TMP/ffmpeg.tar.xz" -C "$TMP"
    FF_PATH="$(find "$TMP" -type f -name ffmpeg | head -n1)"
    if [ -z "$FF_PATH" ]; then log "ffmpeg not found in archive"; exit 1; fi
    mv "$FF_PATH" "$BIN"
    ;;
  *)
    log "unsupported OS: $OS"; exit 1 ;;
esac

chmod +x "$BIN"
log "installed static ffmpeg: $BIN"
echo "$BIN"
