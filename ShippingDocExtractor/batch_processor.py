"""
Batch Processor - Process multiple PDF files and export to Excel

Usage:
    python batch_processor.py --input ./pdfs/ --output results.xlsx
    python batch_processor.py --input ./pdfs/ --api claude
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

import config
from extractors import GeminiExtractor, ClaudeExtractor
from prompts import EXCEL_COLUMNS

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


def get_extractor(api: str):
    """Get the appropriate extractor based on API choice"""
    if api.lower() == "gemini":
        return GeminiExtractor()
    elif api.lower() == "claude":
        return ClaudeExtractor()
    else:
        raise ValueError(f"Unknown API: {api}. Use 'gemini' or 'claude'")


def find_pdfs(directory: Path) -> List[Path]:
    """Find all PDF files in a directory"""
    return sorted(directory.glob("*.pdf"))


def flatten_result(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten extracted result for Excel export
    
    Creates one row per container, with shared document info
    """
    rows = []
    containers = result.get("containers", [])
    
    if not containers:
        # Single row if no containers
        rows.append({
            "التاريخ": result.get("date"),
            "رقم الحاوية": None,
            "عدد الحاويات": result.get("total_containers"),
            "رقم البوليصة": result.get("bill_number"),
            "وصف البضاعة": result.get("description"),
            "الوزن": None,
            "البنك العراقي": result.get("iraqi_bank_name") or "لا يوجد",
            "سعر الوحدة": result.get("unit_price"),
            "العملة": result.get("currency"),
            "يوجد بيان": "نعم" if result.get("has_customs_declaration") else "لا",
            "ملف المصدر": result.get("_source_file"),
        })
    else:
        # One row per container
        for container in containers:
            rows.append({
                "التاريخ": result.get("date"),
                "رقم الحاوية": container.get("number"),
                "عدد الحاويات": result.get("total_containers"),
                "رقم البوليصة": result.get("bill_number"),
                "وصف البضاعة": result.get("description"),
                "الوزن": container.get("weight"),
                "البنك العراقي": result.get("iraqi_bank_name") or "لا يوجد",
                "سعر الوحدة": result.get("unit_price"),
                "العملة": result.get("currency"),
                "يوجد بيان": "نعم" if result.get("has_customs_declaration") else "لا",
                "ملف المصدر": result.get("_source_file"),
            })
    
    return rows


def process_batch(
    input_dir: Path,
    api: str,
    output_excel: Path = None,
    output_json: Path = None
) -> List[Dict[str, Any]]:
    """Process all PDFs in a directory
    
    Args:
        input_dir: Directory containing PDF files
        api: API to use ('gemini' or 'claude')
        output_excel: Path for Excel output
        output_json: Path for JSON output
        
    Returns:
        List of all extracted results
    """
    pdfs = find_pdfs(input_dir)
    
    if not pdfs:
        print(f"❌ No PDF files found in: {input_dir}")
        return []
    
    print(f"📁 Found {len(pdfs)} PDF files")
    print(f"🔌 Using API: {api}\n")
    
    extractor = get_extractor(api)
    results = []
    excel_rows = []
    
    for i, pdf_path in enumerate(pdfs, 1):
        print(f"[{i}/{len(pdfs)}] Processing: {pdf_path.name}...", end=" ")
        
        try:
            result = extractor.extract(pdf_path)
            results.append(result)
            
            if "error" not in result:
                excel_rows.extend(flatten_result(result))
                print("✅")
            else:
                print(f"⚠️ {result.get('error', 'Unknown error')[:50]}")
                
        except Exception as e:
            print(f"❌ {str(e)[:50]}")
            results.append({
                "error": str(e),
                "_source_file": pdf_path.name
            })
    
    # Save JSON output
    if output_json:
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ JSON saved: {output_json}")
    
    # Save Excel output
    if output_excel and PANDAS_AVAILABLE and excel_rows:
        df = pd.DataFrame(excel_rows)
        df.to_excel(output_excel, index=False, engine="openpyxl")
        print(f"✅ Excel saved: {output_excel}")
    elif output_excel and not PANDAS_AVAILABLE:
        print("⚠️ pandas not installed. Install with: pip install pandas openpyxl")
    
    # Print summary
    success_count = sum(1 for r in results if "error" not in r)
    print(f"\n📊 Summary: {success_count}/{len(results)} files processed successfully")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch process Arabic shipping document PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Directory containing PDF files"
    )
    parser.add_argument(
        "--excel", "-e",
        help="Output Excel file path"
    )
    parser.add_argument(
        "--json", "-j",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--api", "-a",
        choices=["gemini", "claude"],
        default=config.DEFAULT_API,
        help=f"API to use (default: {config.DEFAULT_API})"
    )
    
    args = parser.parse_args()
    
    input_dir = Path(args.input)
    if not input_dir.is_dir():
        print(f"❌ Error: Not a directory: {input_dir}")
        sys.exit(1)
    
    # Default output paths
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_path = Path(args.excel) if args.excel else config.OUTPUT_DIR / f"extraction_{timestamp}.xlsx"
    json_path = Path(args.json) if args.json else config.OUTPUT_DIR / f"extraction_{timestamp}.json"
    
    process_batch(
        input_dir=input_dir,
        api=args.api,
        output_excel=excel_path,
        output_json=json_path
    )


if __name__ == "__main__":
    main()
