<div align="center">

# ✨ Distilmark ✨

### 📄 → 📝 The friendliest way to turn PDFs into beautiful Markdown

<p>
  <img alt="lint" src="https://github.com/Hesamsamani/pymupdfgui/actions/workflows/pylint.yml/badge.svg" />
  <img alt="release" src="https://github.com/Hesamsamani/pymupdfgui/actions/workflows/release.yml/badge.svg" />
  <img alt="python" src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white" />
  <img alt="qt" src="https://img.shields.io/badge/PyQt6-41CD52?logo=qt&logoColor=white" />
  <img alt="platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" />
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green" />
  <img alt="version" src="https://img.shields.io/badge/version-v1.0.0-2563eb" />
</p>

<p>
  🌙 <b>Dark & Light themes</b> · 🚀 <b>Drag & Drop</b> · 🔌 <b>7 engines</b> · 👀 <b>Live preview</b> · 🦙 <b>Offline ready</b>
</p>

</div>

---

## 🌟 What is this?

**Distilmark** is a modern, lovingly-designed desktop app that converts PDF files into
clean Markdown. Pick a backend — fully offline native parser, a local Ollama vision
model, or any hosted LLM — drop your files in, and grab your `.md`s. That's it.

> 💡 *Originally a fork of a PDF editor (`pyPDFeditor-GUI`), now reborn as a focused
> PDF → Markdown converter. The legacy editor still ships in the same repo.*

---

## 🚀 Quick start

<table>
<tr>
<td>🪟<br/><b>Windows</b></td>
<td>

Grab the prebuilt `.exe` from the [**📦 Releases page**](https://github.com/Hesamsamani/pymupdfgui/releases) — no Python needed.

</td>
</tr>
<tr>
<td>🐍<br/><b>From source</b></td>
<td>

```bash
pip install git+https://github.com/Hesamsamani/pymupdfgui.git
distilmark
```

</td>
</tr>
<tr>
<td>🛠️<br/><b>Dev mode</b></td>
<td>

```bash
git clone https://github.com/Hesamsamani/pymupdfgui.git
cd pymupdfgui && pip install -r requirements.txt
python -m distilmark
```

</td>
</tr>
</table>

📖 Full setup notes: [**INSTALL.md**](./INSTALL.md)

---

## 🔌 Conversion engines

Pick whichever vibe matches you:

| Engine | Icon | Offline? | Best for | Notes |
|---|:---:|:---:|---|---|
| **Native** | ⚡ | ✅ | Speed, privacy, simple PDFs | PyMuPDF + `pymupdf4llm`, with a heading heuristic fallback. Zero cost. |
| **pdfplumber** | 📐 | ✅ | Table-heavy, layout-sensitive PDFs | Layout-aware extraction, tables → GitHub-flavored Markdown. Tunable. |
| **Compare** | ⚖ | ✅ | Deciding which engine wins | Runs native **and** pdfplumber at once, writes two files + a diff view. |
| **Ollama** | 🦙 | ✅ | Tricky layouts, all-local LLM | Uses local vision models (`llama3.2-vision`, `llava`, …). |
| **OpenAI** | 🤖 | ❌ | Highest fidelity, easy setup | `gpt-4o-mini` and friends. |
| **Anthropic** | 🧠 | ❌ | Great structure on dense PDFs | Claude Haiku/Sonnet/Opus with vision. |
| **OpenAI-compatible** | 🌐 | 🤷 | Groq · OpenRouter · LM Studio · vLLM · anything custom | Plug in any `/chat/completions` endpoint. |

---

## ✨ Features

- 🎯 **Multiple engines** — seven backends, one UI, switch in a single click
- 👀 **Live preview** — source PDF page beside the rendered Markdown; in **Compare** mode get Native / pdfplumber / **Diff** tabs side-by-side
- ⚖ **Dual-engine compare** — run native + pdfplumber together and get two files (`name_native.md` + `name_pdfplumber.md`) to judge for yourself
- 🔍 **OCR fallback** — scanned/image-only pages are run through Tesseract automatically (when installed)
- 🎯 **Page-range selection** — convert just pages 5–20 of a 500-page monster
- 🛑 **Cancel anytime** — a Cancel button stops a long batch mid-run
- 💲 **Cost estimator** — see a rough $ estimate before firing off a paid LLM job
- ⚡ **Parallel pages** — hosted LLM engines can process N pages concurrently for a big speedup
- 🧹 **Post-processing** — merge hyphenated line breaks, collapse blank lines, strip repeating headers/footers
- 🔧 **pdfplumber tuning** — table strategies & snap tolerance exposed in Advanced options
- 🔒 **Privacy-first** — fully offline mode, your PDFs never leave your machine
- 🪄 **Drag & drop files or folders** — drop a whole folder and every PDF inside gets queued automatically
- 📂 **Smart folder scanning** — recursively finds all `.pdf` files in a folder, adds them to the queue in one click
- 📚 **Batch convert** — feed it dozens of PDFs at once, processed one by one with live progress
- 🖼️ **Image extraction with relative paths** — embedded images are saved and referenced as `./name_images/page1_img1.png` so previews work in VS Code, Obsidian, Typora, and any markdown viewer
- 📋 **Conversion history** — every run (success or failure) is logged with timestamp, engine, filename, and page count; persisted across sessions at `~/.distilmark/history.json`
- 🦙 **Ollama model management** — choose a preset tier, browse installed models, and download new ones — all from inside the app
- 🌗 **Dark & Light themes** — modern Tokyo-Night–style dark / clean light
- 🧵 **Threaded worker** — UI stays buttery smooth on long jobs
- 📊 **Live progress** — per-page progress bar and status messages
- 🧩 **Persistent settings** — `~/.distilmark/config.json`
- 🔑 **Hidden keys** — API tokens entered as password fields
- 📦 **Prebuilt `.exe`** — one-click Windows install via GitHub Actions

---

## 🖼️ A peek inside

```
╭────────────────────────────────────────────────────────────╮
│  ◆ Distilmark                                                  │
│                                                            │
│  NAVIGATION                                                │
│  ▸ Convert         ┃  PDF → Markdown                       │
│    Engines         ┃                                       │
│    History         ┃  📄 Add PDFs  📁 Add Folder  Clear    │
│    About           ┃  ╭──────────────────────────────────╮ │
│                    ┃  │ report-2025.pdf  — ~/Docs        │ │
│                    ┃  │ paper.pdf        — ~/Papers      │ │
│                    ┃  │ thesis.pdf       — ~/Desktop     │ │
│                    ┃  ╰──────────────────────────────────╯ │
│  THEME             ┃  3 files in queue                     │
│  [ dark ▾ ]        ┃  ⚙ Engine: ⚡ Balanced (11B)          │
│                    ┃  File 2/3: paper.pdf                  │
│                    ┃  ████████████░░░░░  68%               │
│                    ┃                       [ Convert ]     │
╰────────────────────────────────────────────────────────────╯
```

---

## 🦙 Going offline with Ollama

Distilmark has built-in Ollama model management — no terminal needed.

### Pick a preset tier

| Tier | Model | VRAM needed | Best for |
|------|-------|:-----------:|---------|
| 🚀 **Powerful** | `llama3.2-vision:90b` | 64 GB+ | Maximum accuracy, research PDFs |
| ⚡ **Balanced** | `llama3.2-vision:11b` | 8 GB+ | Great quality, most users |
| 💨 **Light** | `moondream:latest` | 4 GB+ | Speed, simple documents |

### Download a model from inside the app

1. Open **Engines** tab → **Ollama** section
2. Click a preset button to fill the model name, or type your own
3. Click **⬇ Pull / Download** — a live progress bar shows GB downloaded
4. When done, the model appears in the **Active model** dropdown automatically

### Manual terminal setup

```bash
# install Ollama: https://ollama.com/download
ollama serve                          # start the server
ollama pull llama3.2-vision:11b       # or any vision model

# in Distilmark → Engines → Test connection → ✓ Connected — 1 model
```

100% local. Zero network calls. Zero API bills. 🎉

---

## 📋 Conversion history

Every file you convert is logged automatically:

```
✓  2026-06-01 15:30:12  |  report.pdf → report.md    |  native    |  12 pages
✓  2026-06-01 14:55:08  |  thesis.pdf → thesis.md    |  ollama    |  87 pages
✗  2026-06-01 14:40:01  |  broken.pdf                |  native    |  0 pages
```

- History is stored at `~/.distilmark/history.json` and survives restarts
- Switch to the **History** tab any time to review past conversions
- Colour-coded: green ✓ for success, red ✗ for errors
- Clear button wipes the log when you no longer need it

---

## 📂 Folder scanning

Drop a whole folder onto the window (or click **Add Folder**) and Distilmark
recursively finds **every PDF inside** — including sub-folders — and adds
them all to the queue. Files are then converted one by one with a
`File N/total` counter so you always know where you are.

---

## 🛠️ Build your own `.exe`

```powershell
pip install -r requirements.txt pyinstaller pillow
pyinstaller --noconfirm --onefile --windowed --name Distilmark `
  --collect-all pymupdf --collect-all pymupdf4llm `
  --icon icon.ico distilmark_launcher.py
# → dist\Distilmark.exe 🎉
```

Or just push a `v*` tag — the [release workflow](./.github/workflows/release.yml)
builds and uploads `Distilmark.exe` to GitHub Releases automatically.

---

## 📁 Where settings live

| OS | Path |
|---|---|
| 🪟 Windows | `C:\Users\YOU\.distilmark\config.json` |
| 🍎 macOS | `~/.distilmark/config.json` |
| 🐧 Linux | `~/.distilmark/config.json` |

---

## 🧰 Tech stack

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="Qt" src="https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white" />
  <img alt="PyMuPDF" src="https://img.shields.io/badge/PyMuPDF-EE2A7B?style=for-the-badge" />
  <img alt="Ollama" src="https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img alt="OpenAI" src="https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white" />
  <img alt="Anthropic" src="https://img.shields.io/badge/Anthropic-D97757?style=for-the-badge" />
</p>

---

## 📜 Legacy: pyPDFeditor-GUI

The original PDF-editor app this fork was born from is **still included**. Launch it with:

```bash
pdfeditor
```

Features include: merging PDFs/images/e-books · deleting/rotating/rearranging pages ·
extracting images · adding watermarks · password & permissions · catalogue & metadata editing.

📁 Its settings live at `~/.pyPDFeditor-GUI/`.

---

## 🤝 Contributing

PRs, issues, and ✨ stars ✨ all warmly welcome.

1. 🍴 Fork
2. 🌿 Create a branch
3. 🛠️ Code away
4. 📬 Open a PR

---

## 📄 License

MIT — see [`LICENSE`](./LICENSE). Use it, fork it, ship it. 💜

<div align="center">

Made with ❤️ + ☕ + a lot of 🐍

⭐ **If Distilmark saved you time, give it a star!** ⭐

</div>
