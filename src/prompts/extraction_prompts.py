"""
LLM prompt templates
"""

EXTRACTION_PROMPT = """You are a product information extraction assistant. Based on the search results provided, 
extract structured information about the product.

Search Results Context:
{context}

Original Input:
- Model Number: {model_number}
- Asset Classification: {asset_classification}
- Manufacturer (if known): {manufacturer}

Extract the following fields from the search results:
1. asset_classification: The standardized asset classification name (clean up the input classification)
2. manufacturer: The product manufacturer
3. model_number: The model number (confirm or correct if different from input)
4. product_line: The product line or series name
5. summary: A brief 2-3 sentence summary of the product

Rules:
- If information is not available in the context, leave the field empty
- Ensure the summary is factual and based only on the provided context
- Return ONLY a valid JSON object with these exact keys
- Do not include any explanatory text before or after the JSON

Example Output:
{{
    "asset_classification": "Marine Generator",
    "manufacturer": "Cummins",
    "model_number": "MRN85HD",
    "product_line": "Onan",
    "summary": "The Cummins MRN85HD is a marine diesel generator set providing reliable power for maritime applications."
}}

Now, extract the information:
"""
