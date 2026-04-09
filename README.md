# SurvivalAI

An offline AI assistant that runs entirely from a USB drive. Plug it into any computer, run one file, and get an intelligent chatbot backed by a curated survival knowledge base. No internet. No install. No cloud.

Built for preppers, off-grid communities, emergency responders, homesteaders, and anyone who wants critical knowledge accessible when infrastructure fails.

---

## What's on the drive

- **Local LLM** — Quantized 8B parameter model running via llama.cpp. No internet, no API keys, no data leaves the machine.
- **229 Curated Articles** — Sourced from military field manuals, WHO guidelines, and peer-reviewed references. Written for someone under stress with zero prior experience.
- **Full KJV Bible** — 66 books, every chapter and verse, with a dedicated reader interface and full-text search.
- **Intelligent Retrieval** — FTS5 full-text search pulls relevant passages and injects them into the model's context. Answers come from verified material, not hallucinated training data.
- **Fallback Mode** — Standalone HTML page runs keyword search in any browser. No server needed.
- **9 Offline Tools** — Unit converter, Morse code with audio, medication dosage calculator, radio frequency reference, celestial navigation star chart, interactive knot guide, offline map viewer, first aid decision tree, survival checklists.
- **12 Printable Quick-Ref Cards** — One-page PDFs designed to print and laminate for a go-bag.
- **Offline Maps** — Pre-downloaded OpenStreetMap tiles with pan, zoom, waypoints, and coordinate tracking.
- **Cross-Platform** — Pre-compiled binaries for Windows x64, Linux x64, macOS ARM, and macOS Intel.
- **Human-Readable Docs** — Every article is a plain markdown file. If everything else breaks, open the `docs/` folder in Notepad.

## Knowledge base

| Category | Articles | Coverage |
|----------|----------|----------|
| Medicine | 21 | Wound care, CPR, fractures, burns, infections, medications, childbirth, dental, seizures, pediatrics, chest/abdominal trauma, chronic disease, veterinary |
| Food | 17 | Edible/poisonous plants, trapping, fishing, hunting, insects, preservation, fermentation, dairy, mushroom cultivation, sourdough, survival recipes, tracking |
| Water | 10 | Purification, chemical treatment, testing, rainwater, wells, greywater, storage, gravity filters |
| Shelter | 11 | Emergency builds, log cabin, earthen building, chimney/fireplace, roofing, insulation |
| Fire | 7 | Starting methods, wet conditions, fire layouts, fuel management, charcoal, safety |
| Navigation | 11 | Compass/map, celestial, terrain, weather, signaling, river crossing, night movement, desert, winter |
| Energy | 9 | Solar, wind, micro-hydro, batteries, generators, biogas, wood gasification, human power |
| Communications | 7 | Ham radio, antennas, Morse code, mesh networking, radio without license |
| Agriculture | 14 | Soil, seeds, gardening, permaculture, livestock, pest control, irrigation, greenhouses, aquaculture, composting |
| Mechanical | 12 | Engine repair, welding, tools, vehicles, bicycles, plumbing, woodworking, masonry, primitive weapons |
| Chemistry | 8 | Soap, water treatment, adhesives, fuel chemistry, natural medicine, leather, disinfectants, pottery |
| Community | 10 | Organization, barter, security, triage, teaching, legal, urban salvage, perimeter defense, camouflage |
| Textiles | 6 | Clothing repair, spinning/weaving, natural fibers, dyeing, footwear, cordage |
| References | 6 | Unit conversions, knots, radio frequencies, medical dosages, plant ID, glossary |
| Bible | 66 | Complete King James Version |

**Total: 295 searchable documents.**

## Architecture

```
SURVIVALAI/
├── launch.bat / launch.sh      — One-click launchers
├── engine/                     — llama.cpp server (static binaries per platform)
├── model/                      — Quantized GGUF model weights
├── config/                     — System prompt, quick-prompt buttons
├── search/                     — SQLite FTS5 knowledge index
├── docs/                       — 229 articles + 66 Bible books
├── ui/
│   ├── index.html              — Chat interface with sidebar navigation
│   ├── fallback.html           — Browser-only keyword search
│   ├── bible.html              — Bible reader with book/chapter nav
│   ├── first-aid-tree.html     — Interactive first aid decision tree
│   ├── checklists.html         — Survival preparedness checklists
│   ├── dosage-calculator.html  — Weight-based medication dosing
│   ├── unit-converter.html     — Multi-category unit converter
│   ├── morse-code.html         — Encoder/decoder with audio
│   ├── radio-frequencies.html  — Band plan reference
│   ├── knot-guide.html         — 15 knots step-by-step
│   ├── star-chart.html         — Celestial navigation aid
│   ├── map-viewer.html         — Offline map viewer with waypoints
│   └── printable/              — 12 quick-reference PDFs
├── maps/                       — Pre-downloaded OSM tiles
└── history/                    — Chat logs (runtime)
```

## How it works

```
User asks question → FTS5 keyword extraction → search knowledge.db
→ top passages injected into model context → LLM generates grounded answer
```

No embedding model, no vector database. One SQLite file with full-text indexing and porter stemming. The fallback page runs the same queries client-side via sql.js (SQLite compiled to WebAssembly).

## Hardware requirements

| Spec | Minimum | Recommended |
|------|---------|-------------|
| RAM | 6 GB free | 8+ GB |
| CPU | x86_64 or ARM64 | Any modern processor |
| USB | 2.0 | 3.0+ |
| OS | Windows 10+, macOS 11+, Linux 4.x+ | Any |

No GPU required.

## Tech stack

| Component | Technology |
|-----------|-----------|
| LLM | Llama 3.1 8B Instruct, Q4_K_M, GGUF |
| Inference | llama.cpp — static binaries, zero deps |
| Search | SQLite FTS5 with porter stemming |
| UI | Vanilla HTML/CSS/JS — no frameworks, no build tools |
| Filesystem | exFAT |
| Fallback | sql.js (SQLite → WebAssembly) |

## Contact

**Email:** trahgic@gmail.com

---

*This repository is source-available for demonstration purposes. All content, code, and tooling are proprietary. All rights reserved.*
