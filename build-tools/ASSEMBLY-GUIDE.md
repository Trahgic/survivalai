---
title: SurvivalAI Drive Assembly Guide
version: 1.0
last_updated: 2026-04-01
---

# SurvivalAI — Drive Assembly Guide

Step-by-step instructions for building the final USB drive from source components. This document is PRIVATE — not shipped on the drive or published in the repo.

---

## Prerequisites

You need:
- A computer running Linux or macOS (Windows works but cross-compilation is harder)
- Git installed
- A C/C++ compiler (gcc/g++ or clang)
- CMake (3.14+)
- Python 3.8+ (for build_index.py)
- USB drives: 64GB (Standard), 128GB (Explorer), 256GB (Fortress)
- ~20GB free disk space for build artifacts
- Internet connection (for downloads only — the final product needs none)

---

## Step 1: Download the Model

The LLM is Llama 3.1 8B Instruct, quantized to Q4_K_M in GGUF format.

### Option A: Download Pre-Quantized from Hugging Face

```bash
# Create working directory
mkdir -p ~/survivalai-build/model
cd ~/survivalai-build/model

# Download from TheBloke or bartowski (whoever has the latest Q4_K_M)
# Check https://huggingface.co/models?search=llama-3.1-8b-instruct-gguf

# Example (URL will vary — search HuggingFace for current source):
wget https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf

# Rename to a clean filename
mv Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf llama-3.1-8b-instruct-q4km.gguf
```

The file should be approximately 4.9 GB.

### Option B: Quantize from Source Weights

If pre-quantized isn't available or you want to control the process:

```bash
# 1. Request access to Llama 3.1 from Meta
#    https://llama.meta.com/llama-downloads/

# 2. Download the full BF16 weights (requires ~16GB)

# 3. Use llama.cpp's quantize tool (built in Step 2)
./llama-quantize ./Meta-Llama-3.1-8B-Instruct-BF16.gguf ./llama-3.1-8b-instruct-q4km.gguf Q4_K_M
```

### Verify the Model

```bash
ls -lh llama-3.1-8b-instruct-q4km.gguf
# Should be ~4.9 GB

sha256sum llama-3.1-8b-instruct-q4km.gguf
# Record this hash for verification
```

---

## Step 2: Compile llama.cpp Static Binaries

You need static binaries for three platforms:
- `llama-server-linux-x64`
- `llama-server-mac-arm64`
- `llama-server-mac-x64`
- `llama-server-win-x64.exe`

### Clone llama.cpp

```bash
cd ~/survivalai-build
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
git checkout <latest-stable-tag>  # Check releases page for current stable
```

### Build for Linux x64 (Native)

```bash
mkdir build-linux && cd build-linux
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLAMA_STATIC=ON \
  -DLLAMA_NATIVE=OFF \
  -DGGML_CPU_ALL_VARIANTS=ON \
  -DBUILD_SHARED_LIBS=OFF
cmake --build . --config Release -j$(nproc) --target llama-server

# Copy the binary
cp bin/llama-server ../../engine/llama-server-linux-x64
chmod +x ../../engine/llama-server-linux-x64

# Verify it's static
file ../../engine/llama-server-linux-x64
# Should say "statically linked"

ldd ../../engine/llama-server-linux-x64
# Should say "not a dynamic executable"

cd ..
```

### Build for macOS ARM64 (Apple Silicon)

Do this on an M1/M2/M3 Mac:

```bash
mkdir build-mac-arm && cd build-mac-arm
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DLLAMA_STATIC=ON \
  -DLLAMA_METAL=OFF \
  -DBUILD_SHARED_LIBS=OFF
cmake --build . --config Release -j$(sysctl -n hw.ncpu) --target llama-server

cp bin/llama-server ../../engine/llama-server-mac-arm64
chmod +x ../../engine/llama-server-mac-arm64
cd ..
```

### Build for macOS x64 (Intel)

On an Intel Mac, or cross-compile on ARM:

```bash
mkdir build-mac-x64 && cd build-mac-x64
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_OSX_ARCHITECTURES=x86_64 \
  -DLLAMA_STATIC=ON \
  -DLLAMA_METAL=OFF \
  -DBUILD_SHARED_LIBS=OFF
cmake --build . --config Release -j$(sysctl -n hw.ncpu) --target llama-server

cp bin/llama-server ../../engine/llama-server-mac-x64
chmod +x ../../engine/llama-server-mac-x64
cd ..
```

### Build for Windows x64

Cross-compile from Linux using MinGW, or build natively on Windows:

**Cross-compile from Linux:**
```bash
sudo apt install mingw-w64

mkdir build-win && cd build-win
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_SYSTEM_NAME=Windows \
  -DCMAKE_C_COMPILER=x86_64-w64-mingw32-gcc \
  -DCMAKE_CXX_COMPILER=x86_64-w64-mingw32-g++ \
  -DLLAMA_STATIC=ON \
  -DBUILD_SHARED_LIBS=OFF
cmake --build . --config Release -j$(nproc) --target llama-server

cp bin/llama-server.exe ../../engine/llama-server-win-x64.exe
cd ..
```

**Native Windows build (if you have Visual Studio):**
```powershell
mkdir build-win; cd build-win
cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_STATIC=ON -DBUILD_SHARED_LIBS=OFF
cmake --build . --config Release --target llama-server
copy bin\Release\llama-server.exe ..\..\engine\llama-server-win-x64.exe
```

### Verify All Binaries

```bash
cd ~/survivalai-build/engine
ls -lh llama-server-*
# linux-x64:   ~20-30 MB
# mac-arm64:   ~15-25 MB
# mac-x64:     ~20-30 MB
# win-x64.exe: ~20-30 MB
```

Test the Linux binary locally:
```bash
./llama-server-linux-x64 \
  --model ../model/llama-3.1-8b-instruct-q4km.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --ctx-size 4096 \
  --n-predict 512

# In another terminal:
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is the boiling point of water?"}]}'
```

Kill the server with Ctrl+C after verifying it responds.

---

## Step 3: Build the FTS5 Search Index

```bash
cd ~/survivalai-build

# Your docs/ folder should have all 119 articles in category subfolders
# docs/medicine/wound-care.md
# docs/medicine/burns.md
# docs/water/purification-methods.md
# ... etc

# Run the index builder
python3 build_index.py --docs-dir ./docs --output ./search/knowledge.db --verbose --examples

# Verify the index
python3 verify_index.py --db ./search/knowledge.db --docs-dir ./docs

# Both should report 0 errors
```

The resulting `knowledge.db` should be roughly 4-5 MB.

---

## Step 4: Assemble the Drive File Structure

### Format the USB Drive

```bash
# Find the drive device (BE CAREFUL — wrong device = data loss)
lsblk

# Format as exFAT (works on Windows, Mac, Linux)
# Replace /dev/sdX with your actual device
sudo mkfs.exfat -n SURVIVALAI /dev/sdX1

# Mount
sudo mount /dev/sdX1 /mnt/usb
```

On macOS:
```bash
diskutil list                          # Find the drive
diskutil eraseDisk ExFAT SURVIVALAI /dev/diskN
```

On Windows: Right-click the drive in File Explorer → Format → exFAT → "SURVIVALAI"

### Copy the File Structure

```bash
DRIVE=/mnt/usb  # or wherever your USB is mounted

# Root files
cp launch.bat "$DRIVE/"
cp launch.sh "$DRIVE/"
chmod +x "$DRIVE/launch.sh"
cp manifest.json "$DRIVE/"
cp START-HERE.txt "$DRIVE/"
cp LICENSE "$DRIVE/"

# Engine (binaries)
mkdir -p "$DRIVE/engine"
cp engine/llama-server-linux-x64 "$DRIVE/engine/"
cp engine/llama-server-mac-arm64 "$DRIVE/engine/"
cp engine/llama-server-mac-x64 "$DRIVE/engine/"
cp engine/llama-server-win-x64.exe "$DRIVE/engine/"

# Model
mkdir -p "$DRIVE/model"
cp model/llama-3.1-8b-instruct-q4km.gguf "$DRIVE/model/"

# Config
mkdir -p "$DRIVE/config"
cp config/server.json "$DRIVE/config/"
cp config/system-prompt.txt "$DRIVE/config/"
cp config/quick-prompts.json "$DRIVE/config/"

# Search index
mkdir -p "$DRIVE/search"
cp search/knowledge.db "$DRIVE/search/"

# Knowledge base articles
cp -r docs/ "$DRIVE/docs/"

# UI (chat interface + fallback + tools)
mkdir -p "$DRIVE/ui"
cp ui/index.html "$DRIVE/ui/"
cp ui/style.css "$DRIVE/ui/"
cp ui/app.js "$DRIVE/ui/"
cp ui/fallback.html "$DRIVE/ui/"
cp ui/unit-converter.html "$DRIVE/ui/"
cp ui/morse-code.html "$DRIVE/ui/"
cp ui/dosage-calculator.html "$DRIVE/ui/"
cp ui/radio-frequencies.html "$DRIVE/ui/"
cp ui/star-chart.html "$DRIVE/ui/"
cp ui/knot-guide.html "$DRIVE/ui/"
cp ui/map-viewer.html "$DRIVE/ui/"

# Printable reference cards
mkdir -p "$DRIVE/printable"
cp printable/*.pdf "$DRIVE/printable/"

# Chat history directory (empty — populated at runtime)
mkdir -p "$DRIVE/history"

# Maps directory (empty for Standard, populated for Explorer+)
mkdir -p "$DRIVE/maps"
```

### Final Structure on the Drive

```
SURVIVALAI/
├── launch.bat                              # Windows launcher
├── launch.sh                               # Mac/Linux launcher
├── manifest.json                           # Version tracking
├── START-HERE.txt                          # Plain English instructions
├── LICENSE                                 # Proprietary license
├── engine/
│   ├── llama-server-linux-x64              # ~25 MB
│   ├── llama-server-mac-arm64              # ~20 MB
│   ├── llama-server-mac-x64               # ~25 MB
│   └── llama-server-win-x64.exe           # ~25 MB
├── model/
│   └── llama-3.1-8b-instruct-q4km.gguf    # ~4.9 GB
├── config/
│   ├── server.json
│   ├── system-prompt.txt
│   └── quick-prompts.json
├── search/
│   └── knowledge.db                        # ~4 MB
├── docs/                                   # 119 markdown articles
│   ├── medicine/      (17 files)
│   ├── water/         (9 files)
│   ├── food/          (12 files)
│   ├── shelter/       (8 files)
│   ├── fire/          (7 files)
│   ├── navigation/    (7 files)
│   ├── energy/        (7 files)
│   ├── communications/(7 files)
│   ├── agriculture/   (11 files)
│   ├── mechanical/    (8 files)
│   ├── chemistry/     (7 files)
│   ├── community/     (7 files)
│   ├── textiles/      (6 files)
│   └── references/    (6 files)
├── ui/
│   ├── index.html                          # Chat interface
│   ├── style.css
│   ├── app.js
│   ├── fallback.html                       # Browser-only search
│   ├── unit-converter.html
│   ├── morse-code.html
│   ├── dosage-calculator.html
│   ├── radio-frequencies.html
│   ├── star-chart.html
│   ├── knot-guide.html
│   └── map-viewer.html
├── printable/
│   ├── medical-quickref.pdf
│   ├── water-purification-quickref.pdf
│   ├── plants-quickref.pdf
│   ├── knots-quickref.pdf
│   ├── radio-frequencies-quickref.pdf
│   └── navigation-quickref.pdf
├── maps/                                   # Empty (Standard) or tiles (Explorer+)
└── history/                                # Empty — chat logs saved at runtime
```

---

## Step 5: Tier-Specific Setup

### Standard (64GB)

The base assembly above. Total drive usage: ~5.5 GB. Plenty of room on 64GB.

### Explorer (128GB) — Add Map Tiles

Download OpenStreetMap tiles for target regions using a tile downloader:

```bash
# Install a tile downloader
# Options: JTileDownloader, Mobile Atlas Creator, or custom script

# Tile URL pattern: https://tile.openstreetmap.org/{z}/{x}/{y}.png
# Download zoom levels 1-13 for a region (country-scale)
# Download zoom levels 13-16 for a local area (city/county-scale)

# Store in the standard z/x/y structure:
# maps/5/17/11.png
# maps/6/34/22.png
# etc.

# Rough size estimates:
# US lower 48 at z1-12:  ~2 GB
# Single state at z1-16: ~5-15 GB
# Single county at z1-18: ~1-3 GB
```

Copy tiles to `$DRIVE/maps/` preserving the `z/x/y.png` directory structure. The map-viewer.html tool reads from `../maps/{z}/{x}/{y}.png` relative to the `ui/` folder.

### Fortress (256GB) — Add Bootable OS

This requires creating a bootable Linux partition on the USB drive alongside the data partition.

```bash
# Partition the drive:
# Partition 1: ~500MB, FAT32, boot flag — Linux boot partition
# Partition 2: Remaining space, exFAT — SurvivalAI data

# Install a minimal Linux (e.g., Alpine Linux, Tiny Core, or Debian minimal)
# to the boot partition

# Configure the Linux environment to:
# 1. Auto-mount the exFAT data partition
# 2. Auto-start the llama-server on boot
# 3. Auto-open a browser to the chat interface
# 4. Include basic utilities (terminal, file manager, text editor)

# This is a significant undertaking — consider using a tool like:
# - Ventoy (boot multiple ISOs from USB)
# - Ubuntu minimal + custom startup script
# - Alpine Linux (very small footprint)

# The bootable OS adds ~2-4 GB to drive usage
```

Detailed bootable OS setup is beyond this guide — it's a separate project that depends on hardware testing across different BIOS/UEFI configurations.

---

## Step 6: Testing the Final Drive

### Smoke Test Checklist

Run through this on each platform before shipping:

```
[ ] Drive mounts and is readable
[ ] START-HERE.txt is visible and readable
[ ] launch.bat / launch.sh runs without errors
[ ] llama-server starts and binds to port
[ ] Browser opens to chat interface
[ ] Chat interface loads and shows quick-prompt buttons
[ ] Ask a test question — get a grounded answer
[ ] Search returns relevant results (check 3-4 queries)
[ ] Fallback.html loads and searches work without server
[ ] Each offline tool opens and functions:
    [ ] Unit converter — convert 5 miles to km
    [ ] Morse code — encode "SOS", play audio
    [ ] Dosage calculator — select ibuprofen, enter weight
    [ ] Radio frequencies — search "emergency"
    [ ] Star chart — change month, verify stars move
    [ ] Knot guide — open bowline, step through
    [ ] Map viewer — pan, zoom, add waypoint
[ ] Printable PDFs open and look correct
[ ] docs/ folder contains all 119 articles, readable in text editor
[ ] Drive ejects cleanly with no data corruption
```

### Platform-Specific Tests

**Windows 10/11:**
- Double-click launch.bat
- Windows Defender may flag the binary — it's unsigned. User may need to click "Run anyway"
- Test on both Windows 10 and 11 if possible

**macOS (Apple Silicon and Intel):**
- `chmod +x launch.sh` may be needed (exFAT doesn't preserve Unix permissions)
- macOS Gatekeeper will block unsigned binaries: user needs to right-click → Open, or run `xattr -d com.apple.quarantine` on the binary
- Document this in START-HERE.txt

**Linux:**
- `chmod +x launch.sh` and the binary
- Should work on any distro with a modern kernel
- Test on Ubuntu LTS as the baseline

### Performance Benchmarks

Record on a mid-range machine (8GB RAM, no GPU):
- Time to first token after question submitted: target < 5 seconds
- Tokens per second during generation: target > 5 tok/s
- Search latency: target < 50ms per query
- Total startup time (launch to ready): target < 30 seconds on USB 3.0

---

## Step 7: Prepare for Shipping

### Drive Labeling

Print labels with:
- "SurvivalAI" + tier name
- "Plug into any computer — run launch file — no install needed"
- "survivalai@proton.me"

### Packaging

- Anti-static bag for the drive
- Printed quick-start card (1-page: plug in, run file, ask questions)
- Optional: small case or pouch

### Inventory Tracking

For each drive shipped, record:
- Serial number (or just a sequential order number)
- Tier (Standard/Explorer/Fortress)
- Build date
- Manifest version
- Customer email

---

## Step 8: Proton Mail Setup

1. Go to https://proton.me/mail and create account: survivalai@proton.me
2. Set up folders: Orders, Support, Bulk Inquiries
3. Create email templates:
   - Order confirmation
   - Shipping notification
   - Support response
4. Consider Proton's paid tier for custom domain later (e.g., info@survivalai.com)

---

## Maintenance

### Updating Articles

1. Edit markdown files in your local `docs/` directory
2. Rebuild the search index: `python3 build_index.py --docs-dir ./docs --output ./search/knowledge.db`
3. Verify: `python3 verify_index.py --db ./search/knowledge.db --docs-dir ./docs`
4. Copy updated `docs/` and `search/knowledge.db` to the drive image
5. Update `manifest.json` version number and date

### Updating the Model

If a better quantization or model version becomes available:
1. Download/quantize the new model
2. Test thoroughly — verify response quality, speed, and RAM usage
3. Update `config/server.json` if the filename changed
4. Update `manifest.json`

### Updating llama.cpp

When llama.cpp releases performance improvements:
1. Pull the new version
2. Recompile all four platform binaries
3. Test on each platform
4. Update binaries on the drive image

---

## Troubleshooting Build Issues

**cmake can't find compiler:** Install build-essential (Linux) or Xcode CLI tools (Mac)
```bash
# Linux
sudo apt install build-essential cmake

# Mac
xcode-select --install
```

**Model too large for drive:** Verify you're using Q4_K_M quantization (~4.9 GB), not a larger quant.

**Binary segfaults on target machine:** Likely compiled with CPU instructions the target doesn't support. Rebuild with `-DLLAMA_NATIVE=OFF` to disable machine-specific optimizations.

**exFAT not mounting on Linux:** Install exfat-fuse and exfat-utils:
```bash
sudo apt install exfat-fuse exfatprogs
```

**Search returns no results:** Verify knowledge.db was built from the correct docs directory and contains articles. Run verify_index.py.

**Windows blocks the binary:** The executable is unsigned. Users need to click "More info" → "Run anyway" on the SmartScreen warning. Document this in START-HERE.txt.

**macOS blocks the binary:** Run this on the Mac after mounting the drive:
```bash
xattr -d com.apple.quarantine /Volumes/SURVIVALAI/engine/llama-server-mac-*
```
Document in START-HERE.txt.
