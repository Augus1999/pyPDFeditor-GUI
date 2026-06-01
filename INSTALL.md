# Installing Distilmark on Windows

You have three options. Pick whichever you like.

---

## Option A — Use the prebuilt `.exe` (easiest, no Python required)

1. Go to the **Releases** page:
   https://github.com/Hesamsamani/distilmark/releases
2. Download `Distilmark.exe` from the latest release (e.g. `v1.0.0`).
3. Double-click `Distilmark.exe` to run. That's it.

> Windows SmartScreen may warn about an "unrecognized app". Click **More info → Run anyway**. The binary is built in GitHub Actions from the public source — you can verify the build log on the Releases page.

If there is no release yet, push a tag (`git tag v1.0.0 && git push origin v1.0.0`) and the
`release.yml` workflow will build and attach the `.exe` automatically.

---

## Option B — Install from source with `pip`

Requires **Python 3.10+** on PATH.

```powershell
# 1. Clone
git clone https://github.com/Hesamsamani/distilmark.git
cd distilmark

# 2. (Recommended) virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# 3. Install
pip install -r requirements.txt
pip install .

# 4. Run
distilmark
```

You can also run it without installing:

```powershell
python -m distilmark
```

---

## Option C — Build your own `.exe` locally with PyInstaller

```powershell
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --noconfirm --onefile --windowed --name Distilmark `
  --collect-all pymupdf `
  --collect-all pymupdf4llm `
  --icon icon.png `
  distilmark_launcher.py

# Result:
.\dist\Distilmark.exe
```

---

## First-time setup inside the app

1. Launch **Distilmark**.
2. Go to the **Engines** tab in the sidebar.
3. Configure the engines you want to use:
   - **Native** — works out of the box, no setup, fully offline.
   - **Ollama** — install [Ollama for Windows](https://ollama.com/download/windows),
     then run `ollama pull llama3.2-vision` in a terminal. Click **Test connection**
     in the app to verify.
   - **OpenAI / Anthropic** — paste your API key.
   - **Custom (OpenAI-compatible)** — set base URL + key + model for Groq, OpenRouter,
     LM Studio, vLLM, etc.
4. Click **Save settings**.
5. Switch to the **Convert** tab, drag PDFs in (or click *Add PDFs*), pick an engine
   from the dropdown, and click **Convert**.

Settings are stored at `C:\Users\<YOU>\.distilmark\config.json`.

---

## Troubleshooting

- **`Distilmark.exe` won't start** — open a terminal and run it from there to see the error:
  `.\Distilmark.exe`
- **Ollama "Unreachable"** — make sure `ollama serve` is running, and the URL in
  settings matches (default `http://localhost:11434`).
- **API errors** — recheck the API key and base URL on the **Engines** tab.
- **PyQt6 install fails on `pip install`** — upgrade pip first: `python -m pip install --upgrade pip`.
