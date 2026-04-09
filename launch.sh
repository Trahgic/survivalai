#!/usr/bin/env bash
set -euo pipefail

DRIVE_ROOT="$(cd "$(dirname "$0")" && pwd)"
PORT=8080

echo ""
echo "  SurvivalAI — Offline Survival Assistant"
echo "  ========================================="
echo ""

OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS" in
    Linux)  PLATFORM="linux-x64" ;;
    Darwin)
        case "$ARCH" in
            arm64)  PLATFORM="mac-arm64" ;;
            x86_64) PLATFORM="mac-x64" ;;
            *)      echo "[ERROR] Unsupported architecture: $ARCH"; exit 1 ;;
        esac ;;
    *) echo "[ERROR] Unsupported OS: $OS. Use launch.bat on Windows."; exit 1 ;;
esac

SERVER="$DRIVE_ROOT/engine/$PLATFORM/llama-server"
MODEL="$DRIVE_ROOT/model/llama-3.1-8b-q4_k_m.gguf"
UI_DIR="$DRIVE_ROOT/ui"

if [ ! -f "$SERVER" ]; then
    echo "[ERROR] Server binary not found: $SERVER"
    echo "Fallback: open ui/fallback.html in your browser."
    exit 1
fi

if [ ! -f "$MODEL" ]; then
    echo "[ERROR] Model not found: $MODEL"
    exit 1
fi

chmod +x "$SERVER"
mkdir -p "$DRIVE_ROOT/history"

THREADS=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
[ "$THREADS" -gt 2 ] && THREADS=$((THREADS - 1))

echo "  Platform:  $PLATFORM"
echo "  Threads:   $THREADS"
echo "  Server:    http://localhost:$PORT"
echo ""

(sleep 3 && {
    if command -v xdg-open &>/dev/null; then xdg-open "http://localhost:$PORT" 2>/dev/null
    elif command -v open &>/dev/null; then open "http://localhost:$PORT" 2>/dev/null
    fi
}) &

"$SERVER" \
    --model "$MODEL" \
    --ctx-size 4096 \
    --threads "$THREADS" \
    --port "$PORT" \
    --host 127.0.0.1 \
    --path "$UI_DIR" \
    || { echo "[ERROR] Server failed. Fallback: open ui/fallback.html"; exit 1; }
