# Scans (workspace wrapper)
Wrapper folder around an Arabic shipping-document data-extraction tool plus its input scans and generated output. Active, single-commit git repo. The real code lives in `./ShippingDocExtractor/`.

## Stack
- Python 3 CLI tool (no framework). Dependencies live under `ShippingDocExtractor/requirements.txt`.
- Key deps that shape the code: `google-generativeai>=0.8.0` (default API), `anthropic>=0.40.0` (alt API), `pandas` + `openpyxl` (Excel export), `python-dotenv` (env loading).
- LLM-based extraction: sends PDFs to Gemini (`gemini-2.5-flash`) or Claude (`claude-sonnet-4-20250514`); model IDs set in `ShippingDocExtractor/config.py`.

## Structure
- `ShippingDocExtractor/` - the actual project; open Claude Code there and read its own CLAUDE.md and README.md.
- `ShippingDocExtractor/main.py` - CLI entry point (`--input`, `--output`, `--api`, `--batch`, `--excel`).
- `ShippingDocExtractor/extractors/` - Gemini and Claude extractor classes.
- `ShippingDocExtractor/config.py` - API keys, model IDs, output dir; `prompts.py` - extraction prompt; `batch_processor.py` - folder batch run.
- `Scans/` - raw scanned shipping PDFs (input data). NEVER list, read, or scan this dir.
- `shipping_data_extracted.json` (~8 KB) - generated extraction results at root; gitignored.
- `shipping_data_extracted.xlsx` (~11 KB) - same results as Excel (binary); gitignored, do not read.

## Commands
Run all of these from inside `ShippingDocExtractor/`:
- install: `pip install -r requirements.txt` (use a venv)
- run (single): `python main.py --input document.pdf --output result.json`
- run (pick API): `python main.py --input document.pdf --api claude`
- run (batch + Excel): `python main.py --input ./folder/ --batch --excel output.xlsx`
- test: no tests exist

## Conventions & Gotchas
- Required env var NAMES (set in `ShippingDocExtractor/.env`, see `.env.example`): `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `DEFAULT_API` (`gemini` or `claude`). NEVER print their values.
- Output is written to `ShippingDocExtractor/output/` (created automatically, gitignored).
- Root `.gitignore` already covers `venv/`, `.env`, `output/`, `Scans/`, `*.pdf` and the generated json/xlsx; only the source/config files under `ShippingDocExtractor/` are git-tracked.
- Documents are Arabic shipping forms; extraction quality depends on the LLM prompt in `prompts.py`.

## Do NOT read (large/irrelevant; also denied in .claude/settings.json)
- `Scans/` (raw PDF scans, input data)
- `ShippingDocExtractor/output/` (generated results)
- `ShippingDocExtractor/venv/`, `ShippingDocExtractor/__pycache__/`
- `shipping_data_extracted.xlsx` and other binaries
- `.env` files (secrets)
