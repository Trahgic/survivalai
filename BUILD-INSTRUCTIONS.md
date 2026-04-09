---
title: SurvivalAI — Step-by-Step Build Instructions
---

# Building a Working SurvivalAI USB Drive

This guide assumes you have the `survivalai-complete-drive.zip` file. By the end, you'll have a USB drive you can plug into any computer and run the AI assistant.

Total time: 30–60 minutes depending on your internet speed and computer.

---

## What You Need Before Starting

- A computer (Windows, Mac, or Linux)
- Internet connection (only needed during setup — the final drive works offline)
- A USB flash drive, 64GB or larger (USB 3.0 recommended for speed)
- About 10GB of free disk space on your computer for the build process

---

## PART 1: UNZIP THE DRIVE PACKAGE

### Windows

1. Find `survivalai-complete-drive.zip` in your Downloads folder
2. Right-click it → "Extract All..."
3. Choose where to extract (your Desktop is fine)
4. Click "Extract"
5. You should now have a folder called `drive` with subfolders: `config`, `docs`, `engine`, `model`, `printable`, `search`, `ui`, etc.

### Mac

1. Double-click `survivalai-complete-drive.zip` in Finder
2. It extracts automatically into a `drive` folder in the same location
3. Open the `drive` folder and verify you see: `config`, `docs`, `engine`, `model`, `ui`, etc.

### Linux

```bash
cd ~/Downloads
unzip survivalai-complete-drive.zip
cd drive
ls
```

You should see: `build-drive.sh  build-tools  config  docs  engine  history  launch.bat  launch.sh  manifest.json  maps  model  printable  search  START-HERE.txt  ui`

---

## PART 2: DOWNLOAD THE AI MODEL

This is the large language model that powers the AI assistant. It's a single file, about 4.9 GB.

### Step 2.1: Go to HuggingFace

Open your web browser and go to:

```
https://huggingface.co/bartowski/Meta-Llama-3.1-8B-Instruct-GGUF
```

If that page doesn't exist anymore, search HuggingFace for:
```
llama 3.1 8b instruct GGUF
```

Look for a repository that has GGUF quantized versions of Meta's Llama 3.1 8B Instruct model.

### Step 2.2: Download the Q4_K_M File

On the model page, look for the "Files and versions" tab. Find the file that contains `Q4_K_M` in the name. It will be something like:

```
Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

The file size should be approximately **4.9 GB**.

Click the download button (the down arrow icon). This will take a while depending on your internet speed.

**DO NOT** download Q8, Q6, or Q5 versions — they're larger and need more RAM. **DO NOT** download Q2 or Q3 — they're lower quality. Q4_K_M is the sweet spot.

### Step 2.3: Move and Rename the File

After the download finishes:

1. Find the downloaded `.gguf` file (probably in your Downloads folder)
2. **Rename it** to exactly: `llama-3.1-8b-q4_k_m.gguf`
   - On Windows: right-click → Rename
   - On Mac: click the filename, wait, click again to edit
   - On Linux: `mv "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf" llama-3.1-8b-q4_k_m.gguf`
3. **Move it** into the `drive/model/` folder

When you're done, the path should be:
```
drive/model/llama-3.1-8b-q4_k_m.gguf
```

You can delete the README.txt file that was in that folder.

### Step 2.4: Verify

Check that the file is in the right place and roughly the right size:

- **Windows:** Open `drive\model\` in File Explorer. You should see `llama-3.1-8b-q4_k_m.gguf` at about 4.9 GB.
- **Mac:** Open `drive/model/` in Finder. File should be ~4.9 GB.
- **Linux:** `ls -lh drive/model/llama-3.1-8b-q4_k_m.gguf` — should show ~4.9G

---

## PART 3: GET THE LLAMA.CPP SERVER BINARY

This is the program that loads the AI model and serves the chat interface. You need a compiled binary for your operating system.

### Option A: Download a Pre-Built Release (Easiest)

Go to the llama.cpp releases page:

```
https://github.com/ggerganov/llama.cpp/releases
```

Look for the latest release. Under "Assets," find a download for your platform:

| Your Computer | Download File Contains |
|---|---|
| Windows 10/11 (64-bit) | `win-x64` or `windows-x64` in the filename |
| Mac with Apple Silicon (M1/M2/M3/M4) | `macos-arm64` in the filename |
| Mac with Intel chip | `macos-x64` or `macos-x86_64` in the filename |
| Linux (64-bit) | `linux-x64` or `linux-x86_64` in the filename |

Download the zip file for your platform. Extract it. Inside you'll find several files — the one you need is called `llama-server` (or `llama-server.exe` on Windows).

**Note:** The file might be called `server` instead of `llama-server` in some releases. Rename it to `llama-server` (or `llama-server.exe` on Windows).

Now skip to Step 3.3 below.

### Option B: Build From Source (If Pre-Built Doesn't Work)

This compiles llama.cpp yourself. It takes 5–10 minutes.

#### Windows — Building From Source

1. **Install Visual Studio Build Tools** if you don't have them:
   - Go to: https://visualstudio.microsoft.com/downloads/
   - Scroll down to "Tools for Visual Studio"
   - Download "Build Tools for Visual Studio 2022"
   - Run the installer, select "Desktop development with C++"
   - Install (this takes a while)

2. **Install CMake:**
   - Go to: https://cmake.org/download/
   - Download the Windows x64 installer
   - Run it, check "Add CMake to PATH"

3. **Install Git:**
   - Go to: https://git-scm.com/download/win
   - Download and install with default settings

4. **Open "Developer Command Prompt for VS 2022"** from the Start menu (NOT regular Command Prompt)

5. **Run these commands one at a time:**
   ```
   cd %USERPROFILE%\Desktop
   git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp
   mkdir build
   cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF
   cmake --build . --config Release --target llama-server
   ```

6. The binary will be at: `build\bin\Release\llama-server.exe`
   If it's not there, check `build\Release\bin\llama-server.exe` or just search the build folder for `llama-server.exe`.

#### Mac — Building From Source

1. **Install Xcode Command Line Tools** (if you haven't already):
   Open Terminal (Applications → Utilities → Terminal) and run:
   ```bash
   xcode-select --install
   ```
   A popup will ask you to install. Click Install. Wait for it to finish.

2. **Install CMake:**
   ```bash
   # If you have Homebrew:
   brew install cmake

   # If you don't have Homebrew, install it first:
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install cmake
   ```

3. **Build llama.cpp:**
   ```bash
   cd ~/Desktop
   git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_METAL=OFF -DBUILD_SHARED_LIBS=OFF
   cmake --build . --config Release -j$(sysctl -n hw.ncpu) --target llama-server
   ```

4. The binary will be at: `build/bin/llama-server`
   Find it: `find build -name "llama-server" -type f`

#### Linux — Building From Source

1. **Install prerequisites:**
   ```bash
   # Ubuntu/Debian:
   sudo apt update
   sudo apt install -y git cmake build-essential

   # Fedora:
   sudo dnf install -y git cmake gcc-c++ make
   ```

2. **Build:**
   ```bash
   cd ~/Desktop
   git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
   cd llama.cpp
   mkdir build && cd build
   cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_NATIVE=OFF -DBUILD_SHARED_LIBS=OFF
   cmake --build . --config Release -j$(nproc) --target llama-server
   ```

3. The binary will be at: `build/bin/llama-server`

### Step 3.3: Put the Binary in the Right Place

The launch scripts expect the binary at a specific path depending on your platform:

| Your Platform | Copy the binary to |
|---|---|
| Windows | `drive/engine/win-x64/llama-server.exe` |
| Mac (Apple Silicon M1/M2/M3/M4) | `drive/engine/mac-arm64/llama-server` |
| Mac (Intel) | `drive/engine/mac-x64/llama-server` |
| Linux | `drive/engine/linux-x64/llama-server` |

**Windows example:**
1. Open the folder where you built or downloaded `llama-server.exe`
2. Copy `llama-server.exe`
3. Navigate to `drive\engine\win-x64\`
4. Paste it there
5. Delete the README.txt in that folder

**Mac example:**
```bash
# If you're on Apple Silicon:
cp ~/Desktop/llama.cpp/build/bin/llama-server ~/Desktop/drive/engine/mac-arm64/llama-server

# If you're on Intel Mac:
cp ~/Desktop/llama.cpp/build/bin/llama-server ~/Desktop/drive/engine/mac-x64/llama-server
```

**Linux example:**
```bash
cp ~/Desktop/llama.cpp/build/bin/llama-server ~/Desktop/drive/engine/linux-x64/llama-server
```

### Step 3.4: Verify

Check the binary is in place:

- **Windows:** `drive\engine\win-x64\llama-server.exe` should exist
- **Mac ARM:** `drive/engine/mac-arm64/llama-server` should exist
- **Mac Intel:** `drive/engine/mac-x64/llama-server` should exist
- **Linux:** `drive/engine/linux-x64/llama-server` should exist

---

## PART 4: DOWNLOAD SQL.JS

This is a small library (about 1.5 MB) that lets the browser search the knowledge base. Without it, the chat still works but won't inject article context, and the fallback search page won't function.

### Step 4.1: Download Two Files

Open these URLs in your browser and save the files:

**File 1:**
```
https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.11.0/sql-wasm.js
```
Right-click the page → "Save As..." → save as `sql-wasm.js`

**File 2:**
```
https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.11.0/sql-wasm.wasm
```
Right-click the link → "Save Link As..." → save as `sql-wasm.wasm`

**Alternative method (command line):**
```bash
cd drive/ui
curl -O https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.11.0/sql-wasm.js
curl -O https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.11.0/sql-wasm.wasm
```

### Step 4.2: Move to the UI Folder

Move both files into `drive/ui/`:

```
drive/ui/sql-wasm.js
drive/ui/sql-wasm.wasm
```

### Step 4.3: Verify

You should now have these files in `drive/ui/`:
```
app.js
dosage-calculator.html
fallback.html
index.html
knot-guide.html
map-viewer.html
morse-code.html
radio-frequencies.html
sql-wasm.js          ← new
sql-wasm.wasm        ← new
star-chart.html
style.css
unit-converter.html
```

---

## PART 5: TEST ON YOUR COMPUTER (Before Copying to USB)

Test the drive from your local computer first. This way if something's wrong, you fix it before copying 5+ GB to a USB stick.

### Windows

1. Open File Explorer
2. Navigate to the `drive` folder
3. Double-click `launch.bat`
4. A black command prompt window will open showing server startup info
5. Your web browser should open automatically to `http://localhost:8080`
6. You should see the SurvivalAI chat interface with 8 quick-prompt buttons
7. **If Windows Defender blocks the program:** Click "More info" → "Run anyway"
8. Try asking a question: type "How do I purify water?" and press Enter
9. To stop: close the command prompt window or press Ctrl+C

### Mac

1. Open Terminal (Applications → Utilities → Terminal)
2. Navigate to the drive folder:
   ```bash
   cd ~/Desktop/drive
   ```
3. Make the launcher and binary executable:
   ```bash
   chmod +x launch.sh
   chmod +x engine/mac-arm64/llama-server    # or mac-x64 for Intel
   ```
4. **Remove the macOS quarantine flag** (macOS blocks unsigned binaries):
   ```bash
   xattr -d com.apple.quarantine engine/mac-arm64/llama-server    # or mac-x64
   ```
   If you get "No such xattr," that's fine — it means there's nothing to remove.
5. Run the launcher:
   ```bash
   ./launch.sh
   ```
6. Terminal will show server startup info. After a few seconds, your browser should open to `http://localhost:8080`
7. **If macOS still blocks it:** Go to System Settings → Privacy & Security → scroll down → click "Allow Anyway" next to the llama-server message. Then run `./launch.sh` again.
8. Try asking a question: "How do I start a fire without matches?"
9. To stop: press Ctrl+C in Terminal

### Linux

1. Open a terminal
2. Navigate to the drive folder:
   ```bash
   cd ~/Desktop/drive
   ```
3. Make files executable:
   ```bash
   chmod +x launch.sh
   chmod +x engine/linux-x64/llama-server
   ```
4. Run it:
   ```bash
   ./launch.sh
   ```
5. Open `http://localhost:8080` in your browser if it doesn't open automatically
6. Test with a question: "How do I treat a burn?"
7. To stop: Ctrl+C

### What to Expect

- The server takes 10–30 seconds to load the model (you'll see "model loaded" in the terminal)
- First response takes a few seconds to start generating
- Responses stream in word by word at roughly 5–15 tokens per second on modern hardware
- The "Knowledge base loaded" message in the chat footer means FTS5 search is working
- If you see "Search unavailable" — sql.js files might be missing from `drive/ui/`

### Troubleshooting

| Problem | Fix |
|---|---|
| "Server binary not found" | Binary isn't in the right `engine/` subfolder. Check the path. |
| "Model file not found" | Model isn't in `drive/model/` or isn't named exactly `llama-3.1-8b-q4_k_m.gguf` |
| Server starts but browser shows error | Wait 10-20 seconds for model to load, then refresh |
| "Not enough memory" | Close other programs. Need ~6GB free RAM. |
| Very slow responses | Normal on older hardware. Close other programs. USB 3.0 loads faster than 2.0. |
| "Search unavailable" in chat footer | `sql-wasm.js` or `sql-wasm.wasm` missing from `drive/ui/` |
| Chat works but no article context in answers | Same as above — search needs sql.js files |
| Windows blocks the exe | Click "More info" → "Run anyway" on SmartScreen popup |
| Mac blocks the binary | Run the `xattr` command from Step 5, or go to System Settings → Privacy & Security |

---

## PART 6: COPY TO USB DRIVE

Once it's working on your computer:

### Step 6.1: Format the USB Drive

**Windows:**
1. Insert the USB drive
2. Open File Explorer, right-click the USB drive → Format
3. File system: **exFAT**
4. Volume label: **SURVIVALAI**
5. Check "Quick Format"
6. Click Start

**Mac:**
1. Insert the USB drive
2. Open Disk Utility (Applications → Utilities → Disk Utility)
3. Select the USB drive in the left sidebar (the drive, not the partition)
4. Click "Erase"
5. Name: **SURVIVALAI**
6. Format: **ExFAT**
7. Click Erase

**Linux:**
```bash
# Find your USB drive device (BE CAREFUL — wrong device = data loss)
lsblk

# Format (replace sdX1 with your actual partition, e.g. sdb1)
sudo mkfs.exfat -n SURVIVALAI /dev/sdX1
```

### Step 6.2: Copy Everything

Copy the **contents** of the `drive/` folder to the **root** of the USB drive. Not the `drive` folder itself — its contents.

**Windows:**
1. Open the `drive` folder
2. Select All (Ctrl+A)
3. Copy (Ctrl+C)
4. Open the USB drive in File Explorer
5. Paste (Ctrl+V)
6. Wait for the copy to finish (~5 GB, takes a few minutes)

**Mac:**
1. Open the `drive` folder in Finder
2. Select All (Cmd+A)
3. Copy (Cmd+C)
4. Open the SURVIVALAI drive in Finder
5. Paste (Cmd+V)

**Linux:**
```bash
# Mount the drive if not auto-mounted
sudo mount /dev/sdX1 /mnt/usb

# Copy everything
cp -r ~/Desktop/drive/* /mnt/usb/

# Make scripts executable (exFAT doesn't preserve permissions)
chmod +x /mnt/usb/launch.sh
chmod +x /mnt/usb/engine/linux-x64/llama-server

# Unmount cleanly
sudo umount /mnt/usb
```

### Step 6.3: Verify the USB Drive Structure

After copying, the root of your USB drive should look like this:

```
SURVIVALAI (USB Drive)
├── launch.bat
├── launch.sh
├── manifest.json
├── START-HERE.txt
├── config/
│   ├── system-prompt.txt
│   └── quick-prompts.json
├── docs/
│   ├── medicine/   (16 articles)
│   ├── water/      (8 articles)
│   ├── food/       (12 articles)
│   └── ... (14 category folders total)
├── engine/
│   └── (your platform folder with llama-server binary)
├── model/
│   └── llama-3.1-8b-q4_k_m.gguf  (4.9 GB)
├── printable/
│   └── (6 PDF files)
├── search/
│   └── knowledge.db
└── ui/
    ├── index.html
    ├── style.css
    ├── app.js
    ├── fallback.html
    ├── sql-wasm.js
    ├── sql-wasm.wasm
    └── (7 tool HTML files)
```

---

## PART 7: TEST FROM THE USB DRIVE

The real test — running it from the USB stick on a computer.

1. **Safely eject** the USB drive from the computer you copied it on
2. **Plug it into the same computer** (or a different one)
3. Open the USB drive in your file manager
4. **Windows:** Double-click `launch.bat`
5. **Mac/Linux:** Open Terminal, `cd` to the drive, run `chmod +x launch.sh engine/*/llama-server && ./launch.sh`
6. Wait for the browser to open
7. Ask a question

If it works from the USB drive, you're done. You have a working SurvivalAI drive.

---

## PART 8: ADDING MORE PLATFORMS (Optional)

The drive you built only has a binary for YOUR platform. To make it work on other operating systems, you need to add binaries for those platforms too.

The cleanest way: find someone with each platform, have them compile llama.cpp (Part 3, Option B), and send you the `llama-server` binary. Drop each into the right folder:

```
engine/win-x64/llama-server.exe      ← built on Windows
engine/linux-x64/llama-server         ← built on Linux
engine/mac-arm64/llama-server         ← built on Apple Silicon Mac
engine/mac-x64/llama-server           ← built on Intel Mac
```

All four binaries can live on the same drive. The launch scripts auto-detect which platform they're running on and pick the right one.

---

## Quick Reference — File Checklist

Before the drive is complete, verify all of these exist:

```
[  ] launch.bat
[  ] launch.sh
[  ] manifest.json
[  ] START-HERE.txt
[  ] config/system-prompt.txt
[  ] config/quick-prompts.json
[  ] model/llama-3.1-8b-q4_k_m.gguf          (~4.9 GB)
[  ] engine/(your platform)/llama-server       (the compiled binary)
[  ] search/knowledge.db                       (~4 MB)
[  ] ui/index.html
[  ] ui/style.css
[  ] ui/app.js
[  ] ui/fallback.html
[  ] ui/sql-wasm.js                            (~400 KB)
[  ] ui/sql-wasm.wasm                          (~1.1 MB)
[  ] ui/(7 tool HTML files)
[  ] printable/(6 PDF files)
[  ] docs/(14 category folders with 117 articles)
```
