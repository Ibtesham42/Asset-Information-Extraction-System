"""
LLM interaction service (Gemini/GPT)
"""
import json
import re
from typing import List, Dict, Any, Optional
from src.config.settings import settings
from src.utils.logger import get_logger
from src.prompts.extraction_prompts import EXTRACTION_PROMPT

logger = get_logger(__name__)

class LLMService:
    def __init__(self):
        self.model_type = settings.DEFAULT_LLM_MODEL
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize appropriate LLM client"""
        if "gemini" in self.model_type.lower():
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.client = genai.GenerativeModel('gemini-pro')
                logger.info("Initialized Gemini client")
            except ImportError:
                logger.error("Google Generative AI package not installed")
                self.client = None
        else:
            try:
                import openai
                openai.api_key = settings.OPENAI_API_KEY
                self.client = openai
                logger.info("Initialized OpenAI client")
            except ImportError:
                logger.error("OpenAI package not installed")
                self.client = None
                
    async def extract_info(
        self, 
        search_results: List[Dict[str, str]], 
        original_input: Dict[str, Any]
    ) -> Optional[Dict[str, str]]:
        """Extract structured information using LLM"""
        
        if not self.client:
            logger.warning("LLM client not initialized, using mock extraction")
            return self._get_mock_extraction(original_input)
        
        # Prepare context from search results
        context = self._prepare_context(search_results)
        
        # Format prompt
        prompt = EXTRACTION_PROMPT.format(
            context=context,
            model_number=original_input.get('model_number', ''),
            asset_classification=original_input.get('asset_classification_name', ''),
            manufacturer=original_input.get('manufacturer', '')
        )
        
        try:
            if "gemini" in self.model_type.lower():
                response = await self._call_gemini(prompt)
            else:
                response = await self._call_openai(prompt)
                
            # Parse JSON response
            extracted_data = self._parse_response(response)
            
            if extracted_data:
                logger.info(f"Successfully extracted data: {extracted_data}")
                return extracted_data
            else:
                logger.warning("Failed to parse LLM response")
                return self._get_mock_extraction(original_input)
            
        except Exception as e:
            logger.error(f"LLM extraction error: {str(e)}")
            return self._get_mock_extraction(original_input)
            
    def _prepare_context(self, search_results: List[Dict[str, str]]) -> str:
        """Format search results as context for LLM"""
        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(
            f"[Source {i}]\n"
            f"Title: {result.get('title', '')}\n"
            f"Content: {result.get('snippet', '')}\n"
            f"URL: {result.get('link', '')}\n"
        )
            return "\n".join(context_parts)
        
        
    async def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API"""
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise
            
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured information from product data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
        
    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parse LLM response to JSON"""
        # Try to extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
                
        # Try to parse as plain text and structure
        lines = response.strip().split('\n')
        result = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                result[key.strip().lower().replace(' ', '_')] = value.strip()
        
        if result:
            return result
                
        logger.warning("Failed to parse LLM response as JSON")
        return {}
    
    def _get_mock_extraction(self, original_input: Dict[str, Any]) -> Dict[str, str]:
        """Return mock extraction for testing"""
        return {
            'asset_classification': original_input.get('asset_classification_name', 'Marine Generator'),
            'manufacturer': 'Cummins',
            'model_number': original_input.get('model_number', 'MRN85HD'),
            'product_line': 'Onan',
            'summary': f"The {original_input.get('model_number', 'product')} is a marine generator designed for reliable power generation on vessels."
        }
