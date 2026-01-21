"""
Gemini API Extractor for Arabic shipping documents
"""
import google.generativeai as genai
from pathlib import Path
from typing import Dict, Any

from .base import BaseExtractor
from prompts import EXTRACTION_PROMPT
import config


class GeminiExtractor(BaseExtractor):
    """Extract shipping document data using Google Gemini API"""
    
    def __init__(self, api_key: str = None):
        """Initialize Gemini extractor
        
        Args:
            api_key: Gemini API key. Uses config if not provided.
        """
        self.api_key = api_key or config.GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key not configured. Set GEMINI_API_KEY in .env")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(config.GEMINI_MODEL)
    
    def extract(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract data from PDF using Gemini API
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted shipping data
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            return {"error": f"PDF file not found: {pdf_path}"}
        
        pdf_data = self._load_pdf(pdf_path)
        
        try:
            response = self.model.generate_content([
                EXTRACTION_PROMPT,
                {"mime_type": "application/pdf", "data": pdf_data}
            ])
            
            result = self._parse_json_response(response.text)
            result["_source_file"] = str(pdf_path.name)
            result["_api_used"] = "gemini"
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "_source_file": str(pdf_path.name),
                "_api_used": "gemini"
            }
