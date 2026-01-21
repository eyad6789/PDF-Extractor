# PDF Shipping Document Extraction System

نظام استخراج بيانات وثائق الشحن العربية باستخدام الذكاء الاصطناعي

## Features

- ✅ Extract data from Arabic shipping documents (امر التسليم, البوليصة, البيان الجمركي)
- ✅ Support for **Gemini** and **Claude** APIs
- ✅ Single file and batch processing
- ✅ Export to JSON and Excel
- ✅ Iraqi bank detection

## Installation

```bash
cd ShippingDocExtractor
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Add your API keys to `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEFAULT_API=gemini
```

## Usage

### Single File Extraction

```bash
# Using Gemini (default)
python main.py --input document.pdf

# Using Claude
python main.py --input document.pdf --api claude

# Print to console
python main.py --input document.pdf --print

# Custom output path
python main.py --input document.pdf --output result.json
```

### Batch Processing

```bash
# Process all PDFs in a folder
python batch_processor.py --input ./pdfs/

# With Claude API
python batch_processor.py --input ./pdfs/ --api claude

# Custom output paths
python batch_processor.py --input ./pdfs/ --excel results.xlsx --json results.json
```

## Output Format

### JSON Output

```json
{
    "date": "2025/04/07",
    "total_containers": 3,
    "bill_number": "MEDUYX748666",
    "description": "CHAIR, CHAIR, WORDPAD",
    "iraqi_bank_name": null,
    "unit_price": 15000,
    "currency": "USD",
    "has_customs_declaration": true,
    "has_bank": false,
    "containers": [
        {"number": "CAIU8827065", "weight": 6690},
        {"number": "MSBU8337264", "weight": 11200}
    ]
}
```

### Excel Output Columns

| التاريخ | رقم الحاوية | عدد الحاويات | رقم البوليصة | وصف البضاعة | الوزن | البنك العراقي | سعر الوحدة | يوجد بيان |
|---------|-------------|--------------|--------------|-------------|-------|---------------|------------|-----------|

## Quick Start

Process the 8 PDF files in `Scans` folder:

```bash
python batch_processor.py --input "../Scans" --api gemini
```

## Document Types Supported

1. **امر التسليم** (Delivery Order) - Page 1
2. **البوليصة** (Bill of Lading) - Page 2
3. **البيان الجمركي** (Customs Declaration) - Pages 3-4
