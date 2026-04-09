#!/usr/bin/env bash
set -euo pipefail

# SurvivalAI Drive Builder
# Run this on Linux or macOS to build a working USB drive.
# Prerequisites: git, cmake, gcc/g++ (or clang), python3, wget/curl

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
DRIVE_DIR="$SCRIPT_DIR/drive-output"

echo ""
echo "  ============================================"
echo "  SurvivalAI Drive Builder"
echo "  ============================================"
echo ""

mkdir -p "$BUILD_DIR"

# ==================== STEP 1: sql.js ====================
echo "[1/5] Downloading sql.js (SQLite in WebAssembly)..."
if [ -f "$SCRIPT_DIR/drive/ui/sql-wasm.js" ] && [ -f "$SCRIPT_DIR/drive/ui/sql-wasm.wasm" ]; then
    echo "  Already downloaded, skipping."
else
    SQLJS_VERSION="1.11.0"
    SQLJS_URL="https://github.com/AlaSQL/sql.js/releases/download/v${SQLJS_VERSION}"
    # Actually use cdnjs or the sql.js npm package
    SQLJS_CDN="https://cdnjs.cloudflare.com/ajax/libs/sql.js/${SQLJS_VERSION}"
    
    mkdir -p "$SCRIPT_DIR/drive/ui"
    wget -q -O "$SCRIPT_DIR/drive/ui/sql-wasm.js" "${SQLJS_CDN}/sql-wasm.js" 2>/dev/null || \
    curl -sL -o "$SCRIPT_DIR/drive/ui/sql-wasm.js" "${SQLJS_CDN}/sql-wasm.js"
    
    wget -q -O "$SCRIPT_DIR/drive/ui/sql-wasm.wasm" "${SQLJS_CDN}/sql-wasm.wasm" 2>/dev/null || \
    curl -sL -o "$SCRIPT_DIR/drive/ui/sql-wasm.wasm" "${SQLJS_CDN}/sql-wasm.wasm"
    
    echo "  Downloaded sql-wasm.js + sql-wasm.wasm"
fi

# ==================== STEP 2: MODEL ====================
echo ""
echo "[2/5] Checking for model..."
MODEL_DIR="$SCRIPT_DIR/drive/model"
MODEL_FILE="$MODEL_DIR/llama-3.1-8b-q4_k_m.gguf"
mkdir -p "$MODEL_DIR"

if [ -f "$MODEL_FILE" ]; then
    echo "  Model found: $(ls -lh "$MODEL_FILE" | awk '{print $5}')"
else
    echo ""
    echo "  MODEL NOT FOUND."
    echo ""
    echo "  Download the Llama 3.1 8B Instruct Q4_K_M GGUF file and place it at:"
    echo "    $MODEL_FILE"
    echo ""
    echo "  Search HuggingFace for: llama-3.1-8b-instruct gguf q4_k_m"
    echo "  Direct search: https://huggingface.co/models?search=llama+3.1+8b+instruct+gguf"
    echo ""
    echo "  The file should be approximately 4.9 GB."
    echo "  After downloading, rename it to: llama-3.1-8b-q4_k_m.gguf"
    echo ""
    echo "  Then re-run this script."
    echo ""
    exit 1
fi

# ==================== STEP 3: LLAMA.CPP ====================
echo ""
echo "[3/5] Building llama.cpp server..."

OS="$(uname -s)"
ARCH="$(uname -m)"

case "$OS-$ARCH" in
    Linux-x86_64)   PLATFORM="linux-x64" ;;
    Darwin-arm64)   PLATFORM="mac-arm64" ;;
    Darwin-x86_64)  PLATFORM="mac-x64" ;;
    *) echo "  Unsupported platform: $OS-$ARCH"; exit 1 ;;
esac

ENGINE_DIR="$SCRIPT_DIR/drive/engine/$PLATFORM"
BINARY="$ENGINE_DIR/llama-server"

if [ -f "$BINARY" ]; then
    echo "  Binary already exists for $PLATFORM, skipping compilation."
else
    echo "  Building for: $PLATFORM"
    
    LLAMA_DIR="$BUILD_DIR/llama.cpp"
    if [ ! -d "$LLAMA_DIR" ]; then
        echo "  Cloning llama.cpp..."
        git clone --depth 1 https://github.com/ggerganov/llama.cpp.git "$LLAMA_DIR"
    else
        echo "  llama.cpp source already cloned."
    fi
    
    BUILD_SUBDIR="$LLAMA_DIR/build-$PLATFORM"
    mkdir -p "$BUILD_SUBDIR"
    cd "$BUILD_SUBDIR"
    
    CMAKE_ARGS="-DCMAKE_BUILD_TYPE=Release -DLLAMA_NATIVE=OFF -DBUILD_SHARED_LIBS=OFF"
    
    # Static linking where possible
    if [ "$OS" = "Linux" ]; then
        CMAKE_ARGS="$CMAKE_ARGS -DLLAMA_STATIC=ON"
    fi
    
    # Disable Metal on macOS for portability (CPU-only)
    if [ "$OS" = "Darwin" ]; then
        CMAKE_ARGS="$CMAKE_ARGS -DLLAMA_METAL=OFF"
    fi
    
    echo "  Running cmake..."
    cmake .. $CMAKE_ARGS 2>&1 | tail -3
    
    NPROC=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
    echo "  Compiling with $NPROC threads..."
    cmake --build . --config Release -j"$NPROC" --target llama-server 2>&1 | tail -5
    
    mkdir -p "$ENGINE_DIR"
    
    # Find the binary (location varies by version)
    BUILT_BIN=$(find . -name "llama-server" -type f | head -1)
    if [ -z "$BUILT_BIN" ]; then
        echo "  ERROR: llama-server binary not found after build."
        exit 1
    fi
    
    cp "$BUILT_BIN" "$BINARY"
    chmod +x "$BINARY"
    
    cd "$SCRIPT_DIR"
    echo "  Built: $BINARY ($(ls -lh "$BINARY" | awk '{print $5}'))"
fi

# Check for other platform binaries (warn if missing)
echo ""
echo "  Platform binaries status:"
for p in linux-x64 mac-arm64 mac-x64; do
    if [ -f "$SCRIPT_DIR/drive/engine/$p/llama-server" ]; then
        echo "    $p: OK"
    else
        echo "    $p: MISSING (build on that platform or cross-compile)"
    fi
done
if [ -f "$SCRIPT_DIR/drive/engine/win-x64/llama-server.exe" ]; then
    echo "    win-x64: OK"
else
    echo "    win-x64: MISSING (cross-compile with mingw or build on Windows)"
fi

# ==================== STEP 4: SEARCH INDEX ====================
echo ""
echo "[4/5] Building FTS5 search index..."

DOCS_DIR="$SCRIPT_DIR/drive/docs"
SEARCH_DIR="$SCRIPT_DIR/drive/search"
mkdir -p "$SEARCH_DIR"

if [ ! -d "$DOCS_DIR" ] || [ "$(find "$DOCS_DIR" -name '*.md' | wc -l)" -lt 10 ]; then
    echo "  ERROR: docs/ directory missing or too few articles."
    echo "  Place your knowledge base articles in: $DOCS_DIR"
    echo "  Structure: docs/medicine/wound-care.md, docs/water/purification-methods.md, etc."
    exit 1
fi

ARTICLE_COUNT=$(find "$DOCS_DIR" -name '*.md' | wc -l)
echo "  Found $ARTICLE_COUNT articles in docs/"

python3 "$SCRIPT_DIR/build-tools/build_index.py" \
    --docs-dir "$DOCS_DIR" \
    --output "$SEARCH_DIR/knowledge.db" \
    2>&1 | tail -8

echo ""
echo "  Verifying index..."
python3 "$SCRIPT_DIR/build-tools/verify_index.py" \
    --db "$SEARCH_DIR/knowledge.db" \
    --docs-dir "$DOCS_DIR" \
    2>&1 | tail -5

# ==================== STEP 5: ASSEMBLE ====================
echo ""
echo "[5/5] Assembling drive structure..."

# Copy root files
cp "$SCRIPT_DIR/launch.bat" "$SCRIPT_DIR/drive/" 2>/dev/null || echo "  launch.bat: copy from repo"
cp "$SCRIPT_DIR/launch.sh" "$SCRIPT_DIR/drive/" 2>/dev/null || echo "  launch.sh: copy from repo"
chmod +x "$SCRIPT_DIR/drive/launch.sh" 2>/dev/null || true
cp "$SCRIPT_DIR/manifest.json" "$SCRIPT_DIR/drive/" 2>/dev/null || echo "  manifest.json: copy from repo"
cp "$SCRIPT_DIR/START-HERE.txt" "$SCRIPT_DIR/drive/" 2>/dev/null || echo "  START-HERE.txt: copy from repo"

# Copy offline tools into ui/
for tool in unit-converter.html morse-code.html dosage-calculator.html radio-frequencies.html star-chart.html knot-guide.html map-viewer.html; do
    if [ -f "$SCRIPT_DIR/$tool" ]; then
        cp "$SCRIPT_DIR/$tool" "$SCRIPT_DIR/drive/ui/"
    fi
done

# Create runtime directories
mkdir -p "$SCRIPT_DIR/drive/history"
mkdir -p "$SCRIPT_DIR/drive/maps"
mkdir -p "$SCRIPT_DIR/drive/printable"

# Copy printable PDFs if they exist
if ls "$SCRIPT_DIR/printable/"*.pdf 1>/dev/null 2>&1; then
    cp "$SCRIPT_DIR/printable/"*.pdf "$SCRIPT_DIR/drive/printable/"
fi

# Final structure check
echo ""
echo "  Drive structure:"
echo "  ================================================"
find "$SCRIPT_DIR/drive" -maxdepth 3 -not -path '*/docs/*/*.md' | sort | while read f; do
    rel="${f#$SCRIPT_DIR/drive}"
    [ -z "$rel" ] && continue
    if [ -d "$f" ]; then
        count=$(ls "$f" 2>/dev/null | wc -l)
        echo "    $rel/ ($count items)"
    else
        size=$(ls -lh "$f" | awk '{print $5}')
        echo "    $rel ($size)"
    fi
done

echo ""
TOTAL_SIZE=$(du -sh "$SCRIPT_DIR/drive" | awk '{print $1}')
echo "  Total size: $TOTAL_SIZE"
echo ""
echo "  ============================================"
echo "  BUILD COMPLETE"
echo "  ============================================"
echo ""
echo "  To create the USB drive:"
echo "    1. Format a USB drive as exFAT (label: SURVIVALAI)"
echo "    2. Copy everything inside drive/ to the root of the USB drive"
echo "    3. Test: plug into a computer, run launch.bat (Win) or launch.sh (Mac/Linux)"
echo ""
echo "  Missing platform binaries? Build llama.cpp on each target platform"
echo "  and place the binary at: drive/engine/{platform}/llama-server"
echo ""
