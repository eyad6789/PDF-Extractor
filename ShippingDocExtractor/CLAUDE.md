# ShippingDocExtractor
CLI tool that extracts structured data from Arabic shipping-document PDFs (delivery order / bill of lading / customs declaration) via Gemini or Claude vision APIs. Active, working state; single git commit at the parent repo.

## Stack
- Python 3 (run inside ./venv, no pyproject - plain requirements.txt)
- google-generativeai >=0.8.0 (model: gemini-2.5-flash)
- anthropic >=0.40.0 (model: claude-sonnet-4-20250514)
- python-dotenv, pandas + openpyxl (Excel export)

## Structure
| Path | Purpose |
|------|---------|
| main.py | Entry point: single-PDF extraction CLI (`--input`, `--api`, `--output`, `--print`) |
| batch_processor.py | Second entry point: process a folder of PDFs, export Excel+JSON to output/ |
| config.py | Loads .env; holds API keys, DEFAULT_API, model names, OUTPUT_DIR |
| prompts.py | EXTRACTION_PROMPT (Arabic field rules) + EXCEL_COLUMNS Arabic header map |
| extractors/base.py | BaseExtractor ABC: `_parse_json_response()` (strips ```json fences), `_load_pdf()` |
| extractors/gemini_extractor.py | GeminiExtractor (PDF bytes inline) |
| extractors/claude_extractor.py | ClaudeExtractor (base64 PDF document block, max_tokens=4096) |
| output/ | Generated extraction_<timestamp>.json/.xlsx - gitignored, do not read |
| venv/ | Local virtualenv - do not read |

## Commands
- Install: `pip install -r requirements.txt` (inside venv)
- Single file: `python main.py --input document.pdf [--api claude] [--print]`
- Batch (the real workflow): `python batch_processor.py --input "../Scans" --api gemini`
- Custom batch outputs: `python batch_processor.py --input ./pdfs/ --excel results.xlsx --json results.json`
- No tests exist.

## Conventions & Gotchas
- Env var NAMES (in .env, gitignored; template in .env.example): GEMINI_API_KEY, ANTHROPIC_API_KEY, DEFAULT_API (gemini|claude)
- A real .env with live keys exists here - never read or print it
- Extractors never raise: errors come back as `{"error": ..., "_source_file": ..., "_api_used": ...}` dicts; callers check `"error" in result`
- Excel output is one ROW PER CONTAINER (flatten_result in batch_processor.py), Arabic column headers
- Input PDFs live in ../Scans (sibling of this dir) - that dir is data, never scan it
- main.py docstring advertises `--batch --excel` flags that main.py does NOT implement; batch lives in batch_processor.py
- get_extractor() is duplicated in main.py and batch_processor.py
- Output JSON keys prefixed `_` are metadata, not extracted fields

## Do NOT read (large/irrelevant; also denied in .claude/settings.json)
- venv/, __pycache__/, output/
- ../Scans/ (raw scan PDFs), any *.pdf, *.xlsx
- .env (secrets)
