<div align="center">

# ✨ pdf2md ✨

### 📄 → 📝 The friendliest way to turn PDFs into beautiful Markdown

<p>
  <img alt="lint" src="https://github.com/Hesamsamani/pymupdfgui/actions/workflows/pylint.yml/badge.svg" />
  <img alt="release" src="https://github.com/Hesamsamani/pymupdfgui/actions/workflows/release.yml/badge.svg" />
  <img alt="python" src="https://img.shields.io/badge/python-3.10+-blue?logo=python&logoColor=white" />
  <img alt="qt" src="https://img.shields.io/badge/PyQt6-41CD52?logo=qt&logoColor=white" />
  <img alt="platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" />
  <img alt="license" src="https://img.shields.io/badge/license-MIT-green" />
  <img alt="version" src="https://img.shields.io/badge/version-v0.2.0-7aa2f7" />
</p>

<p>
  🌙 <b>Dark & Light themes</b> · 🚀 <b>Drag & Drop</b> · 🔌 <b>5 engines</b> · 🦙 <b>Offline ready</b>
</p>

</div>

---

## 🌟 What is this?

**pdf2md** is a modern, lovingly-designed desktop app that converts PDF files into
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
pdf2md
```

</td>
</tr>
<tr>
<td>🛠️<br/><b>Dev mode</b></td>
<td>

```bash
git clone https://github.com/Hesamsamani/pymupdfgui.git
cd pymupdfgui && pip install -r requirements.txt
python -m pdf2md
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
| **Ollama** | 🦙 | ✅ | Tricky layouts, all-local LLM | Uses local vision models (`llama3.2-vision`, `llava`, …). |
| **OpenAI** | 🤖 | ❌ | Highest fidelity, easy setup | `gpt-4o-mini` and friends. |
| **Anthropic** | 🧠 | ❌ | Great structure on dense PDFs | Claude Haiku/Sonnet/Opus with vision. |
| **OpenAI-compatible** | 🌐 | 🤷 | Groq · OpenRouter · LM Studio · vLLM · anything custom | Plug in any `/chat/completions` endpoint. |

---

## ✨ Features

- 🎯 **Multiple engines** — five backends, one UI, switch in a single click
- 🔒 **Privacy-first** — fully offline mode, your PDFs never leave your machine
- 🪄 **Drag & drop** — chuck files in, watch the queue, profit
- 📚 **Batch convert** — feed it dozens of PDFs at once
- 🌗 **Dark & Light themes** — modern Tokyo-Night–style dark / clean light
- 🧵 **Threaded worker** — UI stays buttery smooth on long jobs
- 📊 **Live progress** — per-page progress bar and status messages
- 🖼️ **Image extraction** — pulls out embedded images (native engine)
- 🧩 **Persistent settings** — `~/.pdf2md/config.json`
- 🔑 **Hidden keys** — API tokens entered as password fields
- 🩺 **Ollama health check** — test connection button lists pulled models
- 📦 **Prebuilt `.exe`** — one-click Windows install via GitHub Actions

---

## 🖼️ A peek inside

```
╭───────────────────────────────────────────────────────╮
│  ◆ pdf2md                                             │
│                                                       │
│  NAVIGATION                                           │
│  ▸ Convert         ┃  PDF → Markdown                  │
│    Engines         ┃                                  │
│    About           ┃  📂 Add PDFs   Clear             │
│                    ┃  ╭─────────────────────────────╮ │
│                    ┃  │ report-2025.pdf  — ~/Docs   │ │
│                    ┃  │ paper.pdf        — ~/Papers │ │
│                    ┃  ╰─────────────────────────────╯ │
│  THEME             ┃  ⚙ Engine: Ollama (llama3.2-…) │
│  [ dark ▾ ]        ┃  ████████████░░░░░  68%         │
│                    ┃                    [ Convert ]   │
╰───────────────────────────────────────────────────────╯
```

---

## 🦙 Going offline with Ollama

```bash
# 1. install ollama (https://ollama.com)
# 2. pull a vision model
ollama pull llama3.2-vision

# 3. in pdf2md → Engines tab → set:
#      Server URL: http://localhost:11434
#      Model:      llama3.2-vision
#    → click "Test connection"  → ✓ Connected
```

100% local. Zero network calls. Zero API bills. 🎉

---

## 🛠️ Build your own `.exe`

```powershell
pip install -r requirements.txt pyinstaller pillow
pyinstaller --noconfirm --onefile --windowed --name pdf2md `
  --collect-all pymupdf --collect-all pymupdf4llm `
  --icon icon.ico pdf2md/__main__.py
# → dist\pdf2md.exe 🎉
```

Or just push a `v*` tag — the [release workflow](./.github/workflows/release.yml)
builds and uploads `pdf2md.exe` to GitHub Releases automatically.

---

## 📁 Where settings live

| OS | Path |
|---|---|
| 🪟 Windows | `C:\Users\YOU\.pdf2md\config.json` |
| 🍎 macOS | `~/.pdf2md/config.json` |
| 🐧 Linux | `~/.pdf2md/config.json` |

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

⭐ **If pdf2md saved you time, give it a star!** ⭐

</div>
