import pdfplumber
import io
import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def extract_data_from_pdf(pdf_content: bytes, fields: list) -> dict:
    """
    Extrae texto y pide a la IA que busque SOLO los campos solicitados por el usuario.
    """
    full_text = ""
    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    # Convertimos la lista de campos en un string para el prompt
    fields_str = "\n".join([f"- {f}" for f in fields])
    keys_str = ", ".join([f'"{f}"' for f in fields])

    dynamic_prompt = f"""
    You are a professional data extractor.
    Extract the following information from the text:
    {fields_str}

    Return ONLY a valid JSON with these exact keys: {keys_str}.
    If a value is not found, set it to null.
    
    Text:
    {full_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Actualizado a la última versión
            contents=dynamic_prompt,
        )
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except Exception as e:
        return {"error": str(e)}