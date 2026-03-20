import pdfplumber
import io
import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

EXTRACTION_PROMPT_TEMPLATE = """
You are an expert data extractor.
I will provide you with the text extracted from a document.
Your mission is to extract the following information:
- Customer or patient name (name)
- Phone number (phone)
- Document date (date)
- Document issuer or company (issuer)

Return ONLY a valid JSON with the keys: "name", "phone", "date", "issuer".
If a value is not found, set it to null. Do not include markdown (like ```json) or additional text.

Document text:
{text}
"""

def extract_data_from_pdf(pdf_content: bytes) -> dict:
    """
    Extracts raw text from a PDF file in memory and uses an LLM to return structured data
    """
    full_text = "" # ¡Esta es la variable que faltaba inicializar!
    
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
                
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(text=full_text)
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        structured_data = json.loads(clean_text)
        return structured_data
        
    except Exception as e:
        return {"error": "AI processing failed", "details": str(e)}