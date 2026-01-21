"""
Base extractor interface
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional
import json


class BaseExtractor(ABC):
    """Abstract base class for document extractors"""
    
    @abstractmethod
    def extract(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract data from a PDF document
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted data
        """
        pass
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from model response, handling markdown code blocks"""
        text = response_text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            return {
                "error": f"Failed to parse JSON: {str(e)}",
                "raw_response": response_text
            }
    
    def _load_pdf(self, pdf_path: Path) -> bytes:
        """Load PDF file as bytes"""
        with open(pdf_path, "rb") as f:
            return f.read()
