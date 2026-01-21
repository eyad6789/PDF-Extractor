"""
Claude API Extractor for Arabic shipping documents
"""
import anthropic
import base64
from pathlib import Path
from typing import Dict, Any

from .base import BaseExtractor
from prompts import EXTRACTION_PROMPT
import config


class ClaudeExtractor(BaseExtractor):
    """Extract shipping document data using Anthropic Claude API"""
    
    def __init__(self, api_key: str = None):
        """Initialize Claude extractor
        
        Args:
            api_key: Anthropic API key. Uses config if not provided.
        """
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("Anthropic API key not configured. Set ANTHROPIC_API_KEY in .env")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = config.CLAUDE_MODEL
    
    def extract(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract data from PDF using Claude API
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing extracted shipping data
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            return {"error": f"PDF file not found: {pdf_path}"}
        
        pdf_data = self._load_pdf(pdf_path)
        pdf_base64 = base64.standard_b64encode(pdf_data).decode("utf-8")
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": EXTRACTION_PROMPT
                        }
                    ]
                }]
            )
            
            response_text = message.content[0].text
            result = self._parse_json_response(response_text)
            result["_source_file"] = str(pdf_path.name)
            result["_api_used"] = "claude"
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "_source_file": str(pdf_path.name),
                "_api_used": "claude"
            }
