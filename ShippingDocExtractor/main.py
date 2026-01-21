"""
PDF Shipping Document Extraction System - Main CLI

Usage:
    python main.py --input document.pdf --output result.json
    python main.py --input document.pdf --api claude
    python main.py --input ./folder/ --batch --excel output.xlsx
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

import config
from extractors import GeminiExtractor, ClaudeExtractor


def get_extractor(api: str):
    """Get the appropriate extractor based on API choice"""
    if api.lower() == "gemini":
        return GeminiExtractor()
    elif api.lower() == "claude":
        return ClaudeExtractor()
    else:
        raise ValueError(f"Unknown API: {api}. Use 'gemini' or 'claude'")


def extract_single(pdf_path: Path, api: str) -> Dict[str, Any]:
    """Extract data from a single PDF
    
    Args:
        pdf_path: Path to PDF file
        api: API to use ('gemini' or 'claude')
        
    Returns:
        Extracted data dictionary
    """
    extractor = get_extractor(api)
    return extractor.extract(pdf_path)


def save_json(data: Dict[str, Any], output_path: Path):
    """Save extracted data as JSON"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract data from Arabic shipping document PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --input document.pdf
  python main.py --input document.pdf --api claude
  python main.py --input document.pdf --output result.json
        """
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to PDF file"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output JSON file path (default: <input>_extracted.json)"
    )
    parser.add_argument(
        "--api", "-a",
        choices=["gemini", "claude"],
        default=config.DEFAULT_API,
        help=f"API to use (default: {config.DEFAULT_API})"
    )
    parser.add_argument(
        "--print", "-p",
        action="store_true",
        help="Print result to console instead of saving"
    )
    
    args = parser.parse_args()
    
    pdf_path = Path(args.input)
    if not pdf_path.exists():
        print(f"❌ Error: File not found: {pdf_path}")
        sys.exit(1)
    
    print(f"📄 Processing: {pdf_path.name}")
    print(f"🔌 Using API: {args.api}")
    
    result = extract_single(pdf_path, args.api)
    
    if args.print:
        print("\n📊 Extracted Data:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        output_path = Path(args.output) if args.output else config.OUTPUT_DIR / f"{pdf_path.stem}_extracted.json"
        save_json(result, output_path)
    
    # Print summary
    if "error" not in result:
        print(f"\n📋 Summary:")
        print(f"   Date: {result.get('date', 'N/A')}")
        print(f"   Bill #: {result.get('bill_number', 'N/A')}")
        print(f"   Containers: {result.get('total_containers', 'N/A')}")
        print(f"   Iraqi Bank: {result.get('iraqi_bank_name', 'لا يوجد') or 'لا يوجد'}")
    else:
        print(f"\n❌ Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
